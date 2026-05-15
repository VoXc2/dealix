"""Workflow metrics keys."""

from __future__ import annotations

WORKFLOW_METRIC_KEYS: tuple[str, ...] = (
    "cycle_time_hours",
    "rework_count",
    "governance_block_rate",
    "proof_first_pass_rate",
)


def workflow_metrics_coverage_score(tracked: frozenset[str]) -> int:
    if not WORKFLOW_METRIC_KEYS:
        return 0
    n = sum(1 for k in WORKFLOW_METRIC_KEYS if k in tracked)
    return (n * 100) // len(WORKFLOW_METRIC_KEYS)


__all__ = ["WORKFLOW_METRIC_KEYS", "workflow_metrics_coverage_score"]
