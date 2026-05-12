"""
Salla — Saudi e-commerce platform. Sync orders → leads.

Operates via OAuth-secured webhooks; we store the per-tenant access
token in `TenantRecord.meta_json.salla_access_token`. This client
exposes only the endpoints we need today: order list + webhook verify.

Reference: https://docs.salla.dev/api-reference
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def is_configured() -> bool:
    return bool(os.getenv("SALLA_CLIENT_ID", "").strip())


def verify_webhook(payload: bytes, signature: str) -> bool:
    secret = os.getenv("SALLA_WEBHOOK_SECRET", "").strip()
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def list_orders(*, access_token: str, since_iso: str | None = None) -> list[dict[str, Any]]:
    if not access_token:
        return []
    params: dict[str, Any] = {"per_page": 50}
    if since_iso:
        params["from_date"] = since_iso
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                "https://api.salla.dev/admin/v2/orders",
                headers={"Authorization": f"Bearer {access_token}"},
                params=params,
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("salla_list_orders_failed")
        return []
    return data.get("data", [])
