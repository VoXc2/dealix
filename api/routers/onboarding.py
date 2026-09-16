"""
Quote-first SaaS onboarding API — gated signup, wizard, and approval-first invites.

The canonical invitation implementation lives here. A compatibility installer
replaces the older ``/api/v1/auth/invite`` creation and acceptance routes before
the FastAPI app includes the auth router, so both public paths share the same
tenant, seat, token, delivery, and single-use safety contracts.
"""

from __future__ import annotations

import os
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user, require_tenant_admin
from api.security.jwt import decode_invite_token, hash_token
from core.email import send_invite_email
from db.models import RoleRecord, UserInviteRecord, UserRecord
from db.models_subscription import PlanRecord
from db.session import get_db as get_db_session
from dealix.onboarding.service import OnboardingService

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding"])
SELF_SERVE_PLAN_SLUGS = ("free", "starter", "growth")
SelfServePlanSlug = Literal["free", "starter", "growth"]
# Public self-serve remains source-disabled until shared multi-tenant SaaS isolation
# is independently accepted. An environment toggle alone can never create authority.
SELF_SERVE_PUBLIC_SIGNUP_AUTHORITY = False


def self_serve_signup_enabled() -> bool:
    """Return whether unattended public tenant creation is explicitly enabled.

    Current commercial authority is quote-first: free Execution Diagnostic,
    Qualified Discovery, then a customer-specific quote. Keep SaaS
    provisioning available without silently creating a public fixed-plan or
    self-checkout authority.
    """

    requested = os.getenv("DEALIX_SELF_SERVE_SIGNUP_ENABLED", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    return SELF_SERVE_PUBLIC_SIGNUP_AUTHORITY and requested


def _require_self_serve_signup_enabled() -> None:
    if self_serve_signup_enabled():
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=(
            "Self-serve signup is not enabled. Start with the free Execution "
            "Diagnostic and Qualified Discovery."
        ),
    )


class PlanOut(BaseModel):
    slug: str
    name_ar: str
    name_en: str
    price_sar_monthly: float
    price_sar_yearly: float | None
    max_users: int
    max_leads_per_month: int
    features: dict[str, Any]


class PlansOut(BaseModel):
    currency: str = "SAR"
    plans: list[PlanOut]


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=2)
    company_name: str = Field(..., min_length=2)
    plan_slug: SelfServePlanSlug = "free"
    billing_cycle: str = Field(default="monthly", pattern="^(monthly|yearly)$")


class SignupOut(BaseModel):
    tenant_id: str
    tenant_slug: str
    user_id: str
    subscription_id: str
    plan_slug: str
    requires_email_verification: bool
    message: str
    message_ar: str


class WizardRequest(BaseModel):
    sector: str | None = None
    company_size: str | None = None
    phone: str | None = None
    website: str | None = None


class InviteRequest(BaseModel):
    email: EmailStr
    role_name: str = Field(default="viewer")
    # Per-action approval. Even when provider delivery is globally enabled, a
    # tenant administrator must explicitly request an email for this invite.
    send_email: bool = False


class LegacyInviteRequest(BaseModel):
    """Backward-compatible request shape for ``/api/v1/auth/invite``."""

    email: EmailStr
    role: str = Field(default="sales_rep")
    send_email: bool = False


class InviteAcceptRequest(BaseModel):
    token: str = Field(..., min_length=20)
    name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=8)


class InviteOut(BaseModel):
    invite_id: str
    invite_url: str
    delivery_status: str
    message: str
    message_ar: str


class LegacyInviteOut(InviteOut):
    email: EmailStr
    role: str


