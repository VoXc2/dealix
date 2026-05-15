"""Operational analytics from traces, incidents, and policy signals."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.tracing import TraceSpan


@dataclass(frozen=True, slots=True)
class OperationalAnalytics:
    failure_rate: float
    latency_p95_ms: float
    open_incidents: int
    policy_violation_rate: float


def _p95(values: tuple[int, ...]) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    idx = min(len(sorted_values) - 1, int(0.95 * (len(sorted_values) - 1)))
    return float(sorted_values[idx])


def build_operational_analytics(
    *,
    spans: tuple[TraceSpan, ...],
    open_incidents: int,
    policy_violations: int,
    total_actions: int,
) -> OperationalAnalytics:
    failures = sum(1 for span in spans if span.status != 'ok')
    failure_rate = 0.0 if len(spans) == 0 else round(failures / len(spans), 4)
    latency_p95 = _p95(tuple(span.duration_ms for span in spans))
    policy_violation_rate = 0.0 if total_actions <= 0 else round(policy_violations / total_actions, 4)
    return OperationalAnalytics(
        failure_rate=failure_rate,
        latency_p95_ms=latency_p95,
        open_incidents=open_incidents,
        policy_violation_rate=policy_violation_rate,
    )


__all__ = ['OperationalAnalytics', 'build_operational_analytics']
