"""Company Growth Beast engine — service for client companies.

Pure-local. NO LLM. NO scraping. NO external HTTP. Reuses Growth
Beast primitives (offer matcher, content engine) but parameterizes
them per client company.
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
    """One-page diagnostic. Says insufficient_evidence when consent missing."""
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
        "company_handle": profile.company_handle,
        "current_situation_ar": f"الشركة في {sector}، المشكلة المعلنة: {problem}",
        "current_situation_en": f"Company in {sector}; declared problem: {problem}",
        "biggest_opportunity": f"focus on {problem} via 7-day proof sprint",
        "biggest_risk": "scope creep without proof events",
        "safest_channel": "warm_intro / inbound / partner_intro",
        "seven_day_plan": [
            "Day 1: ICP + opportunity ranking",
            "Day 2: offer refinement",
            "Day 3: drafts approved + manual sends",
            "Day 4: follow-up calendar",
            "Day 5: risk note",
            "Day 6: proof pack draft",
            "Day 7: review + decision",
        ],
        "recommended_offer": match_offer(sector=sector, signal_type=problem),
        "what_we_will_not_do": [
            "guaranteed revenue", "auto-send", "cold WhatsApp",
            "scraping", "fake testimonials",
        ],
        "next_step": "approve diagnostic + start 7-day pilot",
        "action_mode": "approval_required",
    }


def build_target_segments(profile: CompanyProfile) -> list[dict]:
    """Top 3 target segments for this company. Pure heuristic."""
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
        ("placeholder_segment", "discover_during_pilot", 0.5),
    ])
    return [{"segment": s, "pain": p, "fit_score": int(score * 100),
             "action_mode": "suggest_only"} for s, p, score in rows]


def build_offer_recommendation(profile: CompanyProfile) -> dict:
    return match_offer(
        sector=profile.sector or "b2b_services",
        signal_type=profile.biggest_problem or "needs_growth_clarity",
    )


def build_content_pack(profile: CompanyProfile) -> list[dict]:
    """Pack of 5 content drafts for the client to publish."""
    sector = profile.sector or "b2b_services"
    angle = profile.biggest_problem or "growth_clarity"
    types = ["linkedin_post", "sector_insight", "diagnostic_cta",
             "case_snippet", "objection_post"]
    return [draft_content(sector=sector, angle=angle, content_type=t)
            for t in types]


def support_to_growth_insight(*, ticket_categories: dict[str, int]) -> dict:
    """Convert support category counts into growth insights.

    Top category = repeated pain = opportunity for: KB article,
    landing-page section, content angle.
    """
    if not ticket_categories:
        return {
            "insufficient_data": True,
            "next_action_ar": "لا تذاكر بعد — اجمع بيانات أولاً",
            "next_action_en": "No tickets yet — collect data first.",
        }
    top = max(ticket_categories.items(), key=lambda kv: kv[1])
    top_cat, top_count = top
    return {
        "insufficient_data": False,
        "top_repeated_question": top_cat,
        "occurrences": top_count,
        "growth_action_ar": f"اكتب KB article + LinkedIn post عن '{top_cat}'",
        "growth_action_en": f"Write KB article + LinkedIn post about '{top_cat}'",
        "action_mode": "draft_only",
    }


def build_weekly_report(*, profile: CompanyProfile,
                        diagnostics_done: int = 0,
                        pilots_offered: int = 0,
                        paid_pilots: int = 0,
                        proof_events: int = 0,
                        support_categories: dict[str, int] | None = None) -> dict:
    """One-page weekly executive report for the client company."""
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
            "ركّز على أفضل قطاع",
            "حسّن أعلى معدّل تحويل",
            "وثّق Proof Pack أسبوعي",
        ],
        "top_3_decisions_en": [
            "Focus on best sector",
            "Improve highest conversion path",
            "Document weekly Proof Pack",
        ],
        "next_week_focus": "scale_what_worked + cut_what_didnt",
        "data_status": "live" if diagnostics_done > 0 else "insufficient_data",
        "action_mode": "approval_required",
    }
