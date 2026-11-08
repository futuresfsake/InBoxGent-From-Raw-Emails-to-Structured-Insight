"""Exact-duplicate detection over parsed emails."""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from collections.abc import Iterable

from inboxgent.parse import ParsedEmail

_WS = re.compile(r"\s+")


def exact_key(email: ParsedEmail) -> str:
    """Hash of normalized (sender, subject_norm, body)."""
    body = _WS.sub(" ", email.body_raw).strip().lower()
    payload = "\0".join([email.sender, email.subject_norm, body])
    return hashlib.sha256(payload.encode()).hexdigest()


def exact_clusters(emails: Iterable[ParsedEmail]) -> dict[str, list[str]]:
    """Map cluster key to message ids; clusters of size 1 are included."""
    clusters: dict[str, list[str]] = defaultdict(list)
    for e in emails:
        clusters[exact_key(e)].append(e.message_id)
    return dict(clusters)


def canonical_id(emails: list[ParsedEmail]) -> str:
    """Earliest message wins; a sent-folder copy is preferred on ties; id breaks remaining ties."""

    def rank(e: ParsedEmail) -> tuple[bool, float, bool, str]:
        return (
            e.date_utc is None,
            e.date_utc.timestamp() if e.date_utc else 0.0,
            "sent" not in e.folder.lower(),
            e.message_id,
        )

    return min(emails, key=rank).message_id
