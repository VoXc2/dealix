"""
Zid Admin API Client — Orders, Products, Abandoned Carts.
عميل API زد — الطلبات، المنتجات، السلال المهجورة.

Docs: https://docs.zid.sa/reference/api-endpoints
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# TODO: Verify final API base URL from https://docs.zid.sa/reference/api-endpoints
ZID_API_BASE = "https://api.zid.sa/v1"


class ZidClient:
    """
    Authenticated Zid API client for a single merchant/manager.
    عميل API زد المصادق عليه لتاجر واحد.

    Usage:
        client = ZidClient(access_token="...", store_id="123")
        orders = await client.list_orders()
    """

    def __init__(
        self,
        access_token: str,
        store_id: Optional[str] = None,
        manager_token: Optional[str] = None,
    ) -> None:
        self.access_token = access_token
        self.store_id = store_id
        # Zid uses both Authorization Bearer AND X-Manager-Token in some flows
        self.headers: dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if store_id:
            self.headers["X-Manager-Store-Id"] = str(store_id)
        if manager_token:
            self.headers["X-Manager-Token"] = manager_token

    # ── Internal HTTP helpers ─────────────────────────────

    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        """
        Authenticated GET request.
        طلب GET مصادق عليه.
        """
        async with httpx.AsyncClient(timeout=30.0, headers=self.headers) as client:
            resp = await client.get(f"{ZID_API_BASE}{path}", params=params or {})
            resp.raise_for_status()
            return resp.json()

    async def _post(self, path: str, body: dict) -> dict:
        """
        Authenticated POST request.
        طلب POST مصادق عليه.
        """
        async with httpx.AsyncClient(timeout=30.0, headers=self.headers) as client:
            resp = await client.post(f"{ZID_API_BASE}{path}", json=body)
            resp.raise_for_status()
            return resp.json()

    # ── Store ─────────────────────────────────────────────

    async def store_info(self) -> dict:
        """
        Get merchant store information.
        الحصول على بيانات متجر التاجر.

        TODO: Verify endpoint from https://docs.zid.sa/reference/store
        """
        return await self._get("/store")

    # ── Orders ────────────────────────────────────────────

    async def list_orders(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> dict:
        """
        List store orders with optional filters.
        قائمة الطلبات مع فلاتر اختيارية.

        Args:
            page: Page number (1-indexed)
            per_page: Items per page (max 50)
            status: Order status filter — new|processing|shipped|delivered|cancelled|refunded
            from_date: ISO 8601 date string (e.g. 2024-01-01)
            to_date: ISO 8601 date string

        TODO: Confirm pagination params from https://docs.zid.sa/reference/orders
        """
        params: dict = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        return await self._get("/managers/orders", params=params)

    async def get_order(self, order_id: str | int) -> dict:
        """
        Get a single order by ID.
        الحصول على طلب واحد بواسطة المعرّف.
        """
        return await self._get(f"/managers/orders/{order_id}")

    async def update_order_status(self, order_id: str | int, status: str) -> dict:
        """
        Update order status.
        تحديث حالة الطلب.
        """
        return await self._post(f"/managers/orders/{order_id}/status", {"status": status})

    # ── Products ──────────────────────────────────────────

    async def list_products(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
    ) -> dict:
        """
        List store products.
        قائمة منتجات المتجر.

        TODO: Confirm endpoint from https://docs.zid.sa/reference/products
        """
        params: dict = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        return await self._get("/managers/products", params=params)

    async def get_product(self, product_id: str | int) -> dict:
        """
        Get product details by ID.
        الحصول على تفاصيل منتج بواسطة المعرّف.
        """
        return await self._get(f"/managers/products/{product_id}")

    # ── Abandoned Carts ───────────────────────────────────

    async def list_abandoned_carts(
        self,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """
        Fetch abandoned carts — high-value for recovery WhatsApp campaigns.
        جلب السلال المهجورة — عالية القيمة لحملات استرداد العملاء عبر WhatsApp.

        TODO: Confirm exact endpoint from https://docs.zid.sa/reference/abandoned-carts
        """
        params: dict = {"page": page, "per_page": per_page}
        return await self._get("/managers/abandoned-carts", params=params)

    async def get_abandoned_cart(self, cart_id: str | int) -> dict:
        """
        Get a single abandoned cart by ID.
        الحصول على سلة مهجورة واحدة بواسطة المعرّف.
        """
        return await self._get(f"/managers/abandoned-carts/{cart_id}")

    # ── Customers ─────────────────────────────────────────

    async def list_customers(
        self,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """
        List store customers.
        قائمة عملاء المتجر.
        """
        params: dict = {"page": page, "per_page": per_page}
        return await self._get("/managers/customers", params=params)

    # ── Analytics ─────────────────────────────────────────

    async def get_store_stats(self) -> dict:
        """
        Get basic store analytics/stats.
        الحصول على إحصاءات المتجر الأساسية.

        TODO: Confirm endpoint from https://docs.zid.sa/reference/analytics
        """
        return await self._get("/managers/store/stats")
