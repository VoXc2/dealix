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


@router.get("/{bundle_id}/intake-questions")
async def get_intake_questions(bundle_id: str) -> dict[str, Any]:
    if bundle_id not in INTAKE_QUESTIONS:
        # Bundle exists but no intake (e.g., free_diagnostic falls through to default)
        if not any(b["id"] == bundle_id for b in CATALOG):
            raise HTTPException(status_code=404, detail="bundle_not_found")
        return {"bundle_id": bundle_id, "questions": []}
    return {"bundle_id": bundle_id, "questions": INTAKE_QUESTIONS[bundle_id]}
