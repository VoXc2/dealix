"""Agent control doctrine — autonomy levels and card validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# 0 Read … 6 forbidden external autonomy (see docs)
AUTONOMY_LEVEL_MAX = 6
MVP_AUTONOMY_CEILING = 3
ENTERPRISE_EXTENDED_MAX = 5


@dataclass(frozen=True, slots=True)
class AgentControlCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int
    audit_required: bool


def validate_agent_card(card: AgentControlCard) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not card.agent_id.strip():
        errors.append("agent_id_required")
    if not card.owner.strip():
        errors.append("owner_required")
    if not 0 <= card.autonomy_level <= AUTONOMY_LEVEL_MAX:
        errors.append("autonomy_level_out_of_range")
    return not errors, tuple(errors)


def autonomy_allowed(autonomy_level: int, *, enterprise_tier: bool) -> bool:
    if autonomy_level < 0 or autonomy_level > AUTONOMY_LEVEL_MAX:
        return False
    if autonomy_level <= MVP_AUTONOMY_CEILING:
        return True
    if autonomy_level <= ENTERPRISE_EXTENDED_MAX:
        return enterprise_tier
    return False


def normalize_agent_card_dict(raw: Mapping[str, object]) -> AgentControlCard:
    return AgentControlCard(
        agent_id=str(raw.get("agent_id", "")),
        name=str(raw.get("name", "")),
        owner=str(raw.get("owner", "")),
        purpose=str(raw.get("purpose", "")),
        autonomy_level=int(raw.get("autonomy_level", -1)),
        audit_required=bool(raw.get("audit_required", False)),
    )
