"""Value Ledger — typed Value Events captured per engagement."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ValueType(str, Enum):
    REVENUE = "Revenue Proof"
    TIME = "Time Proof"
    QUALITY = "Quality Proof"
    RISK = "Risk Proof"
    KNOWLEDGE = "Knowledge Proof"


@dataclass(frozen=True)
class ValueEvent:
    value_event_id: str
    project_id: str
    client_id: str
    value_type: ValueType
    metric: str
    before: float
    after: float
    evidence: str
    confidence: str  # low | medium | high
    limitations: str

    def delta(self) -> float:
        return self.after - self.before


class ValueLedger:
    def __init__(self) -> None:
        self._events: list[ValueEvent] = []
        self._ids: set[str] = set()

    def append(self, ev: ValueEvent) -> ValueEvent:
        if ev.value_event_id in self._ids:
            raise ValueError(f"duplicate_value_event:{ev.value_event_id}")
        self._ids.add(ev.value_event_id)
        self._events.append(ev)
        return ev

    def all(self) -> tuple[ValueEvent, ...]:
        return tuple(self._events)

    def for_client(self, client_id: str) -> tuple[ValueEvent, ...]:
        return tuple(e for e in self._events if e.client_id == client_id)

    def by_type(self, value_type: ValueType) -> tuple[ValueEvent, ...]:
        return tuple(e for e in self._events if e.value_type is value_type)
