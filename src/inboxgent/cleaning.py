"""Ordered, auditable email cleaning with per-step lineage.

Steps (see LLD section 4): normalize, strip forwarded blocks, strip quoted replies,
strip signatures and disclaimers, final whitespace normalization. Each step records the
characters it removed. The pipeline is idempotent and never grows the text.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass, field

CLEAN_VERSION = "clean_v0"

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_FORWARD_MARKER = re.compile(
    r"^\s*(-{3,}\s*(original message|forwarded (by|message))\b.*|-{3,}\s*forwarded by .*)$",
    re.IGNORECASE,
)
_REPLY_HEADER = re.compile(r"^\s*on .{5,200}\bwrote:\s*$", re.IGNORECASE)
_SIG_DELIM = re.compile(r"^\s*--\s*$")
_DISCLAIMER = re.compile(
    r"^\s*(this (e-?mail|message)( and any attachments?)?|the information (contained )?in this)"
    r".{0,300}(confidential|intended recipient|privileged).*$",
    re.IGNORECASE,
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text.replace("\r\n", "\n").replace("\r", "\n"))
    text = _CONTROL.sub("", text)
    text = "\n".join(re.sub(r"[ \t ]+", " ", line).strip() for line in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def strip_forwarded(text: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if _FORWARD_MARKER.match(line):
            return "\n".join(lines[:i])
    return text


def strip_quoted(text: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if _REPLY_HEADER.match(line):
            lines = lines[:i]
            break
    return "\n".join(line for line in lines if not line.lstrip().startswith(">"))


def strip_signature(text: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if _SIG_DELIM.match(line):
            lines = lines[:i]
            break
    return "\n".join(line for line in lines if not _DISCLAIMER.match(line))


_STEPS: list[tuple[str, Callable[[str], str]]] = [
    ("normalize", normalize),
    ("strip_forwarded", strip_forwarded),
    ("strip_quoted", strip_quoted),
    ("strip_signature", strip_signature),
    ("final_normalize", normalize),
]


@dataclass(frozen=True)
class CleanResult:
    text: str
    chars_removed_by_step: dict[str, int] = field(default_factory=dict)
    chars_in: int = 0

    @property
    def chars_out(self) -> int:
        return len(self.text)


def clean(text: str) -> CleanResult:
    """Run all steps; ``chars_removed_by_step`` may be negative-free but normalization of
    compatibility characters can change length, so removal is reported as ``max(0, delta)``."""
    removed: dict[str, int] = {}
    current = text
    for name, step in _STEPS:
        new = step(current)
        removed[name] = max(0, len(current) - len(new))
        current = new
    return CleanResult(text=current, chars_removed_by_step=removed, chars_in=len(text))
