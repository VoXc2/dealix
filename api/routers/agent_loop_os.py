"""Agent Runtime router — run a bounded agentic loop, read its traces.

The loop is bounded, kill-switchable, and fully audited. Every response
carries a ``governance_decision``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.agent_loop_os.agent_loop_ledger import list_loops
from auto_client_acquisition.agent_loop_os.loop import AgentLoop
from auto_client_acquisition.agent_loop_os.loop_budget import LoopBudget
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision

router = APIRouter(prefix="/api/v1/agent-runtime", tags=["Agents"])


class RunBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    goal: str = Field(..., min_length=3)
    max_iterations: int = Field(8, ge=1, le=20)


@router.post("/run")
async def run_loop(body: RunBody) -> dict[str, Any]:
    try:
        trace = AgentLoop(budget=LoopBudget(max_iterations=body.max_iterations)).run(
            goal=body.goal,
            customer_id=body.customer_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    payload = trace.to_dict()
    payload["governance_decision"] = (
        GovernanceDecision.ALLOW.value
        if trace.terminated_reason == "goal_met" and not trace.insufficient_evidence
        else GovernanceDecision.DRAFT_ONLY.value
    )
    return payload


@router.get("/{customer_id}/traces")
async def get_traces(
    customer_id: str,
    limit: int = Query(50, ge=1, le=500),
    since_days: int = Query(90, ge=1, le=365),
) -> dict[str, Any]:
    traces = list_loops(customer_id=customer_id, limit=limit, since_days=since_days)
    return {
        "customer_id": customer_id,
        "count": len(traces),
        "traces": traces,
        "governance_decision": GovernanceDecision.ALLOW.value,
    }
