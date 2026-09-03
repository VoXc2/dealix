"""Legacy unified email integration — live provider execution quarantined.

This module historically supported Resend, SendGrid and SMTP directly. During
P0 trust incident #1440 that is too much authority: none of these provider paths
is bound to the canonical Governance/Approval owner, fresh ACTION_HASH, durable
idempotency ledger, or current suppression/evidence state.

The compatibility surface remains so existing callers fail closed cleanly.
No method in this module performs an external email side effect.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.config.settings import get_settings

LIVE_EMAIL_QUARANTINE_REASON = (
    "LIVE_EMAIL_PROVIDER_QUARANTINED_CANONICAL_GOVERNANCE_PROVIDER_NOT_WIRED"
)


@dataclass
class EmailResult:
    success: bool
    provider: str
    message_id: str | None = None
    error: str | None = None


class EmailClient:
    """Compatibility client whose live provider authority is fail-closed."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def _provider(self, fallback: str = "email") -> str:
        value = getattr(self.settings, "email_provider", fallback)
        return str(value or fallback)

    @staticmethod
    def _quarantined(provider: str) -> EmailResult:
        return EmailResult(
            success=False,
            provider=provider,
            message_id=None,
            error=LIVE_EMAIL_QUARANTINE_REASON,
        )

    async def send(
        self,
        *,
        to: str | list[str],
        subject: str,
        body_text: str | None = None,
        body_html: str | None = None,
        reply_to: str | None = None,
    ) -> EmailResult:
        """Fail closed regardless of configured provider or credentials."""
        _ = (to, subject, body_text, body_html, reply_to)
        return self._quarantined(self._provider())

    async def _send_resend(
        self,
        to: str | list[str],
        subject: str,
        body_text: str | None,
        body_html: str | None,
        reply_to: str | None,
    ) -> EmailResult:
        """Private compatibility path; deliberately cannot call Resend."""
        _ = (to, subject, body_text, body_html, reply_to)
        return self._quarantined("resend")

    async def _send_sendgrid(
        self,
        to: str | list[str],
        subject: str,
        body_text: str | None,
        body_html: str | None,
        reply_to: str | None,
    ) -> EmailResult:
        """Private compatibility path; deliberately cannot call SendGrid."""
        _ = (to, subject, body_text, body_html, reply_to)
        return self._quarantined("sendgrid")

    async def _send_smtp(
        self,
        to: str | list[str],
        subject: str,
        body_text: str | None,
        body_html: str | None,
        reply_to: str | None,
    ) -> EmailResult:
        """Private compatibility path; deliberately cannot open SMTP."""
        _ = (to, subject, body_text, body_html, reply_to)
        return self._quarantined("smtp")


__all__ = ["EmailClient", "EmailResult", "LIVE_EMAIL_QUARANTINE_REASON"]
