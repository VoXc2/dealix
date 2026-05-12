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
    event_type = evt.get("type", "")
    obj = ((evt.get("data") or {}).get("object") or {})
    tenant_id = ((obj.get("metadata") or {}).get("tenant_id") or "system")

    # Persist invoice + fan out — only when the event is terminal.
    try:
        import secrets as _secrets
        from sqlalchemy import select

        from db.models import InvoiceRecord
        from db.session import async_session_factory

        terminal = event_type in {
            "payment_intent.succeeded",
            "checkout.session.completed",
            "payment_intent.payment_failed",
            "charge.refunded",
        }
        if terminal:
            status_map = {
                "payment_intent.succeeded": "paid",
                "checkout.session.completed": "paid",
                "payment_intent.payment_failed": "failed",
                "charge.refunded": "refunded",
            }
            external_id = str(obj.get("id") or evt.get("id") or "")
            amount_minor = int(obj.get("amount_total") or obj.get("amount") or 0)
            currency = (obj.get("currency") or "usd").upper()
            async with async_session_factory()() as session:
                existing = (
                    await session.execute(
                        select(InvoiceRecord).where(
                            InvoiceRecord.provider == "stripe",
                            InvoiceRecord.external_id == external_id,
                        )
                    )
                ).scalar_one_or_none()
                if existing is None and external_id:
                    session.add(
                        InvoiceRecord(
                            id="inv_" + _secrets.token_hex(12),
                            tenant_id=tenant_id,
                            provider="stripe",
                            external_id=external_id,
                            status=status_map.get(event_type, "pending"),
                            amount_minor=amount_minor,
                            currency=currency,
                            meta_json={"event_type": event_type},
                        )
                    )
                    await session.commit()

        if event_type in {"payment_intent.succeeded", "checkout.session.completed"}:
            from dealix.billing.lago_client import get_lago_client

            await get_lago_client().meter(
                metric_code="invoice_paid",
                external_customer_id=tenant_id,
                value=1,
                properties={
                    "provider": "stripe",
                    "amount_minor": int(obj.get("amount_total") or 0),
                    "currency": obj.get("currency") or "usd",
                },
            )

            from dealix.marketing.loops_client import get_loops_client

            email = (
                ((obj.get("customer_details") or {}).get("email"))
                or (obj.get("receipt_email"))
                or ""
            )
            if email:
                await get_loops_client().event(
                    event_name="payment_succeeded",
                    email=email,
                    properties={
                        "tenant_id": tenant_id,
                        "amount_minor": int(obj.get("amount_total") or 0),
                        "currency": obj.get("currency") or "usd",
                        "provider": "stripe",
                    },
                )

            from dealix.integrations.knock_client import get_knock_client

            await get_knock_client().notify(
                workflow="payment_succeeded",
                recipients=[{"id": tenant_id, "email": email or "ops@ai-company.sa"}],
                data={"tenant_id": tenant_id, "external_id": (obj.get("id") or "")},
                tenant_id=tenant_id,
            )
    except Exception:
        log.exception("stripe_webhook_fanout_failed", event_type=event_type)

    # Audit the event boundary regardless of fan-out success.
    try:
        from api.security.audit_writer import audit
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            await audit(
                session,
                action=f"stripe.webhook.{event_type or 'unknown'}",
                entity_type="webhook",
                entity_id=str(evt.get("id") or ""),
                tenant_id=tenant_id,
                diff={"livemode": evt.get("livemode")},
            )
    except Exception:
        log.exception("stripe_webhook_audit_failed")

    log.info(
        "stripe_webhook_received",
        event_type=event_type,
        event_id=evt.get("id"),
        tenant_id=tenant_id,
    )
    return {"ok": True}
