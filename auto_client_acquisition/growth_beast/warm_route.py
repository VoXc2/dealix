"""Warm Route Engine — chooses safe channel + drafts message."""
from __future__ import annotations

from typing import Literal

WarmChannel = Literal[
    "founder_warm_intro",
    "partner_intro",
    "existing_customer_referral",
    "manual_linkedin_post",
    "manual_email_to_known_contact",
    "inbound_reply",
    "community_post",
]

# HARD-BLOCKED forever.
_BLOCKED_CHANNELS = {
    "cold_whatsapp",
    "cold_email",
    "linkedin_dm_automation",
    "purchased_list_blast",
    "scrape_then_email",
}


def draft_warm_route(
    *,
    channel: str,
    sector: str,
    placeholder_name: str = "[الاسم]",
    pain_hint: str = "growth_clarity",
) -> dict:
    """Draft a safe-channel outreach. Returns blocked if channel is
    in the forbidden set."""

    if channel in _BLOCKED_CHANNELS:
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": f"القناة {channel} ممنوعة نهائياً",
            "blocked_reason_en": f"Channel {channel} is hard-blocked.",
            "channel": channel,
        }

    if channel not in (
        "founder_warm_intro", "partner_intro", "existing_customer_referral",
        "manual_linkedin_post", "manual_email_to_known_contact",
        "inbound_reply", "community_post",
    ):
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": "قناة غير معروفة — افتراضيا blocked",
            "blocked_reason_en": "Unknown channel — fail-safe blocked.",
            "channel": channel,
        }

    ar = (
        f"السلام عليكم {placeholder_name}،\n"
        f"شفت إن شركتكم في {sector} وعندي ملاحظة سريعة عن {pain_hint}.\n"
        f"عندي Mini Diagnostic مجاني خلال 24 ساعة. أرسله؟"
    )
    en = (
        f"Hi {placeholder_name},\n"
        f"Noticed your company is in {sector}; I have a quick note "
        f"on {pain_hint}.\n"
        f"I have a free Mini Diagnostic ready within 24 hours. Send?"
    )
    return {
        "channel": channel,
        "sector": sector,
        "draft_ar": ar,
        "draft_en": en,
        "send_method": "manual_only",
        "action_mode": "draft_only",
        "approval_required": True,
    }
