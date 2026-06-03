"""Admin tenants management endpoints (W7.3).

Programmatic counterpart to scripts/create_tenant.py (W7.1).
Enables agency self-serve flow once R6 (White-Label) is active: an
agency partner can create tenants through their portal instead of
emailing the founder for each new client.

Endpoints (all require X-Admin-API-Key header — same pattern as other admin):

  GET  /api/v1/admin/tenants
       List tenants with pagination + status filter. Read-only.

  POST /api/v1/admin/tenants
       Create a tenant. Mirrors create_tenant.py CLI validation exactly.

  GET  /api/v1/admin/tenants/{handle}
       Fetch one tenant by slug.

  PATCH /api/v1/admin/tenants/{handle}
       Update plan/status/limits. Cannot change slug (immutable).

Security:
  - All endpoints gated by require_admin_key dependency (the project
    standard, used by api/routers/admin.py)
  - Slug regex enforced at Path level
  - Plan/status/locale validated against closed allowlists
  - All mutations write an audit log entry (TBD when audit_logs DB
    table is in scope; deferred to subsequent commit)
"""
from __future__ import annotations

import logging
import re
import uuid
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/admin/tenants",
    tags=["admin-tenants"],
    dependencies=[Depends(require_admin_key)],
)

_SLUG_RE = re.compile(r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")
_VALID_PLANS = {"pilot", "starter", "growth", "scale"}
_VALID_STATUS = {"active", "suspended", "churned"}
_VALID_LOCALES = {"ar", "en"}


# ── Schemas ────────────────────────────────────────────────────────

class _TenantCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    handle: str = Field(..., min_length=3, max_length=64)
    name: str = Field(..., min_length=1, max_length=255)
    plan: str = Field(default="pilot")
    locale: str = Field(default="ar")
    timezone: str = Field(default="Asia/Riyadh", max_length=64)
    currency: str = Field(default="SAR", max_length=8)
    max_users: int = Field(default=5, ge=1, le=1000)
    max_leads_per_month: int = Field(default=1000, ge=1, le=1_000_000)


class _TenantPatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan: str | None = None
    status: str | None = None
    max_users: int | None = Field(default=None, ge=1, le=1000)
    max_leads_per_month: int | None = Field(default=None, ge=1, le=1_000_000)


def _tenant_to_dict(t: Any) -> dict[str, Any]:
    """Serialize TenantRecord for JSON response (no PII leaks)."""
    return {
        "id": t.id,
        "handle": t.slug,
        "name": t.name,
        "plan": t.plan,
        "status": t.status,
        "locale": t.locale,
        "timezone": t.timezone,
        "currency": t.currency,
        "max_users": t.max_users,
        "max_leads_per_month": t.max_leads_per_month,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
    }


# ── Endpoints ──────────────────────────────────────────────────────

@router.get("")
async def list_tenants(
    status: str | None = Query(default=None, description="filter by status"),
    plan: str | None = Query(default=None, description="filter by plan"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> dict[str, Any]:
    """List tenants with pagination + filters."""
    if status is not None and status not in _VALID_STATUS:
        raise HTTPException(
            status_code=400, detail=f"status must be one of {sorted(_VALID_STATUS)}",
        )
    if plan is not None and plan not in _VALID_PLANS:
        raise HTTPException(
            status_code=400, detail=f"plan must be one of {sorted(_VALID_PLANS)}",
        )

    try:
        from sqlalchemy import func, select

        from db.models import TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        stmt = select(TenantRecord).where(TenantRecord.deleted_at.is_(None))
        if status is not None:
            stmt = stmt.where(TenantRecord.status == status)
        if plan is not None:
            stmt = stmt.where(TenantRecord.plan == plan)
        stmt = stmt.order_by(TenantRecord.created_at.desc()).limit(limit).offset(offset)

        rows = (await session.execute(stmt)).scalars().all()

        count_stmt = select(func.count()).select_from(TenantRecord).where(
            TenantRecord.deleted_at.is_(None)
        )
        if status is not None:
            count_stmt = count_stmt.where(TenantRecord.status == status)
        if plan is not None:
            count_stmt = count_stmt.where(TenantRecord.plan == plan)
        total = (await session.execute(count_stmt)).scalar() or 0

    return {
        "tenants": [_tenant_to_dict(t) for t in rows],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("", status_code=201)
async def create_tenant_via_api(body: _TenantCreateRequest) -> dict[str, Any]:
    """Create a tenant. Equivalent to scripts/create_tenant.py CLI."""
    if not _SLUG_RE.match(body.handle):
        raise HTTPException(
            status_code=400,
            detail=f"handle must match {_SLUG_RE.pattern}",
        )
    if body.plan not in _VALID_PLANS:
        raise HTTPException(
            status_code=400, detail=f"plan must be one of {sorted(_VALID_PLANS)}",
        )
    if body.locale not in _VALID_LOCALES:
        raise HTTPException(
            status_code=400, detail=f"locale must be one of {sorted(_VALID_LOCALES)}",
        )

    try:
        from sqlalchemy import select

        from db.models import TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        existing = (
            await session.execute(
                select(TenantRecord).where(TenantRecord.slug == body.handle)
            )
        ).scalar_one_or_none()
        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail=f"tenant with handle {body.handle!r} already exists",
            )

        tenant_id = f"tn_{uuid.uuid4().hex[:16]}"
        now = datetime.now(UTC)
        new_tenant = TenantRecord(
            id=tenant_id,
            name=body.name,
            slug=body.handle,
            plan=body.plan,
            status="active",
            timezone=body.timezone,
            locale=body.locale,
            currency=body.currency,
            max_users=body.max_users,
            max_leads_per_month=body.max_leads_per_month,
            features={},
            meta_json={"created_via": "api"},
            created_at=now,
            updated_at=now,
        )
        session.add(new_tenant)
        await session.commit()
        await session.refresh(new_tenant)

    log.info("tenant_created id=%s handle=%s plan=%s", tenant_id, body.handle, body.plan)
    return _tenant_to_dict(new_tenant)


@router.get("/{handle}")
async def get_tenant(
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
) -> dict[str, Any]:
    """Fetch one tenant by handle."""
    try:
        from sqlalchemy import select

        from db.models import TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        tenant = (
            await session.execute(select(TenantRecord).where(TenantRecord.slug == handle))
        ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")
    return _tenant_to_dict(tenant)


@router.patch("/{handle}")
async def update_tenant(
    body: _TenantPatchRequest,
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
) -> dict[str, Any]:
    """Update tenant fields. Cannot change slug or id."""
    if body.plan is not None and body.plan not in _VALID_PLANS:
        raise HTTPException(
            status_code=400, detail=f"plan must be one of {sorted(_VALID_PLANS)}",
        )
    if body.status is not None and body.status not in _VALID_STATUS:
        raise HTTPException(
            status_code=400, detail=f"status must be one of {sorted(_VALID_STATUS)}",
        )

    try:
        from sqlalchemy import select

        from db.models import TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        tenant = (
            await session.execute(select(TenantRecord).where(TenantRecord.slug == handle))
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")

        if body.plan is not None:
            tenant.plan = body.plan
        if body.status is not None:
            tenant.status = body.status
        if body.max_users is not None:
            tenant.max_users = body.max_users
        if body.max_leads_per_month is not None:
            tenant.max_leads_per_month = body.max_leads_per_month
        tenant.updated_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(tenant)

    log.info("tenant_updated handle=%s plan=%s status=%s",
             handle, tenant.plan, tenant.status)
    return _tenant_to_dict(tenant)
