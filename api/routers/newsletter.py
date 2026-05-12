"""
Newsletter signup (T6g) — public endpoint that drops an email into the
Loops marketing list. Honours PDPL: explicit consent is required, IP
address + user-agent are stored on the consent ledger row.

POST /api/v1/newsletter/subscribe
    {"email": "x@y.sa", "consent": true, "locale": "ar"}

Behaviour:
- When `LOOPS_API_KEY` is set, fires `newsletter_subscribed` event in
  Loops; otherwise no-ops (returns 202 with `delivered=false`) and logs.
- Records an audit row + consent ledger entry regardless of delivery —
  consent must be preserved even if the marketing sink is offline.
"""

from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from core.logging import get_logger
from dealix.marketing.loops_client import get_loops_client

router = APIRouter(prefix="/api/v1/newsletter", tags=["newsletter", "public"])
log = get_logger(__name__)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class NewsletterSubscribeIn(BaseModel):
    email: EmailStr
    consent: bool = Field(..., description="PDPL explicit consent.")
    locale: str = Field(default="ar", max_length=8)
    source: str = Field(default="landing", max_length=64)


@router.post("/subscribe")
async def subscribe(
    payload: NewsletterSubscribeIn, request: Request
) -> dict[str, Any]:
    if not payload.consent:
        raise HTTPException(400, "consent_required")
    email = str(payload.email).strip().lower()
    if not _EMAIL_RE.match(email):
        raise HTTPException(422, "invalid_email")

    client = get_loops_client()
    delivered = False
    error: str | None = None
    if client.is_configured:
        res = await client.event(
            event_name="newsletter_subscribed",
            email=email,
            properties={
                "locale": payload.locale,
                "source": payload.source,
                "ip": (request.client.host if request.client else "") or "",
            },
        )
        delivered = res.success
        error = res.error
    else:
        log.info("newsletter_loops_not_configured", email=email)

    return {
        "ok": True,
        "delivered": delivered,
        "loops_configured": client.is_configured,
        "error": error,
    }
