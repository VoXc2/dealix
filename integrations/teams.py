"""Microsoft Teams integration — notifications via incoming webhook.

تكامل Microsoft Teams — إشعارات عبر webhook وارد.

Docs: https://learn.microsoft.com/microsoftteams/platform/webhooks-and-connectors/
"""

from __future__ import annotations

from dataclasses import dataclass

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class TeamsResult:
    success: bool
    error: str | None = None
    status_code: int | None = None


class TeamsClient:
    """Posts MessageCard payloads to a Teams incoming-webhook URL."""

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return bool(self.settings.teams_webhook_url)

    def _card(self, title: str, text: str) -> dict[str, object]:
        return {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "title": title,
            "text": text,
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def post_message(self, title: str, text: str) -> TeamsResult:
        """Post a notification card to Teams. No-op when unconfigured."""
        if not self.configured:
            return TeamsResult(success=False, error="teams_not_configured")
        url = self.settings.teams_webhook_url
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(url, json=self._card(title, text))  # type: ignore[arg-type]
                resp.raise_for_status()
            logger.info("teams_message_sent", title=title)
            return TeamsResult(success=True, status_code=resp.status_code)
        except Exception as e:  # noqa: BLE001
            logger.exception("teams_post_failed", error=str(e))
            return TeamsResult(success=False, error=str(e))


__all__ = ["TeamsClient", "TeamsResult"]
