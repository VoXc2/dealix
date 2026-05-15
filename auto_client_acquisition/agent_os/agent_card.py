"""Governed agent identity card (Agent-Safe Dealix — no runtime side effects)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class AgentStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    KILLED = "killed"


@dataclass(frozen=True, slots=True)
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int = 0
    status: str = AgentStatus.PROPOSED.value
    kill_switch_owner: str = ""
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "owner": self.owner,
            "purpose": self.purpose,
            "autonomy_level": int(self.autonomy_level),
            "status": self.status,
            "kill_switch_owner": self.kill_switch_owner,
            "allowed_tools": list(self.allowed_tools),
            "notes": self.notes,
        }


def agent_card_valid(card: AgentCard) -> bool:
    if not (
        card.agent_id.strip()
        and card.name.strip()
        and card.owner.strip()
        and card.purpose.strip()
    ):
        return False
    if card.autonomy_level < 0 or card.autonomy_level > 5:
        return False
    return bool(card.status.strip())


__all__ = ["AgentCard", "AgentStatus", "agent_card_valid"]
