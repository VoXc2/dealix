"""Routing policy — outbound channel selection with consent + cold-WA guard."""
from __future__ import annotations

from auto_client_acquisition.customer_inbox_v10.consent_status import check_consent
from auto_client_acquisition.customer_inbox_v10.schemas import (
    Channel,
    Conversation,
)


def route_to_channel(conv: Conversation, suggested_channel: Channel | str) -> dict:
    """Block unsafe outbound; return draft_only for safe surfaces.

    Rules:
      * outbound_blocked → always blocked
      * inbound_whatsapp outbound → blocked unless consent_status == granted
      * everything else → draft_only
    """
    ch_value = (
        suggested_channel.value
        if isinstance(suggested_channel, Channel)
        else str(suggested_channel)
    )

    if ch_value == Channel.OUTBOUND_BLOCKED.value:
        return {
            "channel": ch_value,
            "action_mode": "blocked",
            "blocked_reason": "outbound_blocked channel is platform-blocked",
        }

    if ch_value == Channel.INBOUND_WHATSAPP.value:
        if not check_consent(conv):
            return {
                "channel": ch_value,
                "action_mode": "blocked",
                "blocked_reason": "no_cold_whatsapp: outbound WhatsApp requires explicit consent",
            }

    return {
        "channel": ch_value,
        "action_mode": "draft_only",
        "blocked_reason": "",
    }
