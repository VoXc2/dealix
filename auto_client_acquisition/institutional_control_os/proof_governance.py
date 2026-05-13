"""Institutional Proof Score — six-component weighted score.

See ``docs/institutional_control/PROOF_AS_GOVERNANCE_ARTIFACT.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProofDecisionTier(str, Enum):
    CASE_CANDIDATE = "case_candidate"     # 85+
    SALES_SUPPORT = "sales_support"       # 70..84
    INTERNAL_LEARNING = "internal_learning"  # <70


# Institutional weights — total 100.
INSTITUTIONAL_PROOF_WEIGHTS: dict[str, int] = {
    "metric_clarity": 20,
    "evidence_quality": 20,
    "source_clarity": 15,
    "governance_confidence": 15,
    "business_relevance": 15,
    "retainer_linkage": 15,
}


@dataclass(frozen=True)
class InstitutionalProofComponents:
    """Each component is 0..100; the score is the weighted average."""

    metric_clarity: int
    evidence_quality: int
    source_clarity: int
    governance_confidence: int
    business_relevance: int
    retainer_linkage: int

    def __post_init__(self) -> None:
        for name in INSTITUTIONAL_PROOF_WEIGHTS:
            value = getattr(self, name)
            if not 0 <= value <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_institutional_proof_score(
    components: InstitutionalProofComponents,
) -> int:
    weighted = 0.0
    for name, weight in INSTITUTIONAL_PROOF_WEIGHTS.items():
        weighted += getattr(components, name) * (weight / 100.0)
    return round(weighted)


def classify_proof_score(score: int) -> ProofDecisionTier:
    if score >= 85:
        return ProofDecisionTier.CASE_CANDIDATE
    if score >= 70:
        return ProofDecisionTier.SALES_SUPPORT
    return ProofDecisionTier.INTERNAL_LEARNING
