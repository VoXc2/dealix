"""
Services catalog router — Service Tower (5 productized bundles).

The catalog is intentionally static. Five bundles, no more — internal
sub-services are NOT exposed publicly. This is the same list the
landing/services.html page renders.

Endpoints:
    GET  /api/v1/services/catalog
        → ordered list of 5 bundles + Free Diagnostic header
    GET  /api/v1/services/{bundle_id}
        → single bundle detail
    GET  /api/v1/services/{bundle_id}/intake-questions
        → 4-7 intake questions before starting the bundle (used by Operator)
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/services", tags=["services"])


# ── Catalog (single source of truth shared with landing/services.html) ──

CATALOG: list[dict[str, Any]] = [
    {
        "id": "free_diagnostic",
        "name_ar": "Free Diagnostic",
        "name_en": "Free Diagnostic",
        "price_sar": 0,
        "price_label": "مجاني",
        "cadence": "one_time",
        "duration_days": 1,
        "for_whom_ar": "تستكشف Dealix قبل الالتزام. خلال 24 ساعة.",
        "deliverables_ar": [
            "تشخيص قنواتك الحالية",
            "3 فرص تحسين فورية",
            "توصية الباقة المناسبة",
        ],
        "proof_metrics": ["sectors_scanned", "improvement_areas", "recommended_bundle"],
        "sla_ar": "24 ساعة",
        "safe_policy_ar": "approval-first. لا تواصل خارجي.",
        "cta_path": "private-beta.html",
    },
    {
        "id": "growth_starter",
        "name_ar": "Growth Starter",
        "name_en": "Growth Starter",
        "price_sar": 499,
        "price_label": "499 ريال / 7 أيام",
        "cadence": "one_time",
        "duration_days": 7,
        "for_whom_ar": "شركة أو وكالة تريد أول Proof سريع قبل الاشتراك.",
        "deliverables_ar": [
            "10 فرص مناسبة",
            "رسائل عربية لكل فرصة",
            "قناة موصى بها (آمنة)",
            "مخاطر يجب تجنبها",
            "Proof Pack مختصر",
        ],
        "proof_metrics": ["opportunities_created", "drafts_created", "risks_blocked", "proof_pack_url"],
        "sla_ar": "Proof Pack خلال 7 أيام",
        "safe_policy_ar": "كل draft يمر بموافقتك. لا cold WhatsApp.",
        "cta_path": "private-beta.html",
    },
    {
        "id": "data_to_revenue",
        "name_ar": "Data to Revenue",
        "name_en": "Data to Revenue",
        "price_sar": 1500,
        "price_label": "1,500 ريال",
        "cadence": "one_time",
        "duration_days": 10,
        "for_whom_ar": "عندك قائمة عملاء/leads وتحتاج تنظيف + تحويل.",
        "deliverables_ar": [
            "CSV / CRM / Sheet intake",
            "Deduplication + normalization",
            "Contactability scoring",
            "Top 50 targets + Arabic drafts",
            "قائمة المحظورين (PDPL)",
            "Proof Pack مفصّل",
        ],
        "proof_metrics": ["records_normalized", "dedup_rate", "contactable_rate", "top_targets"],
        "sla_ar": "Proof Pack خلال 10 أيام",
        "safe_policy_ar": "consent_status لكل سجل، opt-out محترم.",
        "cta_path": "operator.html",
        "highlight": True,
    },
    {
        "id": "executive_growth_os",
        "name_ar": "Executive Growth OS",
        "name_en": "Executive Growth OS",
        "price_sar": 2999,
        "price_label": "2,999 ريال / شهر",
        "cadence": "monthly",
        "duration_days": 30,
        "for_whom_ar": "مدير تنفيذي يريد تشغيل يومي + Proof أسبوعي.",
        "deliverables_ar": [
            "CEO Daily Brief (3 قرارات)",
            "Sales / Growth / Service cards",
            "Approval queue يومي",
            "Weekly Proof Pack",
            "Quarterly review + upsell",
            "كل القنوات بـ approval-first",
        ],
        "proof_metrics": ["daily_decisions", "approvals_processed", "weekly_proof_packs", "qbrs"],
        "sla_ar": "يومي + أسبوعي",
        "safe_policy_ar": "live actions تبقى disabled افتراضياً.",
        "cta_path": "growth-os.html",
    },
    {
        "id": "partnership_growth",
        "name_ar": "Partnership Growth",
        "name_en": "Partnership Growth",
        "price_sar": 3000,
        "price_max_sar": 7500,
        "price_label": "3,000–7,500 ريال",
        "cadence": "one_time",
        "duration_days": 30,
        "for_whom_ar": "تريد بناء قناة شراكات / وكالات.",
        "deliverables_ar": [
            "Partner shortlist + scorecard",
            "Co-branded Proof Pack",
            "Revenue share tracker",
            "Meeting brief لكل شريك",
            "Referral attribution",
        ],
        "proof_metrics": ["partners_shortlisted", "meeting_briefs", "co_branded_proof_packs", "referral_links"],
        "sla_ar": "Pilot على عميل واحد أولاً",
        "safe_policy_ar": "لا exclusivity مبكر، لا revenue share بدون referral متتبع.",
        "cta_path": "agency-partner.html",
    },
    {
        "id": "full_growth_control_tower",
        "name_ar": "Full Growth Control Tower",
        "name_en": "Full Growth Control Tower",
        "price_sar": None,
        "price_label": "Custom",
        "cadence": "monthly",
        "duration_days": None,
        "for_whom_ar": "شركات تحتاج تشغيل كامل + tenant + roles.",
        "deliverables_ar": [
            "كل ما سبق",
            "Multi-role Command Center",
            "Tenant عزل بيانات",
            "Custom integrations",
            "Dedicated CSM + SLA مخصص",
        ],
        "proof_metrics": ["multi_role_seats", "tenant_isolation", "integrations", "dedicated_csm"],
        "sla_ar": "Onboarding 3-4 أسابيع",
        "safe_policy_ar": "Saudi data residency، PDPL audit logs.",
        "cta_path": "support.html#contact",
    },
]


# ── PR-OS-FOUNDATION 1.3: Service Contracts ───────────────────────
# Every bundle gets a full contract. The user's vision: "أي خدمة ما عندها
# هذا الشكل = لا تُباع". Used by /api/v1/services/{id}/contract and by
# Phase 2 service-workflow-execution engine.
SERVICE_CONTRACTS: dict[str, dict[str, Any]] = {
    "free_diagnostic": {
        "ideal_customer_ar": [
            "شركة B2B سعودية تستكشف Dealix قبل أي التزام",
            "تريد تشخيص واضح خلال 24 ساعة",
        ],
        "required_inputs": ["company_name", "sector", "main_offer"],
        "workflow_steps": [
            "تجميع inputs من intake",
            "تحليل قنوات حالية",
            "اقتراح أفضل 3 تحسينات",
            "اختيار الباقة الأنسب",
        ],
        "approval_points": [],  # no outbound, no approvals needed
        "blocked_actions": [],
        "deliverables": [
            "تشخيص قنوات حالية",
            "3 فرص تحسين فورية",
            "توصية الباقة المناسبة",
        ],
        "proof_metrics": ["sectors_scanned", "improvement_areas", "recommended_bundle"],
        "definition_of_done": [
            "diagnostic_report_generated",
            "next_action_recommended",
            "client_update_sent",
        ],
    },
    "growth_starter": {
        "ideal_customer_ar": [
            "شركة B2B سعودية 10-50 موظف",
            "عرض واضح + ICP واضح",
            "تريد أول Proof سريع قبل الاشتراك الشهري",
        ],
        "required_inputs": [
            "company_name", "website", "offer_ar", "ideal_customer_ar",
            "city", "current_channels",
        ],
        "workflow_steps": [
            "qualify company + ICP",
            "اختيار segment الأنسب",
            "بناء قائمة 10 فرص",
            "كتابة 6 رسائل عربية",
            "تحديد 3 follow-up angles",
            "تعليم المخاطر",
            "تجهيز Proof Pack",
            "اقتراح الخطوة التالية",
        ],
        "approval_points": [
            "approve_target_segment",
            "approve_messages",
            "approve_channel",
        ],
        "blocked_actions": ["cold_whatsapp", "linkedin_automation", "guaranteed_revenue_claim", "purchased_lists"],
        "deliverables": [
            "10 فرص مناسبة",
            "6 رسائل عربية مخصصة",
            "3 follow-ups مقترحة",
            "ملاحظات مخاطر",
            "Proof Pack مختصر بـ HMAC",
        ],
        "proof_metrics": [
            "opportunities_created",
            "drafts_created",
            "risks_blocked",
            "proof_pack_url",
        ],
        "definition_of_done": [
            "proof_pack_generated",
            "next_action_recommended",
            "client_update_sent",
            "upsell_card_created",
        ],
    },
    "data_to_revenue": {
        "ideal_customer_ar": [
            "شركة عندها قائمة leads / CRM قديم / Excel",
            "تحتاج تنظيف + تأهيل + رسائل عربية",
        ],
        "required_inputs": [
            "data_source", "row_count", "consent_status", "ideal_customer_ar",
        ],
        "workflow_steps": [
            "intake CSV / Sheet / CRM export",
            "deduplication + normalization",
            "PDPL consent check لكل سجل",
            "contactability scoring",
            "اختيار Top 50 targets",
            "كتابة رسائل عربية",
            "تعليم المحظورين",
            "تجهيز Proof Pack مفصّل",
        ],
        "approval_points": [
            "approve_dedup_strategy",
            "approve_top_50_list",
            "approve_messages",
        ],
        "blocked_actions": ["send_to_no_consent", "cold_whatsapp_to_purchased", "scraping", "linkedin_automation"],
        "deliverables": [
            "قائمة منظفة",
            "Top 50 targets مرتبة",
            "Arabic drafts لكل target",
            "قائمة المحظورين (PDPL)",
            "Proof Pack مفصّل",
        ],
        "proof_metrics": [
            "records_normalized",
            "dedup_rate",
            "contactable_rate",
            "top_targets",
            "blocked_for_pdpl",
        ],
        "definition_of_done": [
            "list_normalized",
            "top_50_approved",
            "drafts_approved",
            "proof_pack_generated",
        ],
    },
    "executive_growth_os": {
        "ideal_customer_ar": [
            "مدير تنفيذي يريد تشغيل يومي للنمو",
            "فريق 5-50 شخص",
            "يحتاج Proof Pack أسبوعي للمجلس",
        ],
        "required_inputs": [
            "company_goals", "pipeline_state", "channels", "weekly_targets",
        ],
        "workflow_steps": [
            "تشغيل 4 daily-ops windows",
            "إصدار CEO/Sales/Growth/CS/Finance/Compliance daily briefs",
            "إدارة Approval queue يومي",
            "مراجعة pipeline أسبوعياً",
            "إصدار Weekly Proof Pack",
            "Quarterly review + upsell roadmap",
        ],
        "approval_points": [
            "approve_weekly_segment",
            "approve_outbound_drafts",
            "approve_upsell_offers",
        ],
        "blocked_actions": ["cold_whatsapp", "live_charge_without_explicit_approval", "linkedin_automation", "auto_email_send"],
        "deliverables": [
            "CEO Daily Brief (3 قرارات)",
            "Sales / Growth / Service cards",
            "Approval queue يومي",
            "Weekly Proof Pack",
            "Monthly review + upsell",
        ],
        "proof_metrics": [
            "daily_decisions",
            "approvals_processed",
            "weekly_proof_packs",
            "qbrs",
        ],
        "definition_of_done": [
            "weekly_proof_pack_delivered",
            "daily_briefs_running",
            "monthly_review_held",
        ],
    },
    "partnership_growth": {
        "ideal_customer_ar": [
            "شركة تريد بناء قناة شراكات / وكالات",
            "عرض واضح للشريك",
            "تقبل revenue share متتبع",
        ],
        "required_inputs": [
            "target_market", "partner_kind", "value_prop_to_partner", "geography",
        ],
        "workflow_steps": [
            "تحديد السوق المستهدف",
            "بناء partner shortlist",
            "scoring لكل شريك محتمل",
            "كتابة intro scripts",
            "تجهيز co-sell offer",
            "meeting briefs",
            "Co-branded Proof Pack",
        ],
        "approval_points": [
            "approve_partner_shortlist",
            "approve_intro_scripts",
            "approve_co_sell_offer",
        ],
        "blocked_actions": ["exclusivity_before_proof", "white_label_before_3_pilots", "revenue_share_without_tracked_referral"],
        "deliverables": [
            "Partner shortlist + scorecard",
            "Co-branded Proof Pack",
            "Revenue share tracker",
            "Meeting brief لكل شريك",
            "Referral attribution",
        ],
        "proof_metrics": [
            "partners_shortlisted",
            "meeting_briefs",
            "co_branded_proof_packs",
            "referral_links",
        ],
        "definition_of_done": [
            "partner_pilot_signed",
            "co_branded_proof_delivered",
            "first_referral_tracked",
        ],
    },
    "full_growth_control_tower": {
        "ideal_customer_ar": [
            "شركة عندها فريق + بيانات",
            "تحتاج multi-role command center",
            "تحتاج tenant عزل بيانات",
        ],
        "required_inputs": [
            "annual_revenue_sar", "team_size", "integrations_needed",
            "data_residency_required",
        ],
        "workflow_steps": [
            "Onboarding 3-4 أسابيع",
            "إعداد Multi-role Command Center",
            "Tenant عزل البيانات",
            "Custom integrations",
            "تعيين Dedicated CSM",
            "إصدار daily/weekly/monthly cadence",
        ],
        "approval_points": [
            "approve_integration_scope",
            "approve_data_residency_setup",
            "approve_custom_workflows",
        ],
        "blocked_actions": ["cross_tenant_data_leak", "non_ksa_data_residency", "live_charge_without_csm_approval"],
        "deliverables": [
            "Multi-role Command Center",
            "Tenant عزل بيانات",
            "Custom integrations",
            "Dedicated CSM + SLA مخصص",
            "Quarterly business review",
        ],
        "proof_metrics": [
            "multi_role_seats",
            "tenant_isolation",
            "integrations",
            "dedicated_csm",
        ],
        "definition_of_done": [
            "tenant_provisioned",
            "all_integrations_live",
            "csm_assigned",
            "first_qbr_held",
        ],
    },
}


def _attach_contracts() -> None:
    """Inject SERVICE_CONTRACTS into the matching CATALOG entry at import time."""
    for entry in CATALOG:
        cid = entry["id"]
        if cid in SERVICE_CONTRACTS:
            entry["contract"] = SERVICE_CONTRACTS[cid]


_attach_contracts()


# Per-bundle intake questions (used by Operator before starting work).
INTAKE_QUESTIONS: dict[str, list[dict[str, str]]] = {
    "free_diagnostic": [
        {"key": "company_name", "label_ar": "اسم الشركة", "type": "text", "required": "true"},
        {"key": "sector", "label_ar": "القطاع", "type": "text", "required": "true"},
        {"key": "city", "label_ar": "المدينة", "type": "text", "required": "false"},
        {"key": "main_offer", "label_ar": "العرض الرئيسي", "type": "textarea", "required": "true"},
    ],
    "growth_starter": [
        {"key": "company_name", "label_ar": "اسم الشركة", "type": "text", "required": "true"},
        {"key": "sector", "label_ar": "القطاع", "type": "text", "required": "true"},
        {"key": "ideal_customer", "label_ar": "العميل المثالي", "type": "textarea", "required": "true"},
        {"key": "avg_deal_sar", "label_ar": "متوسط الصفقة (SAR)", "type": "number", "required": "false"},
        {"key": "current_channels", "label_ar": "القنوات الحالية", "type": "text", "required": "false"},
    ],
    "data_to_revenue": [
        {"key": "data_source", "label_ar": "مصدر البيانات (CSV/CRM/Sheet)", "type": "text", "required": "true"},
        {"key": "row_count", "label_ar": "عدد السجلات تقريباً", "type": "number", "required": "true"},
        {"key": "consent_status", "label_ar": "هل عندهم opt-in؟", "type": "select", "required": "true"},
        {"key": "ideal_customer", "label_ar": "العميل المثالي", "type": "textarea", "required": "true"},
    ],
    "executive_growth_os": [
        {"key": "company_name", "label_ar": "اسم الشركة", "type": "text", "required": "true"},
        {"key": "team_size", "label_ar": "حجم فريق المبيعات", "type": "number", "required": "true"},
        {"key": "ceo_email", "label_ar": "بريد المدير التنفيذي", "type": "email", "required": "true"},
        {"key": "weekly_proof_recipients", "label_ar": "مستلمي Proof الأسبوعي", "type": "text", "required": "false"},
    ],
    "partnership_growth": [
        {"key": "partner_kind", "label_ar": "نوع الشريك المستهدف", "type": "text", "required": "true"},
        {"key": "value_prop_to_partner", "label_ar": "ما الذي تقدمه للشريك", "type": "textarea", "required": "true"},
        {"key": "geography", "label_ar": "النطاق الجغرافي", "type": "text", "required": "false"},
    ],
    "full_growth_control_tower": [
        {"key": "annual_revenue_sar", "label_ar": "الإيراد السنوي (SAR)", "type": "number", "required": "true"},
        {"key": "team_size", "label_ar": "حجم الفريق", "type": "number", "required": "true"},
        {"key": "integrations_needed", "label_ar": "التكاملات المطلوبة", "type": "textarea", "required": "false"},
        {"key": "data_residency_required", "label_ar": "هل تحتاج Saudi data residency؟", "type": "select", "required": "true"},
    ],
}


@router.get("/catalog")
async def get_catalog() -> dict[str, Any]:
    """Return the public 5-bundle Service Tower."""
    return {
        "version": "1.0",
        "currency": "SAR",
        "bundles": CATALOG,
        "policy_notes": [
            "5 bundles only — internal sub-services are not exposed publicly.",
            "Pricing shown as label strings to support Custom (Control Tower).",
        ],
    }


@router.get("/{bundle_id}")
async def get_bundle(bundle_id: str) -> dict[str, Any]:
    for b in CATALOG:
        if b["id"] == bundle_id:
            return b
    raise HTTPException(status_code=404, detail="bundle_not_found")


@router.get("/{bundle_id}/contract")
async def get_contract(bundle_id: str) -> dict[str, Any]:
    """Return the full Service Contract (workflow_steps, approval_points,
    blocked_actions, definition_of_done, etc.) for a single bundle.

    Per the vision: "أي خدمة ما عندها هذا الشكل = لا تُباع".
    Used by the Operator (to explain what we'll deliver), by Phase 2's
    sprint workflow engine, and by trust-center.html.
    """
    if bundle_id not in SERVICE_CONTRACTS:
        if not any(b["id"] == bundle_id for b in CATALOG):
            raise HTTPException(status_code=404, detail="bundle_not_found")
        raise HTTPException(status_code=404, detail="contract_not_defined_for_bundle")
    return {"bundle_id": bundle_id, "contract": SERVICE_CONTRACTS[bundle_id]}


@router.get("/{bundle_id}/intake-questions")
async def get_intake_questions(bundle_id: str) -> dict[str, Any]:
    if bundle_id not in INTAKE_QUESTIONS:
        # Bundle exists but no intake (e.g., free_diagnostic falls through to default)
        if not any(b["id"] == bundle_id for b in CATALOG):
            raise HTTPException(status_code=404, detail="bundle_not_found")
        return {"bundle_id": bundle_id, "questions": []}
    return {"bundle_id": bundle_id, "questions": INTAKE_QUESTIONS[bundle_id]}
