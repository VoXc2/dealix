"""
Zid FastAPI Routes:
- GET  /auth/zid/install    → Redirect merchant to Zid authorization
- GET  /auth/zid/callback   → OAuth2 callback, exchange code for tokens
- POST /webhooks/zid        → Receive and dispatch Zid webhook events

مسارات FastAPI لمنصة زد.
"""

from __future__ import annotations

import logging
import os
import secrets

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse

from .oauth import ZidOAuth
from .webhooks import handle_zid_webhook, verify_zid_signature

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["zid"])

# In-memory state store — replace with Redis in production
# تخزين الـ state في الذاكرة — استبدل بـ Redis في الإنتاج
_states: dict[str, bool] = {}


@router.get("/auth/zid/install", summary="Zid OAuth Install Entry Point")
async def zid_install():
    """
    Entry point when merchant clicks 'Install Dealix' from Zid App Market.
    نقطة البداية عندما يضغط التاجر على 'تثبيت Dealix' من سوق تطبيقات زد.
    """
    oauth = ZidOAuth()
    if not oauth.client_id:
        raise HTTPException(status_code=500, detail="Zid integration not configured — ZID_CLIENT_ID missing")

    state = secrets.token_urlsafe(32)
    _states[state] = True
    url = oauth.authorize_url(state=state)
    return RedirectResponse(url=url)


@router.get("/auth/zid/callback", summary="Zid OAuth2 Callback")
async def zid_callback(code: str, state: str):
    """
    Zid redirects here after merchant authorizes.
    Exchange authorization code for access + refresh tokens.

    يعيد زد التوجيه هنا بعد موافقة التاجر.
    يستبدل رمز التفويض بـ tokens.
    """
    if state not in _states:
        raise HTTPException(status_code=400, detail="Invalid or expired state parameter")
    _states.pop(state, None)

    oauth = ZidOAuth()
    try:
        tokens = await oauth.exchange_code(code)
    except Exception as exc:
        logger.error(f"Zid token exchange failed: {exc}")
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {exc}")

    # TODO: Persist tokens in DB (zid_merchants table)
    # await zid_merchant_repo.upsert(tokens)
    logger.info(f"✅ Zid authorized: store_id={tokens.get('store_id')}")

    dashboard = os.getenv("DASHBOARD_URL", "https://dealix.sa/dashboard")
    return RedirectResponse(url=f"{dashboard}?zid=connected")


@router.post("/webhooks/zid", summary="Zid Webhook Receiver")
async def zid_webhook(
    request: Request,
    x_zid_signature: str = Header(default="", alias="X-Zid-Signature"),
    x_hub_signature_256: str = Header(default="", alias="X-Hub-Signature-256"),
):
    """
    Receive and dispatch webhook events from Zid.
    استقبال وتوجيه أحداث Webhook من منصة زد.

    Zid sends HMAC-SHA256 signature in X-Zid-Signature or X-Hub-Signature-256.
    TODO: Confirm header name from https://docs.zid.sa/reference/webhooks#security
    """
    body = await request.body()

    # Accept either header — whichever Zid sends
    sig = x_zid_signature or x_hub_signature_256
    if not verify_zid_signature(body, sig):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Zid may send event at top level or inside payload.event
    event = payload.get("event") or payload.get("type")
    if not event:
        raise HTTPException(status_code=400, detail="Missing event field in payload")

    result = await handle_zid_webhook(event, payload, db=None)
    return JSONResponse(content={"received": True, **result})
