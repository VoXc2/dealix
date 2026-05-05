"""Conversation lifecycle helpers — start + add inbound (auto-redact)."""
from __future__ import annotations

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.customer_inbox_v10.schemas import (
    Channel,
    ConsentStatus,
    Conversation,
    Message,
    MessageDirection,
)
from auto_client_acquisition.customer_inbox_v10.sla_policy import default_sla_hours


def start_conversation(customer_handle: str, channel: Channel | str) -> Conversation:
    """Start a fresh conversation. Defaults: consent unknown → outbound blocked."""
    ch = Channel(channel) if not isinstance(channel, Channel) else channel
    return Conversation(
        customer_handle=customer_handle,
        channel=ch,
        consent_status=ConsentStatus.UNKNOWN,
        sla_target_hours=default_sla_hours(ch),
    )


def add_inbound(conv: Conversation, body: str) -> Conversation:
    """Append an inbound message. Auto-redacts PII via redact_text()."""
    redacted = redact_text(body)
    msg = Message(
        conversation_id=conv.id,
        channel=Channel(conv.channel) if not isinstance(conv.channel, Channel) else conv.channel,
        direction=MessageDirection.INBOUND,
        body_redacted=redacted,
    )
    conv.messages.append(msg)
    return conv
