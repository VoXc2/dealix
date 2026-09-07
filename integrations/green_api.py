"""GREEN-API transitional WhatsApp transport adapter.

This module intentionally contains transport-only logic. It does not own CRM,
consent, commercial authority, or response policy. GREEN-API is used as a
bounded interim transport until the canonical Meta WhatsApp Business Platform
path is activated.

Security contract:
- production/staging webhook calls are accepted only with a configured
  ``GREEN_API_WEBHOOK_TOKEN`` and matching Authorization header;
- when ``GREEN_API_INSTANCE_ID`` is configured, webhook payloads from any other
  instance are rejected;
- group chats are ignored by default so customer intake cannot be triggered by
  unrelated group traffic;
- parsing is side-effect free; the API router owns routing into Dealix.
"""

from __future__ import annotations

import hmac
import os
import re
from dataclasses import dataclass
from typing import Any

_DIGITS = re.compile(r"\D+")


@dataclass(frozen=True)
class GreenApiInbound:
    """Normalized direct-message envelope produced from a GREEN-API webhook."""

    message_id: str
    phone: str
    contact_name: str
    text: str
    timestamp: int | None
    instance_id: str
    raw_type: str


def configured_webhook_token() -> str:
    """Return the configured webhook token without logging it."""
    return os.getenv("GREEN_API_WEBHOOK_TOKEN", "").strip()


def verify_webhook_authorization(authorization: str, token: str | None = None) -> bool:
    """Verify GREEN-API Webhook URL Token using constant-time comparison.

    GREEN-API sends the configured Webhook URL Token through the Authorization
    header. If no scheme is supplied in GREEN-API settings, Bearer is the
    documented default. Dealix accepts only the Bearer form to keep one
    unambiguous production contract.
    """

    expected = (token if token is not None else configured_webhook_token()).strip()
    if not expected:
        return False
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        return False
    supplied = authorization[len(prefix) :].strip()
    return bool(supplied) and hmac.compare_digest(supplied, expected)


def payload_instance_matches(payload: dict[str, Any], expected: str | None = None) -> bool:
    """Bind a webhook to the configured instance when an instance is known."""

    configured = (expected if expected is not None else os.getenv("GREEN_API_INSTANCE_ID", "")).strip()
    if not configured:
        return True
    actual = str((payload.get("instanceData") or {}).get("idInstance") or "").strip()
    return bool(actual) and hmac.compare_digest(actual, configured)


def _direct_phone(sender: str, chat_id: str) -> str | None:
    """Return E.164-like digits for direct chats; reject groups/broadcasts."""

    candidate = sender or chat_id
    if not candidate:
        return None
    if candidate.endswith("@g.us") or candidate.endswith("@broadcast"):
        return None
    if "@" in candidate:
        candidate = candidate.split("@", 1)[0]
    digits = _DIGITS.sub("", candidate)
    return digits or None


def _extract_text(message_data: dict[str, Any]) -> str:
    """Extract user-visible text from common GREEN-API text envelopes."""

    msg_type = str(message_data.get("typeMessage") or "")
    if msg_type == "textMessage":
        return str((message_data.get("textMessageData") or {}).get("textMessage") or "").strip()

    # URL/extended/quoted messages carry their user text in extendedTextMessageData.
    extended = message_data.get("extendedTextMessageData") or {}
    if isinstance(extended, dict):
        text = str(extended.get("text") or "").strip()
        if text:
            return text

    # Some file/media messages include a caption. Captions are safe to route as
    # text while the binary remains outside the intake path.
    file_data = message_data.get("fileMessageData") or {}
    if isinstance(file_data, dict):
        return str(file_data.get("caption") or "").strip()

    return ""


def parse_incoming(payload: dict[str, Any]) -> GreenApiInbound | None:
    """Normalize one direct incoming GREEN-API message, otherwise return None."""

    if payload.get("typeWebhook") != "incomingMessageReceived":
        return None

    sender_data = payload.get("senderData") or {}
    message_data = payload.get("messageData") or {}
    if not isinstance(sender_data, dict) or not isinstance(message_data, dict):
        return None

    phone = _direct_phone(
        str(sender_data.get("sender") or ""),
        str(sender_data.get("chatId") or ""),
    )
    text = _extract_text(message_data)
    if not phone or not text:
        return None

    raw_timestamp = payload.get("timestamp")
    try:
        timestamp = int(raw_timestamp) if raw_timestamp is not None else None
    except (TypeError, ValueError):
        timestamp = None

    instance_id = str((payload.get("instanceData") or {}).get("idInstance") or "")
    contact_name = str(
        sender_data.get("senderContactName")
        or sender_data.get("senderName")
        or sender_data.get("chatName")
        or ""
    ).strip()

    return GreenApiInbound(
        message_id=str(payload.get("idMessage") or "").strip(),
        phone=phone,
        contact_name=contact_name,
        text=text,
        timestamp=timestamp,
        instance_id=instance_id,
        raw_type=str(message_data.get("typeMessage") or ""),
    )
