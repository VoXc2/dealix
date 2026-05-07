"""LinkedIn channel policy — automation always blocked (NO_LINKEDIN_AUTO)."""
from __future__ import annotations

from auto_client_acquisition.channel_policy_gateway.schemas import (
    ActionKind,
    PolicyDecision,
)


def linkedin_policy(*, action_kind: ActionKind) -> PolicyDecision:
    if action_kind == "automate":
        return PolicyDecision(
            channel="linkedin",
            action_kind=action_kind,
            allowed=False,
            action_mode="blocked",
            reason_ar="ممنوع: NO_LINKEDIN_AUTO — أتمتة LinkedIn مرفوضة.",
            reason_en="Blocked: NO_LINKEDIN_AUTO — LinkedIn automation refused.",
            safe_alternative_ar="انشر يدويّاً أو ابعث رسالة شخصيّة.",
            safe_alternative_en="Post manually or send a personal DM.",
        )
    if action_kind == "scrape":
        return PolicyDecision(
            channel="linkedin",
            action_kind=action_kind,
            allowed=False,
            action_mode="blocked",
            reason_ar="ممنوع: NO_SCRAPING.",
            reason_en="Blocked: NO_SCRAPING.",
        )
    if action_kind == "draft":
        return PolicyDecision(
            channel="linkedin",
            action_kind=action_kind,
            allowed=True,
            action_mode="draft_only",
            reason_ar="مسموح صياغة منشور أو رسالة شخصيّة.",
            reason_en="Drafting a post or personal DM allowed.",
        )
    if action_kind == "manual_outreach":
        return PolicyDecision(
            channel="linkedin",
            action_kind=action_kind,
            allowed=True,
            action_mode="approved_manual",
            reason_ar="مسموح كتواصل يدوي شخصي بعد موافقتك.",
            reason_en="Allowed as manual personal outreach after your approval.",
        )
    return PolicyDecision(
        channel="linkedin",
        action_kind=action_kind,
        allowed=False,
        action_mode="blocked",
        reason_ar="إجراء غير معروف على LinkedIn — مرفوض افتراضياً.",
        reason_en="Unknown LinkedIn action — refused by default.",
    )
