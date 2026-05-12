"""
KNET — Kuwait national payment gateway.

KNET routes KWD-denominated debit-card payments via Kuwait's
inter-bank switch. We integrate at the redirect level: the tenant
hands KNET an `OrderID`, receives a hosted-checkout URL, and
KNET posts the result back to our webhook.

KNET requires a merchant terminal-id (tranportalid) + resource-key
issued by the customer's acquiring bank. Inert without
`KNET_RESOURCE_KEY`.

Reference: https://www.knet.com.kw/
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


class KNetNotConfigured(RuntimeError):
    """Raised when KNET is called without KNET_RESOURCE_KEY."""


class KNetClient:
    BASE = "https://kpaytest.knet.com.kw/kpg"  # sandbox; override via env in prod.

    def __init__(
        self,
        tranportal_id: str | None = None,
        resource_key: str | None = None,
        currency: str = "KWD",
    ) -> None:
        self.tranportal_id = (
            tranportal_id or os.getenv("KNET_TRANPORTAL_ID", "")
        ).strip()
        self.resource_key = (
            resource_key or os.getenv("KNET_RESOURCE_KEY", "")
        ).strip()
        self.currency = currency.upper()

    @property
    def is_configured(self) -> bool:
        return bool(self.tranportal_id and self.resource_key)

    async def create_checkout_session(
        self,
        *,
        amount_minor: int,
        order_id: str,
        success_url: str,
        cancel_url: str,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not self.is_configured:
            raise KNetNotConfigured("KNET_TRANPORTAL_ID or KNET_RESOURCE_KEY not set")
        payload = {
            "id": self.tranportal_id,
            "password": self.resource_key,
            "amt": f"{amount_minor / 1000:.3f}",  # KWD has 3 decimals
            "currencycode": "414",  # KWD
            "trackid": order_id,
            "udf1": (metadata or {}).get("tenant_id", ""),
            "responseURL": success_url,
            "errorURL": cancel_url,
            "action": "1",
            "langid": "ENG",
        }
        async with httpx.AsyncClient(
            base_url=os.getenv("KNET_API_BASE", self.BASE), timeout=15
        ) as c:
            r = await c.post("/PaymentHTTP.htm", data=payload)
            r.raise_for_status()
            return {"redirect_url": r.url, "raw": r.text}

    def verify_webhook(self, payload: bytes, signature_header: str) -> bool:
        """KNET uses an MD5 of (resource_key + concat fields) — we accept HMAC-SHA256
        when the customer fronts the webhook with a small relay (recommended)."""
        if not self.resource_key:
            return False
        expected = hmac.new(
            self.resource_key.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)


_singleton: KNetClient | None = None


def get_knet_client() -> KNetClient:
    global _singleton
    if _singleton is None:
        _singleton = KNetClient()
    return _singleton
