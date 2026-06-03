"""Proof Pack outline generator — aligned with docs/delivery/PROOF_PACK_TEMPLATE.md."""

from __future__ import annotations

from typing import Any

PROOF_PACK_SECTIONS: tuple[tuple[str, str], ...] = (
    ("executive_summary", "ملخص تنفيذي"),
    ("workflow_map", "خريطة مسارات الإيراد"),
    ("source_quality", "جودة المصادر / CRM"),
    ("approval_boundaries", "حدود الموافقة"),
    ("evidence_trail_gaps", "فجوات مسار الأدلة"),
    ("revenue_leakage", "نقاط تسرّب الإيراد"),
    ("top_3_decisions", "أعلى 3 قرارات محكومة"),
    ("recommended_sprint", "توصية Sprint"),
    ("evidence_appendix", "ملحق الأدلة"),
    ("action_plan_30d", "خطة 30 يوم"),
)


def build_proof_pack_draft(
    *,
    company: str = "",
    locale: str = "ar",
    findings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a structured draft; every numeric claim must carry source or is_estimate."""
    company_label = company.strip() or ("العميل" if locale == "ar" else "Client")
    sections: list[dict[str, Any]] = []

    for key, title_ar in PROOF_PACK_SECTIONS:
        sections.append(
            {
                "id": key,
                "title_ar": title_ar,
                "title_en": key.replace("_", " ").title(),
                "body_ar": f"[مسودة — {company_label}] يُعبّأ بعد جمع المدخلات المعتمدة.",
                "body_en": f"[Draft — {company_label}] Populated after approved inputs.",
                "sources": [],
                "is_estimate": False,
                "status": "pending_inputs",
            },
        )

    normalized_findings: list[dict[str, Any]] = []
    for raw in findings or []:
        item = dict(raw)
        if "source" not in item and "sources" not in item:
            item["sources"] = []
            item["missing_source"] = True
        if "is_estimate" not in item:
            item["is_estimate"] = bool(item.get("estimate"))
        normalized_findings.append(item)

    return {
        "locale": locale,
        "company": company_label,
        "sections": sections,
        "findings": normalized_findings,
        "governance": {
            "requires_founder_review_before_external_share": True,
            "no_fake_kpi": True,
            "numeric_claim_policy": "source_or_is_estimate_required",
        },
        "disclaimer_ar": (
            "هذه مسودة هيكلية. أي رقم تجريبي يُوسم is_estimate=true "
            "ولا يُباع كحقيقة تشغيلية."
        ),
        "disclaimer_en": (
            "Structural draft only. Trial numbers must be is_estimate=true "
            "and are not sold as operational fact."
        ),
    }
