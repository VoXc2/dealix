"""Workflow learning from historical runs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowRunStat:
    workflow_id: str
    latency_ms: float
    cost_usd: float
    success: bool


def learn_workflow_patterns(stats: tuple[WorkflowRunStat, ...]) -> dict[str, float]:
    if not stats:
        return {'success_rate': 1.0, 'avg_latency_ms': 0.0, 'avg_cost_usd': 0.0}
    success_rate = sum(1 for row in stats if row.success) / len(stats)
    avg_latency = sum(row.latency_ms for row in stats) / len(stats)
    avg_cost = sum(row.cost_usd for row in stats) / len(stats)
    return {
        'success_rate': round(success_rate, 4),
        'avg_latency_ms': round(avg_latency, 4),
        'avg_cost_usd': round(avg_cost, 4),
    }


__all__ = ['WorkflowRunStat', 'learn_workflow_patterns']
