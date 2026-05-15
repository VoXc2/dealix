"""System 37 — Causal Organizational Reasoning Engine.

Moves from "what happened" to "why": links friction events to the
agent-action events that share their workflow, and attaches a
deterministic hypothesis per friction kind. Read-only, no LLM.
"""

from __future__ import annotations

from auto_client_acquisition.friction_log.store import list_events as friction_list_events
from auto_client_acquisition.org_consciousness_os._common import read_agent_events
from auto_client_acquisition.org_consciousness_os.schemas import (
    CausalLink,
    CausalReasoningReport,
)
from auto_client_acquisition.revenue_memory.event_store import EventStore
from auto_client_acquisition.revenue_memory.events import RevenueEvent

# Deterministic friction-kind → root-cause hypothesis (bilingual-safe, EN).
_HYPOTHESIS: dict[str, str] = {
    "governance_block": "A governance gate rejected the workflow output — "
    "policy or source-passport check failed.",
    "approval_delay": "The approval queue is the bottleneck — work is "
    "waiting on a human decision.",
    "schema_failure": "An agent produced output that failed schema "
    "validation — prompt or contract drift.",
    "manual_override": "A human had to intervene manually — the workflow "
    "did not handle this case autonomously.",
    "retry": "An action failed and was retried — an upstream dependency " "is unstable.",
    "support_ticket": "A customer raised a support ticket — the workflow "
    "outcome did not meet expectations.",
    "missing_source_passport": "Work was blocked because the data source "
    "has no valid Source Passport.",
    "missing_proof_pack": "Delivery stalled because the Proof Pack has not " "been assembled.",
}
_DEFAULT_HYPOTHESIS = "Friction recorded; root cause not classified."


def _event_workflow_id(ev: RevenueEvent) -> str:
    return (
        ev.correlation_id
        or str(ev.payload.get("workflow_id", ""))
        or str(ev.payload.get("parent_workflow_id", ""))
    )


def build_causal_report(
    *,
    customer_id: str,
    window_days: int = 30,
    store: EventStore | None = None,
) -> CausalReasoningReport:
    """Build a causal report linking friction to agent-action events."""
    friction_events = friction_list_events(
        customer_id=customer_id, since_days=window_days, limit=2000
    )
    agent_events = read_agent_events(customer_id=customer_id, window_days=window_days, store=store)

    events_by_workflow: dict[str, list[RevenueEvent]] = {}
    for ev in agent_events:
        wf = _event_workflow_id(ev)
        if wf:
            events_by_workflow.setdefault(wf, []).append(ev)

    links: list[CausalLink] = []
    root_causes: dict[str, int] = {}
    for fe in friction_events:
        root_causes[fe.kind] = root_causes.get(fe.kind, 0) + 1
        linked = events_by_workflow.get(fe.workflow_id, []) if fe.workflow_id else []
        linked_ids = tuple(sorted({ev.subject_id for ev in linked if ev.subject_id}))
        links.append(
            CausalLink(
                friction_event_id=fe.event_id,
                friction_kind=fe.kind,
                workflow_id=fe.workflow_id,
                linked_task_ids=linked_ids,
                hypothesis=_HYPOTHESIS.get(fe.kind, _DEFAULT_HYPOTHESIS),
                confidence="high" if linked_ids else "low",
            )
        )

    top = tuple(sorted(root_causes.items(), key=lambda x: x[1], reverse=True)[:3])
    return CausalReasoningReport(
        customer_id=customer_id,
        window_days=window_days,
        links=tuple(links),
        top_root_causes=top,
    )


__all__ = ["build_causal_report"]
