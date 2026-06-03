"""Maps commercial service lines to repo docs, API runners, and session types."""

from __future__ import annotations

from typing import Any, Literal

ServiceLineId = Literal[
    "grow_revenue",
    "serve_customers",
    "automate_operations",
    "company_brain",
    "govern_ai",
    "data_intelligence",
    "marketing_gtm",
]

DELIVERY_CATALOG: list[dict[str, Any]] = [
    {
        "id": "grow_revenue",
        "name_ar": "نمو الإيراد",
        "name_en": "Grow Revenue",
        "docs": {
            "catalog": "docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md",
            "scope_template": "docs/commercial/templates/SCOPE_SPRINT_SAR.md",
            "code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md",
        },
        "session_service_type": "lead_intelligence_sprint",
        "engagement_api": "/api/v1/commercial/engagements/lead-intelligence-sprint",
    },
    {
        "id": "serve_customers",
        "name_ar": "خدمة العملاء",
        "name_en": "Serve Customers",
        "docs": {
            "checklist": "docs/commercial/checklists/DELIVERY_LEAD_INTELLIGENCE_SPRINT.md",
            "code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md",
        },
        "session_service_type": "support_desk_sprint",
        "engagement_api": "/api/v1/commercial/engagements/support-desk-sprint",
        "inbox_api": "/api/v1/customer-inbox-v10/status",
    },
    {
        "id": "automate_operations",
        "name_ar": "أتمتة العمليات",
        "name_en": "Automate Operations",
        "docs": {"code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md"},
        "session_service_type": "quick_win_ops",
        "engagement_api": "/api/v1/commercial/engagements/quick-win-ops",
    },
    {
        "id": "company_brain",
        "name_ar": "معرفة الشركة",
        "name_en": "Company Brain",
        "docs": {"code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md"},
        "session_service_type": "growth_proof_sprint",
        "brain_api": "POST /api/v1/company-brain/query",
    },
    {
        "id": "govern_ai",
        "name_ar": "حوكمة AI",
        "name_en": "Govern AI",
        "docs": {"code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md"},
        "session_service_type": "diagnostic",
        "risk_api": "/api/v1/governance/risk-dashboard",
    },
    {
        "id": "data_intelligence",
        "name_ar": "البيانات والذكاء",
        "name_en": "Data and Intelligence",
        "docs": {"code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md"},
        "session_service_type": "leadops_sprint",
        "csv_preview_api": "/api/v1/revenue-data/csv-preview",
    },
    {
        "id": "marketing_gtm",
        "name_ar": "التسويق المربوط بالإيراد",
        "name_en": "Marketing GTM",
        "docs": {"code_map": "docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md"},
        "session_service_type": "growth_proof_sprint",
        "engagement_api": "/api/v1/commercial/engagements/campaign-intelligence-sprint",
    },
]


def delivery_catalog_snapshot() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "service_lines": DELIVERY_CATALOG,
        "service_sessions_start": "/api/v1/service-sessions/start",
        "hard_gates": {
            "draft_approval_first": True,
            "no_cold_whatsapp_auto": True,
            "no_linkedin_automation": True,
        },
    }
