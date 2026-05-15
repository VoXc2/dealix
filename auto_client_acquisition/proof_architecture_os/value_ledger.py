"""Value Ledger — auditable value events per engagement."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueLedgerEvent:
    value_event_id: str
    project_id: str
    client_id: str
    value_type: str
    metric: str
    before: int
    after: int
    evidence: str
    confidence: str
    limitations: str


def value_ledger_event_valid(event: ValueLedgerEvent) -> bool:
    return all(
        (
            event.value_event_id.strip(),
            event.project_id.strip(),
            event.client_id.strip(),
            event.value_type.strip(),
            event.metric.strip(),
            event.evidence.strip(),
            event.confidence.strip(),
            event.limitations.strip(),
        ),
    )
