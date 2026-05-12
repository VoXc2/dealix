"""
Customer portal data plane — real DB queries for the customer-facing portal.

Distinct from `customer_company_portal.py` (which serves the 8-section
diagnostic UI). This router exposes the read endpoints the Next.js
dashboard needs to render plan / invoices / team / summary, plus the
write endpoints for team-seat management.

Endpoints (all `/api/v1/customers/{tenant_id}/...`):

    GET    /summary          — KPI envelope (users, leads, deals, last_active)
    GET    /subscription     — plan, status, renewal_at, currency, limits
    GET    /invoices         — Moyasar + Stripe history merged (latest 100)
    GET    /team/members     — UserRecord list scoped to tenant
    POST   /team/invite      — issues UserInviteRecord (uses existing auth flow)
    DELETE /team/members/{user_id} — soft-deletes a user

Authorization: requires API key middleware to have resolved tenant_id;
caller's `request.state.tenant_id` MUST match the path tenant_id, else
`403 cross_tenant_access_denied`. This relies on the existing
TenantIsolationMiddleware contract.
"""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import and_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import (
    AuditLogRecord,
    DealRecord,
    LeadRecord,
    TenantRecord,
    UserInviteRecord,
    UserRecord,
)
from db.session import get_db

router = APIRouter(prefix="/api/v1/customers", tags=["customer-portal"])
log = get_logger(__name__)

_INVITE_TTL = timedelta(hours=72)


def _assert_tenant_match(request: Request, tenant_id: str) -> None:
    """Enforce that the caller's resolved tenant matches the path tenant."""
    caller_tenant = getattr(request.state, "tenant_id", None)
    # super-admin bypass — resolved by APIKeyMiddleware via system_role
    if getattr(request.state, "is_super_admin", False):
        return
    if caller_tenant and caller_tenant != tenant_id:
        log.warning(
            "cross_tenant_access_denied",
            caller_tenant=caller_tenant,
            requested_tenant=tenant_id,
        )
        raise HTTPException(status_code=403, detail="cross_tenant_access_denied")


class TeamInviteIn(BaseModel):
    email: EmailStr
    role: str = Field(default="user", max_length=32)
    name: str = Field(default="", max_length=120)


class TeamInviteOut(BaseModel):
    invite_id: str
    email: str
    role: str
    expires_at: datetime
    invite_url: str


