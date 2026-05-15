"""Platform Foundation router — live proof of the Enterprise Foundation Core.

These admin-key-gated endpoints let the founder walk the canonical enterprise
loop end to end and inspect its append-only audit chain:

    tenant -> users -> roles -> agent -> workflow -> approval
    -> CRM draft -> executive report -> eval report -> rollback -> audit

Run the whole loop in one call (POST /loop/run) or step by step
(POST /loop/{run_id}/step/...). The endpoints ARE the deliverable proof.
"""

from __future__ import annotations

import platform as _stdlib_platform
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from platform_core import enterprise_loop as loop

router = APIRouter(
    prefix="/api/v1/platform",
    tags=["platform-foundation"],
    dependencies=[Depends(require_admin_key)],
)

_RUN_ID = r"^[A-Za-z0-9_-]{3,64}$"


# ── Schemas ─────────────────────────────────────────────────────────

class _RunBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenant_handle: str = Field(default="acme_loop", min_length=3, max_length=64)
    tenant_name: str = Field(default="Acme Loop Co", min_length=1, max_length=255)
    actor: str = Field(default="founder", min_length=1, max_length=64)


class _TenantBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenant_handle: str = Field(default="acme_loop", min_length=3, max_length=64)
    tenant_name: str = Field(default="Acme Loop Co", min_length=1, max_length=255)
    actor: str = Field(default="founder", min_length=1, max_length=64)


class _UsersBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    users: list[dict[str, str]] | None = None


class _RolesBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    roles: list[dict[str, Any]] | None = None


class _AgentBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(default="revenue_intelligence_agent", max_length=128)
    purpose: str = Field(
        default="Qualify inbound Saudi B2B leads and draft responses under approval.",
        max_length=512,
    )
    owner: str | None = Field(default=None, max_length=64)


class _WorkflowBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lead: dict[str, str] | None = None
    icp: dict[str, int] | None = None
    risk: dict[str, bool] | None = None


class _ApprovalBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: str = Field(default="send_email", max_length=64)
    request_external_send_without_approval: bool = False


# ── Helpers ─────────────────────────────────────────────────────────

def _require_run(run_id: str) -> loop.LoopContext:
    ctx = loop.get_run(run_id)
    if ctx is None:
        raise HTTPException(
            status_code=404,
            detail=f"run {run_id!r} not found — start with POST /loop/{run_id}/step/tenant",
        )
    return ctx


# ── Health ──────────────────────────────────────────────────────────

@router.get("/health")
async def health() -> dict[str, Any]:
    """Facade self-check — confirms imports resolve and stdlib is intact."""
    return {
        "status": "ok",
        "facades": [
            "multi_tenant", "identity", "rbac", "workflow_engine",
            "agent_runtime", "governance", "observability",
        ],
        "stdlib_platform_ok": bool(_stdlib_platform.python_version()),
        "active_runs": len(loop.RUN_STORE),
    }


# ── Full loop ───────────────────────────────────────────────────────

