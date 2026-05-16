"""Executive outcome metrics derived from governed workflow runs."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.enterprise_infrastructure.schemas import WorkflowRunResult


def build_executive_report(
    run: WorkflowRunResult,
    *,
    cost_per_step_sar: int = 45,
    retry_penalty_sar: int = 15,
    baseline_hours_per_step: float = 0.8,
) -> dict[str, Any]:
    """Translate technical run telemetry into business outcomes."""
    operating_cost = (
        run.metrics.completed_steps * cost_per_step_sar
        + run.metrics.retries_total * retry_penalty_sar
    )
    value = run.metrics.value_generated_sar
    roi_percent = round(((value - operating_cost) / operating_cost) * 100, 2) if operating_cost else 0.0

    total_steps = max(1, run.metrics.total_steps)
    conversion_lift_percent = round((run.metrics.completed_steps / total_steps) * 100, 2)
    saved_hours = round(run.metrics.completed_steps * baseline_hours_per_step, 2)
    reliability_percent = round(
        ((run.metrics.completed_steps + run.metrics.approvals_granted) / total_steps) * 100,
        2,
    )
    latency_reduction_percent = max(0.0, round(100.0 - (run.metrics.retries_total * 14.0), 2))

    return {
        "roi_percent": roi_percent,
        "conversion_lift_percent": conversion_lift_percent,
        "saved_hours": saved_hours,
        "workflow_latency_reduction_percent": latency_reduction_percent,
        "operational_efficiency_percent": reliability_percent,
        "value_generated_sar": value,
        "operating_cost_sar": operating_cost,
    }
