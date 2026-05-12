"""
BENEFIT — Bahrain's national debit-card switch + national e-KYC + EFTS.

Two complementary surfaces are exposed by BENEFIT (Bahrain Electronic
Network for Financial Transactions):

1. **BenefitPay** — BHD-denominated card + wallet payments (similar to
   KNET in Kuwait).
2. **BENEFIT e-KYC** — national identity verification for Bahrain
   residents (similar to Nafath in Saudi).

We support both with a single client gated by `BENEFIT_API_KEY`.
"""

from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


class BenefitNotConfigured(RuntimeError):
    """Raised when BENEFIT is called without BENEFIT_API_KEY."""


class BenefitClient:
    BASE = "https://api.benefit.bh/v1"

    def __init__(
        self,
        api_key: str | None = None,
        merchant_id: str | None = None,
        webhook_secret: str | None = None,
    ) -> None:
        self.api_key = (api_key or os.getenv("BENEFIT_API_KEY", "")).strip()
        self.merchant_id = (
            merchant_id or os.getenv("BENEFIT_MERCHANT_ID", "")
        ).strip()
        self.webhook_secret = (
            webhook_secret or os.getenv("BENEFIT_WEBHOOK_SECRET", "")
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
        currency: str = "BHD",
        order_id: str,
        success_url: str,
        cancel_url: str,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not self.is_configured:
            raise BenefitNotConfigured("BENEFIT_API_KEY not set")
        payload = {
            "merchantId": self.merchant_id,
            "amount": amount_minor / 1000,  # BHD has 3 decimals
            "currency": currency.upper(),
            "orderId": order_id,
            "successUrl": success_url,
            "cancelUrl": cancel_url,
            "metadata": metadata or {},
        }
        async with httpx.AsyncClient(
            base_url=os.getenv("BENEFIT_API_BASE", self.BASE), timeout=15
        ) as c:
            r = await c.post("/payments", headers=self._headers(), json=payload)
            r.raise_for_status()
            return r.json()

    def verify_webhook(self, payload: bytes, signature_header: str) -> bool:
        if not self.webhook_secret:
            return False
        expected = hmac.new(
            self.webhook_secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)

    async def ekyc_verify(self, *, cpr_number: str) -> "EKYCResult":
        """Bahrain CPR (Central Population Register) e-KYC check."""
        if not self.is_configured:
            raise BenefitNotConfigured("BENEFIT_API_KEY not set")
        async with httpx.AsyncClient(
            base_url=os.getenv("BENEFIT_API_BASE", self.BASE), timeout=15
        ) as c:
            r = await c.post(
                "/ekyc/verify", headers=self._headers(), json={"cpr": cpr_number}
            )
            r.raise_for_status()
            data = r.json()
        return EKYCResult(
            verified=bool(data.get("verified")),
            full_name=data.get("fullName"),
            nationality=data.get("nationality"),
        )


@dataclass(frozen=True)
class EKYCResult:
    verified: bool
    full_name: str | None
    nationality: str | None


_singleton: BenefitClient | None = None


def get_benefit_client() -> BenefitClient:
    global _singleton
    if _singleton is None:
        _singleton = BenefitClient()
    return _singleton
