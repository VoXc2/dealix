"""
LinkedIn integration — SAFE by default.

⚠️ LinkedIn's ToS strictly forbids scraping and aggressive automation.
This module intentionally ships disabled and only exposes an interface
for manually curated posting workflows (e.g., via official LinkedIn API
with a Marketing Developer Platform app, or via Zapier/n8n using user-owned
access tokens).

استخدم هذه الوحدة فقط ضمن الالتزام بشروط LinkedIn الرسمية.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class LinkedInPostResult:
    success: bool
    disabled: bool
    reason: str
    post_urn: str | None = None


class LinkedInClient:
    """Disabled by default — explicit opt-in required via subclass."""

    def __init__(self) -> None:
        self._enabled = False

    async def post_text(self, text: str) -> LinkedInPostResult:
        """
        Post a text update. Disabled by default.
        Enable by implementing a subclass that uses the official LinkedIn API
        with user-granted OAuth tokens.
        """
        logger.warning("linkedin_post_attempted_while_disabled")
        return LinkedInPostResult(
            success=False,
            disabled=True,
            reason=(
                "LinkedIn integration is disabled by default for ToS compliance. "
                "Use the official LinkedIn Marketing API with user OAuth, or "
                "route posts through n8n/Zapier with a user-owned connection."
            ),
        )

    async def send_auto_dm(self, *, recipient_urn: str, text: str) -> LinkedInPostResult:
        """
        Auto-DM is permanently disabled. The linkedin_allow_auto_dm flag is a
        belt-and-suspenders check — even if a future caller flips it to True,
        LinkedIn's ToS forbids automation, so this method always returns disabled.
        """
        from core.config.settings import get_settings
        flag_on = get_settings().linkedin_allow_auto_dm
        logger.warning("linkedin_auto_dm_blocked flag_on=%s", flag_on)
        return LinkedInPostResult(
            success=False,
            disabled=True,
            reason=(
                "LinkedIn auto-DM is forbidden by LinkedIn's User Agreement. "
                "linkedin_allow_auto_dm=False is enforced; manual outreach only."
            ),
        )
