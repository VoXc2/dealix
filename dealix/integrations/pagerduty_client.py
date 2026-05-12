"""
PagerDuty Events API v2 client — minimal, inert without env keys.

Surface:
    PagerDutyClient().is_configured
    await PagerDutyClient().trigger(summary, dedup_key, severity="error", source="dealix-api")
    await PagerDutyClient().resolve(dedup_key)

Reference: https://developer.pagerduty.com/api-reference/368ae3d938c9e-send-an-event
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_EVENTS_URL = "https://events.pagerduty.com/v2/enqueue"


@dataclass
class PagerDutyResult:
    success: bool
    dedup_key: str | None = None
    error: str | None = None


class PagerDutyClient:
    def __init__(self, integration_key: str | None = None) -> None:
        self.integration_key = (
            integration_key or os.getenv("PAGERDUTY_INTEGRATION_KEY", "")
        ).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.integration_key)

    async def _send(self, payload: dict[str, Any]) -> PagerDutyResult:
        if not self.is_configured:
            return PagerDutyResult(success=False, error="pagerduty_disabled")
        try:
            async with httpx.AsyncClient(timeout=5) as c:
                r = await c.post(_EVENTS_URL, json=payload)
                r.raise_for_status()
                data = r.json()
        except Exception as exc:
            log.exception("pagerduty_send_failed")
            return PagerDutyResult(success=False, error=str(exc))
        return PagerDutyResult(success=True, dedup_key=data.get("dedup_key"))

    async def trigger(
        self,
        *,
        summary: str,
        dedup_key: str,
        severity: str = "error",
        source: str = "dealix-api",
        custom_details: dict[str, Any] | None = None,
    ) -> PagerDutyResult:
        payload = {
            "routing_key": self.integration_key,
            "event_action": "trigger",
            "dedup_key": dedup_key,
            "payload": {
                "summary": summary,
                "source": source,
                "severity": severity,
                "custom_details": custom_details or {},
            },
        }
        return await self._send(payload)

    async def resolve(self, dedup_key: str) -> PagerDutyResult:
        return await self._send(
            {
                "routing_key": self.integration_key,
                "event_action": "resolve",
                "dedup_key": dedup_key,
            }
        )


_singleton: PagerDutyClient | None = None


def get_pagerduty_client() -> PagerDutyClient:
    global _singleton
    if _singleton is None:
        _singleton = PagerDutyClient()
    return _singleton
