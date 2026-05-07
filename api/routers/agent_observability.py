"""Agent Observability HTTP surface (Phase 11).

  GET  /api/v1/agent-observability/status
  POST /api/v1/agent-observability/trace
  GET  /api/v1/agent-observability/recent
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.agent_observability import (
    list_recent_traces,
    record_trace,
)
from auto_client_acquisition.agent_observability.quality import quality_summary

router = APIRouter(
    prefix="/api/v1/agent-observability",
    tags=["agent-observability"],
)

_HARD_GATES: dict[str, bool] = {
    "no_raw_pii": True,
    "no_secrets_in_trace": True,
    "no_full_transcripts_by_default": True,
    "no_external_dependency": True,
    "redaction_first": True,
}

_VALID_ACTION_MODES = {
    "draft_only", "approval_required",
    "approved_execute", "approved_manual", "blocked",
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "agent_observability",
        "version": "1.0.0",
        "valid_action_modes": sorted(_VALID_ACTION_MODES),
        "future_adapters": ["langfuse", "opentelemetry"],
        "hard_gates": _HARD_GATES,
    }


@router.post("/trace")
async def trace(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    agent_name = payload.get("agent_name")
    action_mode = payload.get("action_mode")
    if not agent_name:
        raise HTTPException(status_code=422, detail="agent_name required")
    if action_mode not in _VALID_ACTION_MODES:
        raise HTTPException(
            status_code=422,
            detail=f"action_mode must be one of {sorted(_VALID_ACTION_MODES)}",
        )
    t = record_trace(
        agent_name=agent_name,
        action_mode=action_mode,  # type: ignore[arg-type]
        customer_handle=payload.get("customer_handle"),
        workflow=payload.get("workflow", ""),
        input_kind=payload.get("input_kind", ""),
        output_kind=payload.get("output_kind", ""),
        latency_ms=payload.get("latency_ms"),
        cost_estimate=payload.get("cost_estimate"),
        guardrail_result=payload.get("guardrail_result", "ok"),
        approval_status=payload.get("approval_status", "pending"),
        degraded=bool(payload.get("degraded", False)),
        error_type=payload.get("error_type"),
        payload=payload.get("payload") or {},
    )
    return {
        "trace": t.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.get("/recent")
async def recent(limit: int = 50) -> dict[str, Any]:
    traces = list_recent_traces(limit=limit)
    return {
        "count": len(traces),
        "traces": [t.model_dump(mode="json") for t in traces],
        "quality": quality_summary(traces),
        "hard_gates": _HARD_GATES,
    }


@router.get("/cost-summary")
async def cost_summary(limit: int = 500) -> dict[str, Any]:
    """Phase 9 Wave 5 — aggregated cost across recent traces.

    Per-agent + per-workflow breakdown. Total cost in estimated USD.
    """
    traces = list_recent_traces(limit=limit)

    total_cost = 0.0
    by_agent: dict[str, dict[str, Any]] = {}
    by_workflow: dict[str, dict[str, Any]] = {}

    for t in traces:
        cost = t.cost_estimate or 0.0
        total_cost += cost

        agent_bucket = by_agent.setdefault(t.agent_name, {"count": 0, "total_cost_usd": 0.0})
        agent_bucket["count"] += 1
        agent_bucket["total_cost_usd"] = round(agent_bucket["total_cost_usd"] + cost, 6)

        workflow_key = t.workflow or "(unspecified)"
        wf_bucket = by_workflow.setdefault(workflow_key, {"count": 0, "total_cost_usd": 0.0})
        wf_bucket["count"] += 1
        wf_bucket["total_cost_usd"] = round(wf_bucket["total_cost_usd"] + cost, 6)

    return {
        "trace_count": len(traces),
        "total_cost_usd_estimate": round(total_cost, 6),
        "by_agent": by_agent,
        "by_workflow": by_workflow,
        "is_estimate": True,
        "source": "agent_observability + cost_estimate per trace",
        "hard_gates": _HARD_GATES,
    }
