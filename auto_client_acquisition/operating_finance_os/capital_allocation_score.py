"""Capital Allocation Score — 8 dimensions, total 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


CAPITAL_ALLOCATION_WEIGHTS: dict[str, int] = {
    "revenue_impact": 20,
    "repeatability": 15,
    "margin_improvement": 15,
    "governance_value": 15,
    "proof_strength": 10,
    "productization_potential": 10,
    "strategic_moat": 10,
    "speed_to_learn": 5,
}


class CapitalAllocationTier(str, Enum):
    INVEST_NOW = "invest_now"        # 85+
    BUILD_SMALL_MVP = "build_small_mvp"  # 70..84
    TEST_MANUALLY = "test_manually"  # 55..69
    HOLD_OR_REJECT = "hold_or_reject"  # <55


@dataclass(frozen=True)
class CapitalAllocationComponents:
    revenue_impact: int
    repeatability: int
    margin_improvement: int
    governance_value: int
    proof_strength: int
    productization_potential: int
    strategic_moat: int
    speed_to_learn: int

    def __post_init__(self) -> None:
        for name in CAPITAL_ALLOCATION_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_capital_allocation_score(c: CapitalAllocationComponents) -> int:
    weighted = 0.0
    for name, w in CAPITAL_ALLOCATION_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_capital_allocation(score: int) -> CapitalAllocationTier:
    if score >= 85:
        return CapitalAllocationTier.INVEST_NOW
    if score >= 70:
        return CapitalAllocationTier.BUILD_SMALL_MVP
    if score >= 55:
        return CapitalAllocationTier.TEST_MANUALLY
    return CapitalAllocationTier.HOLD_OR_REJECT
