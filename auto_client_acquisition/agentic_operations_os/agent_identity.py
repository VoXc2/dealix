"""Agent identity — no identity/owner/purpose = no agent."""

from __future__ import annotations

from dataclasses import dataclass

MVP_MIN_OPERATING_LEVEL = 1
MVP_MAX_OPERATING_LEVEL = 4


@dataclass(frozen=True, slots=True)
class AgentIdentityCard:
    agent_id: str
    name: str
    business_unit: str
    owner: str
    purpose: str
    operating_level: int
    status: str
    created_at: str
    last_reviewed_at: str


def agent_identity_valid(card: AgentIdentityCard) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not card.agent_id.strip():
        errors.append("agent_id_required")
    if not card.name.strip():
        errors.append("name_required")
    if not card.owner.strip():
        errors.append("owner_required")
    if not card.purpose.strip():
        errors.append("purpose_required")
    return not errors, tuple(errors)


def agent_operating_level_allowed_in_mvp(level: int) -> bool:
    """MVP allows operating levels 1–4 only (see docs/agentic_operations/AGENT_OPERATING_LEVELS.md)."""
    return MVP_MIN_OPERATING_LEVEL <= level <= MVP_MAX_OPERATING_LEVEL
