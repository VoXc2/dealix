"""Dealix governed revenue + AI operations blueprint.

Deterministic source of truth for positioning, offer ladder, and
approval-first operating rules.
"""

from __future__ import annotations

from typing import Any

POSITIONING: dict[str, Any] = {
    "company_type_en": "Governed Revenue & AI Operations Company",
    "company_type_ar": "شركة تشغيل الإيراد والذكاء الاصطناعي المحكوم",
    "vision_en": "Dealix becomes the GCC operating layer for governed revenue and AI workflows.",
    "vision_ar": (
        "تصبح Dealix طبقة التشغيل الخليجية التي تحول تجارب الذكاء الاصطناعي "
        "وعمليات الإيراد إلى workflows محكومة، قابلة للقياس، ومربوطة بالأدلة."
    ),
    "operating_promises": [
        "every_ai_output_has_source",
        "every_external_action_requires_approval",
        "every_opportunity_has_evidence",
        "every_client_decision_has_passport",
        "every_engagement_produces_proof",
        "every_proof_becomes_asset",
    ],
}

NORTH_STAR: dict[str, Any] = {
    "metric_id": "governed_value_decisions_created",
    "name_en": "Governed Value Decisions Created",
    "name_ar": "القرارات القيمية المحكومة المُنجزة",
    "definition_en": (
        "Count of operating or revenue decisions taken with clear source, explicit "
        "approval, documented evidence, and measurable impact."
    ),
    "definition_ar": (
        "عدد القرارات التشغيلية أو الإيرادية التي اتُخذت بمصدر واضح، "
        "موافقة واضحة، دليل موثق، وأثر قابل للقياس."
    ),
    "decision_requirements": {
        "source_clarity": True,
        "approval_recorded": True,
        "evidence_logged": True,
        "measurable_impact": True,
    },
    "example_decisions": [
        "prioritize_high_value_accounts",
        "block_unsafe_workflow",
        "reject_external_send_without_approval",
        "promote_workflow_to_paid_sprint",
        "convert_customer_to_retainer",
    ],
}

OFFERS: tuple[dict[str, Any], ...] = (
    {
        "id": "governed_revenue_ops_diagnostic",
        "name_en": "Governed Revenue Ops Diagnostic",
        "name_ar": "تشخيص عمليات الإيراد المحكومة",
        "price_range_sar": "4,999-15,000",
        "enterprise_price_range_sar": "15,000-25,000",
        "stage": "diagnostic",
        "core_deliverables": [
            "revenue_workflow_map",
            "crm_source_quality_review",
            "pipeline_risk_map",
            "decision_passport",
            "proof_of_value_opportunities",
        ],
    },
    {
        "id": "revenue_intelligence_sprint",
        "name_en": "Revenue Intelligence Sprint",
        "name_ar": "سبرنت ذكاء الإيراد",
        "price_range_sar": "25,000+",
        "enterprise_price_range_sar": "custom_scope",
        "stage": "sprint",
        "core_deliverables": [
            "account_prioritization",
            "deal_risk_scoring",
            "next_best_action_drafts",
            "revenue_opportunity_ledger",
            "proof_pack",
        ],
    },
    {
        "id": "governed_ops_retainer",
        "name_en": "Governed Ops Retainer",
        "name_ar": "عقد تشغيل محكوم شهري",
        "price_range_sar": "4,999-15,000_per_month",
        "enterprise_price_range_sar": "15,000-35,000_per_month",
        "stage": "retainer",
        "core_deliverables": [
            "monthly_revenue_review",
            "ai_decision_review",
            "approved_follow_up_queue",
            "risk_register",
            "board_memo",
        ],
    },
    {
        "id": "ai_governance_for_revenue_teams",
        "name_en": "AI Governance for Revenue Teams",
        "name_ar": "حوكمة الذكاء الاصطناعي لفرق الإيراد",
        "price_range_sar": "scope_based",
        "enterprise_price_range_sar": "scope_based",
        "stage": "governance",
        "core_deliverables": [
            "allowed_ai_actions",
            "forbidden_ai_actions",
            "approval_boundaries",
            "source_rules",
            "evidence_logging",
        ],
    },
    {
        "id": "crm_data_readiness_for_ai",
        "name_en": "CRM / Data Readiness for AI",
        "name_ar": "جاهزية CRM والبيانات للذكاء الاصطناعي",
        "price_range_sar": "scope_based",
        "enterprise_price_range_sar": "scope_based",
        "stage": "data_readiness",
        "core_deliverables": [
            "crm_hygiene_report",
            "source_mapping",
            "missing_fields_map",
            "duplicate_accounts_report",
            "data_readiness_score",
        ],
    },
    {
        "id": "board_decision_memo",
        "name_en": "Board Decision Memo",
        "name_ar": "مذكرة قرار مجلس الإدارة",
        "price_range_sar": "scope_based",
        "enterprise_price_range_sar": "scope_based",
        "stage": "executive",
        "core_deliverables": [
            "top_revenue_decisions",
            "pipeline_risks",
            "ai_governance_risks",
            "capital_allocation_options",
            "build_hold_kill_recommendations",
        ],
    },
    {
        "id": "trust_pack_lite",
        "name_en": "Trust Pack Lite",
        "name_ar": "حزمة الثقة الخفيفة",
        "price_range_sar": "signal_triggered",
        "enterprise_price_range_sar": "signal_triggered",
        "stage": "trust",
        "core_deliverables": [
            "ai_action_policy",
            "approval_matrix",
            "evidence_handling_policy",
            "forbidden_actions",
            "agent_safety_rules",
        ],
    },
)

