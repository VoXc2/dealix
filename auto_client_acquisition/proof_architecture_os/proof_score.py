"""Enterprise Proof Score v2 — eight weighted dimensions (0–100)."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (15, 15, 15, 15, 15, 10, 10, 5)


@dataclass(frozen=True, slots=True)
class EnterpriseProofDimensions:
    metric_clarity: int
    source_clarity: int
    evidence_quality: int
    governance_confidence: int
    business_relevance: int
    before_after_comparison: int
    retainer_linkage: int
    limitations_honesty: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def enterprise_proof_score(dimensions: EnterpriseProofDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.metric_clarity),
        _clamp_pct(d.source_clarity),
        _clamp_pct(d.evidence_quality),
        _clamp_pct(d.governance_confidence),
        _clamp_pct(d.business_relevance),
        _clamp_pct(d.before_after_comparison),
        _clamp_pct(d.retainer_linkage),
        _clamp_pct(d.limitations_honesty),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def proof_score_band(score: int) -> str:
    if score >= 85:
        return "case_candidate"
    if score >= 70:
        return "sales_support"
    if score >= 55:
        return "internal_learning"
    return "weak_proof"


def proof_allows_case_study(score: int) -> bool:
    return score >= 85


def proof_allows_sales_asset(score: int) -> bool:
    return score >= 70


def proof_allows_retainer_pitch(score: int) -> bool:
    return score >= 80
