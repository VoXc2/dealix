"""
Lago — open-source usage-based billing engine.

We meter every billable event (LLM tokens consumed, lead enriched,
WhatsApp message sent) and forward it to Lago; Lago aggregates by
customer / billable metric and generates invoices on a schedule.
Moyasar/Stripe then charge those invoices.

Public surface:
    LagoClient().is_configured
    await LagoClient().meter(metric_code, external_customer_id, value=...)

Inert without LAGO_API_KEY. Reference:
    https://docs.getlago.com/api-reference/events/create
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class MeterResult:
    success: bool
    metric: str
    transaction_id: str | None = None
    error: str | None = None


class LagoClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = (api_key or os.getenv("LAGO_API_KEY", "")).strip()
        self.base_url = (base_url or os.getenv("LAGO_BASE_URL", "https://api.getlago.com")).rstrip("/")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def meter(
        self,
        *,
        metric_code: str,
        external_customer_id: str,
        value: int | float = 1,
        properties: dict[str, Any] | None = None,
    ) -> MeterResult:
        """Record a metered event. Best-effort — never raises into the caller."""
        if not self.is_configured:
            return MeterResult(success=False, metric=metric_code, error="lago_disabled")
        tx_id = secrets.token_urlsafe(16)
        payload = {
            "event": {
                "transaction_id": tx_id,
                "external_customer_id": external_customer_id,
                "code": metric_code,
                "properties": {"value": value, **(properties or {})},
            }
        }
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.post(
                    f"{self.base_url}/api/v1/events",
                    headers=self._headers(),
                    json=payload,
                )
                r.raise_for_status()
        except Exception as exc:
            log.exception(
                "lago_meter_failed",
                metric=metric_code,
                tenant=external_customer_id,
            )
            return MeterResult(
                success=False, metric=metric_code, error=str(exc)
            )
        log.info(
            "lago_event_metered",
            metric=metric_code,
            tenant=external_customer_id,
            value=value,
        )
        return MeterResult(success=True, metric=metric_code, transaction_id=tx_id)


_singleton: LagoClient | None = None


def get_lago_client() -> LagoClient:
    global _singleton
    if _singleton is None:
        _singleton = LagoClient()
    return _singleton
