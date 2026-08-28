"""Company Growth Beast engine — service for client companies.

Pure-local. NO LLM. NO scraping. NO external HTTP. Reuses Growth Beast
primitives but cannot manufacture customer evidence, public claims, prices, or
paid-scope authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.growth_beast.content_engine import draft_content
from auto_client_acquisition.growth_beast.offer_intelligence import match_offer


@dataclass
class CompanyProfile:
    company_handle: str
    sector: str
    offer: str
    ideal_customer: str
    current_channels: str
    biggest_problem: str
    consent_for_diagnostic: bool


def build_company_profile(
    *, company_handle: str, sector: str = "tbd", offer: str = "",
    ideal_customer: str = "", current_channels: str = "",
    biggest_problem: str = "", consent_for_diagnostic: bool = False,
) -> CompanyProfile:
    return CompanyProfile(
        company_handle=company_handle, sector=sector, offer=offer,
        ideal_customer=ideal_customer, current_channels=current_channels,
        biggest_problem=biggest_problem,
        consent_for_diagnostic=consent_for_diagnostic,
    )


def build_growth_diagnostic(profile: CompanyProfile) -> dict:
    """Build a preliminary Free Mini Diagnostic outline.

    Consent to prepare the diagnostic is required. The returned artifact is not
    a paid Pilot proposal, price quote, customer proof, or execution authority.
    """
    if not profile.consent_for_diagnostic:
        return {
            "blocked": True,
            "reason_ar": "لا موافقة على التشخيص — لا يصدر بدون موافقة",
            "reason_en": "No consent for diagnostic — won't generate.",
            "action_mode": "blocked",
        }
    sector = profile.sector or "tbd"
    problem = profile.biggest_problem or "unknown"
    return {
        "status": "preliminary_free_mini_diagnostic",
        "funnel_stage": "free_mini_diagnostic",
        "truth_class": "DRAFT_REQUIRES_SOURCE_VALIDATION",
        "requires_human_review": True,
        "requires_source_validation": True,
        "payment_required": False,
        "external_action_allowed": False,
        "company_handle": profile.company_handle,
        "current_situation_ar": f"الشركة في {sector}، المشكلة المعلنة: {problem}",
        "current_situation_en": f"Company in {sector}; declared problem: {problem}",
        "biggest_opportunity": (
            f"validate a first-party baseline for {problem} before selecting paid scope"
        ),
        "biggest_risk": "scope or outcome claims without source-bound evidence",
        "safest_channel": "existing relationship / inbound / permissioned event follow-up",
        "diagnostic_workplan": [
            "Confirm the stated problem and accountable owner",
            "Identify lawful minimum-necessary source evidence",
            "Establish baseline or record UNKNOWN_NOT_EVIDENCE_BACKED",
            "Map the current workflow and observed leakage/uncertainty",
            "Separate facts, customer-stated inputs, hypotheses, and missing evidence",
            "Return STOP / NEEDS_EVIDENCE / QUALIFIED_FOR_DISCOVERY",
            "If qualified, prepare discovery questions — not a price or commitment",
        ],
        # Backward-compatibility key retained explicitly empty so downstream
        # clients do not silently receive the retired 7-day launch plan.
        "seven_day_plan": [],
        "legacy_seven_day_plan_status": "RETIRED_NOT_COMMERCIAL_AUTHORITY",
        "recommended_motion": match_offer(sector=sector, signal_type=problem),
        "what_we_will_not_do": [
            "guaranteed revenue",
            "invented ROI",
            "auto-send",
            "cold WhatsApp",
            "scraping",
            "fake testimonials or case studies",
            "public fixed Pilot price",
        ],
        "next_step": "human_review_then_qualified_discovery_if_evidence_supports_fit",
        "action_mode": "approval_required",
    }


def build_target_segments(profile: CompanyProfile) -> list[dict]:
    """Return research hypotheses for up to three target segments."""
    sector = profile.sector or "b2b_services"
    base_segments = {
        "marketing_agency": [
            ("smes_with_3_to_30_clients", "need_proof_pack", 0.85),
            ("solo_founders_with_growing_brand", "need_clarity", 0.7),
            ("ecommerce_brands_post_launch", "need_retention", 0.6),
        ],
        "b2b_services": [
            ("law_firms_under_20", "need_followup", 0.8),
            ("accounting_firms_smes", "need_proof", 0.7),
            ("it_consultancies_local", "need_offer_clarity", 0.65),
        ],
        "consulting_training": [
            ("independent_trainers", "need_enrollment_followup", 0.85),
            ("training_firms_smes", "need_offer_clarity", 0.75),
        ],
    }
    rows = base_segments.get(sector, [
        ("unresolved_segment_hypothesis", "discover_from_evidence", 0.5),
    ])
    return [
        {
            "segment": segment,
            "pain": pain,
            "fit_score": int(score * 100),
            "truth_class": "RESEARCH_HYPOTHESIS",
            "relationship_created": False,
            "action_mode": "suggest_only",
        }
        for segment, pain, score in rows
    ]


def build_offer_recommendation(profile: CompanyProfile) -> dict:
    """Return a diagnostic/commercial-motion recommendation, never a price."""
    return match_offer(
        sector=profile.sector or "b2b_services",
        signal_type=profile.biggest_problem or "needs_growth_clarity",
    )


def build_content_pack(profile: CompanyProfile) -> list[dict]:
    """Pack of five content drafts; case content fails closed without proof."""
    sector = profile.sector or "b2b_services"
    angle = profile.biggest_problem or "growth_clarity"
    types = ["linkedin_post", "sector_insight", "diagnostic_cta",
             "case_snippet", "objection_post"]
    return [
        draft_content(sector=sector, angle=angle, content_type=content_type)
        for content_type in types
    ]


def support_to_growth_insight(*, ticket_categories: dict[str, int]) -> dict:
    """Convert support category counts into a content/research hypothesis."""
    if not ticket_categories:
        return {
            "insufficient_data": True,
            "next_action_ar": "لا توجد بيانات كافية — اجمع بيانات أولاً",
            "next_action_en": "Insufficient data — collect evidence first.",
        }
    top_cat, top_count = max(ticket_categories.items(), key=lambda kv: kv[1])
    return {
        "insufficient_data": False,
        "top_repeated_question": top_cat,
        "occurrences": top_count,
        "growth_action_ar": f"حضّر مسودة KB + فرضية محتوى عن '{top_cat}' للمراجعة",
        "growth_action_en": f"Prepare a KB draft + content hypothesis about '{top_cat}' for review",
        "truth_class": "SOURCE_DERIVED_INTERNAL_INSIGHT",
        "action_mode": "draft_only",
    }


def build_weekly_report(*, profile: CompanyProfile,
                        diagnostics_done: int = 0,
                        pilots_offered: int = 0,
                        paid_pilots: int = 0,
                        proof_events: int = 0,
                        support_categories: dict[str, int] | None = None) -> dict:
    """One-page weekly executive report from caller-supplied verified counts."""
    insights = support_to_growth_insight(
        ticket_categories=support_categories or {},
    )
    return {
        "company_handle": profile.company_handle,
        "best_segment": profile.sector,
        "diagnostics_done": diagnostics_done,
        "pilots_offered": pilots_offered,
        "paid_pilots": paid_pilots,
        "proof_events": proof_events,
        "support_insights": insights,
        "top_3_decisions_ar": [
            "تحقق من أفضل مشكلة بالأدلة",
            "حسّن مسار قرار واحد قابل للقياس",
            "وثّق أدلة التسليم قبل تحويلها إلى Proof عام",
        ],
        "top_3_decisions_en": [
            "Verify the highest-priority problem with evidence",
            "Improve one measurable decision path",
            "Document delivery evidence before turning it into public proof",
        ],
        "next_week_focus": "advance_verified_stage_or_stop_low_value_work",
        "data_status": "caller_supplied_counts" if diagnostics_done > 0 else "insufficient_data",
        "action_mode": "approval_required",
    }
