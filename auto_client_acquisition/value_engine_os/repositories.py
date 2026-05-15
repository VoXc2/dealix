"""In-memory value engine repository with source discipline."""

from __future__ import annotations

from uuid import uuid4

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.value_engine_os.schemas import WorkflowValueMetric


class ValueEngineDisciplineError(ValueError):
    """Raised when value metric evidence constraints are violated."""


class InMemoryValueEngineRepository:
    def __init__(self) -> None:
        self._metrics: dict[tuple[str, str], list[WorkflowValueMetric]] = {}

    def add_metric(
        self,
        *,
        tenant_id: str,
        run_id: str,
        metric_name: str,
        metric_type: str,
        value: float,
        source_ref: str = "",
        notes: str = "",
        control_repo: InMemoryControlPlaneRepository | None = None,
    ) -> WorkflowValueMetric:
        mtype = metric_type.strip().lower()
        if mtype not in {"estimated", "measured"}:
            raise ValueEngineDisciplineError("metric_type must be estimated or measured")
        if mtype == "measured" and not source_ref.strip():
            raise ValueEngineDisciplineError("measured metric requires source_ref")
        metric = WorkflowValueMetric(
            metric_id=f"met_{uuid4().hex[:10]}",
            tenant_id=tenant_id,
            run_id=run_id,
            metric_name=metric_name,
            metric_type=mtype,
            value=float(value),
            source_ref=source_ref.strip(),
            notes=notes,
        )
        self._metrics.setdefault((tenant_id, run_id), []).append(metric)
        if control_repo is not None:
            control_repo._emit(  # noqa: SLF001 - explicit trace side effect
                tenant_id=tenant_id,
                event_type="value.metric_recorded",
                actor="value_engine_os",
                run_id=run_id,
                subject_type="value_metric",
                subject_id=metric.metric_id,
                payload={"metric_type": mtype, "source_ref": metric.source_ref},
            )
        return metric

    def list_metrics(self, *, tenant_id: str, run_id: str) -> list[WorkflowValueMetric]:
        return list(self._metrics.get((tenant_id, run_id), []))

    def roi_report(self, *, tenant_id: str, run_id: str) -> dict[str, float]:
        metrics = self.list_metrics(tenant_id=tenant_id, run_id=run_id)
        estimated = sum(m.value for m in metrics if m.metric_type == "estimated")
        measured = sum(m.value for m in metrics if m.metric_type == "measured")
        return {
            "tenant_id": tenant_id,
            "run_id": run_id,
            "estimated_total": round(estimated, 2),
            "measured_total": round(measured, 2),
            "metric_count": float(len(metrics)),
        }
