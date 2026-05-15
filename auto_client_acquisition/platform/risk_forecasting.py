"""Risk forecasting for organizational intelligence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiskSignal:
    open_incidents: int
    policy_violations_last_7d: int
    failure_rate: float
    trend_acceleration: float


def forecast_risk_score(signal: RiskSignal) -> float:
    raw = (
        0.25 * min(signal.open_incidents / 10.0, 1.0)
        + 0.25 * min(signal.policy_violations_last_7d / 20.0, 1.0)
        + 0.35 * min(signal.failure_rate, 1.0)
        + 0.15 * min(max(signal.trend_acceleration, 0.0), 1.0)
    )
    return round(max(0.0, min(raw, 1.0)), 4)


def risk_band(score: float) -> str:
    if score >= 0.75:
        return 'critical'
    if score >= 0.5:
        return 'high'
    if score >= 0.25:
        return 'medium'
    return 'low'


__all__ = ['RiskSignal', 'forecast_risk_score', 'risk_band']
