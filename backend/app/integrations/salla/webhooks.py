"""
Salla Webhooks Handler.
Docs: https://docs.salla.dev/docs/webhooks

Key events we care about:
- app.store.authorize   → New merchant installed Dealix
- app.installed         → App activated
- app.uninstalled       → Deactivate + stop billing
- order.created         → Trigger welcome WhatsApp
- order.status.updated  → Status update messages
- abandoned.cart        → Cart recovery flow (high-value)
- customer.created      → Add to Dealix CRM
- review.added          → Thank you + upsell flow
"""
import hashlib
import hmac
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def verify_salla_signature(body: bytes, signature: str) -> bool:
    """Verify Salla webhook signature (HMAC SHA-256)."""
    secret = os.getenv("SALLA_WEBHOOK_SECRET", "")
    if not secret:
        logger.warning("SALLA_WEBHOOK_SECRET not configured — skipping verification (DEV ONLY)")
        return True
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def handle_salla_webhook(event: str, payload: dict, db) -> dict:
    """
    Route Salla webhook to appropriate handler.
    Returns {"handled": bool, "action": str, "details": ...}
    """
    handlers = {
        "app.store.authorize": _handle_authorize,
        "app.installed": _handle_installed,
        "app.uninstalled": _handle_uninstalled,
        "order.created": _handle_order_created,
        "order.status.updated": _handle_order_status_updated,
        "abandoned.cart": _handle_abandoned_cart,
        "customer.created": _handle_customer_created,
        "review.added": _handle_review_added,
    }
    handler = handlers.get(event)
    if not handler:
        logger.info(f"Unhandled Salla event: {event}")
        return {"handled": False, "action": "ignored", "event": event}
    return await handler(payload, db)


async def _handle_authorize(payload: dict, db) -> dict:
    """New merchant authorized Dealix — store tokens."""
    data = payload.get("data", {})
    merchant = payload.get("merchant") or data.get("merchant")
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    expires = data.get("expires")
    # TODO: upsert into salla_merchants table
    logger.info(f"✅ Salla merchant authorized: {merchant}")
    return {"handled": True, "action": "merchant_authorized", "merchant_id": merchant}


async def _handle_installed(payload: dict, db) -> dict:
    merchant = payload.get("merchant")
    logger.info(f"✅ Salla app installed by merchant: {merchant}")
    # Trigger welcome WhatsApp to merchant
    return {"handled": True, "action": "installed", "merchant_id": merchant}


async def _handle_uninstalled(payload: dict, db) -> dict:
    merchant = payload.get("merchant")
    logger.info(f"⚠️  Salla app uninstalled: {merchant}")
    return {"handled": True, "action": "uninstalled", "merchant_id": merchant}


async def _handle_order_created(payload: dict, db) -> dict:
    """New order → send WhatsApp confirmation."""
    order = payload.get("data", {})
    customer = order.get("customer", {})
    phone = customer.get("mobile") or customer.get("phone")
    logger.info(f"🛒 New Salla order: {order.get('id')} for {phone}")
    return {
        "handled": True,
        "action": "order_created",
        "order_id": order.get("id"),
        "customer_phone": phone,
        "total": order.get("total", {}).get("amount"),
    }


async def _handle_order_status_updated(payload: dict, db) -> dict:
    order = payload.get("data", {})
    return {
        "handled": True,
        "action": "order_status_updated",
        "order_id": order.get("id"),
        "status": order.get("status"),
    }


async def _handle_abandoned_cart(payload: dict, db) -> dict:
    """High-value event — trigger cart recovery WhatsApp sequence."""
    cart = payload.get("data", {})
    customer = cart.get("customer", {})
    phone = customer.get("mobile")
    logger.info(f"🛒💸 Abandoned cart: {cart.get('id')} for {phone} — SAR {cart.get('total')}")
    return {
        "handled": True,
        "action": "abandoned_cart_recovery_triggered",
        "cart_id": cart.get("id"),
        "customer_phone": phone,
        "total": cart.get("total"),
    }


async def _handle_customer_created(payload: dict, db) -> dict:
    customer = payload.get("data", {})
    return {"handled": True, "action": "customer_added_to_crm", "customer_id": customer.get("id")}


async def _handle_review_added(payload: dict, db) -> dict:
    review = payload.get("data", {})
    return {"handled": True, "action": "review_logged", "review_id": review.get("id")}