@router.get("/{tenant_id}/summary")
async def customer_summary(
    request: Request,
    tenant_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """KPI envelope for the customer dashboard.

    Returns counts the founder + customer both rely on; falls back to
    zeros when the underlying tables are absent (test/dev) so the UI
    never breaks.
    """
    _assert_tenant_match(request, tenant_id)
    metrics: dict[str, Any] = {
        "tenant_id": tenant_id,
        "users_active": 0,
        "leads_total": 0,
        "leads_7d": 0,
        "deals_open": 0,
        "deals_won_30d": 0,
        "last_active_at": None,
    }
    cutoff_7d = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7)
    cutoff_30d = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30)

    try:
        tenant = (
            await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(404, "tenant_not_found")

        users_q = await db.execute(
            select(func.count())
            .select_from(UserRecord)
            .where(UserRecord.tenant_id == tenant_id, UserRecord.is_active.is_(True))
        )
        metrics["users_active"] = int(users_q.scalar() or 0)

        leads_total = await db.execute(
            select(func.count()).select_from(LeadRecord).where(LeadRecord.tenant_id == tenant_id)
        )
        metrics["leads_total"] = int(leads_total.scalar() or 0)

        leads_7d = await db.execute(
            select(func.count())
            .select_from(LeadRecord)
            .where(LeadRecord.tenant_id == tenant_id, LeadRecord.created_at >= cutoff_7d)
        )
        metrics["leads_7d"] = int(leads_7d.scalar() or 0)

        deals_open = await db.execute(
            select(func.count())
            .select_from(DealRecord)
            .where(
                DealRecord.tenant_id == tenant_id,
                DealRecord.status.notin_(["won", "lost", "abandoned"]),
            )
        )
        metrics["deals_open"] = int(deals_open.scalar() or 0)

        deals_won_30d = await db.execute(
            select(func.count())
            .select_from(DealRecord)
            .where(
                DealRecord.tenant_id == tenant_id,
                DealRecord.status == "won",
                DealRecord.updated_at >= cutoff_30d,
            )
        )
        metrics["deals_won_30d"] = int(deals_won_30d.scalar() or 0)

        last_audit = await db.execute(
            select(AuditLogRecord.created_at)
            .where(AuditLogRecord.tenant_id == tenant_id)
            .order_by(AuditLogRecord.created_at.desc())
            .limit(1)
        )
        ts = last_audit.scalar_one_or_none()
        metrics["last_active_at"] = ts.isoformat() if ts else None
    except HTTPException:
        raise
    except SQLAlchemyError:
        log.exception("customer_summary_db_failed", extra={"tenant_id": tenant_id})

    return metrics


@router.get("/{tenant_id}/subscription")
async def customer_subscription(
    request: Request,
    tenant_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Subscription state — plan, status, limits, renewal target."""
    _assert_tenant_match(request, tenant_id)
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")

    # Renewal target is meta-driven; default to created_at + 1y if absent.
    meta = tenant.meta_json or {}
    renewal_at = meta.get("subscription_renewal_at")
    if not renewal_at:
        renewal_at = (tenant.created_at + timedelta(days=365)).isoformat()

    return {
        "tenant_id": tenant.id,
        "name": tenant.name,
        "plan": tenant.plan,
        "status": tenant.status,
        "currency": tenant.currency,
        "max_users": tenant.max_users,
        "max_leads_per_month": tenant.max_leads_per_month,
        "renewal_at": renewal_at,
        "features": tenant.features or {},
        "billing_provider": meta.get("billing_provider", "moyasar"),
    }


@router.get("/{tenant_id}/invoices")
async def customer_invoices(
    request: Request,
    tenant_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Invoice history.

    For now reads audit-log rows tagged action='invoice.*' as the
    source of truth (Moyasar webhook handler in pricing.py writes these).
    A first-class InvoiceRecord table is on the roadmap (T2 — Lago).
    """
    _assert_tenant_match(request, tenant_id)
    try:
        rows = (
            await db.execute(
                select(AuditLogRecord)
                .where(
                    AuditLogRecord.tenant_id == tenant_id,
                    AuditLogRecord.entity_type == "invoice",
                )
                .order_by(AuditLogRecord.created_at.desc())
                .limit(100)
            )
        ).scalars().all()
    except SQLAlchemyError:
        log.exception("customer_invoices_db_failed", extra={"tenant_id": tenant_id})
        rows = []

    invoices = [
        {
            "id": r.entity_id,
            "action": r.action,
            "status": r.status,
            "amount_sar": (r.diff or {}).get("amount_sar"),
            "amount_usd": (r.diff or {}).get("amount_usd"),
            "provider": (r.diff or {}).get("provider", "moyasar"),
            "issued_at": r.created_at.isoformat(),
        }
        for r in rows
    ]
    return {"tenant_id": tenant_id, "count": len(invoices), "invoices": invoices}


@router.get("/{tenant_id}/team/members")
async def list_team_members(
    request: Request,
    tenant_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Active + pending members of the tenant."""
    _assert_tenant_match(request, tenant_id)

    users = (
        await db.execute(
            select(UserRecord)
            .where(UserRecord.tenant_id == tenant_id, UserRecord.deleted_at.is_(None))
            .order_by(UserRecord.created_at.asc())
        )
    ).scalars().all()

    pending = (
        await db.execute(
            select(UserInviteRecord)
            .where(
                UserInviteRecord.tenant_id == tenant_id,
                UserInviteRecord.accepted_at.is_(None),
                UserInviteRecord.expires_at > datetime.now(timezone.utc).replace(tzinfo=None),
            )
            .order_by(UserInviteRecord.created_at.desc())
        )
    ).scalars().all()

    return {
        "tenant_id": tenant_id,
        "members": [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "is_active": u.is_active,
                "is_verified": u.is_verified,
                "mfa_enabled": u.mfa_enabled,
                "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ],
        "pending_invites": [
            {
                "id": i.id,
                "email": i.email,
                "expires_at": i.expires_at.isoformat(),
                "invited_by": i.invited_by,
            }
            for i in pending
        ],
    }


@router.post("/{tenant_id}/team/invite", response_model=TeamInviteOut)
async def invite_team_member(
    request: Request,
    payload: TeamInviteIn,
    tenant_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> TeamInviteOut:
    """Issue a single-use invite token. Send via existing email pipeline.

    The token itself is not stored — only its hash. The caller surfaces
    the full URL via `invite_url`, which integrates with the existing
    /api/v1/auth/accept-invite endpoint.
    """
    _assert_tenant_match(request, tenant_id)
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == tenant_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "tenant_not_found")

    # Seat-cap guard.
    user_count = (
        await db.execute(
            select(func.count())
            .select_from(UserRecord)
            .where(
                UserRecord.tenant_id == tenant_id,
                UserRecord.is_active.is_(True),
                UserRecord.deleted_at.is_(None),
            )
        )
    ).scalar() or 0
    if user_count >= tenant.max_users:
        raise HTTPException(
            status_code=402,
            detail={"error": "seat_limit_reached", "max_users": tenant.max_users},
        )

    # Replace any existing pending invite for the same email.
    existing = (
        await db.execute(
            select(UserInviteRecord).where(
                and_(
                    UserInviteRecord.tenant_id == tenant_id,
                    UserInviteRecord.email == payload.email,
                    UserInviteRecord.accepted_at.is_(None),
                )
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        await db.delete(existing)
        await db.flush()

    invite_id = "inv_" + secrets.token_hex(8)
    raw_token = secrets.token_urlsafe(32)
    # Hash the token — never store plaintext.
    import hashlib

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    inviter = getattr(request.state, "user_id", None) or "system"

    invite = UserInviteRecord(
        id=invite_id,
        tenant_id=tenant_id,
        email=payload.email,
        role_id=None,  # role resolved when accepted via auth router
        invited_by=inviter,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + _INVITE_TTL,
    )
    db.add(invite)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        log.exception("invite_commit_failed", extra={"tenant_id": tenant_id})
        raise HTTPException(500, "invite_persistence_failed") from exc

    # Build the URL the FE shows / the email service mails.
    from core.config.settings import get_settings

    base = get_settings().app_url.rstrip("/") if hasattr(get_settings(), "app_url") else ""
    invite_url = f"{base}/accept-invite?token={raw_token}&invite_id={invite_id}"

    log.info(
        "team_invite_created",
        invite_id=invite_id,
        tenant_id=tenant_id,
        email=payload.email,
        invited_by=inviter,
    )
    return TeamInviteOut(
        invite_id=invite_id,
        email=payload.email,
        role=payload.role,
        expires_at=invite.expires_at,
        invite_url=invite_url,
    )


@router.delete("/{tenant_id}/team/members/{user_id}")
async def revoke_team_member(
    request: Request,
    tenant_id: str = Path(..., max_length=64),
    user_id: str = Path(..., max_length=64),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Soft-delete a user (sets deleted_at + is_active=False)."""
    _assert_tenant_match(request, tenant_id)
    user = (
        await db.execute(
            select(UserRecord).where(
                UserRecord.id == user_id, UserRecord.tenant_id == tenant_id
            )
        )
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(404, "user_not_found")

    user.is_active = False
    user.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        log.exception("revoke_member_failed", extra={"user_id": user_id})
        raise HTTPException(500, "revoke_failed") from exc

    log.info(
        "team_member_revoked",
        user_id=user_id,
        tenant_id=tenant_id,
        revoked_by=getattr(request.state, "user_id", "system"),
    )
    return {"ok": True, "user_id": user_id, "status": "revoked"}
