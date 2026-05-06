"""Company-facing snapshot — no internal OS jargon, links only."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_execution.daily_snapshot import build_daily_command_center


def build_company_command_center() -> dict[str, Any]:
    """Mirror operator queues into customer-safe labels (no agent/router names)."""
    inner = build_daily_command_center()
    top = inner.get("today_top_3_decisions", [])[:3]
    return {
        "schema_version": 1,
        "experience_layer": "company_portal",
        "north_star_hint_ar": (
            "خلال أسبوع: تشخيص واضح + خطة + مسودات آمنة + قائمة تسليم + Proof Pack صادق + قرار تالي."
        ),
        "today_top_3_decisions": top,
        "diagnostics_queue": {
            "title_ar": "التشخيص",
            "hint_ar": "ستة أسئلة ثم تقرير صفحة واحدة — راجع وثائق التشخيص.",
            "doc_path": "docs/revenue/04_MINI_DIAGNOSTIC_REVENUE_FLOW.md",
            "cli": "python scripts/dealix_diagnostic.py --company \"...\" --json",
        },
        "growth_queue": {
            "title_ar": "النمو",
            "hint_ar": "خطط ومسودات فقط — لا نشر تلقائي.",
            "api_hint": "استخدم المسودات بعد موافقة المؤسس.",
        },
        "sales_queue": {
            "title_ar": "المبيعات والمتابعة",
            "hint_ar": "مسودات رسائل — إرسال يدوي فقط.",
            "doc_path": "docs/revenue/02_WARM_INTRO_MESSAGE_BANK_AR_EN.md",
        },
        "support_queue": {
            "title_ar": "الدعم",
            "hint_ar": "تصنيف ومسودة — تصعيد للحساس.",
            "post_classify": "/api/v1/support-os/classify",
        },
        "delivery_queue": {
            "title_ar": "التسليم",
            "hint_ar": "قائمة تسليم حسب الخدمة — راجع خطة التسليم مع المشغل.",
            "get_plan": "/api/v1/delivery-os/status",
        },
        "proof_queue": {
            "title_ar": "الإثبات",
            "hint_ar": "أحداث proof فقط — لا أرقام وهمية.",
            "list_events": "/api/v1/proof-ledger/events",
        },
        "compliance_alerts": inner.get("compliance_alerts", []),
        "revenue_pipeline": {
            "title_ar": "مسار الصفقة",
            "api": "GET /api/v1/revenue-pipeline/summary",
        },
        "next_best_actions": [
            {"ar": "راجع التشخيص ووافق على المسودات قبل أي إرسال.", "mode": "approval_first"},
            {"ar": "اطلب Proof Pack فارغ إن لم يوجد أحداث بعد — صدق أفضل من مظهر.", "mode": "proof_first"},
            {"ar": "التقرير الأسبوعي للإدارة: من المشغل بعد تجميع الأسبوع.", "mode": "weekly_brief"},
        ],
        "hard_gates": inner.get("hard_gates", {}),
        "operator_deep_link": "/api/v1/full-ops/daily-command-center",
        "note_ar": "هذه الواجهة لا تعرض تفاصيل تقنية داخلية؛ للمشغل استخدم الرابط الأخير.",
    }
