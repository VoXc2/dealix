"""
High-level WhatsApp send helper — picks an approved Meta template per
intent so callers don't need to know template names.

Intents we support today:
- proposal_followup
- meeting_confirmation
- payment_reminder

Each intent maps to a (template_name, language_code) pair via env
overrides so the founder can rotate templates without code changes.

Usage:
    from dealix.integrations.whatsapp_send import send_intent

    await send_intent(
        intent="proposal_followup",
        to="+966500000000",
        params=["Acme", "https://dealix.me/p/abc"],
        locale="ar",
    )

When META_WHATSAPP_ACCESS_TOKEN is unset the call is a no-op that
returns a result with `success=False, error="whatsapp_not_configured"`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


_INTENT_DEFAULTS: dict[str, tuple[str, str]] = {
    "proposal_followup": ("dealix_proposal_followup_v1", "ar"),
    "meeting_confirmation": ("dealix_meeting_confirmation_v1", "ar"),
    "payment_reminder": ("dealix_payment_reminder_v1", "ar"),
    "trial_expiring": ("dealix_trial_expiring_v1", "ar"),
}


@dataclass
class IntentSendResult:
    success: bool
    intent: str
    template_name: str
    message_id: str | None = None
    error: str | None = None


def _resolve_template(intent: str, locale: str) -> tuple[str, str]:
    """Resolve to (template_name, language_code) honoring env overrides."""
    env_key = f"WHATSAPP_TEMPLATE_{intent.upper()}"
    override = os.getenv(env_key, "").strip()
    if override:
        # Format: "name:language" e.g. "dealix_proposal_v2:ar"
        if ":" in override:
            name, lang = override.split(":", 1)
            return name, lang
        return override, locale
    default_name, default_lang = _INTENT_DEFAULTS.get(
        intent, ("", locale or "ar")
    )
    return default_name, (locale or default_lang)


async def send_intent(
    *,
    intent: str,
    to: str,
    params: list[str] | None = None,
    locale: str = "ar",
) -> IntentSendResult:
    """Send the template matched to `intent` via the existing WhatsAppClient."""
    template_name, language_code = _resolve_template(intent, locale)
    if not template_name:
        return IntentSendResult(
            success=False,
            intent=intent,
            template_name="",
            error="intent_not_mapped",
        )
    try:
        from integrations.whatsapp import WhatsAppClient

        client = WhatsAppClient()
    except Exception as exc:
        log.exception("whatsapp_client_unavailable")
        return IntentSendResult(
            success=False, intent=intent, template_name=template_name, error=str(exc)
        )

    components: list[dict[str, Any]] = []
    if params:
        components.append(
            {
                "type": "body",
                "parameters": [{"type": "text", "text": p} for p in params],
            }
        )
    result = await client.send_template(
        to=to,
        template_name=template_name,
        language_code=language_code,
        components=components,
    )
    return IntentSendResult(
        success=bool(getattr(result, "success", False)),
        intent=intent,
        template_name=template_name,
        message_id=getattr(result, "message_id", None),
        error=getattr(result, "error", None),
    )
