"""Capital priority score — weighted model for internal allocation decisions."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class PriorityInputs(NamedTuple):
    """Subscores on 0–100 (inclusive)."""

    revenue: float
    repeatability: float
    proof: float
    productization: float
    strategic_moat: float
    risk_adjusted: float


class PriorityBand(StrEnum):
    """Outcome band for capital / focus decisions."""

    INVEST_SCALE = "invest_scale"
    BUILD_CAREFULLY = "build_carefully"
    PILOT_ONLY = "pilot_only"
    HOLD = "hold"
    KILL = "kill"


def compute_capital_priority_score(inputs: PriorityInputs) -> float:
    """Return weighted priority 0–100."""
    w = (
        0.25 * inputs.revenue
        + 0.20 * inputs.repeatability
        + 0.20 * inputs.proof
        + 0.15 * inputs.productization
        + 0.10 * inputs.strategic_moat
        + 0.10 * inputs.risk_adjusted
    )
    return max(0.0, min(100.0, float(w)))


def capital_priority_band(score: float) -> PriorityBand:
    """Classify priority score into executive decision band."""
    if score >= 85:
        return PriorityBand.INVEST_SCALE
    if score >= 70:
        return PriorityBand.BUILD_CAREFULLY
    if score >= 55:
        return PriorityBand.PILOT_ONLY
    if score >= 40:
        return PriorityBand.HOLD
    return PriorityBand.KILL
