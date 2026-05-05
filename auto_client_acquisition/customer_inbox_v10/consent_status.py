"""Consent gate helper for inbox conversations."""
from __future__ import annotations

from auto_client_acquisition.customer_inbox_v10.schemas import (
    ConsentStatus,
    Conversation,
)


def check_consent(conversation: Conversation) -> bool:
    """Returns True only if the conversation's consent_status == granted."""
    raw = conversation.consent_status
    value = raw.value if isinstance(raw, ConsentStatus) else raw
    return value == ConsentStatus.GRANTED.value
