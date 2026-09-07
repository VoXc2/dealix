"""Incoming webhooks — WhatsApp, GREEN-API, HubSpot, Calendly."""

from __future__ import annotations

import json
import os
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Query, Request

from api.dependencies import get_acquisition_pipeline
from auto_client_acquisition.agents.intake import LeadSource
from core.config.settings import get_settings
from core.logging import get_logger
from integrations.green_api import (
    parse_incoming as parse_green_api_incoming,
    payload_instance_matches as green_api_instance_matches,
    verify_webhook_authorization as verify_green_api_authorization,
)
from integrations.whatsapp import WhatsAppClient

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


async def _route_whatsapp_text(
    *,
    phone: str,
    text: str,
    contact_name: str = "",
    provider: str,
    provider_message_id: str = "",
) -> str:
    """Route one normalized WhatsApp text message into the canonical pipeline.

    Provider details are carried only as intake metadata inside the existing raw
    payload. They do not create a parallel CRM, conversation store, or consent
    authority.
    """

    pipeline = get_acquisition_pipeline()
    lead_payload = {
        "name": contact_name,
        "phone": phone,
        "message": text,
        "company": "",
        "channel": "whatsapp",
        "provider": provider,
        "provider_message_id": provider_message_id,
    }
    result = await pipeline.run(payload=lead_payload, source=LeadSource.WHATSAPP)
    return result.lead.id


# ── Meta WhatsApp Cloud API ────────────────────────────────────
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
    """Handle incoming Meta WhatsApp messages and route them as leads."""
    body = await request.body()
    client = WhatsAppClient()
    settings = get_settings()

    # SECURITY: the signature-enforcement decision must reflect the live
    # environment, not a process-wide @lru_cache snapshot of settings. If the
    # cached Settings were loaded before APP_ENV / WHATSAPP_APP_SECRET were set,
    # relying on them would silently bypass the Meta-signature gate. Resolve
    # both from os.environ first, falling back to the cached settings.
    app_secret_env = os.environ.get("WHATSAPP_APP_SECRET")
    settings_secret = settings.whatsapp_app_secret
    has_secret = bool(app_secret_env) or bool(settings_secret)
    app_env = (os.environ.get("APP_ENV") or settings.app_env or "").lower()

    # Staging/production with app secret: require valid Meta signature always.
    if has_secret and app_env in ("staging", "production"):
        if not x_hub_signature_256 or not client.verify_signature(body, x_hub_signature_256):
            logger.warning("whatsapp_missing_or_invalid_signature_strict_env")
            raise HTTPException(status_code=403, detail="missing_or_invalid_signature")
    elif x_hub_signature_256 and has_secret and not client.verify_signature(body, x_hub_signature_256):
        logger.warning("whatsapp_invalid_signature")
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}") from exc

    messages = client.parse_incoming(payload)
    processed: list[str] = []

    for msg in messages:
        if msg["type"] != "text" or not msg.get("text") or not msg.get("from"):
            continue
        lead_id = await _route_whatsapp_text(
            phone=f"+{msg['from']}",
            text=msg["text"],
            contact_name=msg.get("contact_name") or "",
            provider="meta_cloud",
            provider_message_id=msg.get("id") or "",
        )
        processed.append(lead_id)

    logger.info("whatsapp_webhook_processed", provider="meta_cloud", count=len(processed))
    return {"processed": processed, "count": len(processed)}


# ── GREEN-API transitional WhatsApp transport ──────────────────
@router.post("/green-api")
async def green_api_incoming(
    request: Request,
    authorization: str = Header(default="", alias="Authorization"),
) -> dict[str, Any]:
    """Receive one GREEN-API webhook through a fail-closed transport boundary.

    GREEN-API is a transitional provider only. This endpoint routes normalized
    direct-message text into the same Dealix WhatsApp intake used by Meta. It
    does not grant outbound, commercial, consent, or production authority.
    """

    body = await request.body()
    settings = get_settings()
    app_env = (os.environ.get("APP_ENV") or settings.app_env or "").lower()
    webhook_token = os.environ.get("GREEN_API_WEBHOOK_TOKEN", "").strip()

    # Production/staging must never expose an unauthenticated GREEN-API webhook.
    if app_env in ("staging", "production") and not webhook_token:
        logger.error("green_api_webhook_token_missing_strict_env")
        raise HTTPException(status_code=503, detail="green_api_webhook_not_configured")

    # Whenever a token exists, require it even in development so tests and local
    # environments exercise the same authorization contract.
    if webhook_token and not verify_green_api_authorization(authorization, webhook_token):
        logger.warning("green_api_invalid_authorization")
        raise HTTPException(status_code=403, detail="missing_or_invalid_authorization")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON object")

    if not green_api_instance_matches(payload):
        logger.warning("green_api_instance_mismatch")
        raise HTTPException(status_code=403, detail="green_api_instance_mismatch")

    msg = parse_green_api_incoming(payload)
    if msg is None:
        # State/outgoing/status notifications and unsupported media are accepted
        # but deliberately do not enter customer intake.
        return {"processed": [], "count": 0}

    lead_id = await _route_whatsapp_text(
        phone=f"+{msg.phone}",
        text=msg.text,
        contact_name=msg.contact_name,
        provider="green_api",
        provider_message_id=msg.message_id,
    )
    logger.info(
        "whatsapp_webhook_processed",
        provider="green_api",
        count=1,
        message_id_present=bool(msg.message_id),
    )
    return {"processed": [lead_id], "count": 1}


# ── Calendly ────────────────────────────────────────────────────
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
