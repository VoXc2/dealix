"""Friction Log — capture adoption friction; surfaces productization candidates."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FrictionType(str, Enum):
    DATA = "data_friction"
    APPROVAL = "approval_friction"
    USER_CONFUSION = "user_confusion"
    WORKFLOW_AMBIGUITY = "workflow_ambiguity"
    TRUST = "trust_concern"
    ARABIC_QUALITY = "arabic_quality_issue"
    INTEGRATION = "integration_issue"
    PRICING = "pricing_concern"


@dataclass(frozen=True)
class FrictionEvent:
    friction_id: str
    client_id: str
    type: FrictionType
    description: str
    impact: str
    response: str
    product_signal: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


class FrictionLog:
    def __init__(self) -> None:
        self._events: list[FrictionEvent] = []

    def append(self, ev: FrictionEvent) -> FrictionEvent:
        self._events.append(ev)
        return ev

    def all(self) -> tuple[FrictionEvent, ...]:
        return tuple(self._events)

    def by_type(self, ft: FrictionType) -> tuple[FrictionEvent, ...]:
        return tuple(e for e in self._events if e.type is ft)

    def product_candidates(self, min_repetitions: int = 3) -> tuple[str, ...]:
        """Return product signals that have repeated above the threshold."""

        counts: dict[str, int] = {}
        for ev in self._events:
            if ev.product_signal:
                counts[ev.product_signal] = counts.get(ev.product_signal, 0) + 1
        return tuple(p for p, n in counts.items() if n >= min_repetitions)
