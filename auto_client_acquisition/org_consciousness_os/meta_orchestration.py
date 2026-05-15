"""System 43 — Meta-Orchestration Engine.

Reads the agent-action workload and recommends how to rebalance it.
Output is advice only — this module never enqueues, approves, routes or
executes anything.
"""

from __future__ import annotations

from auto_client_acquisition.org_consciousness_os._common import read_agent_events
from auto_client_acquisition.org_consciousness_os.schemas import (
    MetaOrchestrationRecommendation,
)
from auto_client_acquisition.revenue_memory.event_store import EventStore

_STATUS_BY_EVENT: dict[str, str] = {
    "agent.action_requested": "pending",
    "agent.action_approved": "approved",
    "agent.action_rejected": "rejected",
    "agent.action_executed": "executed",
    "agent.action_failed": "failed",
}


def _imbalance_score(workload: dict[str, int]) -> int:
    """0 = balanced, 100 = heavily imbalanced toward failure/backlog."""
    total = sum(workload.values())
    if total == 0:
        return 0
    stuck = workload.get("pending", 0) + workload.get("failed", 0) + workload.get("rejected", 0)
    return min(100, int((stuck / total) * 100))


def _recommendations(workload: dict[str, int], imbalance: int) -> tuple[str, ...]:
    recs: list[str] = []
    if workload.get("pending", 0) > workload.get("executed", 0):
        recs.append(
            "Approval backlog exceeds completed work — increase approval "
            "throughput before routing new tasks."
        )
    if workload.get("failed", 0) > 0:
        recs.append(
            "Route new tasks away from action types with recent failures "
            "until resilience recovers."
        )
    if imbalance == 0:
        recs.append("Workload is balanced — maintain current routing.")
    elif not recs:
        recs.append("Minor imbalance — monitor; no routing change needed yet.")
    return tuple(recs)


def recommend_meta_orchestration(
    *,
    customer_id: str,
    window_days: int = 30,
    store: EventStore | None = None,
) -> MetaOrchestrationRecommendation:
    """Recommend workload rebalancing for ``customer_id`` (advice only)."""
    events = read_agent_events(customer_id=customer_id, window_days=window_days, store=store)
    workload: dict[str, int] = {}
    for ev in events:
        status = _STATUS_BY_EVENT.get(ev.event_type)
        if status:
            workload[status] = workload.get(status, 0) + 1

    imbalance = _imbalance_score(workload)
    return MetaOrchestrationRecommendation(
        customer_id=customer_id,
        workload_by_status=workload,
        imbalance_score=imbalance,
        recommendations=_recommendations(workload, imbalance),
        is_recommendation_only=True,
    )


__all__ = ["recommend_meta_orchestration"]
