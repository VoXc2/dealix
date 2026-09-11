"""Channel Registry — 360-degree distribution map.

Each channel has economic scoring, consent/policy requirements, tracking.
States: DISCOVERED→EVALUATING→READY→ACTIVE→DEGRADED→BLOCKED→PAUSED→RETIRED
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class ChannelType(StrEnum):
    OWNED = "owned"
    EARNED = "earned"
    SEARCH = "search"
    AI_SEARCH = "ai_search"
    RELATIONSHIP = "relationship"
    REFERRAL = "referral"
    PARTNER = "partner"
    PROCUREMENT = "procurement"
    MARKETPLACE = "marketplace"
    EVENT = "event"
    COMMUNITY = "community"
    CONTENT = "content"
    INTEGRATION = "integration"
    PRODUCT_LED = "product_led"
    EMAIL = "email"
    WHATSAPP_OPT_IN = "whatsapp_opt_in"
    WEB_CHAT = "web_chat"
    SUPPORT = "support"
    DIRECTORY = "directory"
    ECOSYSTEM = "ecosystem"
    SUPPLIER_PORTAL = "supplier_portal"
    TENDER = "tender"
    CHANNEL_PARTNER = "channel_partner"

class ChannelStatus(StrEnum):
    DISCOVERED = "discovered"
    EVALUATING = "evaluating"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    PAUSED = "paused"
    RETIRED = "retired"

class Channel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    channel_id: str
    channel_type: ChannelType
    target_buyer: str = UNKNOWN
    sector_fit: list[str] = Field(default_factory=list)
    cost_sar: float = 0.0
    founder_minutes: int = 0
    setup_effort: str = UNKNOWN
    conversion_hypothesis: str = UNKNOWN
    consent_requirement: str = UNKNOWN
    policy_requirement: str = UNKNOWN
    technical_dependency: str = UNKNOWN
    tracking_method: str = UNKNOWN
    current_status: ChannelStatus = ChannelStatus.DISCOVERED
    health: str = UNKNOWN
    last_verified: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    evidence: str = UNKNOWN
    next_action: str = UNKNOWN
    kill_condition: str = UNKNOWN

    def economic_score(self) -> float:
        # Simplified: cost + founder time vs hypothesis strength
        cost = self.cost_sar + self.founder_minutes * 5
        # Ready/active channels get bonus
        status_bonus = {ChannelStatus.READY: 1.2, ChannelStatus.ACTIVE: 1.5}.get(self.current_status, 1.0)
        if cost == 0:
            return 1.0 * status_bonus
        return round(status_bonus * 100 / (cost + 10), 3)

class ChannelRegistry:
    def __init__(self) -> None:
        self.channels: dict[str, Channel] = {}

    def register(self, ch: Channel) -> None:
        self.channels[ch.channel_id] = ch

    def rank(self) -> list[Channel]:
        return sorted(self.channels.values(), key=lambda c: c.economic_score(), reverse=True)

    def to_dict(self) -> dict[str, Any]:
        return {"channels": [c.model_dump(mode="json") for c in self.channels.values()], "ranked": [c.channel_id for c in self.rank()]}

__all__ = ["ChannelRegistry", "Channel", "ChannelType", "ChannelStatus", "UNKNOWN"]
