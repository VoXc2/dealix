"""Slack integration — notifications and approval pings.

تكامل Slack — إشعارات وتنبيهات الموافقات.

Docs: https://api.slack.com/methods/chat.postMessage
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SlackResult:
    success: bool
    channel: str | None = None
    error: str | None = None
    raw: dict[str, Any] | None = None


class SlackClient:
    """Thin async client for Slack Web API (chat.postMessage)."""

    BASE_URL = "https://slack.com/api"

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return self.settings.slack_bot_token is not None

    def _headers(self) -> dict[str, str]:
        token = self.settings.slack_bot_token.get_secret_value()  # type: ignore[union-attr]
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def post_message(self, channel: str, text: str) -> SlackResult:
        """Post a message to a Slack channel. No-op when unconfigured."""
        if not self.configured:
            return SlackResult(success=False, channel=channel, error="slack_not_configured")
        url = f"{self.BASE_URL}/chat.postMessage"
        payload = {"channel": channel, "text": text}
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(url, json=payload, headers=self._headers())
                resp.raise_for_status()
                data = resp.json()
            if not data.get("ok"):
                return SlackResult(
                    success=False, channel=channel, error=str(data.get("error")), raw=data
                )
            logger.info("slack_message_sent", channel=channel)
            return SlackResult(success=True, channel=channel, raw=data)
        except Exception as e:  # noqa: BLE001
            logger.exception("slack_post_failed", error=str(e))
            return SlackResult(success=False, channel=channel, error=str(e))


__all__ = ["SlackClient", "SlackResult"]
