"""Responsible AI Score — 7 dimensions, total 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


RESPONSIBLE_AI_WEIGHTS: dict[str, int] = {
    "source_clarity": 15,
    "data_sensitivity_handling": 15,
    "human_oversight": 15,
    "governance_decision_coverage": 15,
    "auditability": 15,
    "proof_of_value": 15,
    "incident_readiness": 10,
}


class ResponsibleAITier(str, Enum):
    READY = "ready"                                  # 85+
    READY_WITH_CONTROLS = "ready_with_controls"      # 70..84
    GOVERNANCE_REVIEW_REQUIRED = "governance_review_required"  # 55..69
    DO_NOT_DEPLOY = "do_not_deploy"                  # <55


@dataclass(frozen=True)
class ResponsibleAIComponents:
    source_clarity: int
    data_sensitivity_handling: int
    human_oversight: int
    governance_decision_coverage: int
    auditability: int
    proof_of_value: int
    incident_readiness: int

    def __post_init__(self) -> None:
        for name in RESPONSIBLE_AI_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_responsible_ai_score(c: ResponsibleAIComponents) -> int:
    weighted = 0.0
    for name, w in RESPONSIBLE_AI_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_responsible_ai(score: int) -> ResponsibleAITier:
    if score >= 85:
        return ResponsibleAITier.READY
    if score >= 70:
        return ResponsibleAITier.READY_WITH_CONTROLS
    if score >= 55:
        return ResponsibleAITier.GOVERNANCE_REVIEW_REQUIRED
    return ResponsibleAITier.DO_NOT_DEPLOY
