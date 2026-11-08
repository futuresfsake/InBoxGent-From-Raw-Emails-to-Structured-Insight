"""Header parsing into typed records with explicit failure accounting.

Parse failures are retained with null fields and counted, never dropped.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses

from dateutil import parser as dateparser

from inboxgent.ingest import ManifestEntry

_PREFIX_RE = re.compile(r"^\s*((re|fw|fwd)\s*:\s*)+", re.IGNORECASE)


@dataclass(frozen=True)
class ParsedEmail:
    message_id: str
    custodian: str
    folder: str
    date_utc: datetime | None
    sender: str
    recipients_to: tuple[str, ...]
    recipients_cc: tuple[str, ...]
    recipients_bcc: tuple[str, ...]
    subject: str
    subject_norm: str
    body_raw: str
    in_reply_to: str | None = None

    @property
    def n_recipients(self) -> int:
        return len(self.recipients_to) + len(self.recipients_cc) + len(self.recipients_bcc)


@dataclass
class ParseStats:
    total: int = 0
    failures: Counter[str] = field(default_factory=Counter)

    def rate(self, name: str) -> float:
        return self.failures[name] / self.total if self.total else 0.0


def normalize_subject(subject: str) -> str:
    return _PREFIX_RE.sub("", subject).strip().lower()


def _addresses(values: list[str]) -> tuple[str, ...]:
    return tuple(addr.strip().lower() for _, addr in getaddresses(values) if addr.strip())


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = dateparser.parse(re.sub(r"\s*\([A-Za-z]{2,5}\)\s*$", "", value))
    except (ValueError, OverflowError):
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def parse_message(raw: bytes, entry: ManifestEntry, stats: ParseStats) -> ParsedEmail:
    """Parse one message. Never raises on malformed input; failures are counted in ``stats``."""
    stats.total += 1
    msg = BytesParser(policy=policy.compat32).parsebytes(raw)

    message_id = (msg.get("Message-ID") or "").strip().strip("<>")
    if not message_id:
        stats.failures["missing_message_id"] += 1
        message_id = "synth-" + hashlib.sha256(raw).hexdigest()[:24]

    date_utc = _parse_date(msg.get("Date"))
    if date_utc is None:
        stats.failures["bad_date"] += 1

    senders = _addresses([str(msg.get("From") or "")])
    if not senders:
        stats.failures["missing_sender"] += 1
    to = _addresses([str(v) for v in msg.get_all("To", [])])
    if not to:
        stats.failures["missing_recipients"] += 1

    payload = msg.get_payload(decode=False)
    body = payload if isinstance(payload, str) else ""
    subject = str(msg.get("Subject") or "")
    reply = (msg.get("In-Reply-To") or "").strip().strip("<>") or None

    return ParsedEmail(
        message_id=message_id,
        custodian=entry.custodian,
        folder=entry.folder,
        date_utc=date_utc,
        sender=senders[0] if senders else "",
        recipients_to=to,
        recipients_cc=_addresses([str(v) for v in msg.get_all("Cc", [])]),
        recipients_bcc=_addresses([str(v) for v in msg.get_all("Bcc", [])]),
        subject=subject,
        subject_norm=normalize_subject(subject),
        body_raw=body,
        in_reply_to=reply,
    )
