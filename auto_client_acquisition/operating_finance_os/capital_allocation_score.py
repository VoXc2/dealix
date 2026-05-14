"""Capital allocation score — weighted investment prioritization (0–100)."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (20, 15, 15, 15, 10, 10, 10, 5)


@dataclass(frozen=True, slots=True)
class CapitalAllocationDimensions:
    revenue_impact: int
    repeatability: int
    margin_improvement: int
    governance_value: int
    proof_strength: int
    productization_potential: int
    strategic_moat: int
    speed_to_learn: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def capital_allocation_score(dimensions: CapitalAllocationDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.revenue_impact),
        _clamp_pct(d.repeatability),
        _clamp_pct(d.margin_improvement),
        _clamp_pct(d.governance_value),
        _clamp_pct(d.proof_strength),
        _clamp_pct(d.productization_potential),
        _clamp_pct(d.strategic_moat),
        _clamp_pct(d.speed_to_learn),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def capital_allocation_band(score: int) -> str:
    if score >= 85:
        return "invest_now"
    if score >= 70:
        return "build_small_mvp"
    if score >= 55:
        return "test_manually"
    return "hold_or_reject"
