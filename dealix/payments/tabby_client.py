"""
Tabby — BNPL (Buy Now Pay Later) primary in Saudi + UAE + Kuwait.

Use at checkout when the order ≥ SAR 500 to lift conversion.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class TabbyCheckoutResult:
    success: bool
    checkout_url: str | None
    transaction_id: str | None
    error: str | None = None


def is_configured() -> bool:
    return bool(os.getenv("TABBY_SECRET_KEY", "").strip())


async def create_session(
    *,
    amount_sar: float,
    customer_email: str,
    customer_phone: str,
    customer_name: str,
    success_url: str,
    cancel_url: str,
    failure_url: str,
    description: str = "Dealix subscription",
) -> TabbyCheckoutResult:
    if not is_configured():
        return TabbyCheckoutResult(
            success=False, checkout_url=None, transaction_id=None, error="tabby_not_configured"
        )
    headers = {
        "Authorization": f"Bearer {os.getenv('TABBY_SECRET_KEY', '').strip()}",
        "Content-Type": "application/json",
    }
    payload = {
        "payment": {
            "amount": f"{amount_sar:.2f}",
            "currency": "SAR",
            "description": description,
            "buyer": {
                "email": customer_email,
                "phone": customer_phone,
                "name": customer_name,
            },
            "merchant_urls": {
                "success": success_url,
                "cancel": cancel_url,
                "failure": failure_url,
            },
        },
        "lang": "ar",
    }
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                "https://api.tabby.ai/api/v2/checkout", headers=headers, json=payload
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("tabby_session_failed")
        return TabbyCheckoutResult(
            success=False, checkout_url=None, transaction_id=None, error=str(exc)
        )
    return TabbyCheckoutResult(
        success=True,
        checkout_url=((data.get("configuration") or {}).get("available_products") or {})
        .get("installments", [{}])[0]
        .get("web_url"),
        transaction_id=str(data.get("id") or ""),
    )
