"""
Self-serve onboarding — turns the founder-led `scripts/dealix_customer_onboarding_wizard.py`
CLI into a 4-step API + frontend wizard.

Endpoints (all `/api/v1/onboarding/...`):

    POST /start          — creates a TenantRecord + first owner UserRecord, returns onboarding_id
    POST /integrations   — records which integrations the customer wants enabled
    POST /dpa            — captures PDPL DPA acceptance + signer name
    POST /finalize       — issues first API key and marks tenant as `onboarded`
    GET  /{onboarding_id} — current state (for resume / refresh)

Idempotency: each step keys off `onboarding_id`; calling /start with the
same email + company within 5 minutes returns the same in-progress record
instead of double-creating tenants.

The endpoints intentionally do not require auth — they are how strangers
become customers. Rate-limited per IP via the existing slowapi setup.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import TenantRecord, UserRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])
log = get_logger(__name__)

# Onboarding sessions live in tenant.meta_json under `onboarding`.
_IDEMPOTENCY_WINDOW = timedelta(minutes=5)


# ── Schemas ──────────────────────────────────────────────────────────


class OnboardingStartIn(BaseModel):
    company: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=120)
    sector: str = Field(default="", max_length=80)
    size: str = Field(default="", max_length=40)
    locale: Literal["ar", "en"] = "ar"
    timezone: str = Field(default="Asia/Riyadh", max_length=64)
    source: str = Field(default="landing.self_serve", max_length=80)


class OnboardingIntegrationsIn(BaseModel):
    onboarding_id: str = Field(..., max_length=64)
    integrations: list[str] = Field(default_factory=list, max_length=20)
    # e.g. ["hubspot", "whatsapp", "calendly", "resend", "moyasar"]


class OnboardingDPAIn(BaseModel):
    onboarding_id: str = Field(..., max_length=64)
    accept: bool
    signer_name: str = Field(..., min_length=1, max_length=120)
    signer_title: str = Field(default="", max_length=120)


class OnboardingFinalizeIn(BaseModel):
    onboarding_id: str = Field(..., max_length=64)
    plan: Literal["pilot", "starter", "growth", "scale"] = "starter"


# ── Helpers ──────────────────────────────────────────────────────────


def _slugify(value: str) -> str:
    base = "".join(c.lower() if c.isalnum() else "-" for c in value).strip("-")
    return (base or "tenant") + "-" + secrets.token_hex(3)


def _onboarding_state(tenant: TenantRecord) -> dict[str, Any]:
    return (tenant.meta_json or {}).get("onboarding", {})


async def _find_in_progress(
    db: AsyncSession, email: str, company: str
) -> TenantRecord | None:
    """Re-attach to an in-progress onboarding within the idempotency window."""
    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - _IDEMPOTENCY_WINDOW
    rows = (
        await db.execute(
            select(TenantRecord)
            .where(TenantRecord.status == "onboarding", TenantRecord.created_at >= cutoff)
            .order_by(TenantRecord.created_at.desc())
            .limit(20)
        )
    ).scalars().all()
    target_email = email.lower()
    target_company = company.strip().lower()
    for t in rows:
        meta = _onboarding_state(t)
        if meta.get("email", "").lower() == target_email and meta.get(
            "company", ""
        ).strip().lower() == target_company:
            return t
    return None


# ── Endpoints ────────────────────────────────────────────────────────


@router.post("/start")
async def start_onboarding(
    payload: OnboardingStartIn, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Step 1: stranger → tenant scaffold + owner user."""
    existing = await _find_in_progress(db, payload.email, payload.company)
    if existing is not None:
        log.info(
            "onboarding_resume",
            tenant_id=existing.id,
            email=payload.email,
            company=payload.company,
        )
        return {
            "onboarding_id": existing.id,
            "tenant_id": existing.id,
            "step": _onboarding_state(existing).get("step", "start"),
            "resumed": True,
        }

    tenant_id = "ten_" + secrets.token_hex(8)
    user_id = "usr_" + secrets.token_hex(8)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    tenant = TenantRecord(
        id=tenant_id,
        name=payload.company,
        slug=_slugify(payload.company),
        plan="pilot",
        status="onboarding",
        timezone=payload.timezone,
        locale=payload.locale,
        currency="SAR" if payload.locale == "ar" else "USD",
        max_users=5,
        max_leads_per_month=1000,
        features={},
        meta_json={
            "onboarding": {
                "step": "start",
                "company": payload.company,
                "email": payload.email,
                "name": payload.name,
                "sector": payload.sector,
                "size": payload.size,
                "source": payload.source,
                "started_at": now.isoformat(),
            }
        },
    )
    owner = UserRecord(
        id=user_id,
        tenant_id=tenant_id,
        email=payload.email,
        name=payload.name,
        hashed_password="",  # set when the user accepts the magic link
        is_active=True,
        is_verified=False,
    )
    db.add_all([tenant, owner])
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        log.exception("onboarding_start_persist_failed", email=payload.email)
        raise HTTPException(500, "onboarding_persistence_failed") from exc

    log.info(
        "onboarding_started",
        tenant_id=tenant_id,
        email=payload.email,
        company=payload.company,
        source=payload.source,
    )
    return {
        "onboarding_id": tenant_id,
        "tenant_id": tenant_id,
        "user_id": user_id,
        "step": "start",
        "next": "integrations",
    }


