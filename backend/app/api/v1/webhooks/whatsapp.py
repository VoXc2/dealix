"""
Dealix — WhatsApp Webhook Router
==================================
FastAPI router that handles WhatsApp inbound messages from Twilio.

This replaces the standalone `whatsapp_webhook.py` pattern, using the
production-ready WhatsAppAgent from the engagement framework.

Endpoints:
  POST /api/v1/webhooks/whatsapp          — Twilio inbound webhook (TwiML response)
  POST /api/v1/webhooks/whatsapp/status   — Twilio message status callback
  GET  /api/v1/webhooks/whatsapp/leads    — Debug: list recent WhatsApp leads
  POST /api/v1/webhooks/whatsapp/send     — Outbound send (internal API)

Security:
  - In production, validate Twilio request signatures using X-Twilio-Signature.
  - The /send endpoint should require authentication (DEALIX_INTERNAL_API_TOKEN).

Usage (Twilio Sandbox):
  1. Start the server: uvicorn app.main:app --reload --port 8000
  2. Expose via tunnel: cloudflared tunnel --url http://localhost:8000
  3. Set Twilio Sandbox webhook URL:
     https://<tunnel>.trycloudflare.com/api/v1/webhooks/whatsapp
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any, Annotated

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse

from app.engagement.base import EngagementSettings, AgentContext
from app.engagement.memory import ConversationMemory
from app.engagement.llm import LLMGateway
from app.engagement.channels.whatsapp import WhatsAppAgent

logger = logging.getLogger("dealix.api.webhooks.whatsapp")

router = APIRouter()


# ─────────────────────────────────────────────────────────────
# Dependency injection
# ─────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _get_settings() -> EngagementSettings:
    return EngagementSettings()


_memory: ConversationMemory | None = None
_agent: WhatsAppAgent | None = None


async def get_agent() -> WhatsAppAgent:
    """
    FastAPI dependency that returns a lazily-initialised WhatsAppAgent.
    Memory is initialised on first request (creates SQLite tables if needed).
    """
    global _memory, _agent
    if _agent is None:
        settings = _get_settings()
        _memory = ConversationMemory(db_path=settings.dealix_db)
        await _memory.init()
        llm = LLMGateway(settings=settings)
        _agent = WhatsAppAgent(settings=settings, memory=_memory, llm=llm)
    return _agent


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@router.post(
    "",
    response_class=PlainTextResponse,
    summary="Twilio WhatsApp inbound webhook",
    description=(
        "Receives inbound WhatsApp messages from Twilio Sandbox or Business API. "
        "Generates an Arabic reply via LLM and returns TwiML."
    ),
)
async def whatsapp_webhook(
    request: Request,
    From: Annotated[str, Form()] = "",
    Body: Annotated[str, Form()] = "",
    MessageSid: Annotated[str | None, Form()] = None,
    ProfileName: Annotated[str | None, Form()] = None,
    NumMedia: Annotated[str, Form()] = "0",
    agent: WhatsAppAgent = Depends(get_agent),
) -> PlainTextResponse:
    """
    Main Twilio WhatsApp webhook.

    Flow:
      1. Parse form data → IncomingMessage
      2. Persist lead + inbound message in SQLite
      3. Generate reply via Groq LLM (Arabic)
      4. Persist outbound reply
      5. Return TwiML so Twilio sends the reply

    Twilio form fields used:
      From       — sender phone (e.g. "whatsapp:+966512345678")
      Body       — message text
      MessageSid — Twilio message ID
      ProfileName — WhatsApp display name
      NumMedia   — number of media attachments
    """
    # Build form_data dict for the agent
    form_data: dict[str, Any] = {
        "From": From,
        "Body": Body,
        "MessageSid": MessageSid,
        "ProfileName": ProfileName,
        "NumMedia": NumMedia,
    }
    # Also pass any extra media URLs
    raw_form = await request.form()
    for key, value in raw_form.items():
        if key not in form_data:
            form_data[key] = str(value)

    phone = From.replace("whatsapp:", "").strip()
    logger.info("Inbound WhatsApp from %s (%s): %.100s…", phone, ProfileName, Body)

    try:
        twiml = await agent.handle_inbound_webhook(form_data)
    except Exception as exc:  # noqa: BLE001
        logger.error("Error processing WhatsApp webhook from %s: %s", phone, exc)
        # Return a safe Arabic fallback so Twilio doesn't show an error to the user
        twiml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Response>"
            "<Message>شكراً لتواصلك مع Dealix. سيرد عليك فريقنا قريباً.</Message>"
            "</Response>"
        )

    return PlainTextResponse(content=twiml, media_type="application/xml")


@router.post(
    "/status",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Twilio message status callback",
)
async def whatsapp_status_callback(
    request: Request,
    MessageSid: Annotated[str | None, Form()] = None,
    MessageStatus: Annotated[str | None, Form()] = None,
    To: Annotated[str | None, Form()] = None,
) -> None:
    """
    Receives Twilio delivery status updates for sent messages.
    (sent, delivered, read, failed, etc.)

    Configure in Twilio: Message status callback URL →
      https://<your-domain>/api/v1/webhooks/whatsapp/status
    """
    phone = (To or "").replace("whatsapp:", "").strip()
    logger.info(
        "WhatsApp status update: sid=%s status=%s to=%s",
        MessageSid, MessageStatus, phone,
    )
    # TODO: Update message status in ConversationMemory when status tracking is needed
    return None


@router.get(
    "/leads",
    summary="List recent WhatsApp leads (debug — protect in production)",
    response_class=JSONResponse,
)
async def list_whatsapp_leads(
    limit: int = 50,
    stage: str | None = None,
    agent: WhatsAppAgent = Depends(get_agent),
) -> JSONResponse:
    """
    Return recent WhatsApp leads for debugging.

    ⚠️  Protect this endpoint with authentication in production.
    """
    leads = await agent.memory.list_leads(
        channel="whatsapp",
        stage=stage,
        limit=limit,
    )
    return JSONResponse(content=leads)


@router.post(
    "/send",
    summary="Send outbound WhatsApp message (internal API)",
)
async def send_whatsapp_message(
    request: Request,
    agent: WhatsAppAgent = Depends(get_agent),
    x_internal_token: Annotated[str | None, Header()] = None,
) -> JSONResponse:
    """
    Send an outbound WhatsApp message.

    Body (JSON):
    {
      "to": "+966512345678",
      "message": "مرحباً، هذا تذكير بموعدكم...",
      "lead_name": "Ahmed",
      "company": "متجر الأفق",
      "opt_in": true
    }

    Requires X-Internal-Token header matching DEALIX_INTERNAL_API_TOKEN.
    """
    settings = _get_settings()
    # Basic auth check
    expected_token = getattr(settings, "dealix_internal_api_token", "")
    if expected_token and x_internal_token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal token",
        )

    body = await request.json()
    to: str = body.get("to", "")
    message: str = body.get("message", "")
    if not to or not message:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Fields 'to' and 'message' are required",
        )

    context = AgentContext(
        lead_phone=to,
        lead_name=body.get("lead_name"),
        company_name=body.get("company"),
        opt_in=body.get("opt_in", True),
    )

    receipt = await agent.send_with_guards(to=to, message=message, context=context)
    return JSONResponse(content=receipt.model_dump(mode="json"))
