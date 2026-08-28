"""Offer Intelligence — sector/pain -> current-authority commercial motion.

This module is callable from the Growth Beast API and Company Growth Beast. It
therefore must never resurrect historical fixed-price/7-day launch offers.

Current authority:
    Free Mini Diagnostic
    -> Qualified Discovery
    -> Customer-Specific Quote
    -> Revenue Command Pilot — 30 days
    -> Proof Pack
    -> Stop / Expand / Redesign
"""
from __future__ import annotations


_ANGLE_MAP: dict[tuple[str, str], dict] = {
    ("marketing_agency", "no_proof_visible"): {
        "diagnostic_focus_ar": "فجوة الإثبات والتقرير للعميل",
        "diagnostic_focus_en": "client proof and reporting gap",
        "hypothesis_ar": "قد توجد فجوة بين التنفيذ وما يستطيع العميل إثباته أو رؤيته.",
        "hypothesis_en": "There may be a gap between delivery and what the client can verify or see.",
    },
    ("b2b_services", "weak_followup"): {
        "diagnostic_focus_ar": "تسرب المتابعة وتملّك الخطوة التالية",
        "diagnostic_focus_en": "follow-up leakage and next-step ownership",
        "hypothesis_ar": "قد تضيع فرص بسبب عدم وضوح المالك أو الخطوة التالية أو دليل المتابعة.",
        "hypothesis_en": "Opportunities may be lost when owner, next step, or follow-up evidence is unclear.",
    },
    ("consulting_training", "needs_growth_clarity"): {
        "diagnostic_focus_ar": "وضوح العرض ومسار الاهتمام إلى قرار",
        "diagnostic_focus_en": "offer clarity and interest-to-decision flow",
        "hypothesis_ar": "قد تكون فجوة التحويل مرتبطة بوضوح العرض أو مسار القرار، ويجب إثبات ذلك بالبيانات.",
        "hypothesis_en": "Conversion friction may relate to offer clarity or the decision path and must be proven with evidence.",
    },
    ("saas", "support_complaints"): {
        "diagnostic_focus_ar": "أنماط الدعم وفجوات المعرفة والتصعيد",
        "diagnostic_focus_en": "support patterns, knowledge gaps, and escalation",
        "hypothesis_ar": "قد تكشف بيانات الدعم عن أسئلة متكررة أو فجوات معرفة قابلة للمعالجة.",
        "hypothesis_en": "Support evidence may reveal repeated questions or knowledge gaps worth addressing.",
    },
    ("ecommerce", "support_complaints"): {
        "diagnostic_focus_ar": "أنماط أسئلة العملاء وفجوات الرد والتصعيد",
        "diagnostic_focus_en": "customer-question patterns, response gaps, and escalation",
        "hypothesis_ar": "قد تظهر من أسئلة العملاء فرص لتحسين الردود أو المعرفة، بدون افتراض أثر إيرادي.",
        "hypothesis_en": "Customer questions may reveal response or knowledge improvements without assuming revenue impact.",
    },
}

_DEFAULT_ANGLE = {
    "diagnostic_focus_ar": "مشكلة إيرادية أو تشغيلية واحدة قابلة للإثبات",
    "diagnostic_focus_en": "one evidence-testable revenue or operating problem",
    "hypothesis_ar": "لا توجد فرضية قطاعية كافية؛ ابدأ من دليل العميل ومشكلته المعلنة.",
    "hypothesis_en": "There is not enough sector-specific evidence; start with the customer's stated problem and source evidence.",
}


def match_offer(*, sector: str, signal_type: str) -> dict:
    """Return a safe commercial-motion recommendation, never a fixed price.

    ``sector`` and ``signal_type`` choose a diagnostic angle only. Research or
    heuristics cannot authorize a relationship, price, commercial outcome, or
    paid scope.
    """
    key = (sector.lower(), signal_type.lower())
    angle = _ANGLE_MAP.get(key, _DEFAULT_ANGLE)
    return {
        **angle,
        "entry_motion": "Free Mini Diagnostic",
        "entry_price_sar": 0,
        "paid_motion": "Revenue Command Pilot — 30 days",
        "paid_motion_duration_days": 30,
        "price_mode": "customer_specific_quote_after_qualified_discovery",
        # Backward-compatible fields are intentionally null. A caller that
        # requires a number must obtain approved named-customer quote evidence.
        "price_sar": None,
        "price_halalah": None,
        "duration_days": None,
        "commercial_path": [
            "FREE_MINI_DIAGNOSTIC",
            "QUALIFIED_DISCOVERY",
            "CUSTOMER_SPECIFIC_QUOTE",
            "30_DAY_REVENUE_COMMAND_PILOT",
            "PROOF_PACK",
            "STOP_EXPAND_REDESIGN",
        ],
        "required_before_paid_scope": [
            "verified_relationship_or_valid_inbound_context",
            "buyer_stated_or_source_bound_problem",
            "qualified_discovery",
            "scope_and_acceptance_criteria",
            "customer_specific_quote_approval",
        ],
        "blocked_claims": [
            "guaranteed_revenue",
            "guaranteed_leads",
            "guaranteed_roi",
            "invented_case_study",
            "public_fixed_pilot_price",
        ],
        "approval_required": True,
        "execution_allowed": False,
        "action_mode": "draft_only",
    }
