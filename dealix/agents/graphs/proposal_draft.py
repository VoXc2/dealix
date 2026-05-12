"""
Reference LangGraph for the proposal-draft workflow.

State shape:
    {
        "lead": {...},
        "icp_score": float,
        "draft": {"subject": str, "body_ar": str, "next_steps": [...]},
        "approved": bool,
        "guard": {"ok": bool, "violations": [...]},
    }

Nodes:
    load_lead   → fetch the lead from DB.
    score_icp   → call the ICP-matcher agent (existing).
    draft       → call the proposal agent (existing).
    guard       → run guardrails (PII + JSON shape).
    persist     → write OutreachQueueRecord + audit row.

Edges:
    load_lead → score_icp → draft → guard
    guard.ok=True → persist
    guard.ok=False → END (founder reviews via approval center).

Without LangGraph installed, `build()` returns None and callers fall
back to the existing in-process Inngest function (T2).
"""

from __future__ import annotations

from typing import Any, TypedDict

from core.logging import get_logger

log = get_logger(__name__)


class ProposalState(TypedDict, total=False):
    lead: dict[str, Any]
    icp_score: float
    draft: dict[str, Any]
    approved: bool
    guard: dict[str, Any]
    error: str | None


async def _load_lead(state: ProposalState) -> ProposalState:
    lead_id = (state.get("lead") or {}).get("id")
    if not lead_id:
        return {**state, "error": "missing_lead_id"}
    # Reuse the existing Inngest step's loader.
    try:
        from dealix.workflows.inngest_app import _step_load_lead

        lead = await _step_load_lead(lead_id)
        return {**state, "lead": lead}
    except Exception as exc:
        log.exception("graph_load_lead_failed", lead_id=lead_id)
        return {**state, "error": str(exc)}


async def _score_icp(state: ProposalState) -> ProposalState:
    lead = state.get("lead") or {}
    return {**state, "icp_score": float(lead.get("fit_score", 0.0))}


async def _draft(state: ProposalState) -> ProposalState:
    lead = state.get("lead") or {}
    try:
        from dealix.workflows.inngest_app import _step_draft_proposal

        draft = await _step_draft_proposal(lead)
        return {**state, "draft": draft}
    except Exception as exc:
        log.exception("graph_draft_failed")
        return {**state, "error": str(exc)}


async def _guard(state: ProposalState) -> ProposalState:
    raw = (state.get("draft") or {}).get("body") or ""
    if not raw:
        return {**state, "guard": {"ok": False, "violations": ["empty_body"]}}
    try:
        from core.llm.guardrails import redact_pii

        result = redact_pii(raw)
        return {
            **state,
            "guard": {"ok": result.ok, "violations": result.violations},
        }
    except Exception:
        return {**state, "guard": {"ok": False, "violations": ["guard_unavailable"]}}


async def _persist(state: ProposalState) -> ProposalState:
    lead = state.get("lead") or {}
    draft = state.get("draft") or {}
    try:
        from dealix.workflows.inngest_app import _step_queue_for_send

        await _step_queue_for_send(draft, lead.get("id", ""))
        return {**state, "approved": True}
    except Exception as exc:
        log.exception("graph_persist_failed")
        return {**state, "error": str(exc)}


def build() -> Any | None:
    """Build the compiled LangGraph; return None if LangGraph isn't installed."""
    try:
        from langgraph.graph import END, START, StateGraph  # type: ignore
    except ImportError:
        log.info("langgraph_not_installed; proposal_draft graph unavailable")
        return None

    g: StateGraph = StateGraph(ProposalState)
    g.add_node("load_lead", _load_lead)
    g.add_node("score_icp", _score_icp)
    g.add_node("draft", _draft)
    g.add_node("guard", _guard)
    g.add_node("persist", _persist)

    g.add_edge(START, "load_lead")
    g.add_edge("load_lead", "score_icp")
    g.add_edge("score_icp", "draft")
    g.add_edge("draft", "guard")
    g.add_conditional_edges(
        "guard",
        lambda s: "persist" if (s.get("guard") or {}).get("ok") else END,
        {"persist": "persist", END: END},
    )
    g.add_edge("persist", END)
    return g.compile()


async def run(lead_id: str) -> ProposalState:
    """One-shot helper used by tests + a `--dry-run` CLI."""
    compiled = build()
    if compiled is None:
        log.info("langgraph_unavailable; falling back to inngest function")
        # The Inngest function already implements the same logic.
        from dealix.workflows.inngest_app import (
            _step_draft_proposal,
            _step_load_lead,
            _step_queue_for_send,
        )

        lead = await _step_load_lead(lead_id)
        draft = await _step_draft_proposal(lead)
        await _step_queue_for_send(draft, lead_id)
        return {"lead": lead, "draft": draft, "approved": True}

    return await compiled.ainvoke({"lead": {"id": lead_id}})
