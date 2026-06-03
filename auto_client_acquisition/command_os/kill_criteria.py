"""Kill criteria — deterministic recommendations from operational signals."""

from __future__ import annotations

from typing import NamedTuple


class KillServiceSignals(NamedTuple):
    win_rate: float  # %
    margin: float  # %
    scope_creep_index: float  # 0–100 higher worse
    proof_strength: float  # 0–100
    retainer_path: bool
    governance_risk: float  # 0–100 higher worse
    repeatability: float  # 0–100


class KillMarketSignals(NamedTuple):
    buyers_clear: bool
    data_risky: bool
    budget_strong: bool
    sales_cycle_months: float
    proof_path: bool


def kill_service_recommended(s: KillServiceSignals) -> bool:
    return (
        s.win_rate < 35
        or s.margin < 25
        or s.scope_creep_index >= 70
        or s.proof_strength < 55
        or not s.retainer_path
        or s.governance_risk >= 75
        or s.repeatability < 45
    )


def kill_feature_recommended(
    *,
    reused: bool,
    saves_time: bool,
    revenue_linked: bool,
    maintenance_drag_high: bool,
    reduces_delivery_effort: bool = True,
) -> bool:
    return (
        maintenance_drag_high
        or not reused
        or not saves_time
        or not revenue_linked
        or not reduces_delivery_effort
    )


def kill_market_recommended(s: KillMarketSignals) -> bool:
    if s.data_risky:
        return True
    if not s.buyers_clear:
        return True
    if not s.budget_strong:
        return True
    if s.sales_cycle_months > 9:
        return True
    return not s.proof_path
