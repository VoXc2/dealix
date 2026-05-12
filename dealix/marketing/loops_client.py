"""
Loops.so marketing automation — modern Mailchimp killer with a
product-first SaaS DX. We use it to run drip sequences:
trial_started → trial_expiring_3d → trial_ended → renewal_alert.

Public surface:
    LoopsClient().is_configured
    await LoopsClient().identify(email, properties)
    await LoopsClient().event(event_name, email, properties=...)

No official Python SDK; REST via httpx. Reference:
    https://loops.so/docs/api-reference
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_BASE = "https://app.loops.so/api/v1"


@dataclass
class LoopsResult:
    success: bool
    event: str
    error: str | None = None


class LoopsClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = (api_key or os.getenv("LOOPS_API_KEY", "")).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def identify(self, email: str, properties: dict[str, Any]) -> bool:
        if not self.is_configured:
            return False
        body = {"email": email, **{k: v for k, v in properties.items() if v is not None}}
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.post(
                    f"{_BASE}/contacts/update", headers=self._headers(), json=body
                )
                r.raise_for_status()
        except Exception:
            log.exception("loops_identify_failed", email=email)
            return False
        return True

    async def event(
        self,
        *,
        event_name: str,
        email: str,
        properties: dict[str, Any] | None = None,
    ) -> LoopsResult:
        if not self.is_configured:
            return LoopsResult(success=False, event=event_name, error="loops_disabled")
        body: dict[str, Any] = {"email": email, "eventName": event_name}
        if properties:
            body["eventProperties"] = properties
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.post(
                    f"{_BASE}/events/send", headers=self._headers(), json=body
                )
                r.raise_for_status()
        except Exception as exc:
            log.exception("loops_event_failed", event=event_name, email=email)
            return LoopsResult(
                success=False, event=event_name, error=str(exc)
            )
        log.info("loops_event_sent", event=event_name, email=email)
        return LoopsResult(success=True, event=event_name)


_singleton: LoopsClient | None = None


def get_loops_client() -> LoopsClient:
    global _singleton
    if _singleton is None:
        _singleton = LoopsClient()
    return _singleton
