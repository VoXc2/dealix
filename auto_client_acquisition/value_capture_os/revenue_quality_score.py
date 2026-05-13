"""Revenue Quality Score — 6 dimensions weighted to 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


REVENUE_QUALITY_WEIGHTS: dict[str, int] = {
    "margin": 20,
    "repeatability": 20,
    "retainer_potential": 20,
    "proof_strength": 15,
    "governance_safety": 15,
    "productization_signal": 10,
}


class RevenueTier(str, Enum):
    EXCELLENT = "excellent"  # 85+
    GOOD = "good"            # 70..84
    CAUTION = "caution"      # 55..69
    BAD = "bad"              # <55


@dataclass(frozen=True)
class RevenueQualityComponents:
    margin: int
    repeatability: int
    retainer_potential: int
    proof_strength: int
    governance_safety: int
    productization_signal: int

    def __post_init__(self) -> None:
        for name in REVENUE_QUALITY_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_revenue_quality_score(c: RevenueQualityComponents) -> int:
    weighted = 0.0
    for name, weight in REVENUE_QUALITY_WEIGHTS.items():
        weighted += getattr(c, name) * (weight / 100.0)
    return round(weighted)


def classify_revenue_tier(score: int) -> RevenueTier:
    if score >= 85:
        return RevenueTier.EXCELLENT
    if score >= 70:
        return RevenueTier.GOOD
    if score >= 55:
        return RevenueTier.CAUTION
    return RevenueTier.BAD
