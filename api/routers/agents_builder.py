"""
Agent builder + workflow marketplace API.

Endpoints:
    GET  /api/v1/agents              — list the caller's custom agents.
    POST /api/v1/agents              — register a new custom agent
                                       (BYOA agent.yaml manifest).
    DELETE /api/v1/agents/{id}       — remove a custom agent.

    GET  /api/v1/workflows/marketplace — list available templates.
    POST /api/v1/workflows/install     — install one for a tenant.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import TenantRecord
from db.session import get_db
from dealix.agents.builder import AgentValidationError, validate
from dealix.workflows.marketplace import by_id as workflow_by_id
from dealix.workflows.marketplace import list_all as list_workflows

router = APIRouter(tags=["agents", "workflows"])
log = get_logger(__name__)


def _tenant(request: Request) -> str:
    tid = getattr(request.state, "tenant_id", None)
    if not tid and not getattr(request.state, "is_super_admin", False):
        raise HTTPException(401, "tenant_unresolved")
    return str(tid or "")


class CustomAgentIn(BaseModel):
    id: str = Field(..., max_length=64)
    name: str = Field(..., max_length=120)
    description: str = Field(default="", max_length=500)
    model: str = Field(..., max_length=120)
    tools: list[str] = Field(default_factory=list, max_length=32)
    prompt_override: str = Field(default="", max_length=8000)
    max_usd_per_request: float = Field(default=0.50, gt=0, le=10)
    locale: str = Field(default="ar", max_length=8)
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.get("/api/v1/agents")
async def list_custom_agents(
    request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    tid = _tenant(request)
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tid))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    catalog = ((tenant.meta_json or {}).get("custom_agents") or {})
    return {
        "tenant_id": tid,
        "count": len(catalog),
        "agents": [
            {"id": k, **{kk: vv for kk, vv in v.items() if kk != "prompt_override"}}
            for k, v in catalog.items()
        ],
    }


@router.post("/api/v1/agents")
async def register_custom_agent(
    payload: CustomAgentIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    tid = _tenant(request)
    try:
        spec = validate(payload.model_dump())
    except AgentValidationError as exc:
        raise HTTPException(422, f"invalid_agent: {exc}") from exc
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tid))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    catalog = dict(meta.get("custom_agents") or {})
    catalog[spec.id] = {
        "name": spec.name,
        "description": spec.description,
        "model": spec.model,
        "tools": spec.tools,
        "prompt_override": spec.prompt_override,
        "max_usd_per_request": spec.max_usd_per_request,
        "locale": spec.locale,
        "metadata": spec.metadata,
    }
    meta["custom_agents"] = catalog
    tenant.meta_json = meta
    try:
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "persist_failed") from None
    log.info("custom_agent_registered", tenant_id=tid, agent_id=spec.id)
    return {"ok": True, "id": spec.id, "tools": spec.tools}


@router.delete("/api/v1/agents/{agent_id}")
async def delete_custom_agent(
    agent_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    tid = _tenant(request)
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tid))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    catalog = dict(meta.get("custom_agents") or {})
    if agent_id not in catalog:
        raise HTTPException(404, "agent_not_found")
    catalog.pop(agent_id)
    meta["custom_agents"] = catalog
    tenant.meta_json = meta
    await db.commit()
    log.info("custom_agent_deleted", tenant_id=tid, agent_id=agent_id)
    return {"ok": True, "id": agent_id}


# ── Workflow marketplace ──────────────────────────────────────────


class InstallWorkflowIn(BaseModel):
    workflow_id: str = Field(..., max_length=64)
    tenant_id: str = Field(..., max_length=64)


@router.get("/api/v1/workflows/marketplace")
async def list_marketplace() -> dict[str, Any]:
    wf = list_workflows()
    return {
        "count": len(wf),
        "workflows": [
            {
                "id": w.id,
                "name": w.name,
                "description": w.description,
                "agents": w.agents,
                "locale": w.locale,
                "version": w.version,
            }
            for w in wf
        ],
    }


@router.post("/api/v1/workflows/install")
async def install_workflow(
    payload: InstallWorkflowIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    caller = getattr(request.state, "tenant_id", None)
    if caller and caller != payload.tenant_id and not getattr(request.state, "is_super_admin", False):
        raise HTTPException(403, "cross_tenant_access_denied")
    w = workflow_by_id(payload.workflow_id)
    if w is None:
        raise HTTPException(404, "workflow_not_found")
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == payload.tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    installed = list(meta.get("installed_workflows") or [])
    if w.id not in installed:
        installed.append(w.id)
    meta["installed_workflows"] = installed
    tenant.meta_json = meta
    await db.commit()
    log.info(
        "workflow_installed", tenant_id=payload.tenant_id, workflow_id=w.id
    )
    return {"ok": True, "tenant_id": payload.tenant_id, "workflow_id": w.id, "agents": w.agents}
