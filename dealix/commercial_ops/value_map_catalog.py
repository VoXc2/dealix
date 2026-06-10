"""Static catalog for COMMERCIAL_VALUE_MAP — docs, funnel, situations, market intel."""

from __future__ import annotations

from typing import Any

# Relative to repo root (docs/commercial/ unless noted)
READING_ORDER_AR: list[dict[str, str]] = [
    {"step": "1", "doc": "docs/commercial/COMMERCIAL_VALUE_MAP_AR.md", "when_ar": "نقطة دخول يومية"},
    {"step": "2", "doc": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md", "when_ar": "5 دقائق صباحاً"},
    {"step": "3", "doc": "docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md", "when_ar": "أسبوعي / قرار قناة"},
    {"step": "4", "doc": "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md", "when_ar": "تكتيك عميق"},
    {"step": "5", "doc": "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md", "when_ar": "قبل فاتورة/دفع"},
]

SITUATION_GUIDE_AR: list[dict[str, str]] = [
    {"situation_ar": "صباح عادي", "start_doc": "MASTER_COMMERCIAL_OPERATING_PLAN_AR.md", "script": "run_founder_commercial_day.ps1"},
    {"situation_ar": "قبل مكالمة", "start_doc": "operations/FOUNDER_SALES_LOOP_AR.md", "script": "founder_meeting_debrief_template.yaml"},
    {"situation_ar": "قبل عرض سعر", "start_doc": "DEALIX_REVOPS_PACKAGES_AR.md", "script": ""},
    {"situation_ar": "قبل Moyasar", "start_doc": "PAID_LAUNCH_AFTER_SOFT_PASS_AR.md", "script": "verify_paid_launch_readiness.py"},
    {"situation_ar": "RFP / قانوني", "start_doc": "MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md", "script": ""},
    {"situation_ar": "بحث سوق", "start_doc": "MARKET_INTELLIGENCE_MASTER_INDEX_AR.md", "script": ""},
    {"situation_ar": "توسيع قوائم", "start_doc": "GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md", "script": "expand_commercial_ops_all.py"},
]

PUBLIC_FUNNEL: list[dict[str, str]] = [
    {"path": "/ar", "role_ar": "صفحة بيع Soft Launch"},
    {"path": "/ar/risk-score", "role_ar": "مغناطيس تأهيل"},
    {"path": "/ar/proof-pack", "role_ar": "نية شراء عالية"},
    {"path": "/ar/dealix-diagnostic", "role_ar": "طلب Diagnostic"},
    {"path": "/ar/learn", "role_ar": "AEO / ثقة"},
    {"path": "/ar/partners", "role_ar": "شراكة"},
    {"path": "/ar/business-now", "role_ar": "قرار مؤسس 8 ركائز"},
]

OPS_UI: list[dict[str, str]] = [
    {"path": "/ar/ops/founder", "role_ar": "مركز قيادة + Value Plan"},
    {"path": "/ar/ops/war-room", "role_ar": "أعلى 10 + مسودات"},
    {"path": "/ar/ops/approvals", "role_ar": "موافقات خارجية"},
    {"path": "/ar/ops/marketing", "role_ar": "سوشال اليوم"},
    {"path": "/ar/ops/evidence", "role_ar": "سجل أدلة"},
]

KEY_APIS: list[dict[str, str]] = [
    {"method": "GET", "path": "/api/v1/ops-autopilot/founder/daily-pack", "role_ar": "حزمة يوم + value_plan"},
    {"method": "GET", "path": "/api/v1/ops-autopilot/founder/value-plan", "role_ar": "لقطة قيمة موحّدة"},
    {"method": "GET", "path": "/api/v1/ops-autopilot/founder/commercial-value-map", "role_ar": "خريطة + كتالوج"},
    {"method": "POST", "path": "/api/v1/public/leads", "role_ar": "التقاط lead"},
    {"method": "POST", "path": "/api/v1/revenue-os/anti-waste/check", "role_ar": "منع هدر"},
    {"method": "GET", "path": "/api/v1/business-now/snapshot", "role_ar": "Business NOW"},
]

def _market_intelligence_docs() -> list[dict[str, str]]:
    from dealix.commercial_ops.market_intelligence_refs import market_intelligence_pillars_flat

    pillars = market_intelligence_pillars_flat()
    if pillars:
        return pillars
    return [
        {"id": "index", "doc": "docs/commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md", "topic_ar": "فهرس"},
    ]


MARKET_INTELLIGENCE_DOCS: list[dict[str, str]] = _market_intelligence_docs()

EXTERNAL_GTM_REFS: list[dict[str, str]] = [
    {
        "title": "ProductQuant GTM 2026",
        "url": "https://productquant.dev/blog/complete-gtm-strategy-guide/",
        "use_ar": "ACV ↔ نمط GTM",
    },
    {
        "title": "Design Revision B2B GTM",
        "url": "https://designrevision.com/blog/b2b-saas-go-to-market-strategy",
        "use_ar": "أول 10 عملاء يدوياً",
    },
    {
        "title": "GCC SaaS Landscape 2026",
        "url": "https://gulfsaasreview.com/article/saas-adoption-gcc-2026-landscape-report",
        "use_ar": "اتجاه اعتماد منطقة",
    },
    {
        "title": "Al-Bahr GCC Sales 2026",
        "url": "https://al-bahr-growth-advisory.com/en/blog/sales-strategy-gcc-2026/",
        "use_ar": "دورة شراء خليجية",
    },
]

DAY_SCRIPTS: dict[str, str] = {
    "value_map_status": "py -3 scripts/commercial_value_map_status.py",
    "value_plan_day": "powershell -File scripts/run_value_plan_day.ps1",
    "founder_morning": "powershell -File scripts/founder_morning.ps1",
    "founder_evening": "powershell -File scripts/founder_evening.ps1",
    "expand_pool": "py -3 scripts/expand_commercial_ops_all.py",
    "export_value_plan": "py -3 scripts/export_value_plan_snapshot.py",
    "verify_value_stack": "py -3 scripts/verify_value_plan_stack.py",
}

REVENUE_OS_APIS: list[dict[str, str]] = [
    {"path": "/api/v1/revenue-os/catalog", "role_ar": "كتالوج خدمات + anti-waste"},
    {"path": "/api/v1/decision-passport/golden-chain", "role_ar": "سلسلة قرار ذهبية"},
    {"path": "/api/v1/decision-passport/evidence-levels", "role_ar": "مستويات L0–L5"},
    {"path": "POST /api/v1/revenue-os/signals/normalize", "role_ar": "إشارات سوق → Why Now"},
]

TRANSFORMATION_DOCS: list[dict[str, str]] = [
    {"doc": "docs/transformation/EXECUTIVE_OPERATING_CHECKLIST_AR.md", "topic_ar": "checklist تنفيذي"},
    {"doc": "dealix/transformation/kpi_founder_commercial_registry.yaml", "topic_ar": "سجل KPI مؤسس"},
    {"doc": "docs/ops/FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md", "topic_ar": "Truth Matrix تكاملات"},
]

DELIVERY_AND_PROOF: list[dict[str, str]] = [
    {"doc": "docs/delivery/PROOF_PACK_TEMPLATE.md", "topic_ar": "قالب Proof 10 أقسام"},
    {"doc": "docs/commercial/operations/CLIENT_PACK_SOP_AR.md", "topic_ar": "حزمة عميل من War Room"},
    {"doc": "scripts/generate_client_pack.py", "topic_ar": "توليد حزمة"},
]

CI_AND_AUTOMATION: list[dict[str, str]] = [
    {"id": "founder_commercial_daily", "path": ".github/workflows/founder_commercial_daily.yml", "role_ar": "صباح CI 05:00 UTC"},
    {"id": "daily_revenue_machine", "path": ".github/workflows/daily-revenue-machine.yml", "role_ar": "آلة إيراد يومية"},
]

AFFILIATE_PARTNERS: list[dict[str, str]] = [
    {"path": "/ar/partners", "role_ar": "طلب شريك"},
    {"doc": "docs/commercial/operations/PARTNER_ONBOARDING_KIT_AR.md", "role_ar": "حزمة onboarding"},
    {"module": "dealix/revenue_ops_autopilot/affiliate_compliance.py", "role_ar": "امتثال إحالة"},
]


def get_value_map_catalog() -> dict[str, Any]:
    return {
        "reading_order_ar": READING_ORDER_AR,
        "situation_guide_ar": SITUATION_GUIDE_AR,
        "public_funnel": PUBLIC_FUNNEL,
        "ops_ui": OPS_UI,
        "key_apis": KEY_APIS,
        "revenue_os_apis": REVENUE_OS_APIS,
        "market_intelligence": MARKET_INTELLIGENCE_DOCS,
        "external_gtm_refs": EXTERNAL_GTM_REFS,
        "transformation_docs": TRANSFORMATION_DOCS,
        "delivery_and_proof": DELIVERY_AND_PROOF,
        "ci_automation": CI_AND_AUTOMATION,
        "affiliate_partners": AFFILIATE_PARTNERS,
        "day_scripts": DAY_SCRIPTS,
    }
