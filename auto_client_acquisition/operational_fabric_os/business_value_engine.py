"""System 34 — Business value and KPI computation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowValueInput:
    revenue_before: float
    revenue_after: float
    hours_before: float
    hours_after: float
    cycle_time_before: float
    cycle_time_after: float
    csat_before: float
    csat_after: float
    cost_of_change: float


@dataclass(frozen=True)
class ValueSnapshot:
    roi: float
    revenue_impact: float
    efficiency_gain_pct: float
    time_saved_hours: float
    execution_speed_gain_pct: float
    csat_delta: float
    kpis: dict[str, float]


def _safe_improvement(before: float, after: float) -> float:
    if before <= 0:
        return 0.0
    return round(((before - after) / before) * 100.0, 2)


def compute_value_snapshot(data: WorkflowValueInput) -> ValueSnapshot:
    revenue_impact = round(data.revenue_after - data.revenue_before, 2)
    time_saved = round(data.hours_before - data.hours_after, 2)
    efficiency_gain = _safe_improvement(data.hours_before, data.hours_after)
    speed_gain = _safe_improvement(data.cycle_time_before, data.cycle_time_after)
    csat_delta = round(data.csat_after - data.csat_before, 2)
    if data.cost_of_change <= 0:
        roi = 0.0
    else:
        roi = round(((revenue_impact - data.cost_of_change) / data.cost_of_change) * 100.0, 2)
    kpis = {
        "roi": roi,
        "revenue_impact": revenue_impact,
        "efficiency_gain_pct": efficiency_gain,
        "time_saved_hours": time_saved,
        "execution_speed_gain_pct": speed_gain,
        "csat_delta": csat_delta,
    }
    return ValueSnapshot(
        roi=roi,
        revenue_impact=revenue_impact,
        efficiency_gain_pct=efficiency_gain,
        time_saved_hours=time_saved,
        execution_speed_gain_pct=speed_gain,
        csat_delta=csat_delta,
        kpis=kpis,
    )


def workflow_has_measurable_kpis(snapshot: ValueSnapshot) -> bool:
    required = {
        "roi",
        "revenue_impact",
        "efficiency_gain_pct",
        "time_saved_hours",
        "execution_speed_gain_pct",
    }
    return required.issubset(snapshot.kpis.keys())
