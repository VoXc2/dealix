"""
Moyasar API Client — Payments, Invoices, Refunds.
عميل API ميسر — المدفوعات، الفواتير، المبالغ المستردة.

Docs: https://docs.moyasar.com/api/payments

Authentication: HTTP Basic Auth using secret API key.
Base URL: https://api.moyasar.com/v1

Environment variables:
- MOYASAR_SECRET_KEY  (sk_live_xxx or sk_test_xxx)
- MOYASAR_PUBLISHABLE_KEY (pk_live_xxx or pk_test_xxx)
"""

from __future__ import annotations

import base64
import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

MOYASAR_API_BASE = "https://api.moyasar.com/v1"


class MoyasarClient:
    """
    Authenticated Moyasar HTTP client.
    عميل HTTP لـ Moyasar مع مصادقة.

    Uses HTTP Basic Auth: Authorization: Basic base64(secret_key:)
    """

    def __init__(
        self,
        secret_key: Optional[str] = None,
        publishable_key: Optional[str] = None,
    ) -> None:
        self.secret_key = secret_key or os.getenv("MOYASAR_SECRET_KEY", "")
        self.publishable_key = publishable_key or os.getenv("MOYASAR_PUBLISHABLE_KEY", "")

        if not self.secret_key:
            logger.warning("MOYASAR_SECRET_KEY not set — Moyasar calls will fail")

        # Basic Auth: base64(secret_key:)
        token = base64.b64encode(f"{self.secret_key}:".encode()).decode()
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # ── Internal HTTP helpers ─────────────────────────────

    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self._headers) as client:
            resp = await client.get(f"{MOYASAR_API_BASE}{path}", params=params or {})
            resp.raise_for_status()
            return resp.json()

    async def _post(self, path: str, body: dict) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self._headers) as client:
            resp = await client.post(f"{MOYASAR_API_BASE}{path}", json=body)
            resp.raise_for_status()
            return resp.json()

    async def _put(self, path: str, body: dict) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self._headers) as client:
            resp = await client.put(f"{MOYASAR_API_BASE}{path}", json=body)
            resp.raise_for_status()
            return resp.json()

    # ── Payments ──────────────────────────────────────────

    async def create_payment(
        self,
        amount: int,
        currency: str = "SAR",
        description: str = "",
        callback_url: str = "",
        source: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Create a new payment.
        إنشاء دفعة جديدة.

        Docs: https://docs.moyasar.com/api/payments/create

        Args:
            amount: Amount in *halalas* (SAR × 100). E.g. 149900 = 1,499 SAR.
            currency: ISO 4217 currency code. Default: SAR
            description: Human-readable description
            callback_url: URL Moyasar redirects to after payment
            source: Payment source dict (e.g. {"type": "creditcard", "token": "..."})
            metadata: Arbitrary key-value metadata dict

        Returns:
            Moyasar payment object with id, status, amount, etc.
        """
        body: dict = {
            "amount": amount,
            "currency": currency,
            "description": description,
            "callback_url": callback_url,
        }
        if source:
            body["source"] = source
        if metadata:
            body["metadata"] = metadata

        return await self._post("/payments", body)

    async def get_payment(self, payment_id: str) -> dict:
        """
        Fetch a payment by ID.
        جلب دفعة بواسطة المعرّف.
        """
        return await self._get(f"/payments/{payment_id}")

    async def list_payments(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
    ) -> dict:
        """
        List payments with optional status filter.
        قائمة المدفوعات مع فلتر الحالة.

        status options: initiated|paid|failed|authorized|captured|voided|refunded
        """
        params: dict = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return await self._get("/payments", params=params)

    async def refund_payment(self, payment_id: str, amount_halalas: Optional[int] = None) -> dict:
        """
        Refund a payment (full or partial).
        استرداد دفعة (كامل أو جزئي).

        Args:
            payment_id: Moyasar payment ID
            amount_halalas: Amount to refund in halalas. None = full refund.
        """
        body: dict = {}
        if amount_halalas is not None:
            body["amount"] = amount_halalas
        return await self._post(f"/payments/{payment_id}/refund", body)

    # ── Invoices ──────────────────────────────────────────

    async def create_invoice(
        self,
        amount: int,
        currency: str = "SAR",
        description: str = "",
        expiry_date: Optional[str] = None,
        callback_url: str = "",
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Create a payment invoice (link-based payment).
        إنشاء فاتورة دفع (دفع عبر رابط).

        Docs: https://docs.moyasar.com/api/invoices/create

        Args:
            amount: Amount in halalas (SAR × 100)
            expiry_date: ISO 8601 datetime string. Defaults to 24h from now.
        """
        body: dict = {
            "amount": amount,
            "currency": currency,
            "description": description,
            "callback_url": callback_url,
        }
        if expiry_date:
            body["expiry_date"] = expiry_date
        if metadata:
            body["metadata"] = metadata

        return await self._post("/invoices", body)

    async def get_invoice(self, invoice_id: str) -> dict:
        """
        Fetch invoice by ID.
        جلب فاتورة بواسطة المعرّف.
        """
        return await self._get(f"/invoices/{invoice_id}")
