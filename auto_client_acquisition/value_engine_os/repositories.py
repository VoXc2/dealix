"""Value Engine repository with strict source discipline."""

from __future__ import annotations

from auto_client_acquisition.value_engine_os.schemas import WorkflowValueMetric


class ValueEngineRepository:
    def __init__(self) -> None:
        self._metrics: list[WorkflowValueMetric] = []

    def record(self, metric: WorkflowValueMetric) -> WorkflowValueMetric:
        tier = metric.tier.strip().lower()
        if tier in {"measured", "verified"} and not metric.source_ref.strip():
            raise ValueError("measured_or_verified_requires_source_ref")
        if tier == "client_confirmed" and not metric.confirmation_ref.strip():
            raise ValueError("client_confirmed_requires_confirmation_ref")
        self._metrics.append(metric)
        return metric

    def list_for_run(self, *, tenant_id: str, run_id: str) -> list[WorkflowValueMetric]:
        return [
            row
            for row in self._metrics
            if row.tenant_id == tenant_id and row.run_id == run_id
        ]

    def roi_report(self, *, tenant_id: str, run_id: str) -> dict[str, float]:
        rows = self.list_for_run(tenant_id=tenant_id, run_id=run_id)
        total = sum(float(row.amount or 0.0) for row in rows)
        measured = sum(
            float(row.amount or 0.0)
            for row in rows
            if row.tier.lower() in {"measured", "verified", "client_confirmed"}
        )
        return {
            "total_estimated_value": round(total, 2),
            "total_measured_value": round(measured, 2),
            "coverage_ratio": round((measured / total), 4) if total else 0.0,
        }

    def clear_for_test(self) -> None:
        self._metrics.clear()


__all__ = ["ValueEngineRepository"]
