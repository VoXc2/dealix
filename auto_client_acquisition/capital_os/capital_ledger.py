"""Capital ledger — records reusable assets produced by governed delivery."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapitalLedgerEvent:
    capital_event_id: str
    project_id: str
    client_id: str
    asset_type: str
    title: str
    description: str
    evidence: str


def capital_ledger_event_valid(event: CapitalLedgerEvent) -> bool:
    return all(
        (
            event.capital_event_id.strip(),
            event.project_id.strip(),
            event.client_id.strip(),
            event.asset_type.strip(),
            event.title.strip(),
            event.description.strip(),
            event.evidence.strip(),
        ),
    )


__all__ = ["CapitalLedgerEvent", "capital_ledger_event_valid"]
