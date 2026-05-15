"""Governed agent identity card (Agent-Safe Dealix — no runtime side effects)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from auto_client_acquisition.agent_os.autonomy_levels import (
    MAX_AUTONOMY_LEVEL_MVP,
    AutonomyLevel,
)
from auto_client_acquisition.agent_os.tool_permissions import FORBIDDEN_TOOLS_MVP


class AgentStatus(StrEnum):
    """Lifecycle status of a registered agent."""

    PROPOSED = "proposed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    KILLED = "killed"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int = int(AutonomyLevel.L1_ANALYZE)
    status: str = AgentStatus.PROPOSED.value
    allowed_tools: tuple[str, ...] = ()
    kill_switch_owner: str = ""
    notes: str = ""
    created_at: str = field(default_factory=_now)
    killed_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def agent_card_valid(card: AgentCard) -> bool:
    if not (
        card.agent_id.strip()
        and card.name.strip()
        and card.owner.strip()
        and card.purpose.strip()
    ):
        return False
    if card.autonomy_level < 0 or card.autonomy_level > int(MAX_AUTONOMY_LEVEL_MVP):
        return False
    return bool(card.status.strip())


def new_card(
    *,
    agent_id: str,
    name: str,
    owner: str,
    purpose: str,
    autonomy_level: int | AutonomyLevel = AutonomyLevel.L1_ANALYZE,
    allowed_tools: list[str] | None = None,
    kill_switch_owner: str = "",
    notes: str = "",
) -> AgentCard:
    """Build a validated :class:`AgentCard`.

    Enforces the agent-identity non-negotiables: an owner and purpose are
    mandatory, L4+ requires a named kill-switch owner, L5 is blocked in the
    MVP, and forbidden tools may never be granted.
    """
    if not (agent_id and agent_id.strip()):
        raise ValueError("agent_id is required")
    if not (name and name.strip()):
        raise ValueError("name is required")
    if not (owner and owner.strip()):
        raise ValueError("owner is required")
    if not (purpose and purpose.strip()):
        raise ValueError("purpose is required")

    level = int(autonomy_level)
    if level < 0 or level > int(AutonomyLevel.L5_FULLY_AUTONOMOUS):
        raise ValueError(f"autonomy_level out of range: {level}")
    if level >= int(AutonomyLevel.L5_FULLY_AUTONOMOUS):
        raise ValueError("autonomy_level L5 (fully autonomous) is blocked in the MVP")

    if level >= int(AutonomyLevel.L4_AUTO_WITH_AUDIT) and not kill_switch_owner.strip():
        raise ValueError("autonomy_level L4+ requires a kill_switch_owner")
    ks_owner = kill_switch_owner.strip() or owner.strip()

    tools = tuple(t.strip().lower() for t in (allowed_tools or []) if t.strip())
    forbidden = [t for t in tools if t in FORBIDDEN_TOOLS_MVP]
    if forbidden:
        raise ValueError(f"allowed_tools includes forbidden tools: {forbidden}")

    return AgentCard(
        agent_id=agent_id.strip(),
        name=name.strip(),
        owner=owner.strip(),
        purpose=purpose.strip(),
        autonomy_level=level,
        status=AgentStatus.PROPOSED.value,
        allowed_tools=tools,
        kill_switch_owner=ks_owner,
        notes=notes.strip(),
    )


__all__ = ["AgentCard", "AgentStatus", "agent_card_valid", "new_card"]
