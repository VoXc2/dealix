"""Proof Score v2 — 8-component weighted score (total 100)."""

from __future__ import annotations

from dataclasses import dataclass


PROOF_SCORE_V2_WEIGHTS: dict[str, int] = {
    "metric_clarity": 15,
    "source_clarity": 15,
    "evidence_quality": 15,
    "governance_confidence": 15,
    "business_relevance": 15,
    "before_after_comparison": 10,
    "retainer_linkage": 10,
    "limitations_honesty": 5,
}


@dataclass(frozen=True)
class ProofComponentsV2:
    metric_clarity: int
    source_clarity: int
    evidence_quality: int
    governance_confidence: int
    business_relevance: int
    before_after_comparison: int
    retainer_linkage: int
    limitations_honesty: int

    def __post_init__(self) -> None:
        for name in PROOF_SCORE_V2_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_proof_score_v2(c: ProofComponentsV2) -> int:
    weighted = 0.0
    for name, weight in PROOF_SCORE_V2_WEIGHTS.items():
        weighted += getattr(c, name) * (weight / 100.0)
    return round(weighted)
