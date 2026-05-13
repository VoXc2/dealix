"""Proof Command — proof score computation and decision tiers.

See ``docs/command_control/PROOF_COMMAND.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from auto_client_acquisition.proof_engine.evidence import EvidenceLevel


class ProofDecisionTier(str, Enum):
    CASE_CANDIDATE = "case_candidate"     # score >= 85
    SALES_SUPPORT = "sales_support"       # 70 <= score < 85
    INTERNAL_LEARNING = "internal_learning"  # score < 70


@dataclass(frozen=True)
class ProofScoreInputs:
    """Inputs to the proof score.

    Each component is 0..1; the score is the weighted composite mapped
    to 0..100.
    """

    metric_quality: float           # baseline + delta strength
    evidence_level: EvidenceLevel
    reproducibility: float          # 0..1
    governance_event_richness: float  # 0..1

    def __post_init__(self) -> None:
        for name, value in (
            ("metric_quality", self.metric_quality),
            ("reproducibility", self.reproducibility),
            ("governance_event_richness", self.governance_event_richness),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name}_out_of_range_0_1")


def compute_proof_score(inputs: ProofScoreInputs) -> int:
    """Compute a 0..100 proof score from weighted components."""

    evidence_norm = int(inputs.evidence_level) / int(EvidenceLevel.L5_REVENUE_EXPANSION)
    weighted = (
        0.40 * inputs.metric_quality
        + 0.25 * evidence_norm
        + 0.20 * inputs.reproducibility
        + 0.15 * inputs.governance_event_richness
    )
    return round(max(0.0, min(1.0, weighted)) * 100)


def classify_proof_score(score: int) -> ProofDecisionTier:
    if score >= 85:
        return ProofDecisionTier.CASE_CANDIDATE
    if score >= 70:
        return ProofDecisionTier.SALES_SUPPORT
    return ProofDecisionTier.INTERNAL_LEARNING
