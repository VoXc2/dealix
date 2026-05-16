"""Metric buffer and aggregation helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricPoint:
    metric_name: str
    value: float
    timestamp_epoch: int


_METRICS: list[MetricPoint] = []


def record_metric(point: MetricPoint) -> None:
    _METRICS.append(point)


def list_metrics(metric_name: str | None = None) -> tuple[MetricPoint, ...]:
    if metric_name is None:
        return tuple(_METRICS)
    return tuple(point for point in _METRICS if point.metric_name == metric_name)


def metric_summary(metric_name: str) -> dict[str, float]:
    values = [point.value for point in _METRICS if point.metric_name == metric_name]
    if not values:
        return {'count': 0.0, 'min': 0.0, 'max': 0.0, 'avg': 0.0}
    return {
        'count': float(len(values)),
        'min': min(values),
        'max': max(values),
        'avg': round(sum(values) / len(values), 4),
    }


def clear_metrics_for_tests() -> None:
    _METRICS.clear()


__all__ = [
    'MetricPoint',
    'clear_metrics_for_tests',
    'list_metrics',
    'metric_summary',
    'record_metric',
]
