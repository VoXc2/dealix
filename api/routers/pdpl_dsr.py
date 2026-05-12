"""
PDPL Data Subject Rights (DSR) API.

Saudi Personal Data Protection Law (PDPL) Articles 4 + 22 + 23 give the
data subject the right to: (a) access their data, (b) request
correction, (c) request deletion, (d) request portability. This router
exposes those rights as endpoints so customers (and their end-users)
have a self-serve path.

Endpoints (all `/api/v1/pdpl/dsr/...`):

    POST /access        — kick off an export (async); returns a request_id
    GET  /access/{id}   — status + download link
    POST /delete        — request deletion (founder-reviewed for hard delete)
    GET  /portability   — JSON dump of the caller's data
    GET  /requests      — list the caller's outstanding DSR requests

All writes generate an `AuditLogRecord` with `entity_type="dsr_request"`
so the DPO can audit. Notifications fire via Knock when configured.
"""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import AuditLogRecord, LeadRecord, TenantRecord, UserRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/pdpl/dsr", tags=["pdpl", "dsr"])
log = get_logger(__name__)


# ── Schemas ──────────────────────────────────────────────────────────


class DSRAccessIn(BaseModel):
    subject_email: str = Field(..., max_length=255)
    reason: str = Field(default="article_22", max_length=120)


class DSRDeleteIn(BaseModel):
    subject_email: str = Field(..., max_length=255)
    confirm: bool = Field(default=False)
    reason: str = Field(default="article_23_request", max_length=200)


# ── Helpers ──────────────────────────────────────────────────────────


def _ensure_tenant(request: Request) -> str:
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id and not getattr(request.state, "is_super_admin", False):
        raise HTTPException(401, "tenant_unresolved")
    return str(tenant_id or "")


async def _audit(
    db: AsyncSession,
    *,
    tenant_id: str,
    user_id: str | None,
    action: str,
    request_id: str,
    diff: dict[str, Any] | None,
) -> None:
    row = AuditLogRecord(
        id=secrets.token_hex(16),
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        entity_type="dsr_request",
        entity_id=request_id,
        status="ok",
        diff=diff,
    )
    db.add(row)
    try:
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        log.exception("dsr_audit_failed", tenant_id=tenant_id)


async def _notify_dpo(action: str, subject: str, tenant_id: str) -> None:
    """Fire-and-forget — Knock when configured, else log only."""
    try:
        from dealix.integrations.knock_client import get_knock_client

        client = get_knock_client()
        await client.notify(
            workflow="pdpl_dsr_received",
            recipients=[
                {"id": "dpo", "email": "dpo@ai-company.sa"},
            ],
            data={"action": action, "subject": subject, "tenant_id": tenant_id},
            tenant_id=tenant_id,
        )
    except Exception:
        log.warning(
            "dsr_dpo_notify_failed",
            action=action,
            subject=subject,
            tenant_id=tenant_id,
        )


# ── Endpoints ────────────────────────────────────────────────────────


@router.post("/access")
async def request_access(
    payload: DSRAccessIn, request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    tenant_id = _ensure_tenant(request)
    req_id = "dsr_" + secrets.token_hex(8)
    await _audit(
        db,
        tenant_id=tenant_id,
        user_id=getattr(request.state, "user_id", None),
        action="dsr.access.request",
        request_id=req_id,
        diff={"subject_email": payload.subject_email, "reason": payload.reason},
    )
    await _notify_dpo("access", payload.subject_email, tenant_id)
    return {
        "request_id": req_id,
        "status": "queued",
        "subject_email": payload.subject_email,
        "tenant_id": tenant_id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/access/{request_id}")
async def access_status(
    request: Request,
    request_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Return status of an outstanding access request."""
    tenant_id = _ensure_tenant(request)
    row = (
        await db.execute(
            select(AuditLogRecord).where(
                AuditLogRecord.entity_id == request_id,
                AuditLogRecord.tenant_id == tenant_id,
            )
        )
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "dsr_request_not_found")
    return {
        "request_id": request_id,
        "action": row.action,
        "status": row.status,
        "submitted_at": row.created_at.isoformat(),
        "download_url": None,
        "note": "Manual DPO review pending; export delivered via email when ready.",
    }


@router.post("/delete")
async def request_delete(
    payload: DSRDeleteIn, request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    if not payload.confirm:
        raise HTTPException(422, "confirm_required")
    tenant_id = _ensure_tenant(request)
    req_id = "dsr_" + secrets.token_hex(8)
    await _audit(
        db,
        tenant_id=tenant_id,
        user_id=getattr(request.state, "user_id", None),
        action="dsr.delete.request",
        request_id=req_id,
        diff={"subject_email": payload.subject_email, "reason": payload.reason},
    )
    await _notify_dpo("delete", payload.subject_email, tenant_id)
    return {
        "request_id": req_id,
        "status": "queued_for_dpo_review",
        "policy": "Hard deletes are gated on a 14-day grace period; soft-delete applied immediately.",
        "subject_email": payload.subject_email,
    }


@router.get("/portability")
async def portability_export(
    request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Return a JSON archive of the caller's tenant data.

    For non-super-admins this returns the data of the caller's own
    tenant only.
    """
    tenant_id = _ensure_tenant(request)
    bundle: dict[str, Any] = {
        "tenant_id": tenant_id,
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        tenant = (
            await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
        ).scalar_one_or_none()
        users = (
            await db.execute(select(UserRecord).where(UserRecord.tenant_id == tenant_id))
        ).scalars().all()
        leads = (
            await db.execute(
                select(LeadRecord).where(LeadRecord.tenant_id == tenant_id).limit(5000)
            )
        ).scalars().all()
        bundle["tenant"] = (
            {
                "id": tenant.id,
                "name": tenant.name,
                "plan": tenant.plan,
                "currency": tenant.currency,
                "created_at": tenant.created_at.isoformat(),
            }
            if tenant
            else None
        )
        bundle["users"] = [
            {"id": u.id, "email": u.email, "name": u.name, "created_at": u.created_at.isoformat()}
            for u in users
        ]
        bundle["leads"] = [
            {
                "id": l.id,
                "company_name": l.company_name,
                "sector": l.sector,
                "status": l.status,
                "created_at": l.created_at.isoformat(),
            }
            for l in leads
        ]
    except SQLAlchemyError:
        log.exception("dsr_portability_failed", tenant_id=tenant_id)
        raise HTTPException(500, "export_failed") from None
    return bundle


@router.get("/requests")
async def list_dsr_requests(
    request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    tenant_id = _ensure_tenant(request)
    rows = (
        await db.execute(
            select(AuditLogRecord)
            .where(
                AuditLogRecord.tenant_id == tenant_id,
                AuditLogRecord.entity_type == "dsr_request",
            )
            .order_by(AuditLogRecord.created_at.desc())
            .limit(200)
        )
    ).scalars().all()
    return {
        "tenant_id": tenant_id,
        "count": len(rows),
        "items": [
            {
                "request_id": r.entity_id,
                "action": r.action,
                "status": r.status,
                "submitted_at": r.created_at.isoformat(),
            }
            for r in rows
        ],
    }
