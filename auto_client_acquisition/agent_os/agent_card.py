"""Governed agent identity card (Agent-Safe Dealix — no runtime side effects)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from auto_client_acquisition.agent_os.autonomy_levels import (
    AutonomyLevel,
    autonomy_allowed_in_mvp,
    requires_kill_switch_owner,
)
from auto_client_acquisition.agent_os.tool_permissions import is_tool_allowed


class AgentStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    KILLED = "killed"


_DEFAULT_ALLOWED_TOOLS: tuple[str, ...] = ("read", "analyze")


@dataclass(frozen=True, slots=True)
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int = int(AutonomyLevel.READ_ONLY)
    status: str = AgentStatus.PROPOSED.value
    kill_switch_owner: str = ""
    allowed_tools: tuple[str, ...] = _DEFAULT_ALLOWED_TOOLS
    notes: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["allowed_tools"] = list(self.allowed_tools)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentCard:
        payload = dict(data)
        tools = payload.get("allowed_tools", _DEFAULT_ALLOWED_TOOLS)
        payload["allowed_tools"] = tuple(tools)
        return cls(**payload)

    def with_status(self, status: str) -> AgentCard:
        from dataclasses import replace

        return replace(self, status=status)


def agent_card_valid(card: AgentCard) -> bool:
    if not (
        card.agent_id.strip()
        and card.name.strip()
        and card.owner.strip()
        and card.purpose.strip()
    ):
        return False
    if card.autonomy_level < 0 or card.autonomy_level > int(AutonomyLevel.L4_AUTO_WITH_AUDIT):
        return False
    return bool(card.status.strip())


def new_card(
    *,
    agent_id: str,
    name: str,
    owner: str,
    purpose: str,
    autonomy_level: AutonomyLevel | int = AutonomyLevel.READ_ONLY,
    kill_switch_owner: str = "",
    allowed_tools: list[str] | None = None,
    notes: str = "",
) -> AgentCard:
    """Build a governed AgentCard, enforcing MVP doctrine on construction."""
    if not agent_id.strip():
        raise ValueError("agent_id is required")
    if not name.strip():
        raise ValueError("name is required")
    if not owner.strip():
        raise ValueError("owner is required")
    if not purpose.strip():
        raise ValueError("purpose is required")

    level = AutonomyLevel(autonomy_level)
    if not autonomy_allowed_in_mvp(level):
        raise ValueError("autonomy level L5 (fully autonomous) is blocked in the MVP")

    effective_kill_switch_owner = kill_switch_owner.strip() or owner.strip()
    if requires_kill_switch_owner(level) and not kill_switch_owner.strip():
        raise ValueError(
            "autonomy level L4 requires an explicit kill_switch_owner"
        )

    tools = list(_DEFAULT_ALLOWED_TOOLS) if allowed_tools is None else list(allowed_tools)
    for tool in tools:
        ok, reason = is_tool_allowed(tool)
        if not ok:
            raise ValueError(f"allowed_tools rejected: {reason}")

    return AgentCard(
        agent_id=agent_id.strip(),
        name=name.strip(),
        owner=owner.strip(),
        purpose=purpose.strip(),
        autonomy_level=int(level),
        status=AgentStatus.PROPOSED.value,
        kill_switch_owner=effective_kill_switch_owner,
        allowed_tools=tuple(tools),
        notes=notes,
    )


__all__ = ["AgentCard", "AgentStatus", "agent_card_valid", "new_card"]