TOP_THREE_OFFERS: tuple[str, ...] = (
    "governed_revenue_ops_diagnostic",
    "revenue_intelligence_sprint",
    "governed_ops_retainer",
)

STATE_MACHINE: tuple[dict[str, Any], ...] = (
    {"state": "prepared_not_sent", "evidence_level": "L2"},
    {"state": "sent", "evidence_level": "L4"},
    {"state": "replied_interested", "evidence_level": "L4"},
    {"state": "meeting_booked", "evidence_level": "L4"},
    {"state": "used_in_meeting", "evidence_level": "L5"},
    {"state": "scope_requested", "evidence_level": "L6"},
    {"state": "pilot_intro_requested", "evidence_level": "L6"},
    {"state": "invoice_sent", "evidence_level": "L7_candidate"},
    {"state": "invoice_paid", "evidence_level": "L7_confirmed"},
)

STATE_RULES: tuple[str, ...] = (
    "cannot_mark_sent_without_founder_confirmed_true",
    "cannot_mark_l5_without_used_in_meeting",
    "cannot_mark_l6_without_scope_or_intro_request",
    "cannot_mark_l7_confirmed_without_payment",
    "cannot_report_revenue_before_invoice_paid",
)

GATES: tuple[dict[str, Any], ...] = (
    {
        "gate": 1,
        "name_en": "First Market Proof",
        "name_ar": "أول إثبات سوق",
        "criteria": ["5_messages_sent", "first_reply_or_silence_classified"],
    },
    {
        "gate": 2,
        "name_en": "Meeting Proof",
        "name_ar": "إثبات الاجتماع",
        "criteria": ["used_in_meeting_equals_L5"],
    },
    {
        "gate": 3,
        "name_en": "Pull Proof",
        "name_ar": "إثبات طلب النطاق",
        "criteria": ["scope_requested_equals_L6"],
    },
    {
        "gate": 4,
        "name_en": "Revenue Proof",
        "name_ar": "إثبات الإيراد",
        "criteria": ["invoice_paid_equals_L7_confirmed"],
    },
    {
        "gate": 5,
        "name_en": "Repeatability",
        "name_ar": "إثبات القابلية للتكرار",
        "criteria": ["same_offer_sold_twice"],
    },
    {
        "gate": 6,
        "name_en": "Retainer",
        "name_ar": "إثبات الاشتراك الشهري",
        "criteria": ["monthly_recurring_value_active"],
    },
    {
        "gate": 7,
        "name_en": "Platform Signal",
        "name_ar": "إشارة المنصة",
        "criteria": ["manual_workflow_repeated_3_plus"],
    },
)

MARKET_SEGMENTS: tuple[dict[str, Any], ...] = (
    {
        "segment": "b2b_services",
        "examples": ["consulting", "agencies", "professional_services", "implementation_firms"],
        "pain_points": ["pipeline_messy", "follow_up_weak", "ai_usage_unmanaged"],
    },
    {
        "segment": "fintech_processors",
        "examples": ["payments", "lending", "financial_operations"],
        "pain_points": ["regulated_workflows", "trust_requirements", "approval_audit_pressure"],
    },
    {
        "segment": "vc_portfolio",
        "examples": ["portfolio_startups", "venture_studios"],
        "pain_points": ["fast_ai_adoption_without_governance", "need_repeatable_playbook"],
    },
)


def get_positioning() -> dict[str, Any]:
    return dict(POSITIONING)


def get_north_star() -> dict[str, Any]:
    return dict(NORTH_STAR)


def get_offers() -> dict[str, Any]:
    return {
        "top_three_offer_ids": list(TOP_THREE_OFFERS),
        "sales_motion": "diagnostic_then_sprint_then_retainer",
        "offers": [dict(offer) for offer in OFFERS],
    }


def get_state_machine() -> dict[str, Any]:
    return {
        "states": [dict(state) for state in STATE_MACHINE],
        "rules": list(STATE_RULES),
    }


def get_gates() -> dict[str, Any]:
    return {"gates": [dict(gate) for gate in GATES]}


def get_market_segments() -> dict[str, Any]:
    return {"segments": [dict(segment) for segment in MARKET_SEGMENTS]}


def get_blueprint() -> dict[str, Any]:
    return {
        "positioning": get_positioning(),
        "north_star": get_north_star(),
        "offers": get_offers(),
        "state_machine": get_state_machine(),
        "gates": get_gates(),
        "market_segments": get_market_segments(),
        "guardrails": {
            "no_autonomous_external_send": True,
            "approval_first": True,
            "evidence_first": True,
            "service_led_software_assisted": True,
        },
    }
