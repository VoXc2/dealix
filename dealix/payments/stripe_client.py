"""
Stripe client — international card payments (USD/EUR/AED/SAR), Checkout
sessions, subscriptions, and webhook signature verification.

Mirrors the Moyasar contract (`create_checkout_session`, `verify_webhook`,
`fetch_payment`) so the rest of the app can stay payment-gateway-agnostic.
Inert unless `STRIPE_API_KEY` env is set; every method raises
`StripeNotConfigured` otherwise so callers can branch deterministically.

References:
    https://docs.stripe.com/api/checkout/sessions/create
    https://docs.stripe.com/webhooks/signatures
"""

from __future__ import annotations

import hashlib
import hmac
import os
import time
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


class StripeNotConfigured(RuntimeError):
    """Raised when a Stripe call is attempted without STRIPE_API_KEY."""


class StripeClient:
    BASE = "https://api.stripe.com/v1"

    def __init__(
        self,
        secret_key: str | None = None,
        webhook_secret: str | None = None,
    ) -> None:
        self.secret_key = secret_key or os.getenv("STRIPE_API_KEY", "").strip()
        self.webhook_secret = webhook_secret or os.getenv(
            "STRIPE_WEBHOOK_SECRET", ""
        ).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.secret_key)

    def _require_configured(self) -> None:
        if not self.is_configured:
            raise StripeNotConfigured("STRIPE_API_KEY not set")

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    async def create_checkout_session(
        self,
        amount_cents: int,
        currency: str = "usd",
        product_name: str = "Dealix subscription",
        success_url: str = "",
        cancel_url: str = "",
        metadata: dict[str, str] | None = None,
        mode: str = "payment",
    ) -> dict[str, Any]:
        """Create a Stripe Checkout Session and return the hosted URL.

        `mode="subscription"` requires a price ID — caller should resolve
        the price ID upstream and pass via `metadata["price_id"]`.
        """
        self._require_configured()
        if not success_url or not cancel_url:
            raise ValueError("success_url and cancel_url are required")
        # Stripe expects form-encoded; we build the nested dict manually.
        data: list[tuple[str, str]] = [
            ("mode", mode),
            ("success_url", success_url),
            ("cancel_url", cancel_url),
        ]
        if mode == "subscription":
            price_id = (metadata or {}).get("price_id")
            if not price_id:
                raise ValueError("metadata.price_id required for subscription mode")
            data.append(("line_items[0][price]", price_id))
            data.append(("line_items[0][quantity]", "1"))
        else:
            data.extend(
                [
                    ("line_items[0][price_data][currency]", currency),
                    ("line_items[0][price_data][unit_amount]", str(int(amount_cents))),
                    (
                        "line_items[0][price_data][product_data][name]",
                        product_name,
                    ),
                    ("line_items[0][quantity]", "1"),
                ]
            )
        if metadata:
            for k, v in metadata.items():
                data.append((f"metadata[{k}]", str(v)))

        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.BASE}/checkout/sessions", headers=self._headers(), data=data
            )
            r.raise_for_status()
            return r.json()

    async def fetch_payment(self, payment_intent_id: str) -> dict[str, Any]:
        self._require_configured()
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{self.BASE}/payment_intents/{payment_intent_id}",
                headers={"Authorization": f"Bearer {self.secret_key}"},
            )
            r.raise_for_status()
            return r.json()

    def verify_webhook(
        self,
        payload: bytes,
        signature_header: str,
        *,
        tolerance: int = 300,
    ) -> bool:
        """Verify a Stripe webhook payload's Stripe-Signature header.

        Implementation per https://docs.stripe.com/webhooks/signatures.
        Returns True if at least one v1 signature matches and timestamp is
        within `tolerance` seconds.
        """
        if not self.webhook_secret:
            log.warning("stripe_webhook_no_secret_configured")
            return False
        try:
            parts = dict(p.split("=", 1) for p in signature_header.split(","))
        except ValueError:
            return False
        ts = parts.get("t")
        v1 = parts.get("v1")
        if not ts or not v1:
            return False
        # Tolerate clock skew.
        try:
            if abs(time.time() - int(ts)) > tolerance:
                return False
        except ValueError:
            return False
        signed_payload = f"{ts}.".encode() + payload
        expected = hmac.new(
            self.webhook_secret.encode(), signed_payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, v1)


# Module-level singleton for convenience; new instance created on each
# call only if env was mutated mid-process (rare, used in tests).
_singleton: StripeClient | None = None


def get_stripe_client() -> StripeClient:
    global _singleton
    if _singleton is None:
        _singleton = StripeClient()
    return _singleton
