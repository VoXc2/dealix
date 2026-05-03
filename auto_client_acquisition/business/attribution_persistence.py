"""
Persist Moyasar webhook events into Subscription / Payment / FunnelEvent.

Pure mapping from a webhook payload → DB rows. Called by the existing
Moyasar webhook handler in api/routers/pricing.py after signature
verification + idempotency check.

Side effects: SQLAlchemy upserts only. No external I/O.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    FunnelEventRecord,
    PaymentRecord,
    SubscriptionRecord,
)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC for TIMESTAMP cols


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:24]}"


# Moyasar event_type → our payment status
_PAYMENT_STATUS_MAP = {
    "payment_paid": "paid",
    "payment.paid": "paid",
    "payment_succeeded": "paid",
    "payment_refunded": "refunded",
    "payment.refunded": "refunded",
    "payment_failed": "failed",
    "payment.failed": "failed",
}

# Moyasar event_type → our subscription status update
_SUBSCRIPTION_STATUS_MAP = {
    "subscription_canceled": "canceled",
    "subscription.canceled": "canceled",
    "subscription_paused": "paused",
    "subscription_resumed": "active",
    "subscription_renewed": "active",
}


def _amount_sar(payment_data: dict[str, Any]) -> float:
    """Moyasar reports amount in halalas (SAR × 100)."""
    raw = payment_data.get("amount") or 0
    try:
        return round(int(raw) / 100.0, 2)
    except (TypeError, ValueError):
        return 0.0


def _extract_metadata(payment_data: dict[str, Any]) -> dict[str, str]:
    """Pull customer/partner/subscription IDs out of Moyasar metadata or top-level."""
    meta = payment_data.get("metadata") or {}
    if isinstance(meta, str):
        # Some Moyasar variants stringify metadata.
        meta = {}
    return {
        "customer_id": str(meta.get("customer_id") or payment_data.get("customer_id") or ""),
        "partner_id": str(meta.get("partner_id") or payment_data.get("partner_id") or ""),
        "subscription_id": str(meta.get("subscription_id") or payment_data.get("subscription_id") or ""),
        "plan_id": str(meta.get("plan") or meta.get("plan_id") or payment_data.get("plan") or ""),
    }


# ── Public entry point ────────────────────────────────────────────


async def persist_moyasar_event(
    session: AsyncSession,
    body: dict[str, Any],
) -> dict[str, Any]:
    """Map a Moyasar webhook body to DB writes.

    Returns a summary dict (used for logging + tests):
        {
          "ok": bool,
          "wrote": ["payment", "subscription", "funnel_event"],
          "payment_id": str|None,
          "subscription_id": str|None,
          "funnel_event_id": str|None,
          "stage": str|None,
        }
    """
    summary: dict[str, Any] = {
        "ok": True,
        "wrote": [],
        "payment_id": None,
        "subscription_id": None,
        "funnel_event_id": None,
        "stage": None,
    }
    event_id = str(body.get("id") or "")
    event_type = str(body.get("type") or "")
    data = body.get("data") or {}

    payment_status = _PAYMENT_STATUS_MAP.get(event_type)
    sub_status = _SUBSCRIPTION_STATUS_MAP.get(event_type)

    if payment_status:
        await _record_payment(session, data, event_id, payment_status, summary)
    if sub_status:
        await _update_subscription_status(session, data, sub_status, summary)
    if payment_status == "paid":
        await _maybe_promote_funnel(session, data, summary)
    return summary


async def _record_payment(
    session: AsyncSession,
    data: dict[str, Any],
    event_id: str,
    status: str,
    summary: dict[str, Any],
) -> None:
    moyasar_payment_id = str(data.get("id") or "")
    if not moyasar_payment_id:
        # No payment id — nothing to persist
        return

    # Idempotency at the row level: don't double-insert the same Moyasar payment.
    existing = await session.execute(
        select(PaymentRecord).where(
            PaymentRecord.moyasar_payment_id == moyasar_payment_id,
            PaymentRecord.moyasar_event_id == event_id,
        )
    )
    if existing.scalar_one_or_none():
        return

    refs = _extract_metadata(data)
    row = PaymentRecord(
        id=_new_id("pay"),
        subscription_id=refs["subscription_id"] or None,
        customer_id=refs["customer_id"] or None,
        partner_id=refs["partner_id"] or None,
        amount_sar=_amount_sar(data),
        currency=str(data.get("currency") or "SAR"),
        status=status,
        moyasar_payment_id=moyasar_payment_id,
        moyasar_event_id=event_id,
        paid_at=_now(),
        invoice_url=str(data.get("invoice_url") or "") or None,
        meta_json={"raw_type": data.get("type") or "", "plan": refs["plan_id"]},
    )
    session.add(row)
    summary["payment_id"] = row.id
    summary["wrote"].append("payment")


async def _update_subscription_status(
    session: AsyncSession,
    data: dict[str, Any],
    new_status: str,
    summary: dict[str, Any],
) -> None:
    moyasar_sub_id = str(data.get("id") or data.get("subscription_id") or "")
    if not moyasar_sub_id:
        return
    existing = await session.execute(
        select(SubscriptionRecord).where(SubscriptionRecord.moyasar_subscription_id == moyasar_sub_id)
    )
    sub = existing.scalar_one_or_none()
    if sub is None:
        # Create a stub if we got a status update before the first payment.
        refs = _extract_metadata(data)
        sub = SubscriptionRecord(
            id=_new_id("sub"),
            customer_id=refs["customer_id"] or "unknown",
            partner_id=refs["partner_id"] or None,
            plan_id=refs["plan_id"] or "unknown",
            status=new_status,
            moyasar_subscription_id=moyasar_sub_id,
        )
        session.add(sub)
    else:
        sub.status = new_status
        if new_status == "canceled":
            sub.canceled_at = _now()
            sub.cancel_reason = str(data.get("cancel_reason") or "")
    summary["subscription_id"] = sub.id
    summary["wrote"].append("subscription")


async def _maybe_promote_funnel(
    session: AsyncSession,
    data: dict[str, Any],
    summary: dict[str, Any],
) -> None:
    """First successful payment → 'paying' event. Recurring → 'renewed'."""
    refs = _extract_metadata(data)
    if not refs["customer_id"]:
        return

    # Count prior payments for this customer to distinguish first vs renewal.
    prior = await session.execute(
        select(PaymentRecord).where(
            PaymentRecord.customer_id == refs["customer_id"],
            PaymentRecord.status == "paid",
        )
    )
    prior_count = len(prior.scalars().all())
    stage = "paying" if prior_count <= 1 else "renewed"

    event = FunnelEventRecord(
        id=_new_id("fnl"),
        lead_id=None,
        customer_id=refs["customer_id"],
        partner_id=refs["partner_id"] or None,
        stage=stage,
        reason=f"moyasar_payment_paid (#{prior_count})",
        actor="moyasar_webhook",
    )
    session.add(event)
    summary["funnel_event_id"] = event.id
    summary["stage"] = stage
    summary["wrote"].append("funnel_event")
