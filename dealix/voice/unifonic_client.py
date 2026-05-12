"""
Unifonic — Saudi-native voice + SMS carrier. Used as the local SIP
upstream for Vapi when the customer prefers in-Kingdom routing, plus
SMS fallback for OTP / urgent comms.

Reference: https://docs.unifonic.com
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class SmsResult:
    ok: bool
    message_id: str | None = None
    error: str | None = None


def is_configured() -> bool:
    return bool(os.getenv("UNIFONIC_APP_SID", "").strip())


async def send_sms(*, to: str, body: str, sender: str | None = None) -> SmsResult:
    sid = os.getenv("UNIFONIC_APP_SID", "").strip()
    if not sid:
        return SmsResult(ok=False, error="unifonic_not_configured")
    sender = sender or os.getenv("UNIFONIC_SENDER_ID", "Dealix").strip()
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                "https://el.cloud.unifonic.com/rest/SMS/messages",
                data={
                    "AppSid": sid,
                    "SenderID": sender,
                    "Recipient": to,
                    "Body": body,
                    "responseType": "JSON",
                },
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("unifonic_sms_failed", to=to)
        return SmsResult(ok=False, error=str(exc))
    msg = (data.get("data") or {}).get("MessageID")
    return SmsResult(ok=True, message_id=str(msg) if msg else None)
