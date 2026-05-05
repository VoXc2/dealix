"""Deterministic goal → service mapper.

Keyword routing only — no LLM, no external HTTP. Output strings are
intentionally kept claim-free (no "نضمن" / "guaranteed" wording).
"""
from __future__ import annotations

from auto_client_acquisition.service_mapping_v7.schemas import (
    FORBIDDEN_ACTIONS,
    MapRequest,
    ServiceRecommendation,
)


# Service id → routing config. First-match wins, scanned in declared order.
_ROUTES: tuple[dict, ...] = (
    {
        "service": "growth_starter",
        "price_band": "499",
        "risk": "low",
        "keywords": ("lead intake", "qualify", "first replies", "first reply", "lead_intake"),
        "deliverables": [
            "10_qualified_opportunities_72h",
            "arabic_outreach_drafts",
            "followup_plan_72h",
            "signed_proof_pack",
        ],
        "proof": ["reply_within_sla_pct", "qualified_count", "drafts_approved_pct"],
        "why_ar": "نقترح بدء التشغيل بـ Growth Starter لأن الفجوة الأولى هي مسار الاستقبال والتأهيل وأوّل ردّ.",
        "why_en": "Growth Starter fits because the first gap is intake + qualification + first reply.",
        "next_step": "Founder review of the 10-opportunity shortlist before any outbound draft is approved.",
    },
    {
        "service": "data_to_revenue",
        "price_band": "1500-3000",
        "risk": "medium",
        "keywords": (
            "list cleanup",
            "list_cleanup",
            "crm",
            "scoring",
            "score_leads",
            "dedupe",
            "dedup",
        ),
        "deliverables": [
            "list_dedup_and_normalize",
            "contactability_score",
            "segmented_message_drafts",
            "risk_report",
        ],
        "proof": ["records_cleaned", "contactability_lift_pct", "segments_delivered"],
        "why_ar": "البيانات الحاليّة بحاجة إلى تنظيف وترتيب قبل أيّ تواصل — Data-to-Revenue يبني الأساس.",
        "why_en": "Existing data needs cleanup + ranking before outreach — Data-to-Revenue builds the base.",
        "next_step": "Founder review of the cleanup plan + sample contactability scores before any segmented draft.",
    },
    {
        "service": "executive_growth_os",
        "price_band": "2999/month",
        "risk": "medium",
        "keywords": ("weekly report", "weekly_report", "executive", "c-level", "c_level", "ceo brief"),
        "deliverables": [
            "weekly_executive_brief",
            "monthly_proof_pack",
            "founder_office_hour_each_week",
            "actual_vs_forecast_view",
        ],
        "proof": ["briefs_delivered", "decisions_logged", "blockers_cleared"],
        "why_ar": "القيادة بحاجة إيقاع تنفيذيّ ثابت — حزمة أسبوعيّة تُغذّي قرارات المؤسس.",
        "why_en": "Leadership needs a steady executive cadence — a weekly pack feeding founder decisions.",
        "next_step": "Founder confirms cadence + scope before the first weekly brief is generated.",
    },
    {
        "service": "partnership_growth",
        "price_band": "3000-7500",
        "risk": "medium",
        "keywords": ("partner", "partnership", "agency", "agencies", "channel"),
        "deliverables": [
            "partner_category_radar",
            "fit_score_per_partner_class",
            "warm_intro_drafts_ar_en",
            "cobranded_proof_pack_template",
        ],
        "proof": ["partner_categories_mapped", "warm_intros_drafted", "fit_scored_partners"],
        "why_ar": "النموّ القادم يأتي من الشركاء — نبدأ بخريطة فئات + نقاط ملاءمة قبل أيّ تواصل.",
        "why_en": "Next growth comes from partners — we map categories + fit before any outreach.",
        "next_step": "Founder review of the partner-category radar before any warm-intro draft is approved.",
    },
)


_DEFAULT_DIAGNOSTIC = {
    "service": "diagnostic",
    "price_band": "0",
    "risk": "low",
    "deliverables": [
        "founder_review_of_inputs",
        "3_specific_recommendations",
        "best_first_offer_recommendation",
    ],
    "proof": ["recommendations_logged", "founder_signoff"],
    "why_ar": "لا توجد إشارة واضحة في الألم المطروح — نبدأ بـ Diagnostic مجاني لتحديد الأولوية الأولى.",
    "why_en": "No clear signal in the stated pain — start with the free Diagnostic to set the first priority.",
    "next_step": "Schedule the 30-60 min Diagnostic; founder reviews inputs before any service is activated.",
}


def _haystack(req: MapRequest) -> str:
    parts: list[str] = []
    if req.goal_ar:
        parts.append(req.goal_ar)
    if req.goal_en:
        parts.append(req.goal_en)
    parts.extend(req.pain_points or [])
    return " ".join(parts).lower()


def _match_route(haystack: str) -> dict | None:
    for route in _ROUTES:
        for kw in route["keywords"]:
            if kw.lower() in haystack:
                return route
    return None


def map_goal_to_service(req: MapRequest) -> ServiceRecommendation:
    """Map a customer goal + pain points to a recommended Dealix service."""
    hay = _haystack(req)
    route = _match_route(hay) or _DEFAULT_DIAGNOSTIC

    return ServiceRecommendation(
        company_handle=req.company_handle,
        recommended_service=route["service"],
        why_ar=route["why_ar"],
        why_en=route["why_en"],
        expected_deliverables=list(route["deliverables"]),
        excluded_actions=list(FORBIDDEN_ACTIONS),
        proof_metrics=list(route["proof"]),
        price_band_sar=route["price_band"],
        risk_level=route["risk"],
        approval_required=True,
        next_step=route["next_step"],
    )
