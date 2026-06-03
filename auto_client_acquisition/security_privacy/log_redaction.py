"""Log redaction wrapper — for middleware that needs to scrub PII
+ secrets out of log entries before persisting them."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_dict,
    redact_text,
)
from auto_client_acquisition.security_privacy.secret_scan_policy import (
    SECRET_PATTERNS,
)


def _redact_secrets_in_text(text: str) -> str:
    """In-place secret scrubbing — replaces matches with [REDACTED_SECRET]."""
    if not isinstance(text, str):
        return text
    out = text
    for _, pat in SECRET_PATTERNS:
        out = pat.sub("[REDACTED_SECRET]", out)
    return out


def redact_log_entry(entry: dict[str, Any] | str) -> dict[str, Any] | str:
    """Apply both PII + secret redaction to a log entry.

    Caller-friendly for either dict-shaped entries (structlog) or
    plain strings (legacy logger).
    """
    if isinstance(entry, str):
        return _redact_secrets_in_text(redact_text(entry))
    if isinstance(entry, dict):
        # First redact PII recursively, then run secret patterns over
        # any remaining string values.
        first = redact_dict(entry)

        def _walk(value):
            if isinstance(value, str):
                return _redact_secrets_in_text(value)
            if isinstance(value, dict):
                return {k: _walk(v) for k, v in value.items()}
            if isinstance(value, list):
                return [_walk(v) for v in value]
            return value

        return _walk(first)
    return entry
