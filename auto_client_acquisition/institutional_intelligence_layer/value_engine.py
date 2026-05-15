"""Institutional value and impact tracking (System 63)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowValueSnapshot:
    workflow_id: str
    kpis: dict[str, float]
    baseline: dict[str, float]
    cost: float
    revenue_gain: float
    risk_reduction_value: float
    executive_visibility: bool


def workflow_roi(snapshot: WorkflowValueSnapshot) -> float | None:
    """Compute ROI for a workflow if denominator is valid."""
    if snapshot.cost <= 0:
        return None
    numerator = snapshot.revenue_gain + snapshot.risk_reduction_value - snapshot.cost
    return round(numerator / snapshot.cost, 4)


def value_engine_status(snapshot: WorkflowValueSnapshot) -> tuple[bool, tuple[str, ...]]:
    """A workflow is value-ready when KPIs, baseline, ROI and visibility exist."""
    blockers: list[str] = []
    if not snapshot.workflow_id.strip():
        blockers.append("workflow_id_missing")
    if len(snapshot.kpis) == 0:
        blockers.append("kpis_missing")
    if len(snapshot.baseline) == 0:
        blockers.append("baseline_missing")
    if workflow_roi(snapshot) is None:
        blockers.append("roi_not_computable")
    if not snapshot.executive_visibility:
        blockers.append("executive_visibility_missing")
    return len(blockers) == 0, tuple(blockers)
