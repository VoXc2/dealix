"""Revenue Quality Score — weighted 0–100 across six commercial-health dimensions."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (20, 20, 20, 15, 15, 10)


@dataclass(frozen=True, slots=True)
class RevenueQualityDimensions:
    margin: int
    repeatability: int
    retainer_potential: int
    proof_strength: int
    governance_safety: int
    productization_signal: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def revenue_quality_score(dimensions: RevenueQualityDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.margin),
        _clamp_pct(d.repeatability),
        _clamp_pct(d.retainer_potential),
        _clamp_pct(d.proof_strength),
        _clamp_pct(d.governance_safety),
        _clamp_pct(d.productization_signal),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def revenue_quality_band(score: int) -> str:
    if score >= 85:
        return "excellent_revenue"
    if score >= 70:
        return "good_revenue"
    if score >= 55:
        return "caution"
    return "bad_revenue"
