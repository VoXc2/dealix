"""
Moyasar Subscriptions — Recurring billing for Dealix SaaS plans.
اشتراكات ميسر — الفوترة المتكررة لخطط Dealix SaaS.

Handles:
- Creating 1,499 SAR/month Starter subscriptions
- Creating 4,999 SAR/month Pro subscriptions
- Fetching subscription status
- Cancelling subscriptions

Docs: https://docs.moyasar.com/api/subscriptions

NOTE: Moyasar Subscriptions API uses the same auth as Payments.
      Amounts are in halalas (SAR × 100).

Environment variables:
- MOYASAR_SECRET_KEY
- MOYASAR_SUBSCRIPTION_CALLBACK_URL
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import httpx
import base64

logger = logging.getLogger(__name__)

MOYASAR_API_BASE = "https://api.moyasar.com/v1"

# Dealix plan amounts in halalas (SAR × 100)
PLAN_AMOUNTS: dict[str, int] = {
    "starter": 149_900,   # 1,499 SAR
    "pro":     499_900,   # 4,999 SAR
}

PLAN_NAMES: dict[str, str] = {
    "starter": "Dealix Starter — 1,499 ريال/شهر",
    "pro":     "Dealix Pro — 4,999 ريال/شهر",
}

PLAN_INTERVALS: dict[str, str] = {
    "starter": "month",
    "pro":     "month",
}


class MoyasarSubscriptions:
    """
    Moyasar recurring subscriptions manager for Dealix.
    مدير الاشتراكات المتكررة عبر ميسر لـ Dealix.

    Usage:
        subs = MoyasarSubscriptions()
        result = await subs.create_starter_subscription(
            tenant_id="abc123",
            customer_name="أحمد العتيبي",
            callback_url="https://api.dealix.sa/payments/moyasar/callback"
        )
    """

    def __init__(self, secret_key: Optional[str] = None) -> None:
        self.secret_key = secret_key or os.getenv("MOYASAR_SECRET_KEY", "")
        if not self.secret_key:
            logger.warning("MOYASAR_SECRET_KEY not set")

        token = base64.b64encode(f"{self.secret_key}:".encode()).decode()
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._callback_url = os.getenv(
            "MOYASAR_SUBSCRIPTION_CALLBACK_URL",
            "https://api.dealix.sa/webhooks/moyasar",
        )

    # ── Internal HTTP ─────────────────────────────────────

    async def _post(self, path: str, body: dict) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self._headers) as client:
            resp = await client.post(f"{MOYASAR_API_BASE}{path}", json=body)
            resp.raise_for_status()
            return resp.json()

    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self._headers) as client:
            resp = await client.get(f"{MOYASAR_API_BASE}{path}", params=params or {})
            resp.raise_for_status()
            return resp.json()

    async def _delete(self, path: str) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self._headers) as client:
            resp = await client.delete(f"{MOYASAR_API_BASE}{path}")
            resp.raise_for_status()
            return resp.json() if resp.text else {}

    # ── Plan helpers ──────────────────────────────────────

    async def create_subscription(
        self,
        plan: str,
        tenant_id: str,
        customer_name: str,
        customer_email: Optional[str] = None,
        callback_url: Optional[str] = None,
        source: Optional[dict] = None,
        trial_days: int = 0,
    ) -> dict:
        """
        Create a recurring subscription for a Dealix plan.
        إنشاء اشتراك متكرر لخطة Dealix.

        Args:
            plan: "starter" or "pro"
            tenant_id: Dealix internal tenant/merchant ID
            customer_name: Full name of the subscriber
            customer_email: Subscriber email (optional)
            callback_url: Override default callback URL
            source: Moyasar payment source dict (token, creditcard, etc.)
            trial_days: Number of free trial days (0 = no trial)

        Returns:
            Moyasar subscription object dict

        TODO: Confirm subscription payload schema from
              https://docs.moyasar.com/api/subscriptions/create
        """
        if plan not in PLAN_AMOUNTS:
            raise ValueError(f"Unknown plan '{plan}'. Valid: {list(PLAN_AMOUNTS.keys())}")

        body: dict = {
            "amount": PLAN_AMOUNTS[plan],
            "currency": "SAR",
            "description": PLAN_NAMES[plan],
            "interval": PLAN_INTERVALS[plan],
            "callback_url": callback_url or self._callback_url,
            "metadata": {
                "tenant_id": tenant_id,
                "plan": plan,
                "customer_name": customer_name,
            },
        }

        if customer_email:
            body["customer_email"] = customer_email

        if source:
            body["source"] = source

        if trial_days > 0:
            body["trial_period"] = trial_days

        result = await self._post("/subscriptions", body)
        logger.info(
            f"✅ Moyasar subscription created: id={result.get('id')} "
            f"plan={plan} tenant={tenant_id}"
        )
        return result

    async def create_starter_subscription(
        self,
        tenant_id: str,
        customer_name: str,
        customer_email: Optional[str] = None,
        callback_url: Optional[str] = None,
        source: Optional[dict] = None,
    ) -> dict:
        """
        Create a Starter subscription — 1,499 SAR/month.
        إنشاء اشتراك Starter — 1,499 ريال/شهر.
        """
        return await self.create_subscription(
            plan="starter",
            tenant_id=tenant_id,
            customer_name=customer_name,
            customer_email=customer_email,
            callback_url=callback_url,
            source=source,
        )

    async def create_pro_subscription(
        self,
        tenant_id: str,
        customer_name: str,
        customer_email: Optional[str] = None,
        callback_url: Optional[str] = None,
        source: Optional[dict] = None,
    ) -> dict:
        """
        Create a Pro subscription — 4,999 SAR/month.
        إنشاء اشتراك Pro — 4,999 ريال/شهر.
        """
        return await self.create_subscription(
            plan="pro",
            tenant_id=tenant_id,
            customer_name=customer_name,
            customer_email=customer_email,
            callback_url=callback_url,
            source=source,
        )

    # ── CRUD ──────────────────────────────────────────────

    async def get_subscription(self, subscription_id: str) -> dict:
        """
        Fetch a subscription by ID.
        جلب اشتراك بواسطة المعرّف.
        """
        return await self._get(f"/subscriptions/{subscription_id}")

    async def list_subscriptions(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
    ) -> dict:
        """
        List all subscriptions.
        قائمة جميع الاشتراكات.

        status: active|past_due|cancelled|trialing
        """
        params: dict = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return await self._get("/subscriptions", params=params)

    async def cancel_subscription(self, subscription_id: str) -> dict:
        """
        Cancel a subscription immediately.
        إلغاء الاشتراك فوراً.

        TODO: Confirm cancel endpoint from https://docs.moyasar.com/api/subscriptions
        """
        return await self._post(f"/subscriptions/{subscription_id}/cancel", {})

    async def pause_subscription(self, subscription_id: str) -> dict:
        """
        Pause a subscription (if supported by Moyasar).
        إيقاف الاشتراك مؤقتاً (إذا كان مدعوماً من ميسر).

        TODO: Verify pause support from https://docs.moyasar.com/api/subscriptions
        """
        return await self._post(f"/subscriptions/{subscription_id}/pause", {})

    async def resume_subscription(self, subscription_id: str) -> dict:
        """
        Resume a paused subscription.
        استئناف اشتراك موقوف.
        """
        return await self._post(f"/subscriptions/{subscription_id}/resume", {})

    # ── Invoice retrieval ─────────────────────────────────

    async def get_subscription_invoices(self, subscription_id: str) -> dict:
        """
        List all invoices for a subscription.
        قائمة الفواتير لاشتراك معين.

        TODO: Confirm endpoint from https://docs.moyasar.com/api/subscriptions/invoices
        """
        return await self._get(f"/subscriptions/{subscription_id}/invoices")
