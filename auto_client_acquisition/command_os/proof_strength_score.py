"""Proof strength score — quality of a proof pack for external use."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class ProofStrengthInputs(NamedTuple):
    """Subscores 0–100."""

    metric_clarity: float
    evidence_quality: float
    before_after_comparison: float
    client_relevance: float
    governance_confidence: float
    retainer_linkage: float


class ProofPackUseTier(StrEnum):
    CASE_CANDIDATE = "case_candidate"
    SALES_SUPPORT = "sales_support"
    INTERNAL_ONLY = "internal_learning_only"


def compute_proof_strength_score(inputs: ProofStrengthInputs) -> float:
    w = (
        0.20 * inputs.metric_clarity
        + 0.20 * inputs.evidence_quality
        + 0.15 * inputs.before_after_comparison
        + 0.15 * inputs.client_relevance
        + 0.15 * inputs.governance_confidence
        + 0.15 * inputs.retainer_linkage
    )
    return max(0.0, min(100.0, float(w)))


def proof_pack_use_tier(score: float) -> ProofPackUseTier:
    if score >= 85:
        return ProofPackUseTier.CASE_CANDIDATE
    if score >= 70:
        return ProofPackUseTier.SALES_SUPPORT
    return ProofPackUseTier.INTERNAL_ONLY
