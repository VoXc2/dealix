"""
Dealix — SMSAgent
==================
Channel agent for SMS via Twilio.

Supports:
  - send()         — auto-truncates to 160 chars (1 SMS segment)
  - receive()      — parse Twilio SMS inbound webhook
  - reply()        — short LLM-generated reply

SMS guidelines:
  - Use only for leads who have explicitly opted in.
  - Keep messages under 160 characters (1 SMS segment) to avoid splitting.
  - Always identify the sender (e.g. "Dealix: ...")
  - Include opt-out instructions for marketing messages ("رد STOP للإلغاء")

Twilio API reference:
  POST https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json
"""

from __future__ import annotations

import logging
from typing import Any

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

logger = logging.getLogger("dealix.engagement.sms")

_TWILIO_MESSAGES_URL = (
    "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
)

_MAX_SMS_CHARS = 160
_SMS_PREFIX = "Dealix: "
_SMS_SUFFIX_OPT_OUT = " | رد STOP للإلغاء"


class SMSAgent(BaseEngagementAgent):
    """
    SMS channel agent via Twilio.
    Short messages only — auto-truncates to fit within one SMS segment.
    """

    channel = ChannelType.SMS

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
        Send an SMS to the given phone number (E.164 format).
        Message is auto-truncated to fit within 160 characters.
        """
        truncated = _truncate_sms(message)
        return await self._send_sms(to, truncated)

    async def receive(self, payload: dict[str, Any]) -> IncomingMessage:
        """
        Parse a Twilio SMS inbound webhook (application/x-www-form-urlencoded).

        Expected keys: From, Body, MessageSid, NumMedia, MediaUrl0, ...
        """
        from_phone: str = payload.get("From", "").strip()
        body: str = payload.get("Body", "").strip()
        sid: str | None = payload.get("MessageSid")
        profile_name: str | None = payload.get("FromCity")  # Twilio provides city

        return IncomingMessage(
            channel=ChannelType.SMS,
            from_address=from_phone,
            body=body,
            provider_message_id=sid,
            profile_name=profile_name,
            raw_payload=dict(payload),
        )

    # ── SMS-specific helpers ─────────────────────────────────

    async def send_reminder(
        self,
        to: str,
        text: str,
        include_opt_out: bool = False,
    ) -> DeliveryReceipt:
        """
        Send a reminder SMS with "Dealix: " prefix.

        Args:
            to:               Recipient phone (E.164).
            text:             Message body (will be prefixed and truncated).
            include_opt_out:  Append opt-out instruction (for marketing messages).
        """
        suffix = _SMS_SUFFIX_OPT_OUT if include_opt_out else ""
        max_body = _MAX_SMS_CHARS - len(_SMS_PREFIX) - len(suffix)
        body = text[:max_body]
        full_message = f"{_SMS_PREFIX}{body}{suffix}"
        return await self._send_sms(to, full_message)

    # ── Internal Twilio call ─────────────────────────────────

    async def _send_sms(self, to: str, body: str) -> DeliveryReceipt:
        """Low-level Twilio SMS send."""
        if not self.settings.twilio_account_sid or not self.settings.twilio_auth_token:
            logger.info("[DRY RUN] SMS → %s: %.80s…", to, body)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.SENT,
                provider_message_id="dry_run",
            )

        url = _TWILIO_MESSAGES_URL.format(
            account_sid=self.settings.twilio_account_sid
        )
        data = {
            "From": self.settings.twilio_sms_number,
            "To": to,
            "Body": body,
        }
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
            logger.error("Twilio SMS send failed for %s: %s", to, error_text)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.FAILED,
                error=error_text,
            )

    # ── Reply generation (override for SMS brevity) ──────────

    async def reply(self, incoming: IncomingMessage) -> str:
        """Generate a very short SMS reply (max 140 chars)."""
        history = await self.memory.get_history(
            channel=self.channel.value,
            address=incoming.from_address,
            limit=4,
        )
        system_prompt = (
            self.llm.get_system_prompt("sms_reminder_ar")
            or "أنت مساعد مبيعات Dealix. رد بجملة واحدة قصيرة لا تتجاوز 100 حرف."
        )
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": incoming.body})
        reply = await self.llm.chat(messages=messages, max_tokens=80)
        return _truncate_sms(reply)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _truncate_sms(text: str, max_chars: int = _MAX_SMS_CHARS) -> str:
    """Truncate text to fit within an SMS segment. Appends '…' if cut."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "…"
