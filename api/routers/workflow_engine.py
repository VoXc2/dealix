"""
Workflow Engine HTTP surface — the governed Lead Qualification vertical slice.

Endpoints:
  GET  /api/v1/workflow/status                     runtime + registry + ROI snapshot
  GET  /api/v1/workflow/definition                 the Lead Qualification definition
  GET  /api/v1/workflow/tools                       typed tool registry
  POST /api/v1/workflow/lead-qualification/run      start a run
  GET  /api/v1/workflow/runs/{run_id}               run snapshot + evals
  GET  /api/v1/workflow/runs/{run_id}/evals         operational evals only
  POST /api/v1/workflow/runs/{run_id}/approve       grant the pending approval → resume
  POST /api/v1/workflow/runs/{run_id}/reject        reject the pending approval → rollback
  GET  /api/v1/workflow/runs/{run_id}/audit         audit trail for the run
  GET  /api/v1/workflow/memory/{entity_id}          permission-aware run history
  GET  /api/v1/workflow/roi                          realised-savings ledger

Hard gate: the outbound `whatsapp.send_message` step ALWAYS escalates to a
human — no run sends a message without an explicit approval on file.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from dealix.execution.engine import WorkflowEngine
from dealix.execution.evals import evaluate_run
from dealix.execution.lead_qualification import (
    build_registry,
    lead_qualification_workflow,
    register_roi_baseline,
)
from dealix.execution.memory import PermissionError_, get_memory
from dealix.execution.roi import get_roi_ledger
from dealix.execution.workflow import RunStatus, WorkflowContext
from dealix.trust.approval import ApprovalCenter
from dealix.trust.audit import InMemoryAuditSink

router = APIRouter(prefix="/api/v1/workflow", tags=["Agents"])

# ── Process-wide runtime (Phase 0–1: in-process; Phase 2: durable) ──
_REGISTRY = build_registry()
_APPROVALS = ApprovalCenter(default_ttl_hours=48)
_AUDIT = InMemoryAuditSink()
_ENGINE = WorkflowEngine(
    _REGISTRY,
    approvals=_APPROVALS,
    audit=_AUDIT,
    memory=get_memory(),
    roi=get_roi_ledger(),
)
_RUNS: dict[str, WorkflowContext] = {}  # live contexts (resume needs the live object)
register_roi_baseline()


def _workflow():  # fresh, deterministic definition each call
    return lead_qualification_workflow()


def _run_view(ctx: WorkflowContext) -> dict[str, Any]:
    snapshot = ctx.to_dict()
    return {"run": snapshot, "evals": evaluate_run(snapshot).to_dict()}


def _get_ctx(run_id: str) -> WorkflowContext:
    ctx = _RUNS.get(run_id)
    if ctx is None:
        raise HTTPException(status_code=404, detail=f"run not found: {run_id}")
    return ctx


# ── Request models ──────────────────────────────────────────────────


class RunRequest(BaseModel):
    tenant_id: str = Field(default="default")
    lead_id: str = Field(..., description="Business entity id for the lead")
    actor_id: str = Field(default="system")
    company: str = ""
    sector: str = ""
    region: str = ""
    phone: str = ""
    budget_sar: float = 0.0
    message: str = ""
    simulate_send_failure: bool = Field(
        default=False, description="Force the outbound step to fail (rollback demo)"
    )


class ApprovalDecisionRequest(BaseModel):
    approver_id: str = Field(..., description="Id of the human approver")
    reason: str = ""


# ── Endpoints ───────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "workflow_engine",
        "version": "1.0.0",
        "runtime": "in_process",
        "registered_tools": len(_REGISTRY.all()),
        "workflows": ["lead_qualification"],
        "runs_tracked": len(_RUNS),
        "memory": get_memory().summary(),
        "roi": get_roi_ledger().summary(),
        "hard_gates": {
            "outbound_requires_approval": True,
            "every_step_policy_gated": True,
            "failed_runs_roll_back": True,
        },
    }


@router.get("/definition")
async def definition() -> dict[str, Any]:
    return _workflow().to_dict()


@router.get("/tools")
async def tools() -> dict[str, Any]:
    return _REGISTRY.to_dict()


@router.post("/lead-qualification/run")
async def run_lead_qualification(body: RunRequest) -> dict[str, Any]:
    trigger_payload: dict[str, Any] = {
        "company": body.company,
        "sector": body.sector,
        "region": body.region,
        "phone": body.phone,
        "budget_sar": body.budget_sar,
        "message": body.message,
        "simulate_send_failure": body.simulate_send_failure,
    }
    ctx = await _ENGINE.start(
        _workflow(),
        tenant_id=body.tenant_id,
        entity_id=body.lead_id,
        trigger_payload=trigger_payload,
        actor_id=body.actor_id,
    )
    _RUNS[ctx.run_id] = ctx
    return _run_view(ctx)


@router.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict[str, Any]:
    return _run_view(_get_ctx(run_id))


@router.get("/runs/{run_id}/evals")
async def get_run_evals(run_id: str) -> dict[str, Any]:
    return evaluate_run(_get_ctx(run_id).to_dict()).to_dict()


@router.post("/runs/{run_id}/approve")
async def approve_run(run_id: str, body: ApprovalDecisionRequest) -> dict[str, Any]:
    ctx = _get_ctx(run_id)
    if ctx.status != RunStatus.AWAITING_APPROVAL or not ctx.pending_approval_id:
        raise HTTPException(status_code=409, detail=f"run not awaiting approval: {ctx.status.value}")
    _APPROVALS.grant(ctx.pending_approval_id, body.approver_id)
    await _ENGINE.resume(_workflow(), ctx)
    return _run_view(ctx)


@router.post("/runs/{run_id}/reject")
async def reject_run(run_id: str, body: ApprovalDecisionRequest) -> dict[str, Any]:
    ctx = _get_ctx(run_id)
    if ctx.status != RunStatus.AWAITING_APPROVAL or not ctx.pending_approval_id:
        raise HTTPException(status_code=409, detail=f"run not awaiting approval: {ctx.status.value}")
    _APPROVALS.reject(ctx.pending_approval_id, body.approver_id, body.reason)
    await _ENGINE.resume(_workflow(), ctx)
    return _run_view(ctx)


@router.get("/runs/{run_id}/audit")
async def get_run_audit(run_id: str) -> dict[str, Any]:
    ctx = _get_ctx(run_id)
    entries = [
        e.model_dump(mode="json")
        for e in _AUDIT.recent(limit=1000)
        if e.workflow_id == run_id
    ]
    return {"run_id": run_id, "entries": entries, "count": len(entries)}


@router.get("/memory/{entity_id}")
async def get_memory_history(
    entity_id: str, tenant_id: str = Query(default="default")
) -> dict[str, Any]:
    try:
        history = get_memory().history_for_entity(entity_id, tenant_id=tenant_id)
    except PermissionError_ as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return {"entity_id": entity_id, "tenant_id": tenant_id, "runs": history}


@router.get("/roi")
async def get_roi(tenant_id: str | None = Query(default=None)) -> dict[str, Any]:
    return get_roi_ledger().summary(tenant_id=tenant_id)
