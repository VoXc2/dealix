"""Organizational intelligence engine."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.bottleneck_detection import (
    WorkflowPerformance,
    detect_bottlenecks,
)
from auto_client_acquisition.platform.optimization import (
    OptimizationSuggestion,
    propose_optimizations,
)
from auto_client_acquisition.platform.risk_forecasting import RiskSignal, forecast_risk_score, risk_band


@dataclass(frozen=True, slots=True)
class OrgIntelligenceReport:
    risk_score: float
    risk_band: str
    bottlenecks: tuple[str, ...]
    optimizations: tuple[OptimizationSuggestion, ...]


def build_org_intelligence(
    *, performance_rows: tuple[WorkflowPerformance, ...], risk_signal: RiskSignal
) -> OrgIntelligenceReport:
    bottlenecks = detect_bottlenecks(performance_rows)
    score = forecast_risk_score(risk_signal)
    band = risk_band(score)
    optimizations = propose_optimizations(bottlenecks=bottlenecks, risk_band=band)
    return OrgIntelligenceReport(
        risk_score=score,
        risk_band=band,
        bottlenecks=bottlenecks,
        optimizations=optimizations,
    )


__all__ = ['OrgIntelligenceReport', 'build_org_intelligence']
