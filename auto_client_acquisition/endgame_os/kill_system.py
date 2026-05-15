"""Kill system — deprioritize services/features/markets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KillServiceSignals:
    low_win_rate: bool
    low_margin: bool
    high_scope_creep: bool
    weak_proof: bool
    no_retainer_path: bool
    high_governance_risk: bool
    no_repeatability: bool


@dataclass(frozen=True, slots=True)
class KillFeatureSignals:
    not_reused: bool
    not_tied_to_revenue: bool
    maintenance_drag: bool
    no_delivery_effort_reduction: bool


@dataclass(frozen=True, slots=True)
class KillMarketSignals:
    buyer_unclear: bool
    budget_weak: bool
    sales_cycle_too_long: bool
    data_risk_too_high: bool
    no_proof_path: bool


def should_kill_service(s: KillServiceSignals) -> bool:
    flags = sum(
        1
        for b in (
            s.low_win_rate,
            s.low_margin,
            s.high_scope_creep,
            s.weak_proof,
            s.no_retainer_path,
            s.high_governance_risk,
            s.no_repeatability,
        )
        if b
    )
    return flags >= 3


def should_kill_feature(s: KillFeatureSignals) -> bool:
    return s.not_reused and (s.not_tied_to_revenue or s.maintenance_drag or s.no_delivery_effort_reduction)


def should_kill_market(s: KillMarketSignals) -> bool:
    return sum(1 for b in (s.buyer_unclear, s.budget_weak, s.data_risk_too_high, s.no_proof_path) if b) >= 2
