"""Incoming webhooks — WhatsApp, HubSpot, Calendly."""

from __future__ import annotations

import json
import os
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Query, Request

from api.dependencies import get_acquisition_pipeline
from auto_client_acquisition.agents.intake import LeadSource
from core.config.settings import get_settings
from core.logging import get_logger
from integrations.whatsapp import WhatsAppClient

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


# ── WhatsApp ───────────────────────────────────────────────────
@router.get("/whatsapp")
async def whatsapp_verify(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
) -> Any:
    """Meta WhatsApp webhook verification."""
    client = WhatsAppClient()
    challenge = client.verify_webhook(hub_mode, hub_verify_token, hub_challenge)
    if challenge is None:
        raise HTTPException(status_code=403, detail="Invalid verification token")
    return int(challenge)


@router.post("/whatsapp")
async def whatsapp_incoming(
    request: Request,
    x_hub_signature_256: str = Header(default=""),
) -> dict[str, Any]:
    """Handle incoming WhatsApp messages — route them as leads."""
    body = await request.body()
    client = WhatsAppClient()
    settings = get_settings()
    has_secret = bool(client.settings.whatsapp_app_secret)

    # Staging/production with app secret: require valid Meta signature always.
    if has_secret and settings.app_env in ("staging", "production"):
        if not x_hub_signature_256 or not client.verify_signature(body, x_hub_signature_256):
            logger.warning("whatsapp_missing_or_invalid_signature_strict_env")
            raise HTTPException(status_code=403, detail="missing_or_invalid_signature")
    elif x_hub_signature_256 and has_secret and not client.verify_signature(body, x_hub_signature_256):
        logger.warning("whatsapp_invalid_signature")
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}") from e

    messages = client.parse_incoming(payload)
    pipeline = get_acquisition_pipeline()
    processed = []

    for msg in messages:
        if msg["type"] != "text" or not msg.get("text"):
            continue
        lead_payload = {
            "name": msg.get("contact_name") or "",
            "phone": f"+{msg['from']}",
            "message": msg["text"],
            "company": "",
        }
        result = await pipeline.run(payload=lead_payload, source=LeadSource.WHATSAPP)
        processed.append(result.lead.id)
    logger.info("whatsapp_webhook_processed", count=len(processed))
    return {"processed": processed, "count": len(processed)}


# ── Calendly ───────────────────────────────────────────────────
@router.post("/calendly")
async def calendly_webhook(
    request: Request,
    calendly_webhook_signature: str = Header(default="", alias="Calendly-Webhook-Signature"),
) -> dict[str, Any]:
    """Receive Calendly event lifecycle notifications."""
    from api.security.webhook_signatures import verify_calendly_signature
    from dealix.revenue_ops_autopilot.webhook_handlers import handle_calendly_webhook

    body = await request.body()
    settings = get_settings()
    has_secret = bool(getattr(settings, "calendly_webhook_secret", None) or os.environ.get("CALENDLY_WEBHOOK_SECRET"))

    if has_secret and settings.app_env in ("staging", "production"):
        if not verify_calendly_signature(body=body, header=calendly_webhook_signature or None):
            logger.warning("calendly_missing_or_invalid_signature_strict_env")
            raise HTTPException(status_code=403, detail="missing_or_invalid_signature")
    elif calendly_webhook_signature and has_secret:
        if not verify_calendly_signature(body=body, header=calendly_webhook_signature):
            logger.warning("calendly_invalid_signature")
            raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}") from exc

    event = payload.get("event") or payload.get("type") or "unknown"
    logger.info("calendly_webhook_received", event=event)
    return handle_calendly_webhook(payload)


# ── HubSpot ────────────────────────────────────────────────────
@router.post("/hubspot")
async def hubspot_webhook(
    request: Request,
    x_hubspot_signature_v3: str = Header(default="", alias="X-HubSpot-Signature-v3"),
    x_hubspot_request_timestamp: str = Header(default="", alias="X-HubSpot-Request-Timestamp"),
) -> dict[str, Any]:
    """Receive HubSpot subscription events."""
    from api.security.webhook_signatures import verify_hubspot_signature
    from dealix.revenue_ops_autopilot.webhook_handlers import handle_hubspot_webhook

    body = await request.body()
    settings = get_settings()
    has_secret = bool(getattr(settings, "hubspot_app_secret", None) or os.environ.get("HUBSPOT_APP_SECRET"))
    url = str(request.url)

    if has_secret and settings.app_env in ("staging", "production"):
        if not verify_hubspot_signature(
            method=request.method,
            url=url,
            body=body,
            timestamp=x_hubspot_request_timestamp or None,
            signature=x_hubspot_signature_v3 or None,
        ):
            logger.warning("hubspot_missing_or_invalid_signature_strict_env")
            raise HTTPException(status_code=403, detail="missing_or_invalid_signature")
    elif x_hubspot_signature_v3 and has_secret:
        if not verify_hubspot_signature(
            method=request.method,
            url=url,
            body=body,
            timestamp=x_hubspot_request_timestamp or None,
            signature=x_hubspot_signature_v3 or None,
        ):
            logger.warning("hubspot_invalid_signature")
            raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}") from exc

    logger.info(
        "hubspot_webhook_received", n_events=len(payload) if isinstance(payload, list) else 1
    )
    return handle_hubspot_webhook(payload)
