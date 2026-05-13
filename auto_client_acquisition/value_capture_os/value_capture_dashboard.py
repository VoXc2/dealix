"""Value Capture Dashboard — board-relevant capture metrics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValueCaptureDashboardSnapshot:
    period: str
    revenue_by_offer: dict[str, float]
    gross_margin_by_offer: dict[str, float]
    revenue_quality_score: float
    client_quality_score: float
    proof_to_retainer_conversion: float
    expansion_revenue: float
    platform_pull_signals: int
    partner_revenue: float
    academy_revenue: float
    venture_readiness: float
    bad_revenue_rejected: float
