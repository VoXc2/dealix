"""Forbidden outbound / marketing patterns (delegates to draft_gate)."""

from __future__ import annotations

from auto_client_acquisition.governance_os.draft_gate import audit_draft_text

FORBIDDEN_CHANNEL_MARKERS = (
    "cold whatsapp",
    "linkedin automation",
    "blast",
)


def is_channel_forbidden(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in FORBIDDEN_CHANNEL_MARKERS)


__all__ = ["FORBIDDEN_CHANNEL_MARKERS", "audit_draft_text", "is_channel_forbidden"]
