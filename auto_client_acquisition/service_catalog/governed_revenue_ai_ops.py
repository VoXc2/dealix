"""Governed Revenue & AI Operations strategic blueprint.

This module is intentionally data-only so product, sales, and API layers
can consume one deterministic source of strategic truth.
"""

from __future__ import annotations

from typing import Any


_POSITIONING = {
    "name_en": "Dealix — Governed Revenue & AI Operations",
    "name_ar": "Dealix — تشغيل إيراد وذكاء اصطناعي محكوم",
    "statement_en": (
        "Dealix helps companies turn AI experimentation and revenue operations "
        "into governed, measurable, evidence-backed workflows."
    ),
    "statement_ar": (
        "Dealix تساعد الشركات على تحويل تجارب الذكاء الاصطناعي وعمليات "
        "الإيراد إلى تشغيل محكوم، قابل للقياس، ومربوط بالأدلة."
    ),
}

_NORTH_STAR = {
    "id": "governed_value_decisions_created",
    "name_en": "Governed Value Decisions Created",
    "name_ar": "عدد قرارات القيمة المحكومة",
    "definition_ar": (
        "قرار تشغيلي أو إيرادي له مصدر واضح، موافقة موثقة، أثر قابل للقياس، "
        "وسجل أدلة مرتبط."
    ),
}

_OPERATING_MOTION = (
    "service_led",
    "software_assisted",
    "evidence_led",
    "retainer_backed",
    "platform_later",
)

_SERVICE_LADDER = (
    {
        "id": "governed_revenue_ops_diagnostic",
        "name_ar": "تشخيص عمليات الإيراد والذكاء الاصطناعي المحكوم",
        "name_en": "Governed Revenue Ops Diagnostic",
        "price_range_sar": [4999, 15000],
        "enterprise_price_range_sar": [15000, 25000],
    },
    {
        "id": "revenue_intelligence_sprint",
        "name_ar": "سبرنت ذكاء الإيراد",
        "name_en": "Revenue Intelligence Sprint",
        "price_starting_sar": 25000,
    },
    {
        "id": "governed_ops_retainer",
        "name_ar": "اشتراك تشغيل محكوم",
        "name_en": "Governed Ops Retainer",
        "price_range_sar_per_month": [4999, 15000],
        "enterprise_price_range_sar_per_month": [15000, 35000],
    },
    {
        "id": "ai_governance_for_revenue_teams",
        "name_ar": "حوكمة الذكاء الاصطناعي لفرق الإيراد",
        "name_en": "AI Governance for Revenue Teams",
    },
    {
        "id": "crm_data_readiness_for_ai",
        "name_ar": "جاهزية CRM والبيانات للذكاء الاصطناعي",
        "name_en": "CRM / Data Readiness for AI",
    },
    {
        "id": "board_decision_memo",
        "name_ar": "مذكرة قرار للإدارة",
        "name_en": "Board Decision Memo",
    },
    {
        "id": "trust_pack_lite",
        "name_ar": "حزمة الثقة الخفيفة",
        "name_en": "Trust Pack Lite",
        "trigger_only_if": "asks_for_security",
    },
)

_STATE_MACHINE = {
    "prepared_not_sent": "L2",
    "sent": "L4",
    "replied_interested": "L4",
    "meeting_booked": "L4",
    "used_in_meeting": "L5",
    "scope_requested": "L6",
    "pilot_intro_requested": "L6",
    "invoice_sent": "L7_candidate",
    "invoice_paid": "L7_confirmed",
}

_STATE_RULES = (
    "no_sent_without_founder_confirmed",
    "no_l5_without_used_in_meeting",
    "no_l6_without_scope_or_intro_request",
    "no_l7_confirmed_without_payment",
    "no_revenue_claim_before_invoice_paid",
)

_CORE_KPIS = (
    "sent_count",
    "reply_count",
    "meeting_count",
    "scope_requested_count",
    "invoice_sent_count",
    "invoice_paid_count",
    "retainer_opportunity_count",
)

_NO_BUILD_GATES = (
    "manual_workflow_repeated_three_times",
    "customer_requested_explicitly",
    "reduces_real_risk",
    "accelerates_paid_delivery",
    "unlocks_retainer",
)


def build_governed_revenue_ai_ops_blueprint() -> dict[str, Any]:
    """Return a read-only strategic payload for founder and product surfaces."""
    return {
        "positioning": dict(_POSITIONING),
        "north_star_metric": dict(_NORTH_STAR),
        "operating_motion": list(_OPERATING_MOTION),
        "service_ladder": [dict(item) for item in _SERVICE_LADDER],
        "recommended_sales_order": [
            "governed_revenue_ops_diagnostic",
            "revenue_intelligence_sprint",
            "governed_ops_retainer",
            "trust_pack_lite",
            "board_decision_memo",
        ],
        "state_machine": {
            "levels": dict(_STATE_MACHINE),
            "rules": list(_STATE_RULES),
        },
        "core_kpis": list(_CORE_KPIS),
        "build_gate_policy": {
            "name": "no_build_without_signal",
            "allowed_only_if_any": list(_NO_BUILD_GATES),
        },
    }
