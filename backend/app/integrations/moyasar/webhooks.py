"""
Moyasar Webhooks Handler — Payment & Subscription events.
معالج Webhooks ميسر — أحداث المدفوعات والاشتراكات.

Docs: https://docs.moyasar.com/docs/webhooks

Key events handled:
- payment.paid          → Activate subscription / deliver service
- payment.failed        → Notify customer, retry billing
- subscription.active   → Mark tenant as active
- subscription.past_due → Grace period + dunning
- subscription.canceled → Deactivate tenant
- subscription.renewed  → Log renewal, send receipt
- refund.created        → Log + notify
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def verify_moyasar_signature(body: bytes, signature: str) -> bool:
    """
    Verify Moyasar webhook HMAC SHA-256 signature.
    التحقق من توقيع Moyasar webhook باستخدام HMAC SHA-256.

    Moyasar sends the signature in the X-Moyasar-Signature header.
    The signature is computed as HMAC-SHA256(body, webhook_secret).

    Docs: https://docs.moyasar.com/docs/webhooks#verifying-webhooks

    Args:
        body: Raw request body bytes
        signature: Value of X-Moyasar-Signature header

    Returns:
        True if signature matches, False otherwise
    """
    secret = os.getenv("MOYASAR_WEBHOOK_SECRET", "")
    if not secret:
        logger.warning("MOYASAR_WEBHOOK_SECRET not configured — skipping verification (DEV ONLY)")
        return True

    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def handle_moyasar_webhook(event_type: str, payload: dict, db) -> dict:
    """
    Route Moyasar webhook event to the appropriate handler.
    توجيه حدث Moyasar webhook إلى المعالج المناسب.

    Args:
        event_type: Event type from payload (e.g. "payment.paid")
        payload: Full webhook payload dict
        db: Database session

    Returns:
        dict with handled, action, and relevant details
    """
    handlers = {
        "payment.paid": _handle_payment_paid,
        "payment.failed": _handle_payment_failed,
        "payment.authorized": _handle_payment_authorized,
        "subscription.active": _handle_subscription_active,
        "subscription.past_due": _handle_subscription_past_due,
        "subscription.canceled": _handle_subscription_canceled,
        "subscription.renewed": _handle_subscription_renewed,
        "refund.created": _handle_refund_created,
    }

    handler = handlers.get(event_type)
    if not handler:
        logger.info(f"Unhandled Moyasar event: {event_type}")
        return {"handled": False, "action": "ignored", "event": event_type}

    return await handler(payload, db)


# ── Payment Handlers ──────────────────────────────────────────────────────────


async def _handle_payment_paid(payload: dict, db) -> dict:
    """
    Payment succeeded → activate feature or provision service.
    نجاح الدفع → تفعيل الخدمة أو الاشتراك.
    """
    payment = payload.get("data", payload)
    payment_id = payment.get("id")
    amount_halalas = payment.get("amount", 0)
    amount_sar = amount_halalas / 100
    metadata = payment.get("metadata", {})
    tenant_id = metadata.get("tenant_id")
    plan = metadata.get("plan")

    logger.info(f"✅ Moyasar payment paid: {payment_id} — SAR {amount_sar} for tenant {tenant_id}")

    # TODO: Activate tenant plan in DB
    # await tenant_repo.activate_plan(tenant_id, plan, payment_id)
    # TODO: Send payment receipt via Unifonic WhatsApp

    return {
        "handled": True,
        "action": "payment_paid",
        "payment_id": payment_id,
        "amount_sar": amount_sar,
        "tenant_id": tenant_id,
        "plan": plan,
    }


async def _handle_payment_failed(payload: dict, db) -> dict:
    """
    Payment failed → notify customer, schedule retry.
    فشل الدفع → إشعار العميل وجدولة إعادة المحاولة.
    """
    payment = payload.get("data", payload)
    payment_id = payment.get("id")
    metadata = payment.get("metadata", {})
    tenant_id = metadata.get("tenant_id")
    failure_msg = payment.get("message") or "Payment declined"

    logger.warning(f"❌ Moyasar payment failed: {payment_id} — {failure_msg} for tenant {tenant_id}")

    # TODO: Send payment failure notification via Unifonic WhatsApp/SMS
    # TODO: Schedule dunning retry (3 days grace period)

    return {
        "handled": True,
        "action": "payment_failed",
        "payment_id": payment_id,
        "tenant_id": tenant_id,
        "failure_reason": failure_msg,
    }


async def _handle_payment_authorized(payload: dict, db) -> dict:
    """
    Payment authorized (not yet captured).
    تم التفويض (لم يُسحب بعد).
    """
    payment = payload.get("data", payload)
    return {
        "handled": True,
        "action": "payment_authorized",
        "payment_id": payment.get("id"),
    }


# ── Subscription Handlers ─────────────────────────────────────────────────────


async def _handle_subscription_active(payload: dict, db) -> dict:
    """
    Subscription became active → provision tenant fully.
    الاشتراك أصبح نشطاً → تفعيل التاجر بالكامل.
    """
    sub = payload.get("data", payload)
    sub_id = sub.get("id")
    metadata = sub.get("metadata", {})
    tenant_id = metadata.get("tenant_id")
    plan = metadata.get("plan", "starter")

    logger.info(f"✅ Subscription active: {sub_id} — plan={plan} tenant={tenant_id}")

    # TODO: Set tenant.subscription_status = "active" in DB
    # TODO: Set tenant.plan = plan
    # TODO: Send welcome WhatsApp message

    return {
        "handled": True,
        "action": "subscription_activated",
        "subscription_id": sub_id,
        "tenant_id": tenant_id,
        "plan": plan,
    }


async def _handle_subscription_past_due(payload: dict, db) -> dict:
    """
    Subscription past due (payment failed) → grace period + dunning.
    الاشتراك متأخر → فترة سماح + إشعارات التحصيل.
    """
    sub = payload.get("data", payload)
    sub_id = sub.get("id")
    metadata = sub.get("metadata", {})
    tenant_id = metadata.get("tenant_id")

    logger.warning(f"⚠️  Subscription past due: {sub_id} for tenant {tenant_id}")

    # TODO: Start 7-day grace period
    # TODO: Send dunning WhatsApp (Day 1, Day 3, Day 7)
    # TODO: Restrict features after grace period expires

    return {
        "handled": True,
        "action": "subscription_past_due",
        "subscription_id": sub_id,
        "tenant_id": tenant_id,
        "grace_period_days": 7,
    }


async def _handle_subscription_canceled(payload: dict, db) -> dict:
    """
    Subscription canceled → deactivate tenant.
    إلغاء الاشتراك → تعطيل التاجر.
    """
    sub = payload.get("data", payload)
    sub_id = sub.get("id")
    metadata = sub.get("metadata", {})
    tenant_id = metadata.get("tenant_id")

    logger.warning(f"🚫 Subscription canceled: {sub_id} for tenant {tenant_id}")

    # TODO: Set tenant.subscription_status = "canceled"
    # TODO: Preserve data for 30 days per KSA regulations (PDPL)
    # TODO: Send offboarding WhatsApp with data export link

    return {
        "handled": True,
        "action": "subscription_canceled",
        "subscription_id": sub_id,
        "tenant_id": tenant_id,
    }


async def _handle_subscription_renewed(payload: dict, db) -> dict:
    """
    Subscription renewed → log and send receipt.
    تجديد الاشتراك → التسجيل وإرسال الإيصال.
    """
    sub = payload.get("data", payload)
    sub_id = sub.get("id")
    metadata = sub.get("metadata", {})
    tenant_id = metadata.get("tenant_id")
    amount_sar = (sub.get("amount", 0)) / 100

    logger.info(f"🔄 Subscription renewed: {sub_id} — SAR {amount_sar} for tenant {tenant_id}")

    # TODO: Log renewal event in billing_events table
    # TODO: Send receipt via Unifonic WhatsApp

    return {
        "handled": True,
        "action": "subscription_renewed",
        "subscription_id": sub_id,
        "tenant_id": tenant_id,
        "amount_sar": amount_sar,
    }


async def _handle_refund_created(payload: dict, db) -> dict:
    """
    Refund created → log and notify.
    إنشاء استرداد → التسجيل والإشعار.
    """
    refund = payload.get("data", payload)
    return {
        "handled": True,
        "action": "refund_logged",
        "refund_id": refund.get("id"),
        "amount_sar": (refund.get("amount", 0)) / 100,
    }
