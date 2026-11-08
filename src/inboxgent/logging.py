"""Logging setup that redacts secrets before they reach any handler."""

from __future__ import annotations

import logging
import re

_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S+"),
]
REDACTED = "[REDACTED]"


def redact(text: str) -> str:
    """Replace anything that looks like a credential."""
    for pattern in _PATTERNS:
        text = pattern.sub(
            lambda m: f"{m.group(1)}={REDACTED}" if m.lastindex else REDACTED, text
        )
    return text


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact(record.getMessage())
        record.args = None
        return True


def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("inboxgent")
    logger.setLevel(level.upper())
    if not any(isinstance(f, RedactingFilter) for f in logger.filters):
        logger.addFilter(RedactingFilter())
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        handler.addFilter(RedactingFilter())
        logger.addHandler(handler)
    return logger
