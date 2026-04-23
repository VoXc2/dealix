"""
Pricing + Moyasar checkout endpoints.

Usage:
  POST /api/v1/checkout   body: {"plan":"starter","email":"x@y.com","lead_id":"optional"}
    → returns {"invoice_id":"...", "payment_url":"https://..."}
  POST /api/v1/webhooks/moyasar  — Moyasar payment webhook (status updates)

Plans are intentionally NOT published on the public landing page; the checkout
endpoint validates against `ALLOWED_PLANS` to prevent tampering.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from dealix.analytics import FUNNEL_EVENTS, capture_event
from dealix.payments import MoyasarClient, verify_webhook
from dealix.reliability.dlq import DLQ, WEBHOOKS_DLQ
from dealix.reliability.idempotency import IdempotencyStore

log = logging.getLogger(__name__)

router = APIRouter(tags=["pricing"])

# Prices in halalas (SAR x 100). Hidden from landing — only exposed when a lead qualifies.
PLANS: dict[str, dict[str, Any]] = {
    "starter": {"name": "Starter", "amount_halalas": 99900, "monthly": True},  # 999 SAR/mo
    "growth": {"name": "Growth", "amount_halalas": 299900, "monthly": True},  # 2,999 SAR/mo
    "scale": {"name": "Scale", "amount_halalas": 799900, "monthly": True},  # 7,999 SAR/mo
    "pilot_1sar": {
        "name": "Pilot (1 SAR)",
        "amount_halalas": 100,
        "monthly": False,
    },  # E2E test transaction
}


@router.get("/api/v1/pricing/plans")
async def list_plans() -> dict[str, Any]:
    """List available plans. Not linked from landing — required for approval-gated quotes."""
    return {
        "currency": "SAR",
        "plans": {
            k: {"name": v["name"], "amount_sar": v["amount_halalas"] / 100, "monthly": v["monthly"]}
            for k, v in PLANS.items()
            if k != "pilot_1sar"  # hide pilot from public listing
        },
    }


@router.post("/api/v1/checkout")
async def create_checkout(req: Request) -> dict[str, Any]:
    body = await req.json()
    plan = str(body.get("plan") or "").lower()
    email = str(body.get("email") or "").strip()
    lead_id = str(body.get("lead_id") or "")

    if plan not in PLANS:
        raise HTTPException(status_code=400, detail=f"unknown_plan: {plan}")
    if "@" not in email:
        raise HTTPException(status_code=400, detail="invalid_email")

    plan_info = PLANS[plan]
    callback_base = os.getenv("APP_URL", "https://dealix.me")
    callback_url = f"{callback_base}/checkout/return"

    client = MoyasarClient()
    try:
        invoice = await client.create_invoice(
            amount_halalas=int(plan_info["amount_halalas"]),
            currency="SAR",
            description=f"Dealix — {plan_info['name']}",
            callback_url=callback_url,
            metadata={
                "plan": plan,
                "email": email,
                "lead_id": lead_id,
                "source": "dealix.checkout",
            },
        )
    except Exception as e:
        log.exception("moyasar_invoice_failed plan=%s email=%s", plan, email)
        raise HTTPException(
            status_code=502,
            detail=f"payment_provider_error: {str(e)[:200]}",
        ) from e

    # Fire CHECKOUT_STARTED funnel event (fire-and-forget).
    await capture_event(
        FUNNEL_EVENTS.CHECKOUT_STARTED,
        distinct_id=str(lead_id or email),
        properties={
            "plan": plan,
            "email": email,
            "lead_id": lead_id,
            "amount_halalas": plan_info["amount_halalas"],
            "invoice_id": invoice.get("id"),
            "source": "dealix.checkout",
        },
    )

    return {
        "invoice_id": invoice.get("id"),
        "status": invoice.get("status"),
        "amount_sar": plan_info["amount_halalas"] / 100,
        "payment_url": invoice.get("url"),
        "plan": plan,
    }


@router.post("/api/v1/webhooks/moyasar")
async def moyasar_webhook(req: Request) -> dict[str, Any]:
    """
    Moyasar payment webhook. Verifies secret_token in body and dedupes by event id.
    Failed processing → DLQ(webhooks) for operator replay.
    """
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    if not verify_webhook(body):
        log.warning("moyasar_webhook_bad_signature")
        raise HTTPException(status_code=401, detail="bad_signature")

    event_id = str(body.get("id") or "")
    event_type = str(body.get("type") or "")
    idem = IdempotencyStore(prefix="idem:moyasar:")
    if event_id and not idem.claim(event_id, ttl_seconds=7 * 86400):
        log.info("moyasar_webhook_duplicate id=%s", event_id)
        return {"status": "duplicate", "id": event_id}

    try:
        data = body.get("data") or {}
        payment = data if data.get("object") in (None, "payment", "invoice") else {}
        status = payment.get("status") or body.get("type")
        log.info(
            "moyasar_webhook ok id=%s type=%s status=%s amount=%s",
            event_id,
            event_type,
            status,
            payment.get("amount"),
        )

        # Fire PostHog funnel events — closes O3 gate when POSTHOG_API_KEY is set.
        # Fire-and-forget; failures never block the 200 response to Moyasar.
        metadata = payment.get("metadata") or {}
        distinct_id = str(
            metadata.get("lead_id")
            or metadata.get("email")
            or payment.get("id")
            or event_id
            or "unknown"
        )
        posthog_props = {
            "payment_id": payment.get("id"),
            "invoice_id": payment.get("invoice_id"),
            "amount_halalas": payment.get("amount"),
            "currency": payment.get("currency") or "SAR",
            "plan": metadata.get("plan"),
            "email": metadata.get("email"),
            "status": status,
            "event_type": event_type,
            "source": "moyasar.webhook",
        }
        if event_type == "payment_paid" or status == "paid":
            await capture_event(FUNNEL_EVENTS.PAYMENT_SUCCEEDED, distinct_id, posthog_props)
        elif event_type == "payment_failed" or status == "failed":
            await capture_event(FUNNEL_EVENTS.PAYMENT_FAILED, distinct_id, posthog_props)

        # TODO: sync to HubSpot via ConnectorFacade in D+2 E2E test
        return {"status": "ok", "event_id": event_id, "event_type": event_type}
    except Exception as e:
        log.exception("moyasar_webhook_processing_failed id=%s", event_id)
        DLQ(WEBHOOKS_DLQ).push(
            source="moyasar.webhook",
            payload=body,
            error=str(e)[:500],
            metadata={"event_id": event_id, "event_type": event_type},
        )
        # Still 200 so Moyasar doesn't retry forever; we own replay via DLQ.
        return {"status": "dlq", "event_id": event_id}
