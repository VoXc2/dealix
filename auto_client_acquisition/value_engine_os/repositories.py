"""Value engine metrics with source discipline rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class WorkflowValueMetric:
    metric_id: str
    tenant_id: str
    run_id: str
    metric_name: str
    metric_kind: str  # estimated | measured
    value: float
    source_ref: str | None = None
    created_at: datetime = field(default_factory=_now)


class InMemoryValueEngineRepository:
    def __init__(self) -> None:
        self._metrics: dict[str, list[WorkflowValueMetric]] = {}

    def record_metric(self, metric: WorkflowValueMetric) -> WorkflowValueMetric:
        tid = resolve_tenant_id(metric.tenant_id)
        if metric.metric_kind == "measured" and not (metric.source_ref or "").strip():
            raise ValueError("measured metrics require source_ref")
        self._metrics.setdefault(tid, []).append(metric)
        return metric

    def list_metrics(self, *, tenant_id: str | None) -> tuple[WorkflowValueMetric, ...]:
        tid = resolve_tenant_id(tenant_id)
        return tuple(self._metrics.get(tid, ()))

    def roi_summary(self, *, tenant_id: str | None) -> dict[str, float]:
        tid = resolve_tenant_id(tenant_id)
        metrics = self._metrics.get(tid, [])
        estimated = sum(metric.value for metric in metrics if metric.metric_kind == "estimated")
        measured = sum(metric.value for metric in metrics if metric.metric_kind == "measured")
        return {"estimated_total": estimated, "measured_total": measured, "delta": measured - estimated}


__all__ = ["InMemoryValueEngineRepository", "WorkflowValueMetric"]
