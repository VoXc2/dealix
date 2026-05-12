"""
Enterprise SSO endpoints — WorkOS-backed SAML/OIDC.

Endpoints:
    GET  /api/v1/auth/sso/start?org_id=...   — 302 to WorkOS authorize URL
    GET  /api/v1/auth/sso/callback?code=...  — exchange code, find/create user, mint our JWT
    POST /api/v1/auth/sso/admin-portal       — return a one-time WorkOS Admin Portal URL

Behaviour without WORKOS_API_KEY: every endpoint returns 503 sso_disabled.
This keeps existing JWT auth path untouched for tenants that don't use SSO.
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import TenantRecord, UserRecord
from db.session import get_db
from dealix.identity.workos_client import WorkOSNotConfigured, get_workos_client

router = APIRouter(prefix="/api/v1/auth/sso", tags=["sso"])
log = get_logger(__name__)


@router.get("/start")
async def sso_start(
    request: Request,
    org_id: str = Query(..., max_length=128, alias="org_id"),
    state: str | None = Query(default=None, max_length=64),
) -> RedirectResponse:
    """Kick off SSO. `org_id` is the WorkOS organization the tenant maps to."""
    client = get_workos_client()
    if not client.is_configured:
        raise HTTPException(503, "sso_disabled")
    base = (os.getenv("APP_URL", "").rstrip("/")) or str(request.base_url).rstrip("/")
    redirect_uri = f"{base}/api/v1/auth/sso/callback"
    try:
        url = client.build_authorization_url(
            redirect_uri=redirect_uri, state=state, organization_id=org_id
        )
    except WorkOSNotConfigured:
        raise HTTPException(503, "sso_disabled") from None
    log.info("sso_authorize_redirect", org_id=org_id)
    return RedirectResponse(url=url, status_code=302)


@router.get("/callback")
async def sso_callback(
    code: str = Query(..., max_length=512),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Complete SSO flow: exchange code → find tenant by workos_org_id → mint our JWT."""
    client = get_workos_client()
    if not client.is_configured:
        raise HTTPException(503, "sso_disabled")
    try:
        profile = await client.exchange_code(code)
    except WorkOSNotConfigured:
        raise HTTPException(503, "sso_disabled") from None
    except Exception:
        log.exception("workos_exchange_failed")
        raise HTTPException(502, "workos_upstream_error") from None

    # Find the tenant whose meta_json carries this workos org id.
    if not profile.organization_id:
        raise HTTPException(422, "missing_organization_id")
    tenant_row = None
    try:
        rows = (
            await db.execute(select(TenantRecord).where(TenantRecord.status == "active"))
        ).scalars().all()
        for t in rows:
            if (t.meta_json or {}).get("workos_org_id") == profile.organization_id:
                tenant_row = t
                break
    except SQLAlchemyError:
        log.exception("workos_tenant_lookup_failed")
        raise HTTPException(500, "tenant_lookup_failed") from None
    if tenant_row is None:
        raise HTTPException(404, "tenant_for_organization_not_found")

    # Upsert the user under that tenant.
    user = (
        await db.execute(
            select(UserRecord).where(
                UserRecord.tenant_id == tenant_row.id, UserRecord.email == profile.email
            )
        )
    ).scalar_one_or_none()
    if user is None:
        import secrets

        user = UserRecord(
            id="usr_" + secrets.token_hex(8),
            tenant_id=tenant_row.id,
            email=profile.email,
            name=" ".join(filter(None, [profile.first_name, profile.last_name])).strip()
            or profile.email.split("@")[0],
            is_active=True,
            is_verified=True,
        )
        db.add(user)
        try:
            await db.commit()
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(500, "user_provision_failed") from None

    # Mint our own JWT pair via the existing auth helper.
    try:
        from api.security.jwt import issue_token_pair  # type: ignore
    except Exception:
        raise HTTPException(500, "jwt_issuer_unavailable") from None
    tokens = issue_token_pair(user_id=user.id, tenant_id=tenant_row.id)

    log.info(
        "sso_login_success",
        tenant_id=tenant_row.id,
        user_id=user.id,
        provider="workos",
    )
    return {
        "ok": True,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "tenant_id": tenant_row.id,
        },
        "tokens": tokens,
    }


class AdminPortalIn(BaseModel):
    organization_id: str = Field(..., max_length=128)
    intent: str = Field(default="sso", max_length=32)


@router.post("/admin-portal")
async def workos_admin_portal(payload: AdminPortalIn) -> dict[str, Any]:
    """One-time WorkOS Admin Portal link the customer's IT admin uses to set up SSO."""
    client = get_workos_client()
    if not client.is_configured:
        raise HTTPException(503, "sso_disabled")
    try:
        link = await client.admin_portal_link(
            payload.organization_id, intent=payload.intent
        )
    except WorkOSNotConfigured:
        raise HTTPException(503, "sso_disabled") from None
    except Exception:
        log.exception("workos_admin_portal_failed", organization=payload.organization_id)
        raise HTTPException(502, "workos_upstream_error") from None
    return {"url": link, "organization_id": payload.organization_id}
