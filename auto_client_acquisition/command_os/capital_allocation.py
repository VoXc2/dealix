"""World-class capital allocation score — distinct weights from intelligence_os capital_allocator."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class WorldClassAllocationInputs(NamedTuple):
    """Subscores 0–100 for investment prioritization."""

    revenue_impact: float
    margin_impact: float
    risk_reduction: float
    proof_creation: float
    productization_potential: float
    market_authority: float
    strategic_fit: float


class WorldClassAllocationBand(StrEnum):
    INVEST_HARD = "invest_hard"
    BUILD = "build"
    PILOT = "pilot"
    HOLD = "hold"
    KILL = "kill"


def compute_world_class_allocation_score(inputs: WorldClassAllocationInputs) -> float:
    w = (
        0.20 * inputs.revenue_impact
        + 0.15 * inputs.margin_impact
        + 0.15 * inputs.risk_reduction
        + 0.15 * inputs.proof_creation
        + 0.15 * inputs.productization_potential
        + 0.10 * inputs.market_authority
        + 0.10 * inputs.strategic_fit
    )
    return max(0.0, min(100.0, float(w)))


def world_class_allocation_band(score: float) -> WorldClassAllocationBand:
    if score >= 85:
        return WorldClassAllocationBand.INVEST_HARD
    if score >= 70:
        return WorldClassAllocationBand.BUILD
    if score >= 55:
        return WorldClassAllocationBand.PILOT
    if score >= 40:
        return WorldClassAllocationBand.HOLD
    return WorldClassAllocationBand.KILL
