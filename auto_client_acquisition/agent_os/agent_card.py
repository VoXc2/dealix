"""AgentCard — the identity document every agent must carry.

No agent in production without a complete card. Enforced by agent_registry.register_agent.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from auto_client_acquisition.agent_os.autonomy_levels import (
    AutonomyLevel,
    is_mvp_allowed,
    requires_per_session_approval,
)
from auto_client_acquisition.agent_os.tool_permissions import (
    FORBIDDEN_MVP_TOOLS,
)


class AgentStatus(StrEnum):
    PROPOSED = "proposed"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    PAUSED = "paused"
    KILLED = "killed"


@dataclass
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int = int(AutonomyLevel.L1_DRAFT_ASSISTED)
    allowed_tools: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=lambda: list(FORBIDDEN_MVP_TOOLS))
    kill_switch_owner: str = ""
    status: str = AgentStatus.PROPOSED.value
    audit_card_ref: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    last_updated_at: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def new_card(
    *,
    agent_id: str,
    name: str,
    owner: str,
    purpose: str,
    autonomy_level: AutonomyLevel | int = AutonomyLevel.L1_DRAFT_ASSISTED,
    allowed_tools: list[str] | None = None,
    kill_switch_owner: str = "",
    notes: str = "",
) -> AgentCard:
    """Construct + validate a new AgentCard.

    Raises ValueError on:
      - missing agent_id / name / owner / purpose
      - autonomy_level above MVP_MAX
      - missing kill_switch_owner for L4+
      - any forbidden tool included in allowed_tools
    """
    if not agent_id:
        raise ValueError("agent_id is required")
    if not name:
        raise ValueError("name is required")
    if not owner:
        raise ValueError("owner is required")
    if not purpose:
        raise ValueError("purpose is required")
    level = int(autonomy_level)
    if not is_mvp_allowed(level):
        raise ValueError(
            f"autonomy_level {level} not allowed in MVP (max {int(AutonomyLevel.L3_CONDITIONAL_AUTO)})"
        )
    if requires_per_session_approval(level) and not kill_switch_owner:
        raise ValueError(
            "kill_switch_owner is required for L4+ (per-session approval)"
        )
    tools = list(allowed_tools or [])
    bad = [t for t in tools if t.lower() in FORBIDDEN_MVP_TOOLS]
    if bad:
        raise ValueError(f"allowed_tools includes forbidden MVP tools: {bad}")

    if not kill_switch_owner:
        kill_switch_owner = owner

    return AgentCard(
        agent_id=agent_id,
        name=name,
        owner=owner,
        purpose=purpose,
        autonomy_level=level,
        allowed_tools=tools,
        forbidden_tools=list(FORBIDDEN_MVP_TOOLS),
        kill_switch_owner=kill_switch_owner,
        notes=notes,
    )


__all__ = ["AgentCard", "AgentStatus", "new_card"]
