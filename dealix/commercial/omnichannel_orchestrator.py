"""Omnichannel Orchestrator — all communication channels automated, governed.

Channels: WEBSITE, WEB_CHAT, EMAIL, WHATSAPP_OPT_IN, MEETING, SUPPORT, CUSTOMER_PORTAL, PARTNER, PROCUREMENT, EVENT, REFERRAL, MARKETPLACE
Each with owner, purpose, response policy, consent, tracking, handoff, SLA, cost, conversion.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.consent_registry import ConsentRegistry, ConsentState
from dealix.commercial.channel_registry import ChannelRegistry, ChannelType
from dealix.commercial.relationship_graph import RelationshipGraph

UNKNOWN = "UNKNOWN"

class ChannelId(StrEnum):
    WEBSITE = "website"
    WEB_CHAT = "web_chat"
    EMAIL = "email"
    WHATSAPP_OPT_IN = "whatsapp_opt_in"
    MEETING = "meeting"
    SUPPORT = "support"
    CUSTOMER_PORTAL = "customer_portal"
    PARTNER = "partner"
    PROCUREMENT = "procurement"
    EVENT = "event"
    REFERRAL = "referral"
    MARKETPLACE = "marketplace"

class OmnichannelMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_id: str
    channel: ChannelId
    recipient_id: str
    content_ar: str = UNKNOWN
    content_en: str = UNKNOWN
    purpose: str = UNKNOWN
    consent_state: ConsentState = ConsentState.NO_CONSENT
    tracking_id: str = UNKNOWN
    handoff: str = UNKNOWN
    sla_hours: int = 24
    cost_sar: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    approval_required: bool = True
    sent: bool = False

    def can_send(self, consent_ok: bool) -> bool:
        if self.channel == ChannelId.WHATSAPP_OPT_IN and not consent_ok:
            return False
        return consent_ok or self.channel in (ChannelId.WEBSITE, ChannelId.SUPPORT)

class OmnichannelOrchestrator:
    def __init__(self, consent: ConsentRegistry | None = None, channels: ChannelRegistry | None = None, relationships: RelationshipGraph | None = None) -> None:
        self.consent = consent or ConsentRegistry()
        self.channels = channels or ChannelRegistry()
        self.relationships = relationships or RelationshipGraph()
        self.queue: list[OmnichannelMessage] = []
        self.sent: list[OmnichannelMessage] = []

    def prepare_draft(self, channel: ChannelId, recipient_id: str, ar: str, en: str, purpose: str) -> OmnichannelMessage:
        # Consent check
        state = self.consent.get_state(recipient_id, channel.value)
        consent_ok = self.consent.can_send(recipient_id, channel.value)
        msg = OmnichannelMessage(
            message_id=f"msg_{channel.value}_{recipient_id}_{int(datetime.now(UTC).timestamp())}",
            channel=channel,
            recipient_id=recipient_id,
            content_ar=ar,
            content_en=en,
            purpose=purpose,
            consent_state=state,
            approval_required=True,
            sent=False,
        )
        # Never draft cold WhatsApp without opt-in
        if channel == ChannelId.WHATSAPP_OPT_IN and not consent_ok:
            msg.handoff = "blocked_no_consent"
            return msg
        self.queue.append(msg)
        return msg

    def approve_and_send(self, message_id: str, approved_by: str) -> OmnichannelMessage | None:
        # L5: requires explicit approval, here simulated as approved_by provided
        for msg in self.queue:
            if msg.message_id == message_id:
                # Verify consent again
                if not self.consent.can_send(msg.recipient_id, msg.channel.value) and msg.channel == ChannelId.WHATSAPP_OPT_IN:
                    return None
                msg.sent = True
                self.sent.append(msg)
                self.queue.remove(msg)
                return msg
        return None

    def channel_health(self) -> dict[str, Any]:
        return {
            "queued": len(self.queue),
            "sent": len(self.sent),
            "channels": len(self.channels.channels) if hasattr(self.channels, "channels") else 0,
            "whatsapp_blocked": len([m for m in self.queue if m.handoff == "blocked_no_consent"]),
        }

    def to_dict(self) -> dict[str, Any]:
        return {"queue": [m.model_dump(mode="json") for m in self.queue], "sent": [m.model_dump(mode="json") for m in self.sent], "health": self.channel_health()}

__all__ = ["OmnichannelOrchestrator", "OmnichannelMessage", "ChannelId", "UNKNOWN"]
