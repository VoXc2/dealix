"""Warm Route Engine — chooses a bounded channel and drafts a message.

This module drafts only. It does not prove relationship/consent, send messages,
or authorize commercial commitments.
"""
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

_BLOCKED_CHANNELS = {
    "cold_whatsapp",
    "cold_email",
    "linkedin_dm_automation",
    "purchased_list_blast",
    "scrape_then_email",
}

_ALLOWED_CHANNELS = {
    "founder_warm_intro",
    "partner_intro",
    "existing_customer_referral",
    "manual_linkedin_post",
    "manual_email_to_known_contact",
    "inbound_reply",
    "community_post",
}


def draft_warm_route(
    *,
    channel: str,
    sector: str,
    placeholder_name: str = "[الاسم]",
    pain_hint: str = "growth_clarity",
) -> dict:
    """Draft a channel-safe message; external action remains separately gated."""

    if channel in _BLOCKED_CHANNELS:
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": f"القناة {channel} محظورة في هذا المسار",
            "blocked_reason_en": f"Channel {channel} is blocked in this route.",
            "channel": channel,
        }

    if channel not in _ALLOWED_CHANNELS:
        return {
            "action_mode": "blocked",
            "blocked_reason_ar": "قناة غير معروفة — الافتراضي هو المنع",
            "blocked_reason_en": "Unknown channel — fail-safe blocked.",
            "channel": channel,
        }

    ar = (
        f"السلام عليكم {placeholder_name}،\n"
        f"عندي سؤال بخصوص {pain_hint} في سياق {sector}. إذا كانت هذه مشكلة فعلية عندكم، "
        "أقدر أشارك Mini Diagnostic مجاني يحدد المشكلة والأدلة المطلوبة والخطوة التالية قبل أي التزام مدفوع. "
        "هل يناسبك؟"
    )
    en = (
        f"Hi {placeholder_name},\n"
        f"I have a question about {pain_hint} in a {sector} context. If this is a real issue for your team, "
        "I can share a free Mini Diagnostic that defines the problem, required evidence, and next step before any paid commitment. "
        "Would that be useful?"
    )
    return {
        "channel": channel,
        "sector": sector,
        "draft_ar": ar,
        "draft_en": en,
        "send_method": "manual_or_policy_governed_only",
        "action_mode": "draft_only",
        "relationship_or_consent_proven_by_this_function": False,
        "external_send_allowed_by_this_function": False,
        "approval_required": True,
    }
