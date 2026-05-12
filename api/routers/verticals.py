"""
Vertical bundles — discover which sectors are pre-configured and apply
one to the caller's tenant.

Endpoints:
    GET  /api/v1/verticals          — list all verticals.
    GET  /api/v1/verticals/{id}     — single vertical's bundle.
    POST /api/v1/verticals/apply    — set the caller's tenant default.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.logging import get_logger
from db.models import TenantRecord
from db.session import get_db
from dealix.verticals import by_id, list_all

router = APIRouter(prefix="/api/v1/verticals", tags=["verticals"])
log = get_logger(__name__)


class ApplyVerticalIn(BaseModel):
    tenant_id: str = Field(..., max_length=64)
    vertical_id: str = Field(..., max_length=64)


@router.get("")
async def list_verticals() -> dict[str, Any]:
    verts = list_all()
    return {
        "count": len(verts),
        "verticals": [
            {
                "id": v.id,
                "label_ar": v.label_ar,
                "label_en": v.label_en,
                "description_en": v.description_en,
                "agents": v.agents,
                "workflows": v.workflows,
                "pricing_default_plan": v.pricing_default_plan,
            }
            for v in verts
        ],
    }


@router.get("/{vertical_id}")
async def get_vertical(vertical_id: str = Path(..., max_length=64)) -> dict[str, Any]:
    v = by_id(vertical_id)
    if v is None:
        raise HTTPException(404, "vertical_not_found")
    return {
        "id": v.id,
        "label_ar": v.label_ar,
        "label_en": v.label_en,
        "description_ar": v.description_ar,
        "description_en": v.description_en,
        "agents": v.agents,
        "workflows": v.workflows,
        "pricing_default_plan": v.pricing_default_plan,
        "lead_form_fields": v.lead_form_fields,
    }


@router.post("/apply")
async def apply_vertical(
    payload: ApplyVerticalIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    caller = getattr(request.state, "tenant_id", None)
    if caller and caller != payload.tenant_id and not getattr(request.state, "is_super_admin", False):
        raise HTTPException(403, "cross_tenant_access_denied")
    v = by_id(payload.vertical_id)
    if v is None:
        raise HTTPException(404, "vertical_not_found")
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == payload.tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    meta["vertical"] = {
        "id": v.id,
        "applied_agents": v.agents,
        "applied_workflows": v.workflows,
        "applied_at": __import__("datetime").datetime.utcnow().isoformat(),
    }
    tenant.meta_json = meta
    if v.pricing_default_plan and tenant.plan in ("pilot", "starter"):
        tenant.plan = v.pricing_default_plan
    try:
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "apply_failed") from None
    log.info(
        "vertical_applied",
        tenant_id=tenant.id,
        vertical=v.id,
        agents=v.agents,
        workflows=v.workflows,
    )
    return {"ok": True, "tenant_id": tenant.id, "vertical": v.id, "plan": tenant.plan}
