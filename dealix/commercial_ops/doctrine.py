"""Commercial doctrine — non-negotiables + SOAEN daily block (governed GTM)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

SOAEN_CHECKLIST_AR = [
    "مصدر الفكرة موثّق (call / Proof / اعتراض)",
    "مالك النشر والرد على التعليقات محدد",
    "مراجعة المسودة قبل النشر (Approval)",
    "لا أرقام إيراد بدون دفع مثبت (Evidence)",
    "CTA واحد: Risk Score أو Sample Proof أو ديمو 10 دقائق (Next Action)",
]

NON_NEGOTIABLE_RULES: list[dict[str, str]] = [
    {
        "id": "no_cold_whatsapp",
        "ar": "لا إرسال واتساب بارد — مسودة + موافقة فقط",
        "en": "no_cold_whatsapp",
    },
    {
        "id": "no_linkedin_automation",
        "ar": "لا أتمتة LinkedIn — انشر يدوياً بعد SOAEN",
        "en": "no_linkedin_automation",
    },
    {
        "id": "no_external_gmail_without_approval",
        "ar": "لا Gmail خارجي بدون موافقة صريحة",
        "en": "external_action_requires_approval",
    },
    {
        "id": "no_invented_crm_kpi",
        "ar": "لا أرقام CRM أو KPI مخترعة — من kpi_founder_commercial_import.yaml فقط",
        "en": "kpi_from_import_only",
    },
    {
        "id": "no_revenue_before_paid",
        "ar": "لا upsell قبل Proof · لا إيراد قبل invoice_paid",
        "en": "proof_before_upsell",
    },
]

SOAEN_FIELDS_AR = [
    ("Source", "مصدر"),
    ("Owner", "مالك"),
    ("Approval", "موافقة"),
    ("Evidence", "دليل"),
    ("Next Action", "الخطوة التالية"),
]


def build_soaen_daily(*, date_str: str | None = None) -> dict[str, Any]:
    """Machine-readable SOAEN + doctrine snapshot for digest / API / CI."""
    from dealix.commercial_ops.strategy_refs import load_founder_strategy_refs, strategy_links_flat

    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    refs = load_founder_strategy_refs()
    return {
        "date": day,
        "schema_version": "1.0",
        "non_negotiables": NON_NEGOTIABLE_RULES,
        "soaen_checklist_ar": list(SOAEN_CHECKLIST_AR),
        "soaen_fields": [{"en": e, "ar": a} for e, a in SOAEN_FIELDS_AR],
        "approval_ui": "/ar/ops/approvals",
        "founder_ops": "/ar/ops/founder",
        "war_room": "/ar/ops/war-room",
        "marketing": "/ar/ops/marketing",
        "mode": "draft_only",
        "strategy_refs": refs,
        "strategy_doc_links": strategy_links_flat(),
        "strategy_cadence_ar": refs.get("cadence_ar"),
    }


def format_doctrine_markdown(block: dict[str, Any] | None = None) -> str:
    """Arabic markdown block for founder brief / terminal."""
    b = block or build_soaen_daily()
    lines = [
        f"## حوكمة اليوم · SOAEN · {b.get('date', '')}",
        "",
        "### غير قابل للتجاوز",
        "",
    ]
    for rule in b.get("non_negotiables") or []:
        lines.append(f"- **{rule.get('id')}** — {rule.get('ar')}")
    lines.extend(["", "### SOAEN (قبل أي لمسة أو منشور)", ""])
    for item in b.get("soaen_checklist_ar") or []:
        lines.append(f"- [ ] {item}")
    lines.extend(
        [
            "",
            f"- مركز الموافقات: `{b.get('approval_ui')}`",
            f"- وضع التشغيل: **{b.get('mode')}**",
            "",
        ]
    )
    return "\n".join(lines)


def doctrine_status() -> dict[str, Any]:
    """Quick health for launch verify — rules present, checklist non-empty."""
    block = build_soaen_daily()
    ok = bool(NON_NEGOTIABLE_RULES) and len(SOAEN_CHECKLIST_AR) >= 5
    return {
        "ok": ok,
        "rules_count": len(NON_NEGOTIABLE_RULES),
        "checklist_count": len(SOAEN_CHECKLIST_AR),
        "block": block,
    }
