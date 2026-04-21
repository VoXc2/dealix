"""
Zid Webhooks Handler.
معالج Webhooks من منصة زد.

Docs: https://docs.zid.sa/reference/webhooks

Key events handled:
- order.created              → Trigger order confirmation WhatsApp
- order.status.updated       → Order status update message
- order.abandoned_cart       → Cart recovery flow
- product.created            → Inventory sync
- product.updated            → Inventory sync
- app.uninstalled            → Deactivate + stop billing
- refund.created             → Refund notification
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os

logger = logging.getLogger(__name__)


def verify_zid_signature(body: bytes, signature: str) -> bool:
    """
    Verify Zid webhook HMAC SHA-256 signature.
    التحقق من توقيع Zid webhook باستخدام HMAC SHA-256.

    Zid sends the signature in the X-Zid-Signature or X-Hub-Signature-256 header.
    TODO: Confirm exact header name from https://docs.zid.sa/reference/webhooks#security

    Args:
        body: Raw request body bytes
        signature: Signature string from header (format: sha256=<hex>)

    Returns:
        True if signature is valid, False otherwise
    """
    secret = os.getenv("ZID_WEBHOOK_SECRET", "")
    if not secret:
        logger.warning("ZID_WEBHOOK_SECRET not configured — skipping verification (DEV ONLY)")
        return True

    # Strip sha256= prefix if present
    if signature.startswith("sha256="):
        signature = signature[7:]

    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def handle_zid_webhook(event: str, payload: dict, db) -> dict:
    """
    Route Zid webhook to the appropriate handler.
    توجيه webhook من زد إلى المعالج المناسب.

    Args:
        event: Event type string (e.g. "order.created")
        payload: Parsed JSON payload dict
        db: Database session (SQLAlchemy AsyncSession or similar)

    Returns:
        dict with handled, action, and relevant details
    """
    handlers = {
        "order.created": _handle_order_created,
        "order.status.updated": _handle_order_status_updated,
        "order.abandoned_cart": _handle_abandoned_cart,
        "product.created": _handle_product_created,
        "product.updated": _handle_product_updated,
        "app.uninstalled": _handle_app_uninstalled,
        "refund.created": _handle_refund_created,
    }

    handler = handlers.get(event)
    if not handler:
        logger.info(f"Unhandled Zid event: {event}")
        return {"handled": False, "action": "ignored", "event": event}

    return await handler(payload, db)


# ── Event Handlers ────────────────────────────────────────────────────────────


async def _handle_order_created(payload: dict, db) -> dict:
    """
    New order created → trigger WhatsApp order confirmation.
    طلب جديد → إرسال تأكيد الطلب عبر WhatsApp.
    """
    order = payload.get("order", payload.get("data", {}))
    customer = order.get("customer", {})
    phone = customer.get("mobile") or customer.get("phone")
    order_id = order.get("id") or order.get("reference")

    logger.info(f"🛒 New Zid order: {order_id} for {phone}")

    # TODO: Trigger WhatsApp confirmation via Unifonic
    # await unifonic_whatsapp.send_order_confirmation(phone, order)

    return {
        "handled": True,
        "action": "order_created",
        "order_id": order_id,
        "customer_phone": phone,
        "total": order.get("total") or order.get("payment", {}).get("total"),
    }


async def _handle_order_status_updated(payload: dict, db) -> dict:
    """
    Order status changed → send update WhatsApp.
    تغيير حالة الطلب → إرسال رسالة تحديث عبر WhatsApp.
    """
    order = payload.get("order", payload.get("data", {}))
    new_status = order.get("status") or payload.get("status")

    return {
        "handled": True,
        "action": "order_status_updated",
        "order_id": order.get("id"),
        "status": new_status,
    }


async def _handle_abandoned_cart(payload: dict, db) -> dict:
    """
    Abandoned cart → trigger recovery WhatsApp sequence (high value).
    سلة مهجورة → بدء تسلسل استرداد العميل عبر WhatsApp (عالي القيمة).
    """
    cart = payload.get("cart", payload.get("data", {}))
    customer = cart.get("customer", {})
    phone = customer.get("mobile") or customer.get("phone")
    total = cart.get("total")

    logger.info(f"🛒💸 Zid abandoned cart: {cart.get('id')} — SAR {total} for {phone}")

    # TODO: Trigger recovery sequence via Unifonic WhatsApp
    # await unifonic_whatsapp.send_cart_recovery(phone, cart)

    return {
        "handled": True,
        "action": "abandoned_cart_recovery_triggered",
        "cart_id": cart.get("id"),
        "customer_phone": phone,
        "total": total,
    }


async def _handle_product_created(payload: dict, db) -> dict:
    """
    New product created → sync to Dealix catalog.
    منتج جديد → مزامنة مع كتالوج Dealix.
    """
    product = payload.get("product", payload.get("data", {}))
    logger.info(f"📦 Zid product created: {product.get('id')} — {product.get('name')}")
    # TODO: Upsert into products / catalog table
    return {
        "handled": True,
        "action": "product_synced",
        "product_id": product.get("id"),
    }


async def _handle_product_updated(payload: dict, db) -> dict:
    """
    Product updated → sync changes.
    تحديث المنتج → مزامنة التغييرات.
    """
    product = payload.get("product", payload.get("data", {}))
    return {
        "handled": True,
        "action": "product_updated",
        "product_id": product.get("id"),
    }


async def _handle_app_uninstalled(payload: dict, db) -> dict:
    """
    App uninstalled → deactivate merchant, stop workflows.
    إلغاء تثبيت التطبيق → إلغاء تفعيل التاجر وإيقاف التدفقات.
    """
    merchant_id = payload.get("merchant_id") or payload.get("store_id")
    logger.warning(f"⚠️  Zid app uninstalled for merchant: {merchant_id}")
    # TODO: Mark merchant inactive in DB, cancel active campaigns
    return {
        "handled": True,
        "action": "merchant_deactivated",
        "merchant_id": merchant_id,
    }


async def _handle_refund_created(payload: dict, db) -> dict:
    """
    Refund created → log and notify.
    إنشاء استرداد → التسجيل والإشعار.
    """
    refund = payload.get("refund", payload.get("data", {}))
    return {
        "handled": True,
        "action": "refund_logged",
        "refund_id": refund.get("id"),
        "amount": refund.get("amount"),
    }
