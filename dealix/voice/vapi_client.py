"""
Vapi orchestration client — manages SIP / call routing / function calls.

We push our toolset (lead_capture, qualify, book_meeting, escalate)
to Vapi as functions the in-call agent can invoke; Vapi calls our
`/api/v1/voice/inbound` webhook with the function-call envelope.
"""

from __future__ import annotations

import hmac
import hashlib
import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class VapiResult:
    ok: bool
    call_id: str | None = None
    error: str | None = None


def is_configured() -> bool:
    return bool(os.getenv("VAPI_API_KEY", "").strip())


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {os.getenv('VAPI_API_KEY', '').strip()}",
        "Content-Type": "application/json",
    }


def verify_signature(body: bytes, signature: str) -> bool:
    """Verify Vapi's HMAC-SHA256 signature on inbound webhooks."""
    secret = os.getenv("VAPI_WEBHOOK_SECRET", "").strip()
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def place_outbound(
    *,
    to: str,
    assistant_id: str,
    tenant_id: str,
    locale: str = "ar",
) -> VapiResult:
    """Place an outbound call. Requires prior consent — PDPL compliance."""
    if not is_configured():
        return VapiResult(ok=False, error="vapi_not_configured")
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                "https://api.vapi.ai/call",
                headers=_headers(),
                json={
                    "phoneNumberId": os.getenv("VAPI_PHONE_NUMBER_ID", "").strip(),
                    "customer": {"number": to},
                    "assistantId": assistant_id,
                    "metadata": {"tenant_id": tenant_id, "locale": locale},
                },
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("vapi_outbound_failed", to=to)
        return VapiResult(ok=False, error=str(exc))
    return VapiResult(ok=True, call_id=data.get("id"))
