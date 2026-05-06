"""V12.5 Role Command — 9 role-specific daily decision endpoints."""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/role-command-v125", tags=["role-command-v125"])

_HARD_GATES = {
    "no_live_send": True, "no_live_charge": True,
    "approval_required_for_external_actions": True,
}

Role = Literal["ceo", "growth", "sales", "support", "cs", "delivery",
               "finance", "compliance", "ops"]

_ROLE_PAYLOADS: dict[str, dict] = {
    "ceo": {
        "title_ar": "المؤسس / الرئيس التنفيذي",
        "title_en": "Founder / CEO",
        "top_3_decisions_ar": [
            "اعتمد أفضل warm intro اليوم",
            "اعتمد أفضل عرض",
            "تجاهل أي action محظور",
        ],
        "top_3_decisions_en": [
            "Approve best warm intro today",
            "Approve best offer", "Ignore any blocked action",
        ],
        "metrics": ["cash_collected", "pipeline_value", "blocked_actions"],
        "approvals_needed": ["outreach_drafts", "proof_pack_external_publish"],
    },
    "growth": {
        "title_ar": "مدير النمو", "title_en": "Head of Growth",
        "top_3_decisions_ar": ["اختر القطاع اليوم", "اعتمد المحتوى",
                               "ابدأ تجربة الأسبوع"],
        "top_3_decisions_en": ["Pick today's sector", "Approve content",
                               "Start weekly experiment"],
        "metrics": ["best_segment", "reply_rate", "experiment_status"],
        "approvals_needed": ["outreach_drafts", "content_publish"],
    },
    "sales": {
        "title_ar": "مدير المبيعات", "title_en": "Sales Manager",
        "top_3_decisions_ar": ["تابع أهم 3 صفقات", "ردّ على اعتراضات",
                               "اعرض pilot على المرشح الأعلى"],
        "top_3_decisions_en": ["Follow up top 3 deals",
                               "Respond to objections",
                               "Offer pilot to highest-fit lead"],
        "metrics": ["hot_leads", "pilot_conversion_rate", "stalled_deals"],
        "approvals_needed": ["pilot_offer", "external_messages"],
    },
    "support": {
        "title_ar": "قائد الدعم", "title_en": "Support Lead",
        "top_3_decisions_ar": ["صعّد القضايا الحساسة",
                               "اعتمد ردود الـ KB",
                               "أضف KB articles من ثغرات اليوم"],
        "top_3_decisions_en": ["Escalate sensitive cases",
                               "Approve KB replies",
                               "Add KB articles from today's gaps"],
        "metrics": ["tickets_by_priority", "sla_breaches", "knowledge_gaps"],
        "approvals_needed": ["external_replies", "policy_changes"],
    },
    "cs": {
        "title_ar": "نجاح العملاء", "title_en": "Customer Success",
        "top_3_decisions_ar": ["تواصل مع العميل الأكثر خطراً",
                               "حدّد عميل جاهز للـ upsell",
                               "اعتمد weekly check-in draft"],
        "top_3_decisions_en": ["Reach out to highest-risk customer",
                               "Identify upsell-ready customer",
                               "Approve weekly check-in draft"],
        "metrics": ["health_scores", "renewal_risk", "upsell_candidates"],
        "approvals_needed": ["check_in_messages", "upsell_proposal"],
    },
    "delivery": {
        "title_ar": "مدير التسليم", "title_en": "Delivery Manager",
        "top_3_decisions_ar": ["سلّم أهم deliverable اليوم",
                               "تابع المدخلات المفقودة",
                               "اعتمد proof event"],
        "top_3_decisions_en": ["Deliver today's top deliverable",
                               "Chase missing inputs",
                               "Approve proof event"],
        "metrics": ["active_sessions", "missing_inputs", "sla_status"],
        "approvals_needed": ["customer_deliverables", "proof_events"],
    },
    "finance": {
        "title_ar": "المالية والإدارة", "title_en": "Finance / Admin",
        "top_3_decisions_ar": ["أكّد الدفعات الجديدة بدليل",
                               "راجع invoice drafts المعلّقة",
                               "احسب margin هذا الشهر"],
        "top_3_decisions_en": ["Confirm new payments with evidence",
                               "Review pending invoice drafts",
                               "Compute monthly margin"],
        "metrics": ["cash_collected", "commitments_open",
                    "payment_confirmations_count", "avg_margin_pct"],
        "approvals_needed": ["payment_confirmations", "refund_decisions"],
    },
    "compliance": {
        "title_ar": "المسؤول عن البيانات والامتثال",
        "title_en": "Data / Compliance Owner",
        "top_3_decisions_ar": ["راجع الإجراءات المحظورة",
                               "صعّد طلبات حذف/تصدير البيانات",
                               "اعتمد أو ارفض أي outbound"],
        "top_3_decisions_en": ["Review blocked actions",
                               "Escalate delete/export requests",
                               "Approve or reject any outbound"],
        "metrics": ["unsafe_action_attempts", "consent_unknowns",
                    "pdpl_requests"],
        "approvals_needed": ["all_external_outbound", "data_rights_requests"],
    },
    "ops": {
        "title_ar": "العمليات", "title_en": "Operations Manager",
        "top_3_decisions_ar": ["شغّل verifier اليومي",
                               "حدّث الـ status board",
                               "تابع SLA breaches"],
        "top_3_decisions_en": ["Run daily verifier", "Update status board",
                               "Track SLA breaches"],
        "metrics": ["verifier_status", "incidents_open", "sla_breaches"],
        "approvals_needed": ["incident_responses"],
    },
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {"service": "role_command_v125", "version": "v12.5",
            "roles_supported": list(_ROLE_PAYLOADS.keys()),
            "hard_gates": _HARD_GATES,
            "next_action_ar": "اطلب /today/{role} لأي دور",
            "next_action_en": "Call /today/{role} for any role."}


@router.get("/today/{role}")
async def today(role: Role) -> dict[str, Any]:
    payload = _ROLE_PAYLOADS.get(role)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"unknown role: {role}")
    return {
        "role": role,
        **payload,
        "risks": [], "blocked_items": [],
        "next_best_action_ar": payload["top_3_decisions_ar"][0],
        "next_best_action_en": payload["top_3_decisions_en"][0],
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }
