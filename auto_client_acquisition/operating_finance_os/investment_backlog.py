"""Investment backlog row shape for capital dashboard."""

from __future__ import annotations

from dataclasses import dataclass

INVESTMENT_BACKLOG_FIELDS: tuple[str, ...] = (
    "investment_name",
    "allocation_score",
    "decision_band",
    "owner",
    "rationale",
    "expected_impact",
    "next_condition",
)


@dataclass(frozen=True, slots=True)
class InvestmentBacklogEntry:
    investment_name: str
    allocation_score: int
    decision_band: str
    owner: str
    rationale: str
    expected_impact: str
    next_condition: str


def investment_entry_complete(entry: InvestmentBacklogEntry) -> bool:
    return all(
        (
            entry.investment_name.strip(),
            entry.decision_band.strip(),
            entry.owner.strip(),
            entry.rationale.strip(),
            entry.expected_impact.strip(),
            entry.next_condition.strip(),
        ),
    )