@router.post("/integrations")
async def record_integrations(
    payload: OnboardingIntegrationsIn, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Step 2: capture which integrations the customer wants enabled."""
    tenant = (
        await db.execute(
            select(TenantRecord).where(TenantRecord.id == payload.onboarding_id)
        )
    ).scalar_one_or_none()
    if tenant is None or tenant.status != "onboarding":
        raise HTTPException(404, "onboarding_not_found_or_already_finalized")

    meta = dict(tenant.meta_json or {})
    state = dict(meta.get("onboarding") or {})
    state["integrations"] = sorted(set(payload.integrations))
    state["step"] = "integrations"
    state["integrations_at"] = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    meta["onboarding"] = state
    tenant.meta_json = meta
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(500, "onboarding_persistence_failed") from exc

    return {
        "onboarding_id": tenant.id,
        "step": "integrations",
        "integrations": state["integrations"],
        "next": "dpa",
    }


@router.post("/dpa")
async def accept_dpa(
    payload: OnboardingDPAIn, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Step 3: capture PDPL Data Processing Agreement acceptance."""
    if not payload.accept:
        raise HTTPException(422, "dpa_required")

    tenant = (
        await db.execute(
            select(TenantRecord).where(TenantRecord.id == payload.onboarding_id)
        )
    ).scalar_one_or_none()
    if tenant is None or tenant.status != "onboarding":
        raise HTTPException(404, "onboarding_not_found_or_already_finalized")

    meta = dict(tenant.meta_json or {})
    state = dict(meta.get("onboarding") or {})
    state["dpa"] = {
        "accepted": True,
        "signer_name": payload.signer_name,
        "signer_title": payload.signer_title,
        "accepted_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
    }
    state["step"] = "dpa"
    meta["onboarding"] = state
    tenant.meta_json = meta
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(500, "onboarding_persistence_failed") from exc

    log.info(
        "onboarding_dpa_accepted",
        tenant_id=tenant.id,
        signer=payload.signer_name,
    )
    return {"onboarding_id": tenant.id, "step": "dpa", "next": "finalize"}


@router.post("/finalize")
async def finalize_onboarding(
    payload: OnboardingFinalizeIn, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Step 4: flip tenant to active + issue first API key.

    The API key is hashed before storage (mirrors invite-token discipline);
    the raw key is shown to the customer exactly once. They are expected to
    store it in their own secrets manager.
    """
    tenant = (
        await db.execute(
            select(TenantRecord).where(TenantRecord.id == payload.onboarding_id)
        )
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "onboarding_not_found")
    state = _onboarding_state(tenant)
    if not state.get("dpa", {}).get("accepted"):
        raise HTTPException(409, "dpa_not_accepted")

    raw_key = "dlx_live_" + secrets.token_urlsafe(28)
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    meta = dict(tenant.meta_json or {})
    api_keys = list(meta.get("api_keys") or [])
    api_keys.append(
        {
            "label": "first-key",
            "hash": key_hash,
            "prefix": raw_key[:12],
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
        }
    )
    meta["api_keys"] = api_keys
    onboarding = dict(state)
    onboarding["step"] = "finalized"
    onboarding["finalized_at"] = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    meta["onboarding"] = onboarding
    tenant.meta_json = meta
    tenant.plan = payload.plan
    tenant.status = "active"
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(500, "onboarding_persistence_failed") from exc

    log.info(
        "onboarding_finalized",
        tenant_id=tenant.id,
        plan=payload.plan,
        key_prefix=raw_key[:12],
    )
    return {
        "ok": True,
        "tenant_id": tenant.id,
        "plan": tenant.plan,
        "api_key": raw_key,  # shown ONCE — caller must persist
        "api_key_prefix": raw_key[:12],
        "next_step": "log_in_with_owner_email_and_password_reset",
    }


@router.get("/{onboarding_id}")
async def get_onboarding_state(
    onboarding_id: str, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    """Return the current onboarding state — used by the FE wizard to resume."""
    tenant = (
        await db.execute(select(TenantRecord).where(TenantRecord.id == onboarding_id))
    ).scalar_one_or_none()
    if tenant is None:
        raise HTTPException(404, "onboarding_not_found")
    state = _onboarding_state(tenant)
    return {
        "onboarding_id": tenant.id,
        "status": tenant.status,
        "plan": tenant.plan,
        "step": state.get("step", "start"),
        "company": state.get("company"),
        "integrations": state.get("integrations", []),
        "dpa_accepted": bool(state.get("dpa", {}).get("accepted")),
    }
