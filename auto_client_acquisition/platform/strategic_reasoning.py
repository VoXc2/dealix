"""Strategic reasoning based on forecast and org intelligence."""

from __future__ import annotations

from auto_client_acquisition.platform.forecasting import ExecutiveForecast
from auto_client_acquisition.platform.org_intelligence import OrgIntelligenceReport


def generate_strategic_recommendations(
    *, forecast: ExecutiveForecast, org_report: OrgIntelligenceReport
) -> tuple[str, ...]:
    recommendations: list[str] = []
    if forecast.execution_risk_score >= 0.6:
        recommendations.append('freeze_non_critical_expansion_and_fix_risk_drivers')
    if forecast.projected_roi_ratio >= 0.4 and forecast.confidence >= 0.6:
        recommendations.append('scale_productized_offers_with_governed_capacity')
    if org_report.bottlenecks:
        recommendations.append('prioritize_workflow_bottleneck_remediation')
    if not recommendations:
        recommendations.append('maintain_operating_cadence_and_monitor')
    return tuple(recommendations)


__all__ = ['generate_strategic_recommendations']
