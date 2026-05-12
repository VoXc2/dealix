"""
Tap Payments — pan-GCC card payments. Used as a fallback / alternative
to Moyasar for customers in Kuwait / Bahrain / UAE / Oman / Egypt
who can't reach Moyasar.

Mirrors `MoyasarClient` and `StripeClient` so the rest of the app
stays gateway-agnostic.

Reference: https://developers.tap.company/docs/api
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


class TapNotConfigured(RuntimeError):
    """Raised when a Tap call is made without TAP_SECRET_KEY."""


class TapClient:
    BASE = "https://api.tap.company/v2"

    def __init__(
        self,
        secret_key: str | None = None,
        webhook_secret: str | None = None,
    ) -> None:
        self.secret_key = (secret_key or os.getenv("TAP_SECRET_KEY", "")).strip()
        self.webhook_secret = (
            webhook_secret or os.getenv("TAP_WEBHOOK_SECRET", "")
        ).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.secret_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    async def create_checkout_session(
        self,
        *,
        amount_minor: int,
        currency: str = "SAR",
        product_name: str = "Dealix subscription",
        success_url: str = "",
        cancel_url: str = "",
        customer_email: str = "",
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not self.is_configured:
            raise TapNotConfigured("TAP_SECRET_KEY not set")
        payload: dict[str, Any] = {
            "amount": amount_minor / 100,
            "currency": currency.upper(),
            "customer_initiated": True,
            "threeDSecure": True,
            "description": product_name,
            "metadata": metadata or {},
            "redirect": {"url": success_url},
            "post": {"url": cancel_url},
            "customer": {"email": customer_email} if customer_email else {},
            "source": {"id": "src_all"},
        }
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.BASE}/charges", headers=self._headers(), json=payload
            )
            r.raise_for_status()
            return r.json()

    def verify_webhook(self, payload: bytes, signature_header: str) -> bool:
        if not self.webhook_secret:
            return False
        expected = hmac.new(
            self.webhook_secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)


_singleton: TapClient | None = None


def get_tap_client() -> TapClient:
    global _singleton
    if _singleton is None:
        _singleton = TapClient()
    return _singleton
