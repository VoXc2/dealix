"""PII redactor — pure functions, no I/O.

Used by evidence exports + log sinks before anything leaves the
process. Conservative regexes — false positives ok, false
negatives are not (PDPL fines).
"""
from __future__ import annotations

import re

# Email pattern — RFC-light (good enough for redaction).
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")

# Saudi/Gulf phone patterns (covers +966, 00966, 05XXXXXXXX).
_PHONE_RE = re.compile(
    r"(?:\+?966|00966)[-\s]?5\d{8}"
    r"|\b05\d{8}\b"
    r"|\b5\d{8}\b"
    r"|\+?\d{1,3}[-\s]?\d{3,5}[-\s]?\d{3,5}[-\s]?\d{0,4}",
)

# Saudi national ID — 10 digits starting with 1 or 2.
_SAUDI_ID_RE = re.compile(r"\b[12]\d{9}\b")


def redact_email(text: str) -> str:
    """Replace each email with `local***@domain` form."""
    def _replace(m: re.Match) -> str:
        s = m.group(0)
        if "@" not in s:
            return "***"
        local, _, domain = s.partition("@")
        if not local:
            return "***@" + domain
        return local[0] + "***@" + domain
    return _EMAIL_RE.sub(_replace, text)


def redact_phone(text: str) -> str:
    """Replace each phone-like substring with `***REDACTED_PHONE***`."""
    return _PHONE_RE.sub("***REDACTED_PHONE***", text)


def redact_saudi_id(text: str) -> str:
    return _SAUDI_ID_RE.sub("***REDACTED_ID***", text)


def redact_text(text: str) -> str:
    """Apply all redactors in safe order (ID first to avoid phone regex
    swallowing it)."""
    if not isinstance(text, str):
        return text
    out = redact_saudi_id(text)
    out = redact_phone(out)
    out = redact_email(out)
    return out


def redact_dict(data: dict) -> dict:
    """Redact every string value recursively. Keys are NOT redacted."""
    def _walk(value):
        if isinstance(value, str):
            return redact_text(value)
        if isinstance(value, dict):
            return {k: _walk(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_walk(v) for v in value]
        if isinstance(value, tuple):
            return tuple(_walk(v) for v in value)
        return value
    return _walk(data)
