"""
Tamara — BNPL (alternative to Tabby) — strong in Saudi + UAE.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class TamaraCheckoutResult:
    success: bool
    checkout_url: str | None
    order_id: str | None
    error: str | None = None


def is_configured() -> bool:
    return bool(os.getenv("TAMARA_API_TOKEN", "").strip())


async def create_checkout(
    *,
    amount_sar: float,
    customer_email: str,
    customer_phone: str,
    customer_name: str,
    success_url: str,
    cancel_url: str,
    failure_url: str,
    order_reference_id: str,
) -> TamaraCheckoutResult:
    if not is_configured():
        return TamaraCheckoutResult(
            success=False, checkout_url=None, order_id=None, error="tamara_not_configured"
        )
    payload = {
        "order_reference_id": order_reference_id,
        "total_amount": {"amount": amount_sar, "currency": "SAR"},
        "description": "Dealix subscription",
        "country_code": "SA",
        "payment_type": "PAY_BY_LATER",
        "locale": "ar_SA",
        "consumer": {
            "first_name": customer_name.split(" ")[0],
            "last_name": " ".join(customer_name.split(" ")[1:]) or customer_name,
            "phone_number": customer_phone,
            "email": customer_email,
        },
        "merchant_url": {"success": success_url, "cancel": cancel_url, "failure": failure_url, "notification": cancel_url},
    }
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                "https://api.tamara.co/checkout",
                headers={
                    "Authorization": f"Bearer {os.getenv('TAMARA_API_TOKEN', '').strip()}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("tamara_checkout_failed")
        return TamaraCheckoutResult(
            success=False, checkout_url=None, order_id=None, error=str(exc)
        )
    return TamaraCheckoutResult(
        success=True,
        checkout_url=data.get("checkout_url"),
        order_id=str(data.get("order_id") or ""),
    )
