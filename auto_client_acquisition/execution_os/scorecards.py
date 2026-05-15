"""Scorecard aggregates + execution law (work must produce asset-class outputs)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ExecutionWorkTier = Literal["stop", "cautious", "moderate", "priority"]

EXECUTION_OUTPUT_BUCKETS: frozenset[str] = frozenset(
    {
        "revenue",
        "proof",
        "trust",
        "product",
        "knowledge",
        "distribution",
        "governance",
        "capital",
    },
)


def execution_work_tier(produced: frozenset[str]) -> ExecutionWorkTier:
    """How to treat work based on how many output buckets it feeds."""
    n = len(produced & EXECUTION_OUTPUT_BUCKETS)
    if n == 0:
        return "stop"
    if n == 1:
        return "cautious"
    if n == 2:
        return "moderate"
    return "priority"


@dataclass(frozen=True, slots=True)
class ProjectScorecard:
    scope_clarity: int
    data_readiness: int
    governance_safety: int
    qa: int
    proof_strength: int
    capital_creation: int
    margin: int
    retainer_readiness: int

    def __post_init__(self) -> None:
        for name, val in (
            ("scope_clarity", self.scope_clarity),
            ("data_readiness", self.data_readiness),
            ("governance_safety", self.governance_safety),
            ("qa", self.qa),
            ("proof_strength", self.proof_strength),
            ("capital_creation", self.capital_creation),
            ("margin", self.margin),
            ("retainer_readiness", self.retainer_readiness),
        ):
            if not 0 <= val <= 100:
                msg = f"{name} must be 0..100, got {val}"
                raise ValueError(msg)


def average_project_score(card: ProjectScorecard) -> int:
    fields = (
        card.scope_clarity,
        card.data_readiness,
        card.governance_safety,
        card.qa,
        card.proof_strength,
        card.capital_creation,
        card.margin,
        card.retainer_readiness,
    )
    return sum(fields) // len(fields)
