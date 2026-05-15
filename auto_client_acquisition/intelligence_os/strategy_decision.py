"""Strategy Office decision score — composite 0–100 and primary band for CEO."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class StrategySignalInputs(NamedTuple):
    """Subscores 0–100 after normalization from ledgers/metrics."""

    revenue_signal: float
    margin_signal: float
    proof_signal: float
    repeatability_signal: float
    governance_safety: float
    productization_signal: float
    strategic_moat: float


class StrategyDecisionBand(StrEnum):
    SCALE = "scale"
    BUILD = "build"
    PILOT = "pilot"
    HOLD = "hold"
    KILL = "kill"


def compute_strategy_decision_score(inputs: StrategySignalInputs) -> float:
    w = (
        0.20 * inputs.revenue_signal
        + 0.15 * inputs.margin_signal
        + 0.15 * inputs.proof_signal
        + 0.15 * inputs.repeatability_signal
        + 0.15 * inputs.governance_safety
        + 0.10 * inputs.productization_signal
        + 0.10 * inputs.strategic_moat
    )
    return max(0.0, min(100.0, float(w)))


def strategy_decision_band(score: float) -> StrategyDecisionBand:
    if score >= 85:
        return StrategyDecisionBand.SCALE
    if score >= 70:
        return StrategyDecisionBand.BUILD
    if score >= 55:
        return StrategyDecisionBand.PILOT
    if score >= 40:
        return StrategyDecisionBand.HOLD
    return StrategyDecisionBand.KILL
