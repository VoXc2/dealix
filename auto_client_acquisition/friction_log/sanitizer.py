"""Friction log PII sanitizer — delegates to the canonical redactor.

Any text persisted into the friction log MUST pass through this. The
default redactor handles email, Saudi+Gulf phone, and Saudi national ID.
Caps note length to avoid log bloat from accidental large pastes.
"""
from __future__ import annotations

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

_MAX_NOTE_CHARS = 500


def sanitize_notes(text: str) -> str:
    """Redact PII and cap length."""
    if not text:
        return ""
    redacted = redact_text(text)
    if len(redacted) > _MAX_NOTE_CHARS:
        return redacted[:_MAX_NOTE_CHARS] + "…"
    return redacted


__all__ = ["sanitize_notes"]
