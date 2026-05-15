"""Lifecycle unit economics governance primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LifecycleEconomicsInputs:
    monthly_revenue_sar: float
    monthly_delivery_cost_sar: float
    acquisition_cost_sar: float
    retention_months: float
    expansion_revenue_sar: float = 0.0


@dataclass(frozen=True, slots=True)
class LifecycleEconomicsSnapshot:
    gross_margin_pct: float
    contribution_margin_sar: float
    ltv_sar: float
    cac_payback_months: float


def compute_lifecycle_economics(inputs: LifecycleEconomicsInputs) -> LifecycleEconomicsSnapshot:
    revenue = max(0.0, float(inputs.monthly_revenue_sar))
    cost = max(0.0, float(inputs.monthly_delivery_cost_sar))
    acquisition = max(0.0, float(inputs.acquisition_cost_sar))
    retention = max(1.0, float(inputs.retention_months))
    expansion = max(0.0, float(inputs.expansion_revenue_sar))

    contribution_monthly = revenue - cost
    gross_margin_pct = round(0.0 if revenue <= 0 else (contribution_monthly / revenue) * 100.0, 2)
    ltv = round((contribution_monthly * retention) + expansion, 2)
    payback = round(float("inf") if contribution_monthly <= 0 else acquisition / contribution_monthly, 2)

    return LifecycleEconomicsSnapshot(
        gross_margin_pct=gross_margin_pct,
        contribution_margin_sar=round(contribution_monthly, 2),
        ltv_sar=ltv,
        cac_payback_months=payback,
    )


def margin_floor_violation(snapshot: LifecycleEconomicsSnapshot, floor_pct: float = 35.0) -> bool:
    return snapshot.gross_margin_pct < float(floor_pct)


__all__ = [
    "LifecycleEconomicsInputs",
    "LifecycleEconomicsSnapshot",
    "compute_lifecycle_economics",
    "margin_floor_violation",
]
