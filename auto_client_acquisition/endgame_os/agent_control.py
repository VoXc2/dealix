"""Agent Control Doctrine — Agent Cards and the Agent Registry.

Every agent that runs inside or on behalf of Dealix must be backed by an
``AgentCard``. Agents without a card cannot be invoked by the LLM gateway.

See ``docs/endgame/AGENT_CONTROL_DOCTRINE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum


class AutonomyLevel(IntEnum):
    READ = 0
    ANALYZE = 1
    DRAFT_RECOMMEND = 2
    QUEUE_FOR_APPROVAL = 3
    EXECUTE_INTERNAL_AFTER_APPROVAL = 4
    EXTERNAL_RESTRICTED = 5
    AUTONOMOUS_EXTERNAL_FORBIDDEN = 6


DEFAULT_AUTONOMY: AutonomyLevel = AutonomyLevel.DRAFT_RECOMMEND


@dataclass(frozen=True)
class AgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    allowed_inputs: tuple[str, ...] = ()
    forbidden_actions: tuple[str, ...] = ()
    autonomy_level: AutonomyLevel = DEFAULT_AUTONOMY
    approval_required_for: tuple[str, ...] = ()
    audit_required: bool = True

    def __post_init__(self) -> None:
        if self.autonomy_level >= AutonomyLevel.AUTONOMOUS_EXTERNAL_FORBIDDEN:
            raise ValueError(
                "autonomous_external_action_forbidden_by_doctrine"
            )
        if not self.agent_id:
            raise ValueError("agent_id_required")
        if not self.owner:
            raise ValueError("owner_required")

    def can_perform(self, action: str) -> bool:
        """Return True only if the action is not explicitly forbidden."""

        return action not in self.forbidden_actions

    def requires_approval(self, action_class: str) -> bool:
        return action_class in self.approval_required_for


@dataclass
class _AgentRegistryRow:
    card: AgentCard
    status: str = "active"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AgentRegistry:
    """In-memory agent registry.

    Persistence is intentionally out of scope here; the registry is the
    typed interface. Storage backends adapt to this surface.
    """

    def __init__(self) -> None:
        self._rows: dict[str, _AgentRegistryRow] = {}

    def register(self, card: AgentCard) -> AgentCard:
        if card.agent_id in self._rows:
            raise ValueError(f"agent_already_registered:{card.agent_id}")
        self._rows[card.agent_id] = _AgentRegistryRow(card=card)
        return card

    def get(self, agent_id: str) -> AgentCard:
        row = self._rows.get(agent_id)
        if row is None or row.status != "active":
            raise LookupError(f"agent_not_available:{agent_id}")
        return row.card

    def pause(self, agent_id: str) -> None:
        row = self._rows.get(agent_id)
        if row is None:
            raise LookupError(f"agent_not_found:{agent_id}")
        row.status = "paused"
        row.updated_at = datetime.now(timezone.utc)

    def retire(self, agent_id: str) -> None:
        row = self._rows.get(agent_id)
        if row is None:
            raise LookupError(f"agent_not_found:{agent_id}")
        row.status = "retired"
        row.updated_at = datetime.now(timezone.utc)

    def list_active(self) -> tuple[AgentCard, ...]:
        return tuple(
            row.card for row in self._rows.values() if row.status == "active"
        )
