"""Executive Operating System for weekly insights."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.forecasting import ExecutiveForecast, build_executive_forecast
from auto_client_acquisition.platform.org_health import OrgHealthSnapshot, compute_org_health
from auto_client_acquisition.platform.org_intelligence import OrgIntelligenceReport
from auto_client_acquisition.platform.strategic_reasoning import generate_strategic_recommendations


@dataclass(frozen=True, slots=True)
class ExecutiveInsightPack:
    week_label: str
    forecast: ExecutiveForecast
    org_health: OrgHealthSnapshot
    recommendations: tuple[str, ...]
    risk_band: str


def build_executive_insight_pack(
    *,
    week_label: str,
    revenue_growth_ratio: float,
    cost_efficiency_ratio: float,
    sla_hit_ratio: float,
    governance_coverage_ratio: float,
    org_report: OrgIntelligenceReport,
) -> ExecutiveInsightPack:
    forecast = build_executive_forecast(
        revenue_growth_ratio=revenue_growth_ratio,
        cost_efficiency_ratio=cost_efficiency_ratio,
        risk_score=org_report.risk_score,
    )
    health = compute_org_health(
        failure_rate=min(org_report.risk_score, 1.0),
        sla_hit_ratio=sla_hit_ratio,
        governance_coverage_ratio=governance_coverage_ratio,
    )
    recommendations = generate_strategic_recommendations(forecast=forecast, org_report=org_report)
    return ExecutiveInsightPack(
        week_label=week_label,
        forecast=forecast,
        org_health=health,
        recommendations=recommendations,
        risk_band=org_report.risk_band,
    )


__all__ = ['ExecutiveInsightPack', 'build_executive_insight_pack']
