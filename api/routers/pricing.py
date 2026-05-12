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

import hashlib
import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from dealix.payments import MoyasarClient, verify_webhook
from dealix.reliability.dlq import DLQ, WEBHOOKS_DLQ
from dealix.reliability.idempotency import IdempotencyStore

log = logging.getLogger(__name__)

router = APIRouter(tags=["pricing"])


def _fingerprint(value: str) -> str:
    if not value:
        return ""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


async def _persist_payment_event(
    *,
    event_id: str,
    event_type: str,
    payment: dict[str, Any],
    raw_event: dict[str, Any],
) -> None:
    """
    Upsert a row in `payments` keyed by (provider, provider_payment_id).
    Safe to call before migration 005 runs — it logs and returns on any error.
    """
    try:
        from sqlalchemy import select
        from db.models import PaymentRecord
        from db.session import async_session_factory
    except Exception as exc:  # noqa: BLE001
        log.debug("payments_persist_skipped reason=imports error=%s", exc)
        return

    provider_payment_id = str(payment.get("id") or event_id or "").strip()
    if not provider_payment_id:
        return
    amount = int(payment.get("amount") or 0)
    currency = str(payment.get("currency") or "SAR")[:8]
    status = str(payment.get("status") or event_type or "pending")[:32]
    email = (payment.get("metadata") or {}).get("email") or payment.get("source", {}).get("email")
    plan = (payment.get("metadata") or {}).get("plan")
    customer_handle = (payment.get("metadata") or {}).get("customer_handle")

    try:
        async with async_session_factory()() as session:
            stmt = select(PaymentRecord).where(
                PaymentRecord.provider == "moyasar",
                PaymentRecord.provider_payment_id == provider_payment_id,
            )
            existing = (await session.execute(stmt)).scalar_one_or_none()
            if existing is None:
                row = PaymentRecord(
                    id=f"pay_{_fingerprint(provider_payment_id)}_{provider_payment_id[:24]}",
                    provider="moyasar",
                    provider_payment_id=provider_payment_id,
                    plan=plan,
                    amount_halalas=amount,
                    currency=currency,
                    status=status,
                    email=email,
                    customer_handle=customer_handle,
                    last_event_id=event_id or None,
                    last_event_type=event_type or None,
                    raw_event=raw_event,
                )
                session.add(row)
            else:
                existing.status = status
                existing.amount_halalas = amount or existing.amount_halalas
                existing.currency = currency
                existing.last_event_id = event_id or existing.last_event_id
                existing.last_event_type = event_type or existing.last_event_type
                existing.raw_event = raw_event
                if email and not existing.email:
                    existing.email = email
                if plan and not existing.plan:
                    existing.plan = plan
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("payments_persist_failed provider_payment_id=%s error=%s",
                    provider_payment_id, exc)


# Prices in halalas (SAR x 100). Hidden from landing — only exposed when a lead qualifies.
# Plan kinds:
#   "subscription" — recurring monthly Moyasar invoice
#   "one_off"      — single charge (e.g. pilot)
#   "metered"      — billed per usage event (LaaS R3 model)
PLANS: dict[str, dict[str, Any]] = {
    "starter": {
        "name": "Starter",
        "amount_halalas": 99900,
        "monthly": True,
        "kind": "subscription",
    },  # 999 SAR/mo
    "growth": {
        "name": "Growth",
        "amount_halalas": 299900,
        "monthly": True,
        "kind": "subscription",
    },  # 2,999 SAR/mo
    "scale": {
        "name": "Scale",
        "amount_halalas": 799900,
        "monthly": True,
        "kind": "subscription",
    },  # 7,999 SAR/mo
    "pilot_managed": {
        "name": "Managed Pilot (7 days)",
        "amount_halalas": 49900,
        "monthly": False,
        "kind": "one_off",
    },  # 499 SAR one-off — founder-led pilot per v4 §3 R1
    "laas_per_reply": {
        "name": "Lead-as-a-Service · Per Reply",
        "amount_halalas": 2500,
        "monthly": False,
        "kind": "metered",
        "unit": "arabic_replied_lead",
    },  # 25 SAR per Arabic-replied lead
    "laas_per_demo": {
        "name": "Lead-as-a-Service · Per Demo",
        "amount_halalas": 15000,
        "monthly": False,
        "kind": "metered",
        "unit": "booked_demo",
    },  # 150 SAR per booked demo
    "pilot_1sar": {
        "name": "Pilot (1 SAR)",
        "amount_halalas": 100,
        "monthly": False,
        "kind": "one_off",
    },  # E2E test transaction
}


@router.get("/api/v1/pricing/plans")
async def list_plans() -> dict[str, Any]:
    """List available plans. Not linked from landing — required for approval-gated quotes.

    Hides `pilot_1sar` (E2E test plan only). Surfaces all other plans including
    one-off pilot, metered LaaS plans, and recurring subscriptions.
    """
    hidden = {"pilot_1sar"}
    plans = {}
    for k, v in PLANS.items():
        if k in hidden:
            continue
        entry = {
            "name": v["name"],
            "amount_sar": v["amount_halalas"] / 100,
            "monthly": v["monthly"],
            "kind": v.get("kind", "subscription"),
        }
        if v.get("unit"):
            entry["unit"] = v["unit"]
        plans[k] = entry
    return {"currency": "SAR", "plans": plans}


