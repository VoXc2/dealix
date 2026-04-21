"""
Salla FastAPI Routes:
- GET  /auth/salla/install   → Redirect merchant to Salla authorize
- GET  /auth/salla/callback  → OAuth callback
- POST /webhooks/salla       → Salla webhook receiver
"""
import os
import secrets
import logging
from fastapi import APIRouter, Request, HTTPException, Header, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from .oauth import SallaOAuth
from .webhooks import handle_salla_webhook, verify_salla_signature

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["salla"])

# In-memory state store (replace with Redis in prod)
_states: dict = {}


@router.get("/auth/salla/install")
async def salla_install():
    """Entry point — merchant clicks 'Install Dealix' from Salla App Store."""
    oauth = SallaOAuth()
    if not oauth.client_id:
        raise HTTPException(500, "Salla integration not configured")
    state = secrets.token_urlsafe(32)
    _states[state] = True
    url = oauth.authorize_url(state=state)
    return RedirectResponse(url=url)


@router.get("/auth/salla/callback")
async def salla_callback(code: str, state: str):
    """Salla redirects here after merchant authorizes. Exchange code for tokens."""
    if state not in _states:
        raise HTTPException(400, "Invalid state parameter")
    _states.pop(state, None)

    oauth = SallaOAuth()
    try:
        tokens = await oauth.exchange_code(code)
    except Exception as e:
        logger.error(f"Salla token exchange failed: {e}")
        raise HTTPException(400, f"Token exchange failed: {e}")

    # TODO: Store tokens in DB (salla_merchants table)
    logger.info(f"✅ Salla authorized: scope={tokens.get('scope')}")

    # Redirect to Dealix dashboard with success flag
    dashboard = os.getenv("DASHBOARD_URL", "https://dealix.sa/dashboard")
    return RedirectResponse(url=f"{dashboard}?salla=connected")


@router.post("/webhooks/salla")
async def salla_webhook(request: Request, x_salla_signature: str = Header(default="")):
    """Receive webhook events from Salla."""
    body = await request.body()

    if not verify_salla_signature(body, x_salla_signature):
        raise HTTPException(401, "Invalid signature")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid JSON")

    event = payload.get("event")
    if not event:
        raise HTTPException(400, "Missing event field")

    result = await handle_salla_webhook(event, payload, db=None)
    return JSONResponse(content={"received": True, **result})
