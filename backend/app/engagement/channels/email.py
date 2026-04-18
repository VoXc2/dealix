"""
Dealix — EmailAgent
====================
Channel agent for Email via SendGrid (primary) with Gmail API (alternative).

Supports:
  - send()              — HTML + plain text multipart
  - receive()           — parse inbound email webhook
  - reply()             — LLM-generated reply
  - open/click tracking hooks
  - Threading support (References + In-Reply-To headers)

SendGrid API reference:
  POST https://api.sendgrid.com/v3/mail/send

Gmail API reference (alternative):
  POST https://gmail.googleapis.com/gmail/v1/users/me/messages/send
"""

from __future__ import annotations

import base64
import email as email_lib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

logger = logging.getLogger("dealix.engagement.email")

_SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


class EmailAgent(BaseEngagementAgent):
    """
    Email channel agent — cold outreach, nurture, and follow-up.

    Supports SendGrid (primary) and Gmail API (alternative).
    Dependency-injected settings.
    """

    channel = ChannelType.EMAIL

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
        Send a plain-text email. Subject is derived from the first line of message
        or defaults to a generic subject.

        For HTML emails with subjects and threading, use send_email() directly.
        """
        lines = message.strip().splitlines()
        subject = lines[0] if lines else "رسالة من Dealix"
        body_plain = "\n".join(lines[1:]).strip() if len(lines) > 1 else message

        return await self.send_email(
            to=to,
            subject=subject,
            body_plain=body_plain,
            body_html=_plain_to_html(body_plain),
            context=context,
        )

    async def receive(self, payload: dict[str, Any]) -> IncomingMessage:
        """
        Parse an inbound email webhook payload.

        Supports:
          - SendGrid Inbound Parse webhook (multipart/form-data)
          - Generic JSON payload with "from", "subject", "text"/"html" keys
        """
        # SendGrid Inbound Parse format
        from_addr = (
            payload.get("from")
            or payload.get("sender_ip", "unknown@unknown.com")
        )
        subject = payload.get("subject", "")
        body = payload.get("text") or payload.get("body", "")
        message_id = payload.get("headers", {}).get("Message-ID") if isinstance(
            payload.get("headers"), dict
        ) else payload.get("message_id")

        # Parse "Name <email>" format
        parsed_from = email_lib.utils.parseaddr(from_addr)
        name = parsed_from[0] or None
        address = parsed_from[1] or from_addr

        full_body = f"Subject: {subject}\n\n{body}".strip() if subject else body.strip()

        return IncomingMessage(
            channel=ChannelType.EMAIL,
            from_address=address,
            body=full_body,
            provider_message_id=message_id,
            profile_name=name,
            raw_payload=dict(payload),
        )

    # ── Rich email send ──────────────────────────────────────

    async def send_email(
        self,
        to: str,
        subject: str,
        body_plain: str,
        body_html: str | None = None,
        context: AgentContext | None = None,
        in_reply_to: str | None = None,
        references: list[str] | None = None,
        tracking: bool = True,
    ) -> DeliveryReceipt:
        """
        Send a multipart HTML + plain email via SendGrid.

        Args:
            to:           Recipient email address.
            subject:      Email subject line.
            body_plain:   Plain-text body.
            body_html:    HTML body (auto-generated from plain if None).
            context:      AgentContext for observability.
            in_reply_to:  Message-ID of the email being replied to (threading).
            references:   List of Message-IDs for thread References header.
            tracking:     Enable SendGrid open + click tracking.
        """
        if not self.settings.sendgrid_api_key:
            logger.info("[DRY RUN] Email → %s: %s", to, subject)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.SENT,
                provider_message_id="dry_run",
                metadata={"subject": subject},
            )

        html = body_html or _plain_to_html(body_plain)

        payload: dict[str, Any] = {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {
                "email": self.settings.sendgrid_from_email,
                "name": self.settings.sendgrid_from_name,
            },
            "subject": subject,
            "content": [
                {"type": "text/plain", "value": body_plain},
                {"type": "text/html", "value": html},
            ],
            "tracking_settings": {
                "click_tracking": {"enable": tracking, "enable_text": False},
                "open_tracking": {"enable": tracking},
            },
        }

        # Threading headers
        if in_reply_to or references:
            headers: dict[str, str] = {}
            if in_reply_to:
                headers["In-Reply-To"] = in_reply_to
            if references:
                headers["References"] = " ".join(references)
            payload["headers"] = headers

        headers_http = {
            "Authorization": f"Bearer {self.settings.sendgrid_api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(
                    _SENDGRID_URL, json=payload, headers=headers_http
                )
                resp.raise_for_status()
                # SendGrid returns 202 with empty body on success
                msg_id = resp.headers.get("X-Message-Id")
                return DeliveryReceipt(
                    channel=self.channel,
                    to=to,
                    status=DeliveryStatus.SENT,
                    provider_message_id=msg_id,
                    metadata={"subject": subject},
                )
        except httpx.HTTPStatusError as exc:
            error_text = exc.response.text if exc.response else str(exc)
            logger.error("SendGrid send failed for %s: %s", to, error_text)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.FAILED,
                error=error_text,
            )

    # ── Open / Click tracking hooks ──────────────────────────

    async def handle_open_event(self, payload: dict[str, Any]) -> None:
        """
        Handle a SendGrid email open event.

        Payload fields (from SendGrid Event Webhook):
          email, event="open", sg_message_id, timestamp
        """
        email_addr = payload.get("email", "")
        sg_id = payload.get("sg_message_id", "")
        logger.info("Email open: %s (msg=%s)", email_addr, sg_id)

        await self.memory.upsert_conversation(
            channel=self.channel.value,
            address=email_addr,
            intent="opened_email",
        )

    async def handle_click_event(self, payload: dict[str, Any]) -> None:
        """
        Handle a SendGrid link click event.

        Payload fields: email, event="click", url, sg_message_id, timestamp
        """
        email_addr = payload.get("email", "")
        url = payload.get("url", "")
        logger.info("Email click: %s → %s", email_addr, url)

        await self.memory.upsert_conversation(
            channel=self.channel.value,
            address=email_addr,
            intent="clicked_link",
        )

    # ── Gmail API alternative ────────────────────────────────

    async def send_via_gmail(
        self,
        to: str,
        subject: str,
        body_plain: str,
        body_html: str | None = None,
        access_token: str | None = None,
    ) -> DeliveryReceipt:
        """
        Send an email via Gmail API (alternative to SendGrid).

        Requires a valid OAuth2 access token for the Gmail account.
        Uses MIME multipart encoding as required by the Gmail API.
        """
        if not access_token:
            logger.warning("Gmail API: no access token provided")
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.FAILED,
                error="No Gmail access token",
            )

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["To"] = to
        msg["From"] = self.settings.sendgrid_from_email  # reuse from setting

        msg.attach(MIMEText(body_plain, "plain", "utf-8"))
        if body_html:
            msg.attach(MIMEText(body_html, "html", "utf-8"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        payload = {"raw": raw}

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                result = resp.json()
                return DeliveryReceipt(
                    channel=self.channel,
                    to=to,
                    status=DeliveryStatus.SENT,
                    provider_message_id=result.get("id"),
                    metadata={"thread_id": result.get("threadId")},
                )
        except httpx.HTTPStatusError as exc:
            error_text = exc.response.text if exc.response else str(exc)
            logger.error("Gmail API send failed for %s: %s", to, error_text)
            return DeliveryReceipt(
                channel=self.channel,
                to=to,
                status=DeliveryStatus.FAILED,
                error=error_text,
            )


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _plain_to_html(text: str) -> str:
    """Convert plain text to minimal HTML (paragraph tags, line breaks)."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    html_parts = ["<html><body dir='rtl'>"]
    for para in paragraphs:
        lines = para.splitlines()
        html_parts.append("<p>" + "<br>".join(lines) + "</p>")
    html_parts.append("</body></html>")
    return "\n".join(html_parts)
