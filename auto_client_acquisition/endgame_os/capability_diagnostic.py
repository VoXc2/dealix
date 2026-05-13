"""Capability Diagnostic — scoring and report shape.

See ``docs/endgame/CAPABILITY_DIAGNOSTIC.md``. Every axis is scored 0–5
and produces a structured recommendation that points back into the
productized offer stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CapabilityAxis(str, Enum):
    REVENUE = "revenue"
    DATA = "data"
    GOVERNANCE = "governance"
    KNOWLEDGE = "knowledge"
    OPERATIONS = "operations"
    PROOF = "proof"


@dataclass(frozen=True)
class CapabilityScore:
    axis: CapabilityAxis
    score: int  # 0..5

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 5:
            raise ValueError("score_out_of_range_0_5")


# Mapping from the weakest axis to the recommended sprint. The diagnostic
# recommends one sprint at a time — see the doctrine.
RECOMMENDED_SPRINT_BY_AXIS: dict[CapabilityAxis, str] = {
    CapabilityAxis.REVENUE: "Revenue Intelligence Sprint",
    CapabilityAxis.DATA: "Revenue Intelligence Sprint",
    CapabilityAxis.GOVERNANCE: "AI Governance Review",
    CapabilityAxis.KNOWLEDGE: "Company Brain Sprint",
    CapabilityAxis.OPERATIONS: "AI Quick Win Sprint",
    CapabilityAxis.PROOF: "AI Governance Review",
}


# Natural retainer that follows the recommended sprint.
RETAINER_BY_SPRINT: dict[str, str] = {
    "Revenue Intelligence Sprint": "Monthly RevOps OS",
    "AI Governance Review": "Monthly Governance",
    "Company Brain Sprint": "Monthly Company Brain",
    "AI Quick Win Sprint": "Monthly AI Ops",
}


@dataclass(frozen=True)
class CapabilityDiagnosticReport:
    client: str
    scores: tuple[CapabilityScore, ...]
    transformation_gap: str
    data_readiness: bool
    governance_risk: str
    highest_value_opportunity: str
    recommended_sprint: str
    expected_proof: tuple[str, ...]
    retainer_path: str
    notes: tuple[str, ...] = field(default_factory=tuple)

    def composite(self) -> float:
        if not self.scores:
            return 0.0
        return sum(s.score for s in self.scores) / len(self.scores)

    def weakest_axis(self) -> CapabilityAxis:
        return min(self.scores, key=lambda s: s.score).axis


def recommend_sprint(scores: tuple[CapabilityScore, ...]) -> tuple[str, str]:
    """Return ``(sprint, retainer)`` for the weakest scored axis."""

    if not scores:
        raise ValueError("scores_required")
    weakest = min(scores, key=lambda s: s.score).axis
    sprint = RECOMMENDED_SPRINT_BY_AXIS[weakest]
    return sprint, RETAINER_BY_SPRINT[sprint]
