"""Client Proof Timeline — chronological proof + value + blocked-risk events."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class TimelineEventKind(str, Enum):
    PROOF = "proof_event"
    VALUE = "value_event"
    BLOCKED_RISK = "blocked_risk"
    APPROVAL = "approval"


@dataclass(frozen=True)
class ProofTimelineEvent:
    event_id: str
    kind: TimelineEventKind
    title: str
    description: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = field(default_factory=dict)


class ProofTimeline:
    def __init__(self, client_id: str) -> None:
        self.client_id = client_id
        self._events: list[ProofTimelineEvent] = []

    def append(self, ev: ProofTimelineEvent) -> ProofTimelineEvent:
        self._events.append(ev)
        return ev

    def all(self) -> tuple[ProofTimelineEvent, ...]:
        return tuple(sorted(self._events, key=lambda e: e.timestamp))

    def by_kind(self, kind: TimelineEventKind) -> tuple[ProofTimelineEvent, ...]:
        return tuple(e for e in self._events if e.kind is kind)
