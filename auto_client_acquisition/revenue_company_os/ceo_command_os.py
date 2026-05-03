"""
CEO Command OS — top 3 decisions + revenue risk + Proof summary + partners.

Composes signals from sales/growth/CS/finance into a 3-decision daily brief.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


def build_brief(
    *,
    sales_summary: dict[str, Any] | None = None,
    growth_summary: dict[str, Any] | None = None,
    proof_summary: dict[str, Any] | None = None,
    partner_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sales = sales_summary or {}
    growth = growth_summary or {}
    proof = proof_summary or {}
    partner = partner_summary or {}

    decisions: list[dict[str, Any]] = []

    if sales.get("deals_at_risk", 0) > 0:
        decisions.append({
            "type": "executive_decision",
            "title_ar": f"{sales['deals_at_risk']} صفقة في خطر",
            "why_now_ar": "Pipeline يخسر زخم — التأخير يُكلّف صفقات.",
            "recommended_action_ar": "صعّد لمدير المبيعات اليوم + اعتمد follow-ups جاهزة.",
            "risk_level": "high",
            "proof_impact": ["deals_unblocked", "revenue_protected"],
            "action_mode": "approval_required",
            "buttons_ar": ["صعّد", "اعرض الصفقات", "اعتمد follow-ups"],
        })

    if sales.get("pilot_offers_ready", 0) > 0:
        decisions.append({
            "type": "executive_decision",
            "title_ar": f"{sales['pilot_offers_ready']} عرض Pilot 499 جاهز",
            "why_now_ar": "Sessions في حالة waiting_inputs — تحويل Pilot إلى دفع يبدأ المسار للـ Growth OS.",
            "recommended_action_ar": "اعتمد إرسال intake + رابط Moyasar manual.",
            "risk_level": "low",
            "proof_impact": ["pilot_offer_ready", "payment_link_drafted"],
            "action_mode": "approval_required",
            "buttons_ar": ["اعتمد", "اعرض العملاء", "تخطي"],
        })

    if proof.get("totals", {}).get("pending_approvals", 0) > 0:
        decisions.append({
            "type": "proof_review",
            "title_ar": f"{proof['totals']['pending_approvals']} عنصر في Approval queue",
            "why_now_ar": "Drafts تتراكم — كلما تأخّرت الموافقة قلّت احتمالية الإرسال.",
            "recommended_action_ar": "افتح Approval queue (10 دقائق) واعتمد ما يناسب.",
            "risk_level": "medium",
            "proof_impact": ["approval_collected", "deals_unblocked"],
            "action_mode": "approval_required",
            "buttons_ar": ["افتح القائمة", "اعتمد الكل", "تخطي"],
        })

    if not decisions and partner.get("hot_partners", 0) > 0:
        decisions.append({
            "type": "partner_opportunity",
            "title_ar": f"{partner['hot_partners']} شركاء جاهزون للـ pilot",
            "why_now_ar": "وكالات أبدت اهتماماً — Co-branded Proof Pack يحوّلهم لقناة توزيع.",
            "recommended_action_ar": "احجز اجتماع 30 دقيقة + جهّز Proof sample.",
            "risk_level": "low",
            "proof_impact": ["partner_meetings", "cobranded_proof_packs"],
            "action_mode": "approval_required",
            "buttons_ar": ["احجز اجتماع", "أرسل Proof sample", "تخطي"],
        })

    decisions = decisions[:3]

    return {
        "role": "ceo",
        "brief_type": "ceo_daily",
        "date": _now().date().isoformat(),
        "summary": {
            "deals_at_risk": sales.get("deals_at_risk", 0),
            "pilot_offers_ready": sales.get("pilot_offers_ready", 0),
            "weekly_proof_revenue_sar": (proof.get("totals") or {}).get("estimated_revenue_impact_sar", 0),
            "growth_segment_today": growth.get("focus_segment", "—"),
            "hot_partners": partner.get("hot_partners", 0),
        },
        "top_decisions": decisions,
        "blocked_today_ar": [
            "لا cold WhatsApp",
            "لا live charge",
            "لا 'guaranteed' claims",
            "لا اشتراك بدون Proof Pack",
        ],
    }
