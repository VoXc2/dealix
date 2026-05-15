"""Agent lifecycle: lifecycle states plus the governed card factory.

``new_card`` is the single chokepoint that enforces the agent
non-negotiables before a card may exist: identity, owner, purpose,
kill-switch ownership for high autonomy, and a clean tool grant.
"""

from __future__ import annotations

from collections.abc import Iterable
from enum import StrEnum

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus
from auto_client_acquisition.agent_os.autonomy_levels import (
    AutonomyLevel,
    autonomy_allowed_mvp,
    autonomy_requires_kill_switch,
)
from auto_client_acquisition.agent_os.tool_permissions import FORBIDDEN_TOOLS_MVP


class AgentLifecycleState(StrEnum):
    DRAFT = "draft"
    STAGING = "staging"
    PRODUCTION = "production"
    SUSPENDED = "suspended"
    RETIRED = "retired"


def lifecycle_allows_production_tools(state: AgentLifecycleState) -> bool:
    return state == AgentLifecycleState.PRODUCTION


def new_card(
    *,
    agent_id: str,
    name: str,
    owner: str,
    purpose: str,
    autonomy_level: AutonomyLevel | int = AutonomyLevel.L0_READ_ONLY,
    allowed_tools: Iterable[str] | None = None,
    kill_switch_owner: str = "",
    notes: str = "",
) -> AgentCard:
    """Build a governed agent card, rejecting any non-negotiable violation."""
    if not agent_id.strip():
        msg = "agent_id is required"
        raise ValueError(msg)
    if not name.strip():
        msg = "name is required"
        raise ValueError(msg)
    if not owner.strip():
        msg = "owner is required"
        raise ValueError(msg)
    if not purpose.strip():
        msg = "purpose is required"
        raise ValueError(msg)

    level = int(autonomy_level)
    if level < 0 or level > 5:
        msg = f"autonomy_level out of range: {level}"
        raise ValueError(msg)
    if not autonomy_allowed_mvp(level):
        msg = "autonomy_level L5_FULLY_AUTONOMOUS is blocked in the MVP"
        raise ValueError(msg)

    resolved_kill_owner = kill_switch_owner.strip() or owner.strip()
    if autonomy_requires_kill_switch(level) and not kill_switch_owner.strip():
        msg = "autonomy_level L4+ requires an explicit kill_switch_owner"
        raise ValueError(msg)

    tools = tuple(t.strip() for t in (allowed_tools or ()) if t.strip())
    forbidden = sorted({t for t in tools if t.lower() in FORBIDDEN_TOOLS_MVP})
    if forbidden:
        msg = f"allowed_tools includes hard-blocked tools: {forbidden}"
        raise ValueError(msg)

    return AgentCard(
        agent_id=agent_id.strip(),
        name=name.strip(),
        owner=owner.strip(),
        purpose=purpose.strip(),
        autonomy_level=level,
        status=AgentStatus.PROPOSED.value,
        kill_switch_owner=resolved_kill_owner,
        allowed_tools=tools,
        notes=notes.strip(),
    )


__all__ = [
    "AgentLifecycleState",
    "lifecycle_allows_production_tools",
    "new_card",
]
