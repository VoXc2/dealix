"""Bottleneck detection from workflow performance telemetry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowPerformance:
    workflow_id: str
    latency_minutes_p95: float
    sla_minutes: float
    retry_rate: float
    queue_wait_minutes: float


def detect_bottlenecks(performance_rows: tuple[WorkflowPerformance, ...]) -> tuple[str, ...]:
    findings: list[str] = []
    for row in performance_rows:
        if row.latency_minutes_p95 > row.sla_minutes:
            findings.append(f'{row.workflow_id}:sla_breach')
        if row.retry_rate > 0.2:
            findings.append(f'{row.workflow_id}:retry_churn')
        if row.queue_wait_minutes > (0.5 * row.sla_minutes):
            findings.append(f'{row.workflow_id}:queue_pressure')
    return tuple(findings)


__all__ = ['WorkflowPerformance', 'detect_bottlenecks']
