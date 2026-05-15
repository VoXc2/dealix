"""System 36 — Organizational Consciousness Engine.

Real-time operational awareness: fuses friction events, observability
traces, agent-action events and the bottleneck radar into a single
execution-health signal. Read-only.
"""

from __future__ import annotations

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.bottleneck_radar.computer import compute_bottleneck
from auto_client_acquisition.friction_log.aggregator import aggregate as friction_aggregate
from auto_client_acquisition.observability_v10.buffer import list_v10_traces
from auto_client_acquisition.observability_v10.report import summarize_traces
from auto_client_acquisition.org_consciousness_os._common import read_agent_events
from auto_client_acquisition.org_consciousness_os.schemas import ExecutionHealthSignal
from auto_client_acquisition.revenue_memory.event_store import EventStore

_SEVERITY_PENALTY: dict[str, int] = {
    "clear": 0,
    "watch": 5,
    "blocking": 15,
    "critical": 30,
}


def _health_score(
    *,
    friction_wow_delta: int,
    failure_count: int,
    executed_count: int,
    bottleneck_severity: str,
) -> int:
    score = 100
    if friction_wow_delta > 0:
        score -= min(30, friction_wow_delta * 3)
    total_actions = failure_count + executed_count
    if total_actions > 0:
        score -= int((failure_count / total_actions) * 40)
    score -= _SEVERITY_PENALTY.get(bottleneck_severity, 0)
    return max(0, min(100, score))


def _band(score: int) -> str:
    if score >= 80:
        return "healthy"
    if score >= 60:
        return "watch"
    if score >= 40:
        return "strained"
    return "critical"


def compute_execution_health(
    *,
    customer_id: str,
    window_days: int = 30,
    store: EventStore | None = None,
    approval_store: ApprovalStore | None = None,
) -> ExecutionHealthSignal:
    """Synthesize an execution-health signal for ``customer_id``."""
    agg = friction_aggregate(customer_id=customer_id, window_days=window_days)

    traces = [t for t in list_v10_traces(limit=2000) if t.customer_id == customer_id]
    trace_summary = summarize_traces(traces)

    events = read_agent_events(customer_id=customer_id, window_days=window_days, store=store)
    congestion: dict[str, int] = {}
    for ev in events:
        congestion[ev.event_type] = congestion.get(ev.event_type, 0) + 1
    failure_count = congestion.get("agent.action_failed", 0)
    executed_count = congestion.get("agent.action_executed", 0)

    approvals = approval_store or get_default_approval_store()
    blocking_approvals = sum(1 for r in approvals.list_pending() if r.customer_id == customer_id)

    bottleneck = compute_bottleneck(
        customer_handle=customer_id,
        blocking_approvals_count=blocking_approvals,
        pending_proof_packs_to_send=agg.by_kind.get("missing_proof_pack", 0),
        sla_at_risk_tickets=agg.by_kind.get("support_ticket", 0),
    )

    score = _health_score(
        friction_wow_delta=agg.week_over_week_delta,
        failure_count=failure_count,
        executed_count=executed_count,
        bottleneck_severity=bottleneck.severity,
    )

    return ExecutionHealthSignal(
        customer_id=customer_id,
        window_days=window_days,
        friction_total=agg.total,
        friction_cost_minutes=agg.total_cost_minutes,
        top_friction_kinds=tuple((k, v) for k, v in agg.top_3_kinds),
        friction_wow_delta=agg.week_over_week_delta,
        trace_count=int(trace_summary["trace_count"]),
        total_cost_usd=float(trace_summary["total_cost_usd"]),
        avg_latency_ms=float(trace_summary["avg_latency_ms"]),
        congestion_events=congestion,
        bottleneck=bottleneck.model_dump(),
        execution_health_score=score,
        health_band=_band(score),
    )


__all__ = ["compute_execution_health"]