@router.get("/plans", response_model=PlansOut)
async def list_self_serve_plans(
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Return self-serve plans only when that commercial surface is enabled."""

    _require_self_serve_signup_enabled()
    result = await session.execute(
        select(PlanRecord)
        .where(PlanRecord.slug.in_(SELF_SERVE_PLAN_SLUGS))
        .order_by(PlanRecord.sort_order, PlanRecord.price_sar_monthly)
    )
    by_slug = {plan.slug: plan for plan in result.scalars().all()}
    plans = []
    for slug in SELF_SERVE_PLAN_SLUGS:
        plan = by_slug.get(slug)
        if plan is None:
            continue
        plans.append(
            {
                "slug": plan.slug,
                "name_ar": plan.name_ar,
                "name_en": plan.name_en,
                "price_sar_monthly": float(plan.price_sar_monthly or 0),
                "price_sar_yearly": (
                    float(plan.price_sar_yearly) if plan.price_sar_yearly is not None else None
                ),
                "max_users": int(plan.max_users or 1),
                "max_leads_per_month": int(plan.max_leads_per_month or 0),
                "features": dict(plan.features or {}),
            }
        )
    return {"currency": "SAR", "plans": plans}


@router.post("/signup", response_model=SignupOut, status_code=status.HTTP_201_CREATED)
async def signup(
    req: SignupRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Create a tenant only when unattended SaaS signup is explicitly enabled."""
    _require_self_serve_signup_enabled()
    svc = OnboardingService(session)
    try:
        result = await svc.signup(
            email=str(req.email),
            password=req.password,
            name=req.name,
            company_name=req.company_name,
            plan_slug=req.plan_slug,
            billing_cycle=req.billing_cycle,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    await session.commit()
    return {
        "tenant_id": result["tenant"].id,
        "tenant_slug": result["tenant"].slug,
        "user_id": result["user"].id,
        "subscription_id": result["subscription"].id,
        "plan_slug": req.plan_slug,
        "requires_email_verification": result["requires_email_verification"],
        "message": "Account and workspace created successfully.",
        "message_ar": "تم إنشاء الحساب ومساحة العمل بنجاح.",
    }


@router.post("/wizard")
async def complete_wizard(
    req: WizardRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """Complete the tenant onboarding profile."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = OnboardingService(session)
    await svc.complete_onboarding_wizard(
        tenant_id=tenant_id,
        sector=req.sector,
        company_size=req.company_size,
        phone=req.phone,
        website=req.website,
    )
    await session.commit()

    return {
        "status": "completed",
        "message": "Onboarding completed successfully.",
        "message_ar": "تم إكمال الإعداد بنجاح.",
    }


async def _create_invite_response(
    *,
    email: str,
    role_name: str,
    send_email: bool,
    session: AsyncSession,
    current_user: Any,
) -> dict[str, Any]:
    """Create an invite and optionally perform one explicitly approved delivery."""

    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    normalized_email = email.strip().lower()
    normalized_role = role_name.strip().lower()
    svc = OnboardingService(session)
    try:
        result = await svc.invite_team_member(
            tenant_id=tenant_id,
            invited_by=current_user.id,
            email=normalized_email,
            role_name=normalized_role,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    # Persist the invitation before any optional external delivery attempt.
    await session.commit()

    web_base_url = os.getenv("DEALIX_WEB_URL", "https://dealix.me").rstrip("/")
    invite_url = f"{web_base_url}{result['invite_url']}"

    if not send_email:
        delivery_status = "manual_share_required"
        message = "Invitation created for manual sharing. Nothing was sent."
        message_ar = "تم إنشاء الدعوة للمشاركة اليدوية. لم يتم إرسال أي رسالة."
    else:
        delivery = await send_invite_email(
            to_email=normalized_email,
            invited_by_name=current_user.name or current_user.email or "Dealix admin",
            accept_url=invite_url,
        )

        if delivery.delivered:
            delivery_status = "delivered"
            message = "Invitation created and delivered."
            message_ar = "تم إنشاء الدعوة وإرسالها."
        elif delivery.blocked_by_policy:
            delivery_status = "manual_share_required"
            message = "Invitation created for manual sharing. Nothing was sent."
            message_ar = "تم إنشاء الدعوة للمشاركة اليدوية. لم يتم إرسال أي رسالة."
        else:
            delivery_status = "delivery_failed_manual_share_required"
            message = "Invitation created, but delivery failed. Share the link manually."
            message_ar = "تم إنشاء الدعوة، لكن تعذر الإرسال. شارك الرابط يدويًا."

    return {
        "invite_id": result["invite"].id,
        "invite_url": invite_url,
        "delivery_status": delivery_status,
        "message": message,
        "message_ar": message_ar,
    }


@router.post("/invite", response_model=InviteOut, status_code=status.HTTP_201_CREATED)
async def invite_team_member(
    req: InviteRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_tenant_admin),
) -> dict[str, Any]:
    """Create a single-use invitation with explicit, policy-gated delivery."""

    return await _create_invite_response(
        email=str(req.email),
        role_name=req.role_name,
        send_email=req.send_email,
        session=session,
        current_user=current_user,
    )


async def legacy_auth_invite(
    req: LegacyInviteRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_tenant_admin),
) -> dict[str, Any]:
    """Compatibility endpoint backed by the canonical safe invite flow."""

    response = await _create_invite_response(
        email=str(req.email),
        role_name=req.role,
        send_email=req.send_email,
        session=session,
        current_user=current_user,
    )
    return {**response, "email": str(req.email).strip().lower(), "role": req.role.strip().lower()}


async def legacy_auth_invite_accept(
    req: InviteAcceptRequest,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Redeem an invite using the persisted record as the authority.

    The row lock makes concurrent redemption deterministic. The role comes from
    the stored invite and must belong to the same tenant; the signed JWT role is
    treated as a consistency check, not the authorization source.
    """

    from api.routers import auth as auth_module

    try:
        payload = decode_invite_token(req.token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invite token",
        ) from exc

    email = str(payload.get("sub") or "").strip().lower()
    tenant_id = str(payload.get("tid") or "").strip()
    token_role_id = payload.get("rid")
    if not email or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invite token claims",
        )

    invite_result = await session.execute(
        select(UserInviteRecord)
        .where(
            and_(
                UserInviteRecord.tenant_id == tenant_id,
                UserInviteRecord.email == email,
                UserInviteRecord.token_hash == hash_token(req.token),
                UserInviteRecord.accepted_at.is_(None),
                UserInviteRecord.expires_at > auth_module._utcnow(),
            )
        )
        .with_for_update()
    )
    invite = invite_result.scalar_one_or_none()
    if invite is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite not found, expired, or already used",
        )

    if not invite.role_id or invite.role_id != token_role_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite role mismatch",
        )

    role_result = await session.execute(
        select(RoleRecord).where(
            RoleRecord.id == invite.role_id,
            RoleRecord.tenant_id == tenant_id,
        )
    )
    role = role_result.scalar_one_or_none()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite role is no longer valid",
        )

    existing_result = await session.execute(
        select(UserRecord).where(
            UserRecord.tenant_id == tenant_id,
            UserRecord.email == email,
        )
    )
    if existing_result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered for this tenant",
        )

    user = UserRecord(
        id=auth_module._new_id("usr_"),
        tenant_id=tenant_id,
        role_id=invite.role_id,
        email=email,
        name=req.name.strip(),
        hashed_password=auth_module._hash_password(req.password),
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    invite.accepted_at = auth_module._utcnow()
    await session.flush()

    return await auth_module._issue_tokens(user, session, request)


def _install_auth_invite_compatibility() -> None:
    """Replace legacy invite routes before ``auth.router`` is included.

    ``api.main`` imports the auth module before this onboarding module and only
    includes routers afterwards, making this deterministic and avoiding
    duplicate runtime and OpenAPI routes.
    """

    from api.routers import auth as auth_module

    replaced_paths = {"/invite", "/invite/accept"}
    retained_routes = []
    for route_item in auth_module.router.routes:
        methods = set(getattr(route_item, "methods", set()) or set())
        if getattr(route_item, "path", None) in replaced_paths and "POST" in methods:
            continue
        retained_routes.append(route_item)
    auth_module.router.routes = retained_routes
    auth_module.router.add_api_route(
        "/invite",
        legacy_auth_invite,
        methods=["POST"],
        status_code=status.HTTP_201_CREATED,
        response_model=LegacyInviteOut,
        name="legacy_auth_invite_compatibility",
    )
    auth_module.router.add_api_route(
        "/invite/accept",
        legacy_auth_invite_accept,
        methods=["POST"],
        status_code=status.HTTP_201_CREATED,
        response_model=auth_module.TokenResponse,
        name="legacy_auth_invite_accept_compatibility",
    )


def _quarantine_retired_self_serve_routes() -> None:
    """Keep retired public self-serve plan/signup routes out of launch runtime.

    The implementation remains source-available for a future explicitly approved
    SaaS launch, but environment state alone cannot remount commercial authority.
    """

    retired = {"/api/v1/onboarding/plans", "/api/v1/onboarding/signup"}
    router.routes = [
        route_item
        for route_item in router.routes
        if getattr(route_item, "path", None) not in retired
    ]


_quarantine_retired_self_serve_routes()
_install_auth_invite_compatibility()
