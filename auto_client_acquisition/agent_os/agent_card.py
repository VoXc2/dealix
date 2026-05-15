"""Governed agent identity card (Agent-Safe Dealix — no runtime side effects)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int
    status: str
    tenant_id: str = "default"
    """Tenant scope for isolation. ``"default"`` in dev/test; production
    callers pass a real tenant id (no agent without a tenant)."""


def agent_card_valid(card: AgentCard) -> bool:
    if not (card.agent_id.strip() and card.name.strip() and card.owner.strip() and card.purpose.strip()):
        return False
    if not card.tenant_id.strip():
        return False
    if card.autonomy_level < 0 or card.autonomy_level > 4:
        return False
    return bool(card.status.strip())


__all__ = ["AgentCard", "agent_card_valid"]
