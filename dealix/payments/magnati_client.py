"""
Magnati — UAE merchant-acquiring (formerly Network International
Merchant Services). Card payments + wallet, AED-denominated, with
3-D Secure.

Used by UAE-based tenants who can't use Moyasar (KSA-only) or Tap
(GCC-wide but UAE-specific issuer routing is sometimes weaker).

Inert without `MAGNATI_API_KEY`.

Reference: https://www.magnati.com
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


class MagnatiNotConfigured(RuntimeError):
    """Raised when Magnati is called without MAGNATI_API_KEY."""


class MagnatiClient:
    BASE = "https://api.magnati.com/v1"

    def __init__(
        self,
        api_key: str | None = None,
        merchant_id: str | None = None,
        webhook_secret: str | None = None,
    ) -> None:
        self.api_key = (api_key or os.getenv("MAGNATI_API_KEY", "")).strip()
        self.merchant_id = (
            merchant_id or os.getenv("MAGNATI_MERCHANT_ID", "")
        ).strip()
        self.webhook_secret = (
            webhook_secret or os.getenv("MAGNATI_WEBHOOK_SECRET", "")
        ).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.merchant_id)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def create_checkout_session(
        self,
        *,
        amount_minor: int,
        currency: str = "AED",
        order_id: str,
        success_url: str,
        cancel_url: str,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not self.is_configured:
            raise MagnatiNotConfigured("MAGNATI_API_KEY not set")
        payload = {
            "merchantId": self.merchant_id,
            "amount": amount_minor / 100,
            "currency": currency.upper(),
            "orderId": order_id,
            "successUrl": success_url,
            "cancelUrl": cancel_url,
            "threeDSecure": True,
            "metadata": metadata or {},
        }
        async with httpx.AsyncClient(
            base_url=os.getenv("MAGNATI_API_BASE", self.BASE), timeout=15
        ) as c:
            r = await c.post("/checkout/sessions", headers=self._headers(), json=payload)
            r.raise_for_status()
            return r.json()

    def verify_webhook(self, payload: bytes, signature_header: str) -> bool:
        if not self.webhook_secret:
            return False
        expected = hmac.new(
            self.webhook_secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)


_singleton: MagnatiClient | None = None


def get_magnati_client() -> MagnatiClient:
    global _singleton
    if _singleton is None:
        _singleton = MagnatiClient()
    return _singleton
