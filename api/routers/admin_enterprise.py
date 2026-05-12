"""
Enterprise admin surface (T6e):

    POST   /api/v1/admin/sandbox/spin-up         — clone tenant settings into a sandbox shadow.
    POST   /api/v1/admin/tenant/{id}/ip-allowlist — set per-tenant CIDR list.
    DELETE /api/v1/admin/tenant/{id}/ip-allowlist — remove.
    POST   /api/v1/admin/tenant/{id}/webhook-keys/rotate — rotate a tenant's signing secret.
    GET    /api/v1/admin/byok/status             — surface which BYOK provider is wired.
    GET    /api/v1/admin/audit-forward/status    — surface which sinks are configured.

Admin-only via ADMIN_API_KEYS or super_admin claim — same gate as the
existing admin routers.
"""

from __future__ import annotations

import os
import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from dealix.audit.byok import BYOKProvider
from db.models import TenantRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/admin", tags=["admin", "enterprise"])
log = get_logger(__name__)


def _require_admin(request: Request) -> None:
    if getattr(request.state, "is_super_admin", False):
        return
    api_key = request.headers.get("x-api-key", "")
    admin_keys = {k.strip() for k in os.getenv("ADMIN_API_KEYS", "").split(",") if k.strip()}
    if api_key not in admin_keys:
        raise HTTPException(403, "admin_only")


class SandboxSpinUpIn(BaseModel):
    tenant_id: str = Field(..., max_length=64)
    label: str = Field(default="sandbox", max_length=64)


@router.post("/sandbox/spin-up")
async def sandbox_spin_up(
    payload: SandboxSpinUpIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _require_admin(request)
    source = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == payload.tenant_id))
    ).scalar_one_or_none()
    if source is None:
        raise HTTPException(404, "tenant_not_found")
    sandbox_id = f"sandbox_{payload.tenant_id}_{secrets.token_hex(4)}"
    meta = dict(source.meta_json or {})
    sandbox = TenantRecord(
        id=sandbox_id,
        name=f"[Sandbox] {source.name}",
        slug=f"{source.slug}-sandbox-{secrets.token_hex(2)}",
        plan="pilot",
        status="active",
        timezone=source.timezone,
        locale=source.locale,
        currency=source.currency,
        max_users=source.max_users,
        max_leads_per_month=source.max_leads_per_month,
        features=source.features or {},
        meta_json={**meta, "sandbox_of": payload.tenant_id, "label": payload.label},
    )
    db.add(sandbox)
    try:
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "sandbox_persist_failed") from None
    log.info(
        "sandbox_spun_up",
        source_tenant_id=payload.tenant_id,
        sandbox_tenant_id=sandbox_id,
        label=payload.label,
    )
    return {"ok": True, "tenant_id": sandbox_id, "source": payload.tenant_id}


class IPAllowlistIn(BaseModel):
    cidrs: list[str] = Field(..., max_length=64)


@router.post("/tenant/{tenant_id}/ip-allowlist")
async def set_ip_allowlist(
    tenant_id: str,
    payload: IPAllowlistIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _require_admin(request)
    import ipaddress

    parsed: list[str] = []
    for c in payload.cidrs:
        try:
            ipaddress.ip_network(c, strict=False)
            parsed.append(c)
        except ValueError as exc:
            raise HTTPException(422, f"invalid_cidr:{c}:{exc}") from exc

    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    meta["ip_allowlist"] = parsed
    tenant.meta_json = meta
    await db.commit()
    log.info("ip_allowlist_set", tenant_id=tenant_id, cidrs=parsed)
    return {"ok": True, "tenant_id": tenant_id, "cidrs": parsed}


@router.delete("/tenant/{tenant_id}/ip-allowlist")
async def clear_ip_allowlist(
    tenant_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _require_admin(request)
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    meta.pop("ip_allowlist", None)
    tenant.meta_json = meta
    await db.commit()
    return {"ok": True, "tenant_id": tenant_id}


@router.post("/tenant/{tenant_id}/webhook-keys/rotate")
async def rotate_webhook_keys(
    tenant_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _require_admin(request)
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")
    meta = dict(tenant.meta_json or {})
    new_secret = secrets.token_urlsafe(32)
    rotated = list(meta.get("webhook_keys_rotated") or [])
    rotated.append(
        {"prefix": new_secret[:8], "rotated_at": __import__("datetime").datetime.utcnow().isoformat()}
    )
    meta["webhook_secret_current_prefix"] = new_secret[:8]
    meta["webhook_keys_rotated"] = rotated
    tenant.meta_json = meta
    await db.commit()
    log.info("webhook_secret_rotated", tenant_id=tenant_id, prefix=new_secret[:8])
    return {
        "ok": True,
        "tenant_id": tenant_id,
        "webhook_secret": new_secret,  # shown once
        "prefix": new_secret[:8],
    }


@router.get("/byok/status")
async def byok_status(request: Request) -> dict[str, Any]:
    _require_admin(request)
    provider = BYOKProvider.from_env()
    return {
        "configured": provider is not None,
        "provider": os.getenv("KMS_PROVIDER", "").strip() or None,
        "key_id_present": bool(os.getenv("KMS_KEY_ID", "").strip()),
    }


@router.get("/audit-forward/status")
async def audit_forward_status(request: Request) -> dict[str, Any]:
    _require_admin(request)
    return {
        "datadog": bool(os.getenv("AUDIT_FORWARD_DATADOG_API_KEY", "").strip()),
        "splunk": bool(os.getenv("AUDIT_FORWARD_SPLUNK_URL", "").strip())
        and bool(os.getenv("AUDIT_FORWARD_SPLUNK_TOKEN", "").strip()),
        "s3": bool(os.getenv("AUDIT_FORWARD_S3_BUCKET", "").strip()),
    }
