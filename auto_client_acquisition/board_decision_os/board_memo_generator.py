"""Board memo — Markdown template + deterministic fill."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.schemas import BoardMemoMetrics

MEMO_SECTIONS_AR: list[tuple[str, str]] = [
    ("ملخص تنفيذي", "executive_summary_ar"),
    ("جودة الإيراد", "revenue_quality_ar"),
    ("الدليل والقيمة", "proof_value_ar"),
    ("فرص الريتينر", "retainer_ar"),
    ("الحوكمة والمخاطر", "governance_ar"),
    ("طابور المنتَجات", "productization_ar"),
    ("صحة العملاء", "client_health_ar"),
    ("ذكاء السوق", "market_intel_ar"),
    ("نضج وحدات الأعمال", "bu_maturity_ar"),
    ("قائمة الإيقاف", "kill_list_ar"),
    ("تخصيص رأس المال", "capital_allocation_ar"),
    ("الرهانات الاستراتيجية القادمة", "next_bets_ar"),
]

MEMO_SECTIONS_EN: list[tuple[str, str]] = [
    ("Executive Summary", "executive_summary_en"),
    ("Revenue Quality", "revenue_quality_en"),
    ("Proof & Value", "proof_value_en"),
    ("Retainer Opportunities", "retainer_en"),
    ("Governance & Risk", "governance_en"),
    ("Productization Queue", "productization_en"),
    ("Client Health", "client_health_en"),
    ("Market Intelligence", "market_intel_en"),
    ("Business Unit Maturity", "bu_maturity_en"),
    ("Stop / Kill List", "kill_list_en"),
    ("Capital Allocation", "capital_allocation_en"),
    ("Next Strategic Bets", "next_bets_en"),
]


def board_memo_template_markdown() -> str:
    lines = ["# Dealix Board Memo", "", "_Template — املأ الأقسام بالبيانات أو عبر واجهة API._", ""]
    for title, _ in MEMO_SECTIONS_AR:
        lines.append(f"## {title}")
        lines.append("")
        lines.append("<!-- TODO -->")
        lines.append("")
    return "\n".join(lines)


def build_board_memo(metrics: BoardMemoMetrics, *, locale: str = "bilingual") -> str:
    """Return Markdown memo with Arabic and/or English sections."""
    data = metrics.model_dump()
    parts: list[str] = ["# Dealix Board Memo", ""]

    if locale in ("ar", "bilingual"):
        parts.append("## النسخة العربية")
        parts.append("")
        for title, key in MEMO_SECTIONS_AR:
            body = (data.get(key) or "_لا توجد بيانات بعد._").strip()
            parts.append(f"### {title}")
            parts.append("")
            parts.append(body)
            parts.append("")

    if locale in ("en", "bilingual"):
        parts.append("## English")
        parts.append("")
        for title, key in MEMO_SECTIONS_EN:
            body = (data.get(key) or "_No data yet._").strip()
            parts.append(f"### {title}")
            parts.append("")
            parts.append(body)
            parts.append("")

    return "\n".join(parts).strip() + "\n"
