"""Agent Identity Card — non-human worker identity."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class AgentRiskTier(IntEnum):
    TIER_1_LOW = 1
    TIER_2_MEDIUM = 2
    TIER_3_HIGH = 3
    TIER_4_RESTRICTED = 4


@dataclass(frozen=True)
class AgentIdentityCard:
    agent_id: str
    name: str
    type: str  # always "non_human_worker"
    business_unit: str
    owner: str
    purpose: str
    status: str  # active | paused | retired
    environment: str  # sandbox | mvp_internal | client_draft_only | retainer | enterprise
    risk_tier: AgentRiskTier
    created_at: str
    last_reviewed_at: str | None = None

    def __post_init__(self) -> None:
        if not self.agent_id:
            raise ValueError("agent_id_required")
        if not self.owner:
            raise ValueError("owner_required")
        if not self.purpose:
            raise ValueError("purpose_required")
        if self.type != "non_human_worker":
            raise ValueError("type_must_be_non_human_worker")
        if self.status not in {"active", "paused", "retired"}:
            raise ValueError("invalid_status")

    def is_production(self) -> bool:
        return self.environment in {"client_draft_only", "retainer", "enterprise"}
