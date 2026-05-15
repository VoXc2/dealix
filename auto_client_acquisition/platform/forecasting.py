"""Executive forecasting signals."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutiveForecast:
    projected_roi_ratio: float
    execution_risk_score: float
    confidence: float


def build_executive_forecast(
    *, revenue_growth_ratio: float, cost_efficiency_ratio: float, risk_score: float
) -> ExecutiveForecast:
    roi = max(0.0, (0.7 * revenue_growth_ratio) + (0.3 * cost_efficiency_ratio))
    confidence = max(0.0, min(1.0, 1.0 - (0.6 * risk_score)))
    return ExecutiveForecast(
        projected_roi_ratio=round(roi, 4),
        execution_risk_score=round(max(0.0, min(risk_score, 1.0)), 4),
        confidence=round(confidence, 4),
    )


__all__ = ['ExecutiveForecast', 'build_executive_forecast']
