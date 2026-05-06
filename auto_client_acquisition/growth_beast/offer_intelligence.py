"""Offer Intelligence — sector/pain → recommended offer."""
from __future__ import annotations


_OFFER_MAP: dict[tuple[str, str], dict] = {
    ("marketing_agency", "no_proof_visible"): {
        "offer_name_ar": "Sprint إثبات النتائج للوكالات",
        "offer_name_en": "Agency Proof Sprint",
        "headline_ar": "Proof Pack أسبوعي يحتفظ لك بعملائك",
        "headline_en": "Weekly Proof Pack that keeps your clients longer",
        "promise": "delivered_outputs_documented_for_each_client",
        "non_promise": "no_guaranteed_lead_count_for_their_clients",
    },
    ("b2b_services", "weak_followup"): {
        "offer_name_ar": "Sprint تحويل المتابعة B2B",
        "offer_name_en": "B2B Follow-up Conversion Sprint",
        "headline_ar": "حوّل الاستفسارات إلى مسار متابعة منظّم خلال 7 أيام",
        "headline_en": "Convert inquiries into an organized follow-up flow in 7 days",
        "promise": "drafts_and_calendar",
        "non_promise": "no_guaranteed_meetings",
    },
    ("consulting_training", "needs_growth_clarity"): {
        "offer_name_ar": "Sprint تحسين العرض والتسجيل",
        "offer_name_en": "Offer & Enrollment Sprint",
        "headline_ar": "وضّح عرضك وحسّن تحويل المهتمين",
        "headline_en": "Clarify your offer and improve enrollment conversion",
        "promise": "objection_bank_and_followup_drafts",
        "non_promise": "no_guaranteed_enrollment",
    },
    ("saas", "support_complaints"): {
        "offer_name_ar": "Sprint اكتشاف ثغرات الدعم",
        "offer_name_en": "SaaS Support Gap Sprint",
        "headline_ar": "صنّف تذاكرك واكتشف ثغرات KB",
        "headline_en": "Classify tickets and discover KB gaps",
        "promise": "tickets_classified_and_drafts",
        "non_promise": "no_full_support_replacement",
    },
    ("ecommerce", "support_complaints"): {
        "offer_name_ar": "Sprint رؤى الدعم للتجارة الإلكترونية",
        "offer_name_en": "Ecommerce Support Insight Sprint",
        "headline_ar": "ردود أسرع + تعلم من أسئلة العملاء",
        "headline_en": "Faster responses + learning from customer questions",
        "promise": "categorized_support_drafts_only",
        "non_promise": "no_auto_refund_no_live_send",
    },
}


_DEFAULT_OFFER = {
    "offer_name_ar": "Sprint نمو مخصّص — 7 أيّام",
    "offer_name_en": "Custom 7-Day Growth Proof Sprint",
    "headline_ar": "نخرج معك خلال 7 أيّام بـ Proof Pack داخلي وخطة تنفيذ",
    "headline_en": "We deliver in 7 days an internal Proof Pack and execution plan",
    "promise": "diagnostic_plan_drafts_proof_pack",
    "non_promise": "no_guaranteed_revenue",
}


def match_offer(*, sector: str, signal_type: str) -> dict:
    """Pick the best-fit offer template. Always 499 SAR pilot tier
    unless the founder explicitly upgrades the customer to 30-day
    or monthly later."""
    key = (sector.lower(), signal_type.lower())
    base = _OFFER_MAP.get(key, _DEFAULT_OFFER)
    return {
        **base,
        "price_sar": 499,
        "price_halalah": 49900,
        "duration_days": 7,
        "seven_day_plan": [
            "Day 0: intake + diagnostic kickoff",
            "Day 1-2: opportunities + drafts",
            "Day 3: approved manual sends",
            "Day 4: follow-up plan",
            "Day 5: risk note",
            "Day 6: proof pack draft",
            "Day 7: review + upsell decision",
        ],
        "blocked_claims": ["guaranteed_revenue", "guaranteed_leads", "guaranteed_roi"],
        "approval_required": True,
        "action_mode": "draft_only",
    }
