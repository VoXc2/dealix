"""
Dealix — WhatsAppAgent
=======================
Channel agent for WhatsApp Business via Twilio.

Supports:
  - send_template(sid, variables)       — approved template messages
  - send_freeform(to, body)             — free-form (only inside 24h session window)
  - handle_inbound_webhook(form_data)   — returns TwiML reply string
  - 24-hour session window tracking

WhatsApp Business Policy notes:
  - Outbound messages to users who have NOT sent a message in the last 24h
    MUST use a pre-approved Message Service template (send_template).
  - Freeform text can only be sent within 24h of the user's last inbound message.

Twilio API reference:
  POST https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any
from xml.sax.saxutils import escape as xml_escape

import httpx

from ..base import (
    AgentContext,
    BaseEngagementAgent,
    ChannelType,
    DeliveryReceipt,
    DeliveryStatus,
    EngagementSettings,
    IncomingMessage,
)
from ..memory import ConversationMemory
from ..llm import LLMGateway

logger = logging.getLogger("dealix.engagement.whatsapp")

_TWILIO_MESSAGES_URL = (
    "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
)

# How long after the last user message the freeform window remains open (24h)
_SESSION_WINDOW_HOURS = 24


class WhatsAppAgent(BaseEngagementAgent):
    """
    WhatsApp Business channel agent — the primary Gulf sales channel.

    Dependency-injected:
        settings: EngagementSettings  (Twilio creds, rate limits, etc.)
        memory:   ConversationMemory  (optional — lazily created if None)
        llm:      LLMGateway          (optional — lazily created if None)
    """

    channel = ChannelType.WHATSAPP

    def __init__(
        self,
        settings: EngagementSettings,
        memory: ConversationMemory | None = None,
        llm: LLMGateway | None = None,
    ) -> None:
        super().__init__(settings=settings, memory=memory, llm=llm)

    # ── Abstract interface implementation ────────────────────

    async def send(
        self, to: str, message: str, context: AgentContext
    ) -> DeliveryReceipt:
        """
        Send a WhatsApp message to the given phone number.
        Automatically decides freeform vs. template based on session window.

        `to` should be a phone in E.164 format, e.g. "+966512345678".
        The Twilio WhatsApp prefix ("whatsapp:") is added automatically.
        """
        in_window = await self._in_session_window(to)

        if in_window:
            return await self.send_freeform(to, message)
        else:
            # Outside 24h window — must use a template.
            # For now we attempt freeform (works in Sandbox);
            # in production replace with send_template().
            logger.warning(
                "Sending freeform to %s outside session window (sandbox mode). "
                "Use send_template() in production.",
                to,
            )
            return await self.send_freeform(to, message)

    async def receive(self, payload: dict[str, Any]) -> IncomingMessage:
        """
        Parse a Twilio WhatsApp inbound form payload (application/x-www-form-urlencoded).

        Expected keys: From, Body, MessageSid, ProfileName, NumMedia, MediaUrl0, ...
        """
        raw_from: str = payload.get("From", "")
        phone = raw_from.replace("whatsapp:", "").strip()
        body: str = payload.get("Body", "").strip()
        sid: str | None = payload.get("MessageSid")
        profile_name: str | None = payload.get("ProfileName")

        media_urls: list[str] = []
        num_media = int(payload.get("NumMedia", "0"))
        for i in range(num_media):
            url = payload.get(f"MediaUrl{i}")
            if url:
                media_urls.append(url)

        incoming = IncomingMessage(
            channel=ChannelType.WHATSAPP,
            from_address=phone,
            body=body,
            provider_message_id=sid,
            profile_name=profile_name,
            media_urls=media_urls,
            raw_payload=dict(payload),
        )

        # Update session window (user has just messaged us → open 24h window)
        expires = datetime.now(timezone.utc) + timedelta(hours=_SESSION_WINDOW_HOURS)
        await self.memory.upsert_conversation(
            channel=self.channel.value,
            address=phone,
            session_active=True,
            session_expires=expires.isoformat(),
        )

        return incoming

    # ── Freeform + template helpers ──────────────────────────

    async def send_freeform(self, to: str, body: str) -> DeliveryReceipt:
        """
        Send a free-form WhatsApp message via Twilio.
        Only valid within the 24-hour session window.
        """
        if not self.settings.twilio_account_sid or not self.settings.twilio_auth_token:
            logger.info("[DRY RUN] WhatsApp freeform → %s: %.80s…", to, body)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.SENT,
                provider_message_id="dry_run",
            )

        wa_to = f"whatsapp:{to}" if not to.startswith("whatsapp:") else to
        wa_from = self.settings.twilio_whatsapp_number

        url = _TWILIO_MESSAGES_URL.format(
            account_sid=self.settings.twilio_account_sid
        )
        data = {"From": wa_from, "To": wa_to, "Body": body}
        auth = (
            self.settings.twilio_account_sid,
            self.settings.twilio_auth_token,
        )

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(url, data=data, auth=auth)
                resp.raise_for_status()
                result = resp.json()
                return DeliveryReceipt(
                    channel=self.channel,
                    to=to,
                    status=DeliveryStatus.SENT,
                    provider_message_id=result.get("sid"),
                    metadata={"twilio_status": result.get("status")},
                )
        except httpx.HTTPStatusError as exc:
            error_text = exc.response.text if exc.response else str(exc)
            logger.error("Twilio send failed for %s: %s", to, error_text)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.FAILED,
                error=error_text,
            )

    async def send_template(
        self,
        to: str,
        content_sid: str,
        variables: dict[str, str] | None = None,
    ) -> DeliveryReceipt:
        """
        Send a pre-approved WhatsApp template (Content Template).
        Required for outbound messages outside the 24-hour session window.

        Args:
            to:          Recipient phone in E.164 format.
            content_sid: Twilio Content Template SID (HX...).
            variables:   Template variable substitutions (e.g. {"1": "Ahmed"}).
        """
        import json

        if not self.settings.twilio_account_sid or not self.settings.twilio_auth_token:
            logger.info("[DRY RUN] WhatsApp template %s → %s", content_sid, to)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.SENT,
                provider_message_id="dry_run_template",
            )

        wa_to = f"whatsapp:{to}" if not to.startswith("whatsapp:") else to
        wa_from = self.settings.twilio_whatsapp_number

        url = _TWILIO_MESSAGES_URL.format(
            account_sid=self.settings.twilio_account_sid
        )
        data: dict[str, str] = {
            "From": wa_from,
            "To": wa_to,
            "ContentSid": content_sid,
        }
        if variables:
            data["ContentVariables"] = json.dumps(variables)

        auth = (
            self.settings.twilio_account_sid,
            self.settings.twilio_auth_token,
        )

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(url, data=data, auth=auth)
                resp.raise_for_status()
                result = resp.json()
                return DeliveryReceipt(
                    channel=self.channel,
                    to=to,
                    status=DeliveryStatus.SENT,
                    provider_message_id=result.get("sid"),
                    metadata={
                        "content_sid": content_sid,
                        "twilio_status": result.get("status"),
                    },
                )
        except httpx.HTTPStatusError as exc:
            error_text = exc.response.text if exc.response else str(exc)
            logger.error("Template send failed for %s (sid=%s): %s", to, content_sid, error_text)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.FAILED,
                error=error_text,
            )

    # ── Inbound webhook handler ──────────────────────────────

    async def handle_inbound_webhook(
        self, form_data: dict[str, Any]
    ) -> str:
        """
        Process an inbound Twilio WhatsApp webhook and return a TwiML response.

        Flow:
          1. Parse payload → IncomingMessage
          2. Persist lead + message to memory
          3. Generate reply via LLM
          4. Persist outbound reply
          5. Return TwiML XML string

        Returns TwiML XML string (media_type="application/xml").
        """
        incoming = await self.receive(form_data)
        context = AgentContext(
            lead_phone=incoming.from_address,
            lead_name=incoming.profile_name,
            opt_in=True,
        )

        # Persist inbound
        await self.persist_inbound(incoming, context)

        # Generate reply
        reply_text = await self.reply(incoming)

        # Persist outbound
        await self.memory.save_message(
            channel=self.channel.value,
            address=incoming.from_address,
            direction="out",
            body=reply_text,
        )

        return _build_twiml(reply_text)

    # ── Session window tracking ──────────────────────────────

    async def _in_session_window(self, phone: str) -> bool:
        """
        Return True if the user has sent a message within the last 24 hours
        (i.e. we are inside the WhatsApp freeform session window).
        """
        conv = await self.memory.get_conversation(
            channel=self.channel.value,
            address=phone,
        )
        if not conv:
            return False

        expires_str: str | None = conv.get("session_expires")
        if not expires_str:
            return False

        try:
            expires = datetime.fromisoformat(expires_str)
            if expires.tzinfo is None:
                expires = expires.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) < expires
        except ValueError:
            return False


# ─────────────────────────────────────────────────────────────
# TwiML builder
# ─────────────────────────────────────────────────────────────

def _build_twiml(message: str) -> str:
    """Build a minimal TwiML <Response><Message> XML."""
    safe = xml_escape(message)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<Response>\n"
        f"    <Message>{safe}</Message>\n"
        "</Response>"
    )
