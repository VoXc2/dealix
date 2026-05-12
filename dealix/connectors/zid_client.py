"""
Zid — alternative Saudi e-commerce platform. Same pattern as Salla.

Reference: https://docs.zid.sa
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
    return bool(os.getenv("ZID_API_TOKEN", "").strip())


def verify_webhook(payload: bytes, signature: str) -> bool:
    secret = os.getenv("ZID_WEBHOOK_SECRET", "").strip()
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def list_orders(*, access_token: str | None = None) -> list[dict[str, Any]]:
    token = access_token or os.getenv("ZID_API_TOKEN", "").strip()
    if not token:
        return []
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                "https://api.zid.sa/v1/managers/store/orders",
                headers={"Authorization": f"Bearer {token}"},
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("zid_list_orders_failed")
        return []
    return data.get("orders", [])
