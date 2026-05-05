"""SLA policy — channel-specific reply targets."""
from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.customer_inbox_v10.schemas import (
    Channel,
    Conversation,
    SLAStatus,
)


_TARGET_HOURS_BY_CHANNEL: dict[str, float] = {
    Channel.INBOUND_WHATSAPP.value: 5 / 60,  # 5 minutes
    Channel.WEBSITE_CHAT.value: 1.0,
    Channel.EMAIL.value: 24.0,
    Channel.MANUAL_LINKEDIN_NOTE.value: 24.0,
    Channel.SUPPORT_FORM.value: 24.0,
    Channel.OUTBOUND_BLOCKED.value: 24.0,
}


def default_sla_hours(channel: Channel | str) -> int:
    """Integer hour target for a channel (rounded up; 5min → 1hr int)."""
    value = channel.value if isinstance(channel, Channel) else str(channel)
    raw = _TARGET_HOURS_BY_CHANNEL.get(value, 24.0)
    # Convert fractional to int hours (min 1).
    if raw < 1:
        return 1
    return int(raw)


def _channel_target_hours_float(channel: str) -> float:
    return _TARGET_HOURS_BY_CHANNEL.get(channel, 24.0)


def compute_sla(conv: Conversation) -> SLAStatus:
    """Compute SLA status for a conversation.

    Uses the most recent inbound message (or, if none, conversation
    is treated as zero-elapsed). For inbound_whatsapp the underlying
    target is 5 minutes; for website_chat it's 1 hour; for email it's
    24 hours.
    """
    channel_value = (
        conv.channel.value
        if hasattr(conv.channel, "value")
        else str(conv.channel)
    )
    target_hours_float = _channel_target_hours_float(channel_value)
    target_hours_int = default_sla_hours(channel_value)

    # Find latest inbound message (the SLA clock starts on inbound).
    last_inbound_at: datetime | None = None
    for m in conv.messages:
        direction = m.direction.value if hasattr(m.direction, "value") else str(m.direction)
        if direction == "inbound":
            ts = m.created_at
            if last_inbound_at is None or ts > last_inbound_at:
                last_inbound_at = ts

    if last_inbound_at is None:
        elapsed_hours = 0.0
    else:
        delta = datetime.now(UTC) - last_inbound_at
        elapsed_hours = delta.total_seconds() / 3600.0

    breached = elapsed_hours > target_hours_float
    if not breached:
        action = "proceed"
    elif elapsed_hours <= target_hours_float * 2:
        action = "escalate"
    else:
        action = "alert_founder"

    return SLAStatus(
        conversation_id=conv.id,
        target_hours=target_hours_int,
        elapsed_hours=round(elapsed_hours, 4),
        breached=breached,
        action=action,
    )


def sla_table() -> dict[str, int]:
    """Return the channel → target_hours table (for /sla-policy endpoint)."""
    return {
        ch: default_sla_hours(ch) for ch in _TARGET_HOURS_BY_CHANNEL
    }
