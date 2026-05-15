"""System 34 — the Business Value Engine.

Measures the business value of workflow runs: revenue impact, time saved,
execution speed, efficiency gain, and ROI.

Tier discipline (mirrors `value_os`): a `measured` metric must carry a
verifiable `source_ref` — otherwise it is not a real outcome and is rejected
with `ValueDisciplineError` (`no_unverified_outcomes` / `no_fake_proof`). The
engine measures only; it never charges anything.
"""

from __future__ import annotations

from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit
from auto_client_acquisition.value_engine_os.schemas import (
    ROIReport,
    ValueTier,
    WorkflowValueMetric,
)

_MODULE = "value_engine_os"


class ValueDisciplineError(ValueError):
    """Raised when a `measured` metric lacks a verifiable source reference."""


class ValueEngine:
    """Records workflow value metrics and computes ROI."""

    def __init__(self) -> None:
        self._metrics: list[WorkflowValueMetric] = []

    def record_metric(
        self,
        *,
        run_id: str,
        workflow_id: str,
        revenue_impact_sar: float = 0.0,
        time_saved_minutes: float = 0.0,
        execution_speed_ms: float = 0.0,
        efficiency_gain_pct: float = 0.0,
        tier: ValueTier | str = ValueTier.ESTIMATED,
        source_ref: str = "",
    ) -> WorkflowValueMetric:
        """Record a value metric. `measured` tier requires a `source_ref`."""
        tier_value = ValueTier(tier)
        if tier_value == ValueTier.MEASURED and not source_ref.strip():
            raise ValueDisciplineError(
                "a 'measured' value metric requires a verifiable source_ref"
            )
        metric = WorkflowValueMetric(
            run_id=run_id,
            workflow_id=workflow_id,
            revenue_impact_sar=revenue_impact_sar,
            time_saved_minutes=time_saved_minutes,
            execution_speed_ms=execution_speed_ms,
            efficiency_gain_pct=efficiency_gain_pct,
            tier=tier_value,
            source_ref=source_ref,
        )
        self._metrics.append(metric)
        emit(
            event_type=ControlEventType.VALUE_MEASURED,
            source_module=_MODULE,
            subject_type="workflow",
            subject_id=workflow_id,
            run_id=run_id,
            payload={
                "tier": str(tier_value),
                "revenue_impact_sar": revenue_impact_sar,
                "time_saved_minutes": time_saved_minutes,
            },
        )
        return metric

    def metrics_for(self, workflow_id: str) -> list[WorkflowValueMetric]:
        return [m for m in self._metrics if m.workflow_id == workflow_id]

    def roi_for_workflow(
        self, workflow_id: str, *, period: str = "all-time", cost_sar: float = 0.0
    ) -> ROIReport:
        """Aggregate ROI for one workflow. roi_ratio is value / cost when cost > 0."""
        metrics = self.metrics_for(workflow_id)
        total_value = round(sum(m.revenue_impact_sar for m in metrics), 2)
        total_time = round(sum(m.time_saved_minutes for m in metrics), 2)
        avg_eff = (
            round(sum(m.efficiency_gain_pct for m in metrics) / len(metrics), 2)
            if metrics
            else 0.0
        )
        roi_ratio = round(total_value / cost_sar, 4) if cost_sar > 0 else 0.0
        suggestions: list[str] = []
        if avg_eff < 20.0:
            suggestions.append("low efficiency gain — review workflow steps")
        if total_value == 0.0:
            suggestions.append("no recorded revenue impact — verify value capture")
        return ROIReport(
            workflow_id=workflow_id,
            period=period,
            metric_count=len(metrics),
            total_value_sar=total_value,
            total_time_saved_minutes=total_time,
            avg_efficiency_gain_pct=avg_eff,
            cost_sar=cost_sar,
            roi_ratio=roi_ratio,
            optimization_suggestions=suggestions,
        )

    def optimization_candidates(self, *, efficiency_threshold: float = 20.0) -> list[str]:
        """Workflow IDs whose average efficiency gain is below the threshold."""
        workflow_ids = sorted({m.workflow_id for m in self._metrics})
        candidates: list[str] = []
        for wf in workflow_ids:
            report = self.roi_for_workflow(wf)
            if report.avg_efficiency_gain_pct < efficiency_threshold:
                candidates.append(wf)
        return candidates


_ENGINE: ValueEngine | None = None


def get_value_engine() -> ValueEngine:
    """Return the process-scoped value engine singleton."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = ValueEngine()
    return _ENGINE


def reset_value_engine() -> None:
    """Test helper: drop the cached engine."""
    global _ENGINE
    _ENGINE = None


__all__ = [
    "ValueDisciplineError",
    "ValueEngine",
    "get_value_engine",
    "reset_value_engine",
]
