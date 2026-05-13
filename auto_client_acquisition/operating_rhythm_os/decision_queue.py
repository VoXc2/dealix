"""Decision Queue — append-only typed queue for execution decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class DecisionType(str, Enum):
    BUILD = "build"
    SCALE = "scale"
    KILL = "kill"
    HOLD = "hold"
    OFFER_RETAINER = "offer_retainer"
    RAISE_PRICE = "raise_price"
    REJECT_REVENUE = "reject_revenue"
    CREATE_PLAYBOOK = "create_playbook"
    CREATE_BENCHMARK = "create_benchmark"
    CREATE_STANDARD = "create_standard"
    CREATE_VENTURE_CANDIDATE = "create_venture_candidate"


class DecisionStatus(str, Enum):
    PENDING = "pending"
    DECIDED = "decided"
    DEFERRED = "deferred"
    REJECTED = "rejected"


@dataclass(frozen=True)
class DecisionQueueEntry:
    decision_id: str
    type: DecisionType
    target: str
    evidence: tuple[str, ...]
    owner: str
    deadline: str
    decision_status: DecisionStatus = DecisionStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError("decision_requires_evidence")
        if not self.owner:
            raise ValueError("decision_requires_owner")


class DecisionQueue:
    def __init__(self) -> None:
        self._entries: list[DecisionQueueEntry] = []
        self._ids: set[str] = set()

    def append(self, entry: DecisionQueueEntry) -> DecisionQueueEntry:
        if entry.decision_id in self._ids:
            raise ValueError(f"duplicate_decision_id:{entry.decision_id}")
        self._ids.add(entry.decision_id)
        self._entries.append(entry)
        return entry

    def pending(self) -> tuple[DecisionQueueEntry, ...]:
        return tuple(e for e in self._entries if e.decision_status is DecisionStatus.PENDING)

    def by_type(self, t: DecisionType) -> tuple[DecisionQueueEntry, ...]:
        return tuple(e for e in self._entries if e.type is t)
