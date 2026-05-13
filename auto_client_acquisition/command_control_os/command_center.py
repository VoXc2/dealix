"""Command Center — decision shape and append-only decision log.

See ``docs/command_control/COMMAND_CENTER.md``. This module is the typed
contract for decisions surfaced by the Command Center; persistence is
out of scope.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class CommandDecisionType(str, Enum):
    SCALE = "SCALE"
    BUILD = "BUILD"
    PILOT = "PILOT"
    HOLD = "HOLD"
    KILL = "KILL"
    RAISE_PRICE = "RAISE_PRICE"
    PRODUCTIZE = "PRODUCTIZE"
    OFFER_RETAINER = "OFFER_RETAINER"
    CREATE_BUSINESS_UNIT = "CREATE_BUSINESS_UNIT"
    CREATE_VENTURE_CANDIDATE = "CREATE_VENTURE_CANDIDATE"


class CommandPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class CommandDecision:
    decision: CommandDecisionType
    target: str
    reason: str
    expected_impact: str
    priority: CommandPriority
    owner: str
    inputs: tuple[str, ...] = ()
    recommended_offer: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.target:
            raise ValueError("target_required")
        if not self.reason:
            raise ValueError("reason_required")
        if not self.owner:
            raise ValueError("owner_required")

    def to_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "target": self.target,
            "reason": self.reason,
            "expected_impact": self.expected_impact,
            "priority": self.priority.value,
            "owner": self.owner,
            "inputs": list(self.inputs),
            "recommended_offer": self.recommended_offer,
            "created_at": self.created_at.isoformat(),
        }


class DecisionLog:
    """Append-only log of structured Command Center decisions.

    The log is intentionally in-memory; storage adapters wrap this surface.
    """

    def __init__(self) -> None:
        self._entries: list[CommandDecision] = []

    def append(self, decision: CommandDecision) -> CommandDecision:
        self._entries.append(decision)
        return decision

    def all(self) -> tuple[CommandDecision, ...]:
        return tuple(self._entries)

    def by_type(self, decision_type: CommandDecisionType) -> tuple[CommandDecision, ...]:
        return tuple(d for d in self._entries if d.decision is decision_type)

    def latest_for(self, target: str) -> CommandDecision | None:
        for entry in reversed(self._entries):
            if entry.target == target:
                return entry
        return None
