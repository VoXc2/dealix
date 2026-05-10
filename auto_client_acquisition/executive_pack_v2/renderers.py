"""Wave 13 Phase 5 — Weekly Executive Pack renderers (customer + founder).

Two render functions:
  - render_for_customer(pack)  → Arabic-first MD; no internal terms; commitment language
  - render_for_founder(pack)   → full detail MD; internal terms allowed

Article 4: NEVER auto-sends; render returns string for founder to copy/paste.
Article 8: every numeric is_estimate=True; no fake revenue; commitment language only
  ("نسعى" / "هدفنا"), never "نضمن"/"guaranteed".
Article 11: thin renderers (~150 LOC); zero new business logic.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import (
    ExecutivePackRecord,
)


# Tokens forbidden in customer-facing output (Article 8 honesty)
_CUSTOMER_FORBIDDEN_TOKENS = (
    "guaranteed",
    "نضمن",
    "guarantee",
    "certified",
    "100%",
)

# Internal jargon never shown to customer (Article 6 — keep it customer-safe)
_INTERNAL_JARGON = (
    "leadops_spine",
    "support_inbox",
    "approval_center",
    "service_sessions",
    "customer_brain",
    "v10",
    "v11",
    "v12",
    "v13",
    "stacktrace",
    "pyo3",
    "_pycache_",
)


def _scrub_for_customer(text: str) -> str:
    """Remove internal jargon from customer-facing strings."""
    out = text
    for tok in _INTERNAL_JARGON:
        out = out.replace(tok, "")
    return out


def _kpi_line(label_ar: str, label_en: str, value: int | float, *, is_estimate: bool = True) -> str:
    """Render one KPI line bilingual with optional is_estimate marker."""
    suffix = "" if not is_estimate else " *"
    return f"- **{label_ar}** / {label_en}: {value}{suffix}"


def render_for_customer(pack: ExecutivePackRecord) -> str:
    """Customer-facing weekly pack (Arabic-first, no internal terms).

    5 sections per spec:
      1. ملخص الأسبوع
      2. أهم 3 نتائج
      3. أهم 3 قرارات الأسبوع القادم
      4. المخاطر
      5. التوصية الواحدة
    """
    leads = pack.leads or {}
    support = pack.support or {}
    decisions = pack.decisions or []
    risks = pack.risks or []
    next_actions = pack.next_3_actions or []

    label = pack.week_label or "هذا الأسبوع"

    lines: list[str] = []
    lines.append(f"# تقرير Dealix الأسبوعي — {label}")
    lines.append("")
    lines.append(f"**العميل:** {pack.customer_handle}")
    lines.append(f"**التاريخ:** {pack.built_at.date().isoformat()}")
    lines.append("")

    # 1. ملخص الأسبوع
    lines.append("## 1. ملخص الأسبوع")
    summary = pack.executive_summary_ar or "لا توجد تحديثات هذا الأسبوع."
    lines.append(_scrub_for_customer(summary))
    lines.append("")

    # 2. أهم 3 نتائج (KPIs)
    lines.append("## 2. أهم النتائج")
    lines.append(_kpi_line("الفرص الجديدة", "New leads", int(leads.get("leads_total", 0))))
    lines.append(_kpi_line("الفرص المسموح بها", "Allowed leads", int(leads.get("leads_allowed", 0))))
    lines.append(_kpi_line("المسودات الجاهزة", "Drafts ready for approval", int(leads.get("drafts_created", 0))))
    if support:
        lines.append(_kpi_line("تذاكر الدعم المفتوحة", "Open support tickets", int(support.get("tickets_open", 0))))
    lines.append("")

    # 3. أهم 3 قرارات للأسبوع القادم
    lines.append("## 3. أهم قرارات الأسبوع القادم")
    if next_actions:
        for i, act in enumerate(next_actions[:3], 1):
            summary_ar = _scrub_for_customer(act.get("summary_ar", "") or "")[:120]
            risk = act.get("risk_level", "low")
            lines.append(f"{i}. {summary_ar} _(مستوى المخاطرة: {risk})_")
    else:
        lines.append("لا قرارات معلّقة هذا الأسبوع.")
    lines.append("")

    # 4. المخاطر
    lines.append("## 4. المخاطر")
    if risks:
        for r in risks[:5]:
            lines.append(f"- {_scrub_for_customer(str(r.get('summary_ar', r)))}")
    else:
        lines.append("لا مخاطر مرصودة.")
    lines.append("")

    # 5. التوصية الواحدة (highest priority next action)
    lines.append("## 5. التوصية")
    if next_actions:
        top = next_actions[0]
        rec_ar = _scrub_for_customer(top.get("summary_ar", "") or "")[:200]
        lines.append(f"> {rec_ar}")
    else:
        lines.append("> ابدأ بمراجعة الفرص الجديدة في البوابة.")
    lines.append("")

    # Footer disclaimer (Article 8)
    lines.append("---")
    lines.append("_(*) جميع الأرقام تقديرات_ / _All numbers are estimates._")

    out = "\n".join(lines)

    # Final scrub: assert no forbidden tokens leaked
    lower = out.lower()
    for tok in _CUSTOMER_FORBIDDEN_TOKENS:
        if tok.lower() in lower:
            # Replace with neutral phrasing rather than crash (Article 8 graceful)
            out = out.replace(tok, "نسعى لتحقيقها")
    return out


def render_for_founder(pack: ExecutivePackRecord) -> str:
    """Founder-facing weekly pack (full detail; internal terms OK).

    Same 5 sections + appendix with internal data sources.
    """
    leads = pack.leads or {}
    support = pack.support or {}
    decisions = pack.decisions or []
    blockers = pack.blockers or []
    risks = pack.risks or []
    next_actions = pack.next_3_actions or []
    appendix = pack.appendix or {}

    label = pack.week_label or "this_week"

    lines: list[str] = []
    lines.append(f"# Dealix Weekly Executive Pack — {label} (FOUNDER VIEW)")
    lines.append("")
    lines.append(f"**Customer:** {pack.customer_handle}")
    lines.append(f"**Cadence:** {pack.cadence}")
    lines.append(f"**Built at:** {pack.built_at.isoformat()}")
    lines.append(f"**Pack id:** {pack.pack_id}")
    lines.append("")

    # 1. Summary (bilingual)
    lines.append("## 1. Summary / ملخص الأسبوع")
    lines.append(f"**EN:** {pack.executive_summary_en}")
    lines.append(f"**AR:** {pack.executive_summary_ar}")
    lines.append("")

    # 2. KPIs (full)
    lines.append("## 2. KPIs (full)")
    lines.append("### Lead KPIs")
    for k, v in leads.items():
        lines.append(f"  - `{k}`: {v}")
    lines.append("### Support KPIs")
    for k, v in support.items():
        lines.append(f"  - `{k}`: {v}")
    lines.append("### Revenue movement")
    for k, v in (pack.revenue_movement or {}).items():
        lines.append(f"  - `{k}`: {v}")
    lines.append("")

    # 3. Top 3 next actions (full detail)
    lines.append("## 3. Top 3 next actions")
    for i, act in enumerate(next_actions[:3], 1):
        lines.append(f"{i}. **{act.get('action_type', '?')}** "
                     f"(channel={act.get('channel', '?')}, risk={act.get('risk_level', '?')})")
        lines.append(f"   - approval_id: `{act.get('approval_id', 'n/a')}`")
        lines.append(f"   - AR: {act.get('summary_ar', '')[:200]}")
    lines.append("")

    # 4. Risks + blockers
    lines.append("## 4. Risks + blockers")
    lines.append("### Risks")
    for r in risks:
        lines.append(f"  - {r}")
    lines.append("### Blockers")
    for b in blockers:
        lines.append(f"  - {b}")
    lines.append("")

    # 5. Recommendation (founder-flavored)
    lines.append("## 5. Recommendation")
    if next_actions:
        top = next_actions[0]
        lines.append(f"Approve action `{top.get('approval_id', '?')}` first; it has the highest "
                     f"customer-impact + lowest risk.")
    else:
        lines.append("No pending actions; consider sending a fresh lead-prep run.")
    lines.append("")

    # Appendix
    lines.append("## Appendix")
    lines.append(f"  - sector_context: `{pack.sector_context}`")
    lines.append(f"  - active_sessions: `{appendix.get('active_sessions', [])}`")
    lines.append(f"  - built_from: `{appendix.get('built_from', [])}`")
    lines.append(f"  - safety_summary: `{pack.safety_summary}`")
    lines.append("")
    lines.append("---")
    lines.append("_All metrics are estimates; revenue is recognized only on payment_confirmed state._")

    return "\n".join(lines)


def render_pack(pack: ExecutivePackRecord, *, audience: str = "customer") -> str:
    """Dispatch to the right renderer based on audience."""
    if audience == "founder":
        return render_for_founder(pack)
    if audience == "customer":
        return render_for_customer(pack)
    raise ValueError(f"unknown audience: {audience} (expected 'customer' or 'founder')")
