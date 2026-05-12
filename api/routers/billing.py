"""
Billing router — Stripe Checkout + webhook + provider-agnostic invoice list.

This sits beside the existing Moyasar surface in `api/routers/pricing.py`.
Stripe is the international (USD/EUR/AED) fallback; Moyasar stays the
default for SAR. The router degrades gracefully when Stripe is unconfigured.

Endpoints:
    POST /api/v1/billing/checkout/stripe   — create a hosted Checkout session
    POST /api/v1/billing/webhooks/stripe   — Stripe webhook signature-verified
    GET  /api/v1/billing/health            — config visibility (no secrets)
"""

from __future__ import annotations

import os
from typing import Any, Literal

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from core.logging import get_logger
from dealix.payments.stripe_client import (
    StripeNotConfigured,
    get_stripe_client,
)

router = APIRouter(prefix="/api/v1/billing", tags=["billing"])
log = get_logger(__name__)


class StripeCheckoutIn(BaseModel):
    tenant_id: str = Field(..., max_length=64)
    plan: Literal["starter", "growth", "scale"] = "starter"
    amount_cents: int = Field(..., ge=100, le=10_000_000)
    currency: Literal["usd", "eur", "aed", "sar"] = "usd"
    email: EmailStr
    success_url: str = Field(..., max_length=500)
    cancel_url: str = Field(..., max_length=500)
    mode: Literal["payment", "subscription"] = "payment"
    price_id: str | None = Field(default=None, max_length=120)


@router.get("/health")
async def billing_health() -> dict[str, Any]:
    """Surface which gateway is configured. No secret values leak."""
    # Replace ad-hoc env reads with the PostHog-backed wrapper so per-
    # tenant overrides are possible later. flag_or_env keeps the env
    # fallback path so behaviour is identical today.
    from core.feature_flags import flag_or_env

    stripe_via_flag = (
        flag_or_env("stripe", "STRIPE_ENABLED")
        or get_stripe_client().is_configured
    )
    return {
        "moyasar_configured": bool(os.getenv("MOYASAR_SECRET_KEY", "").strip()),
        "stripe_configured": stripe_via_flag,
        "primary": "moyasar",
        "international_fallback": "stripe",
    }


@router.post("/checkout/stripe")
async def create_stripe_checkout(payload: StripeCheckoutIn) -> dict[str, Any]:
    """Create a Stripe Checkout Session; returns the hosted URL.

    Returns 503 with `stripe_disabled` if the env key is missing — the
    caller (frontend) is expected to gracefully degrade to Moyasar in that
    case.
    """
    client = get_stripe_client()
    if not client.is_configured:
        raise HTTPException(status_code=503, detail="stripe_disabled")
    try:
        meta: dict[str, str] = {
            "tenant_id": payload.tenant_id,
            "plan": payload.plan,
            "email": payload.email,
        }
        if payload.price_id:
            meta["price_id"] = payload.price_id
        session = await client.create_checkout_session(
            amount_cents=payload.amount_cents,
            currency=payload.currency,
            product_name=f"Dealix {payload.plan}",
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
            metadata=meta,
            mode=payload.mode,
        )
    except StripeNotConfigured:
        raise HTTPException(status_code=503, detail="stripe_disabled") from None
    except Exception:
        log.exception("stripe_checkout_failed", tenant_id=payload.tenant_id)
        raise HTTPException(status_code=502, detail="stripe_upstream_error") from None

    log.info(
        "stripe_checkout_created",
        tenant_id=payload.tenant_id,
        plan=payload.plan,
        session_id=session.get("id"),
    )
    return {
        "id": session.get("id"),
        "url": session.get("url"),
        "tenant_id": payload.tenant_id,
        "plan": payload.plan,
        "currency": payload.currency,
    }


@router.post("/webhooks/stripe")
async def stripe_webhook(
    req: Request,
    stripe_signature: str = Header(default="", alias="Stripe-Signature"),
) -> dict[str, Any]:
    """Verify + acknowledge Stripe webhooks.

    Only the signature gate runs here; downstream side-effects (invoice
    persistence, tenant activation) will land in `dealix/payments/stripe_*`
    handlers as the integration matures. For now we audit and 200.
    """
    client = get_stripe_client()
    body = await req.body()
    if not client.verify_webhook(body, stripe_signature):
        log.warning("stripe_webhook_bad_signature")
        raise HTTPException(status_code=400, detail="invalid_signature")
    try:
        evt = await req.json()
    except Exception:
        evt = {}
    # Audit the event boundary (no PII; just type + id).
    try:
        from api.security.audit_writer import audit
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            await audit(
                session,
                action=f"stripe.webhook.{evt.get('type', 'unknown')}",
                entity_type="webhook",
                entity_id=str(evt.get("id") or ""),
                tenant_id="system",
                diff={"livemode": evt.get("livemode")},
            )
    except Exception:
        log.exception("stripe_webhook_audit_failed")

    log.info(
        "stripe_webhook_received",
        event_type=evt.get("type"),
        event_id=evt.get("id"),
    )
    return {"ok": True}
