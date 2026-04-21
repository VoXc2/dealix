"""
Salla Admin API Client — Fetch orders, products, customers.
Docs: https://docs.salla.dev/docs/merchant/apis
"""
import httpx
from typing import Optional


SALLA_API_BASE = "https://api.salla.dev/admin/v2"


class SallaClient:
    """Authenticated Salla API client for a single merchant."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        async with httpx.AsyncClient(timeout=30.0, headers=self.headers) as client:
            resp = await client.get(f"{SALLA_API_BASE}{path}", params=params or {})
            resp.raise_for_status()
            return resp.json()

    async def store_info(self) -> dict:
        """Get merchant store details."""
        return await self._get("/store/info")

    async def list_orders(self, page: int = 1, per_page: int = 15, status: Optional[str] = None) -> dict:
        """List orders. status: pending|payment_pending|under_review|in_progress|completed|delivering|delivered|shipped|canceled|restoring|restored."""
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return await self._get("/orders", params=params)

    async def get_order(self, order_id: int) -> dict:
        return await self._get(f"/orders/{order_id}")

    async def list_customers(self, page: int = 1, per_page: int = 15) -> dict:
        return await self._get("/customers", params={"page": page, "per_page": per_page})

    async def list_products(self, page: int = 1, per_page: int = 15) -> dict:
        return await self._get("/products", params={"page": page, "per_page": per_page})

    async def list_abandoned_carts(self, page: int = 1, per_page: int = 15) -> dict:
        """Abandoned carts — the gold for cart-recovery WhatsApp campaigns."""
        return await self._get("/carts/abandoned", params={"page": page, "per_page": per_page})
