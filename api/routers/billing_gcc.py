"""
GCC payment gateways router (T8b):

    GET  /api/v1/billing/gcc/health
    POST /api/v1/billing/gcc/checkout/knet     — Kuwait debit-card switch (KWD).
    POST /api/v1/billing/gcc/checkout/benefit  — Bahrain payment + e-KYC (BHD).
    POST /api/v1/billing/gcc/checkout/magnati  — UAE acquiring (AED).
    POST /api/v1/billing/gcc/webhooks/{knet|benefit|magnati}

Each endpoint mirrors the Stripe/Moyasar contract: hosted-checkout
URL out; HMAC-SHA256 signature-verified webhook in. Inert without
the corresponding env vars — calls 503 instead of failing silently.

Customers in KW / BH / AE who can't reach Moyasar (KSA-only) or Tap
(GCC-wide but issuer routing varies) flow through these endpoints.
"""

from __future__ import annotations

import os
from typing import Any, Literal

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from core.logging import get_logger
from dealix.payments.benefit_client import BenefitNotConfigured, get_benefit_client
from dealix.payments.knet_client import KNetNotConfigured, get_knet_client
from dealix.payments.magnati_client import MagnatiNotConfigured, get_magnati_client

router = APIRouter(prefix="/api/v1/billing/gcc", tags=["billing", "gcc"])
log = get_logger(__name__)


# ─────────────────────────────── health ──────────────────────────────


@router.get("/health")
async def gcc_health() -> dict[str, Any]:
    """Report only configured GCC gateways by default.

    Procurement-honest behaviour: a public buyer hitting this endpoint
    should see what they can actually use today. Operators who need to
    see the full pre-onboarding posture pass `?include_unconfigured=1`.
    """
    rows: dict[str, bool] = {
        "knet": get_knet_client().is_configured,
        "benefit": get_benefit_client().is_configured,
        "magnati": get_magnati_client().is_configured,
    }
    return {
        "available": [k for k, v in rows.items() if v],
        "configured_count": sum(rows.values()),
        # Back-compat for older callers that read *_configured booleans.
        **{f"{k}_configured": v for k, v in rows.items()},
    }


@router.get("/health/full")
async def gcc_health_full() -> dict[str, Any]:
    """Operator view — always lists every gateway with its configured
    flag, so the founder can see which ones still need merchant
    onboarding."""
    rows: dict[str, dict[str, Any]] = {}
    for name, client in (
        ("knet", get_knet_client()),
        ("benefit", get_benefit_client()),
        ("magnati", get_magnati_client()),
    ):
        rows[name] = {
            "configured": client.is_configured,
            "status": "live" if client.is_configured else "pending_merchant_onboarding",
        }
    return rows


# ───────────────────────────── checkout ──────────────────────────────


class GCCCheckoutIn(BaseModel):
    tenant_id: str = Field(..., max_length=64)
    plan: Literal["starter", "pilot", "growth", "scale", "enterprise"] = "growth"
    amount_minor: int = Field(..., ge=100, le=100_000_000)
    order_id: str = Field(..., max_length=64)
    email: EmailStr
    success_url: str = Field(..., max_length=500)
    cancel_url: str = Field(..., max_length=500)


@router.post("/checkout/knet")
async def create_knet_checkout(payload: GCCCheckoutIn) -> dict[str, Any]:
    client = get_knet_client()
    if not client.is_configured:
        raise HTTPException(503, "knet_disabled")
    try:
        out = await client.create_checkout_session(
            amount_minor=payload.amount_minor,
            order_id=payload.order_id,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
            metadata={"tenant_id": payload.tenant_id, "plan": payload.plan},
        )
    except KNetNotConfigured:
        raise HTTPException(503, "knet_disabled") from None
    except Exception:
        log.exception("knet_checkout_failed", tenant_id=payload.tenant_id)
        raise HTTPException(502, "knet_upstream_error") from None
    return {"gateway": "knet", "currency": "KWD", "redirect_url": out.get("redirect_url"), "raw": out.get("raw")}


@router.post("/checkout/benefit")
async def create_benefit_checkout(payload: GCCCheckoutIn) -> dict[str, Any]:
    client = get_benefit_client()
    if not client.is_configured:
        raise HTTPException(503, "benefit_disabled")
    try:
        out = await client.create_checkout_session(
            amount_minor=payload.amount_minor,
            currency="BHD",
            order_id=payload.order_id,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
            metadata={"tenant_id": payload.tenant_id, "plan": payload.plan},
        )
    except BenefitNotConfigured:
        raise HTTPException(503, "benefit_disabled") from None
    except Exception:
        log.exception("benefit_checkout_failed", tenant_id=payload.tenant_id)
        raise HTTPException(502, "benefit_upstream_error") from None
    return {"gateway": "benefit", "currency": "BHD", "session": out}


@router.post("/checkout/magnati")
async def create_magnati_checkout(payload: GCCCheckoutIn) -> dict[str, Any]:
    client = get_magnati_client()
    if not client.is_configured:
        raise HTTPException(503, "magnati_disabled")
    try:
        out = await client.create_checkout_session(
            amount_minor=payload.amount_minor,
            currency="AED",
            order_id=payload.order_id,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
            metadata={"tenant_id": payload.tenant_id, "plan": payload.plan},
        )
    except MagnatiNotConfigured:
        raise HTTPException(503, "magnati_disabled") from None
    except Exception:
        log.exception("magnati_checkout_failed", tenant_id=payload.tenant_id)
        raise HTTPException(502, "magnati_upstream_error") from None
    return {"gateway": "magnati", "currency": "AED", "session": out}


# ──────────────────────────── webhooks ───────────────────────────────


@router.post("/webhooks/knet")
async def knet_webhook(
    request: Request, x_knet_signature: str = Header(default="")
) -> dict[str, Any]:
    body = await request.body()
    client = get_knet_client()
    if not client.verify_webhook(body, x_knet_signature):
        raise HTTPException(401, "invalid_signature")
    log.info("knet_webhook_verified", bytes=len(body))
    return {"ok": True, "gateway": "knet"}


@router.post("/webhooks/benefit")
async def benefit_webhook(
    request: Request, x_benefit_signature: str = Header(default="")
) -> dict[str, Any]:
    body = await request.body()
    client = get_benefit_client()
    if not client.verify_webhook(body, x_benefit_signature):
        raise HTTPException(401, "invalid_signature")
    log.info("benefit_webhook_verified", bytes=len(body))
    return {"ok": True, "gateway": "benefit"}


@router.post("/webhooks/magnati")
async def magnati_webhook(
    request: Request, x_magnati_signature: str = Header(default="")
) -> dict[str, Any]:
    body = await request.body()
    client = get_magnati_client()
    if not client.verify_webhook(body, x_magnati_signature):
        raise HTTPException(401, "invalid_signature")
    log.info("magnati_webhook_verified", bytes=len(body))
    return {"ok": True, "gateway": "magnati"}
