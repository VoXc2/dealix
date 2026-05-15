"""Governed agent identity card + the ``new_card`` validating factory.

Doctrine: no AI agent without identity, owner, scope, and audit. L4+ needs a
kill-switch owner; L5 is blocked in the MVP; forbidden tools are rejected.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.agent_os.agent_status import AgentStatus
from auto_client_acquisition.agent_os.autonomy_levels import (
    DEFAULT_AUTONOMY,
    AutonomyLevel,
    autonomy_blocked_in_mvp,
    coerce_autonomy,
    requires_kill_switch_owner,
)
from auto_client_acquisition.agent_os.tool_permissions import forbidden_tools_in

RISK_LEVELS: frozenset[str] = frozenset({"low", "med", "high"})

_CARD_FIELDS: frozenset[str] = frozenset(
    {
        "agent_id",
        "name",
        "owner",
        "purpose",
        "autonomy_level",
        "status",
        "allowed_tools",
        "kill_switch_owner",
        "notes",
        "role",
        "scope",
        "risk_level",
        "created_at",
        "killed_reason",
    },
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def valid_risk_level(value: str) -> bool:
    return value in RISK_LEVELS


@dataclass(frozen=True, slots=True)
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int = int(DEFAULT_AUTONOMY)
    status: str = AgentStatus.PROPOSED.value
    allowed_tools: tuple[str, ...] = ()
    kill_switch_owner: str = ""
    notes: str = ""
    role: str = ""
    scope: str = ""
    risk_level: str = "low"
    created_at: str = ""
    killed_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["allowed_tools"] = list(self.allowed_tools)
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentCard:
        clean = {k: v for k, v in data.items() if k in _CARD_FIELDS}
        if "allowed_tools" in clean and clean["allowed_tools"] is not None:
            clean["allowed_tools"] = tuple(clean["allowed_tools"])
        return cls(**clean)


def agent_card_valid(card: AgentCard) -> bool:
    """Structural validity — non-blank identity, in-range autonomy + status."""
    if not (
        card.agent_id.strip()
        and card.name.strip()
        and card.owner.strip()
        and card.purpose.strip()
    ):
        return False
    if not (0 <= int(card.autonomy_level) <= int(AutonomyLevel.L5_FULLY_AUTONOMOUS)):
        return False
    return bool(card.status.strip())


def new_card(
    *,
    agent_id: str,
    name: str,
    owner: str,
    purpose: str,
    autonomy_level: int | AutonomyLevel = DEFAULT_AUTONOMY,
    allowed_tools: list[str] | None = None,
    kill_switch_owner: str = "",
    notes: str = "",
    role: str = "",
    scope: str = "",
    risk_level: str = "low",
) -> AgentCard:
    """Build a validated, governed agent card.

    Raises ValueError when any non-negotiable identity/governance rule fails.
    """
    if not agent_id.strip():
        raise ValueError("agent_id is required")
    if not name.strip():
        raise ValueError("name is required")
    if not owner.strip():
        raise ValueError("owner is required")
    if not purpose.strip():
        raise ValueError("purpose is required")

    level = coerce_autonomy(autonomy_level)
    if autonomy_blocked_in_mvp(level):
        raise ValueError("autonomy L5 (fully autonomous) is blocked in the MVP")

    owner_clean = owner.strip()
    ks_owner = kill_switch_owner.strip() or owner_clean
    if requires_kill_switch_owner(level) and not kill_switch_owner.strip():
        raise ValueError("autonomy L4+ requires an explicit kill_switch_owner")

    if not valid_risk_level(risk_level):
        raise ValueError(f"risk_level must be one of {sorted(RISK_LEVELS)}")

    tools = tuple(allowed_tools or ())
    blocked = forbidden_tools_in(tools)
    if blocked:
        raise ValueError(f"allowed_tools contains forbidden tools: {blocked}")

    return AgentCard(
        agent_id=agent_id.strip(),
        name=name.strip(),
        owner=owner_clean,
        purpose=purpose.strip(),
        autonomy_level=int(level),
        status=AgentStatus.PROPOSED.value,
        allowed_tools=tools,
        kill_switch_owner=ks_owner,
        notes=notes.strip(),
        role=role.strip(),
        scope=scope.strip(),
        risk_level=risk_level,
        created_at=_now_iso(),
    )


__all__ = [
    "RISK_LEVELS",
    "AgentCard",
    "agent_card_valid",
    "new_card",
    "valid_risk_level",
]