@router.post("/loop/run")
async def run_loop(body: _RunBody) -> dict[str, Any]:
    """Run all eleven governed steps in one call."""
    try:
        ctx = await loop.run_enterprise_loop(
            tenant_handle=body.tenant_handle,
            tenant_name=body.tenant_name,
            actor=body.actor,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ctx.as_dict()


# ── Step-by-step ────────────────────────────────────────────────────

@router.post("/loop/{run_id}/step/tenant")
async def step_tenant(
    body: _TenantBody,
    run_id: str = Path(..., pattern=_RUN_ID),
) -> dict[str, Any]:
    """Step 1 — provision the tenant. Creates the run if it does not exist."""
    ctx = loop.get_run(run_id)
    if ctx is None:
        ctx = loop.LoopContext(run_id=run_id, actor=body.actor)
        loop.RUN_STORE[run_id] = ctx
    try:
        result = await loop.step_provision_tenant(
            ctx,
            tenant_handle=body.tenant_handle,
            tenant_name=body.tenant_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/users")
async def step_users(
    body: _UsersBody,
    run_id: str = Path(..., pattern=_RUN_ID),
) -> dict[str, Any]:
    """Step 2 — create the loop's users."""
    ctx = _require_run(run_id)
    result = await loop.step_create_users(ctx, users=body.users)
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/roles")
async def step_roles(
    body: _RolesBody,
    run_id: str = Path(..., pattern=_RUN_ID),
) -> dict[str, Any]:
    """Step 3 — create the loop's RBAC roles."""
    ctx = _require_run(run_id)
    result = await loop.step_create_roles(ctx, roles=body.roles)
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/agent")
async def step_agent(
    body: _AgentBody,
    run_id: str = Path(..., pattern=_RUN_ID),
) -> dict[str, Any]:
    """Step 4 — register one governed agent (identity + owner + autonomy)."""
    ctx = _require_run(run_id)
    result = await loop.step_register_agent(
        ctx, name=body.name, purpose=body.purpose, owner=body.owner,
    )
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/workflow")
async def step_workflow(
    body: _WorkflowBody,
    run_id: str = Path(..., pattern=_RUN_ID),
) -> dict[str, Any]:
    """Step 5 — run the AI Revenue OS workflow (intake -> qualify -> draft)."""
    ctx = _require_run(run_id)
    result = await loop.step_run_workflow(
        ctx, lead=body.lead, icp=body.icp, risk=body.risk,
    )
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/approval")
async def step_approval(
    body: _ApprovalBody,
    run_id: str = Path(..., pattern=_RUN_ID),
) -> dict[str, Any]:
    """Step 6 — apply the approval rule. Doctrine violations return HTTP 403."""
    ctx = _require_run(run_id)
    try:
        result = await loop.step_apply_approval(
            ctx,
            action=body.action,
            request_external_send_without_approval=body.request_external_send_without_approval,
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/crm")
async def step_crm(run_id: str = Path(..., pattern=_RUN_ID)) -> dict[str, Any]:
    """Step 7 — stage the CRM update as a draft (no live send)."""
    ctx = _require_run(run_id)
    result = await loop.step_crm_update(ctx)
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/executive-report")
async def step_executive_report(run_id: str = Path(..., pattern=_RUN_ID)) -> dict[str, Any]:
    """Step 8 — emit the executive report."""
    ctx = _require_run(run_id)
    result = await loop.step_executive_report(ctx)
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/eval-report")
async def step_eval_report(run_id: str = Path(..., pattern=_RUN_ID)) -> dict[str, Any]:
    """Step 9 — emit the eval report."""
    ctx = _require_run(run_id)
    result = await loop.step_eval_report(ctx)
    return {"run_id": run_id, "step": result.as_dict()}


@router.post("/loop/{run_id}/step/rollback")
async def step_rollback(run_id: str = Path(..., pattern=_RUN_ID)) -> dict[str, Any]:
    """Step 10 — run the rollback drill (soft-delete + deregister)."""
    ctx = _require_run(run_id)
    result = await loop.step_rollback_drill(ctx)
    return {"run_id": run_id, "step": result.as_dict()}


# ── Read / verify ───────────────────────────────────────────────────

@router.get("/loop/{run_id}")
async def read_run(run_id: str = Path(..., pattern=_RUN_ID)) -> dict[str, Any]:
    """Read the full run state + audit chain."""
    return _require_run(run_id).as_dict()


@router.get("/loop/{run_id}/audit")
async def verify_audit(run_id: str = Path(..., pattern=_RUN_ID)) -> dict[str, Any]:
    """Step 11 — verify and return the append-only audit chain."""
    ctx = _require_run(run_id)
    result = await loop.step_verify_audit(ctx)
    events = [s.as_dict()["audit"] for s in ctx.steps]
    return {
        "run_id": run_id,
        "events": events,
        "event_count": len(events),
        "all_valid": result.detail["all_valid"],
        "step": result.as_dict(),
    }