@router.post("/api/v1/pricing/usage")
async def record_usage(req: Request) -> dict[str, Any]:
    """Record a metered-billing usage event for LaaS R3 plans.

    Body:
      {
        "plan": "laas_per_reply" | "laas_per_demo",
        "customer_handle": "<tenant handle>",
        "event_id": "<idempotency key, e.g. lead_msg_id>",
        "lead_id": "<optional>",
        "metadata": {...}
      }

    This endpoint records the event for downstream invoicing. For the
    first 5 customers, invoicing is processed manually from the recorded
    events (see docs/ops/LAAS_DELIVERY_RUNBOOK.md). Automation moves the
    accumulation step to a scheduled job once volume justifies it.

    Idempotency: the same event_id never produces a duplicate charge.
    """
    body = await req.json()
    plan = str(body.get("plan") or "").lower()
    customer_handle = str(body.get("customer_handle") or "").strip()
    event_id = str(body.get("event_id") or "").strip()

    if plan not in PLANS or PLANS[plan].get("kind") != "metered":
        raise HTTPException(status_code=400, detail="plan must be a metered LaaS plan")
    if not customer_handle:
        raise HTTPException(status_code=400, detail="customer_handle required")
    if not event_id:
        raise HTTPException(status_code=400, detail="event_id required (idempotency key)")

    plan_info = PLANS[plan]
    amount_halalas = int(plan_info["amount_halalas"])
    unit = plan_info.get("unit", "event")
    metadata = dict(body.get("metadata") or {})
    metadata.update({"customer_handle": customer_handle, "plan": plan, "unit": unit})

    # Idempotent record: keyed by event_id so retries don't double-charge.
    # `claim` returns True on first-write only — second attempt returns False.
    idem = IdempotencyStore(prefix="laas:")
    record_key = f"{plan}:{customer_handle}:{event_id}"
    if not idem.claim(record_key, ttl_seconds=30 * 86400):  # 30-day window
        return {
            "status": "duplicate",
            "event_id": event_id,
            "plan": plan,
            "amount_halalas": amount_halalas,
            "amount_sar": amount_halalas / 100,
        }

    log.info(
        "laas_usage_recorded plan=%s handle=%s event=%s amount_halalas=%d",
        plan, customer_handle, event_id, amount_halalas,
    )

    return {
        "status": "recorded",
        "event_id": event_id,
        "plan": plan,
        "amount_halalas": amount_halalas,
        "amount_sar": amount_halalas / 100,
        "unit": unit,
        "customer_handle": customer_handle,
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
    except Exception as exc:
        log.exception(
            "moyasar_invoice_failed plan=%s email_fp=%s",
            plan,
            _fingerprint(email),
        )
        raise HTTPException(
            status_code=502,
            detail="payment_provider_error",
        ) from exc

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
    except Exception as exc:
        raise HTTPException(status_code=400, detail="invalid_json") from exc

    if not verify_webhook(body):
        log.warning("moyasar_webhook_bad_signature")
        raise HTTPException(status_code=401, detail="bad_signature")

    event_id = str(body.get("id") or "")
    event_type = str(body.get("type") or "")
    event_fp = _fingerprint(event_id)
    idem = IdempotencyStore(prefix="idem:moyasar:")
    if event_id and not idem.claim(event_id, ttl_seconds=7 * 86400):
        log.info("moyasar_webhook_duplicate event_fp=%s", event_fp)
        return {"status": "duplicate", "id": event_id}

    try:
        data = body.get("data") or {}
        payment = data if data.get("object") in (None, "payment", "invoice") else {}
        status = payment.get("status") or body.get("type")
        log.info(
            "moyasar_webhook_processed event_fp=%s type=%s status=%s amount=%s",
            event_fp,
            event_type,
            status,
            payment.get("amount"),
        )
        # Persist for reconciliation; failure here is non-fatal so a missing
        # migration in production doesn't break payment processing.
        await _persist_payment_event(
            event_id=event_id,
            event_type=event_type,
            payment=payment,
            raw_event=body,
        )
        # TODO: sync to HubSpot via ConnectorFacade in D+2 E2E test
        return {"status": "ok", "event_id": event_id, "event_type": event_type}
    except Exception as exc:
        log.exception("moyasar_webhook_processing_failed event_fp=%s", event_fp)
        DLQ(WEBHOOKS_DLQ).push(
            source="moyasar.webhook",
            payload=body,
            error=str(exc)[:500],
            metadata={"event_id": event_id, "event_type": event_type},
        )
        # Still 200 so Moyasar doesn't retry forever; we own replay via DLQ.
        return {"status": "dlq", "event_id": event_id}
