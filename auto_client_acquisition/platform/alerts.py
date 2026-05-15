"""Alert rules over aggregated metrics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Alert:
    alert_id: str
    severity: str
    metric_name: str
    value: float
    threshold: float
    message: str


def evaluate_threshold_alert(
    *, metric_name: str, value: float, warning_threshold: float, critical_threshold: float
) -> Alert | None:
    if value >= critical_threshold:
        return Alert(
            alert_id=f'critical:{metric_name}',
            severity='critical',
            metric_name=metric_name,
            value=value,
            threshold=critical_threshold,
            message=f'{metric_name} exceeded critical threshold',
        )
    if value >= warning_threshold:
        return Alert(
            alert_id=f'warning:{metric_name}',
            severity='warning',
            metric_name=metric_name,
            value=value,
            threshold=warning_threshold,
            message=f'{metric_name} exceeded warning threshold',
        )
    return None


__all__ = ['Alert', 'evaluate_threshold_alert']
