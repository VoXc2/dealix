"""DealixOrchestrator — governed automation surface.

Exposes the agent registry, the task queue, the policy layer and the
trigger-based automations. High-risk automations always queue an
approval; this router never executes a high-risk action directly.
"""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auto_client_acquisition.dealix_orchestrator.automations import (
    AUTOMATIONS,
    run_automation,
)
from auto_client_acquisition.dealix_orchestrator.policy import (
    HIGH_RISK_ACTIONS,
    can_auto_send,
    claim_has_source,
    requires_approval,
    stage_transition_allowed,
)
from auto_client_acquisition.dealix_orchestrator.runtime import get_default_task_queue
from auto_client_acquisition.revenue_graph.agent_registry import (
    ALL_AGENTS,
    agents_summary,
)

router = APIRouter(prefix="/api/v1/orchestrator", tags=["orchestrator"])


class TriggerBody(BaseModel):
    entity_id: str
    payload: dict | None = None
    tenant_id: str | None = None


class PolicyCheckBody(BaseModel):
    action: str | None = None
    claim: str | None = None
    source: str | None = None
    from_stage: str | None = None
    to_stage: str | None = None


@router.get("/status")
async def status() -> dict:
    queue = get_default_task_queue()
    return {
        "module": "dealix_orchestrator",
        "automations": sorted(AUTOMATIONS.keys()),
        "high_risk_actions": sorted(HIGH_RISK_ACTIONS),
        "agents": agents_summary(),
        "task_summary": queue.summary(),
        "guardrails": {
            "high_risk_actions_always_approval_gated": True,
            "every_trigger_writes_evidence": True,
        },
    }


@router.get("/agents")
async def list_agents() -> dict:
    agents = [
        {
            "agent_id": a.agent_id,
            "autonomy_level": a.autonomy_level,
            "spec": asdict(a),
        }
        for a in ALL_AGENTS
    ]
    return {"count": len(agents), "agents": agents}


@router.get("/tasks")
async def list_tasks(status: str | None = None, customer_id: str | None = None) -> dict:
    queue = get_default_task_queue()
    tasks = list(queue.tasks.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    if customer_id:
        tasks = [t for t in tasks if t.customer_id == customer_id]
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    return {"count": len(tasks), "tasks": [asdict(t) for t in tasks]}


@router.get("/tasks/{task_id}")
async def get_task(task_id: str) -> dict:
    queue = get_default_task_queue()
    task = queue.tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task_not_found")
    return asdict(task)


@router.post("/trigger/{automation}")
async def trigger(automation: str, body: TriggerBody) -> dict:
    try:
        return run_automation(
            automation,
            entity_id=body.entity_id,
            payload=body.payload,
            tenant_id=body.tenant_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/policy/check")
async def policy_check(body: PolicyCheckBody) -> dict:
    """Dry-run policy evaluation — runs whichever checks have inputs."""
    result: dict = {}
    if body.action is not None:
        allowed, reason = can_auto_send(body.action)
        result["action"] = {
            "action": body.action,
            "requires_approval": requires_approval(body.action),
            "can_auto_send": allowed,
            "reason": reason,
        }
    if body.claim is not None:
        ok, reason = claim_has_source(body.claim, body.source)
        result["claim"] = {"ok": ok, "reason": reason}
    if body.from_stage is not None and body.to_stage is not None:
        ok, reason = stage_transition_allowed(body.from_stage, body.to_stage)
        result["stage_transition"] = {"allowed": ok, "reason": reason}
    if not result:
        raise HTTPException(status_code=422, detail="no policy inputs provided")
    return result
