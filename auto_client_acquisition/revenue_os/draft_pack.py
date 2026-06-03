"""Governed draft pack builder (doctrine-enforced; external channels draft-only)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_os.followup_plan import default_follow_up_plan_bullets
from auto_client_acquisition.safe_send_gateway import enforce_doctrine_non_negotiables


def build_revenue_draft_pack(
    top_account_row: dict[str, Any],
    *,
    request_cold_whatsapp: bool = False,
    request_linkedin_automation: bool = False,
    request_scraping: bool = False,
    request_bulk_outreach: bool = False,
    include_whatsapp_draft: bool = False,
    relationship_status: str = "",
) -> dict[str, Any]:
    enforce_doctrine_non_negotiables(
        request_cold_whatsapp=request_cold_whatsapp,
        request_linkedin_automation=request_linkedin_automation,
        request_scraping=request_scraping,
        request_bulk_outreach=request_bulk_outreach,
    )
    company = str(top_account_row.get("company_name") or "العميل")
    pack: dict[str, Any] = {
        "email_ar": f"موضوع: متابعة ذكية محكومة — {company}\n\nنرحّب بكم، نجهّز مسودة للمراجعة فقط.",
        "email_en": f"Subject: Governed follow-up — {company}\n\nDraft only; no automated send.",
        "linkedin_draft_en": (
            f"Hi — quick note on {company}: we'd like to share a governed, draft-only follow-up. "
            "No automation; human sends only after approval."
        ),
        "linkedin_draft_ar": (
            f"تحية — ملاحظة موجزة حول {company}: نجهّز متابعة محكومة كمسودة فقط. "
            "لا أتمتة؛ الإرسال يدوي بعد الموافقة."
        ),
        "call_script_ar": "افتح باحترام، اسأل عن الأولويات، لا تعد مبيعات.",
        "call_script_en": "Open professionally, ask priorities, no guaranteed outcomes.",
        "follow_up_plan": default_follow_up_plan_bullets(),
    }
    rs = relationship_status.strip().lower()
    if include_whatsapp_draft and rs in ("explicit_consent", "warm_intro"):
        pack["whatsapp_draft"] = {
            "ar": f"مسودة واتساب (موافقة/علاقة: {rs}) — لا إرسال تلقائي.",
            "en": f"WhatsApp draft (relationship={rs}) — no auto-send.",
        }
    elif include_whatsapp_draft:
        pack["whatsapp_blocked_reason"] = {
            "ar": "مسودة واتساب تتطلب explicit_consent أو warm_intro.",
            "en": "WhatsApp draft requires explicit_consent or warm_intro.",
        }
    return pack


__all__ = ["build_revenue_draft_pack"]
