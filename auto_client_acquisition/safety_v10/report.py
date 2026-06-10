"""Bilingual markdown report rendering for an EvalReport."""
from __future__ import annotations

from auto_client_acquisition.safety_v10.schemas import EvalReport


def render_report(report: EvalReport) -> str:
    """Render an EvalReport as bilingual (Arabic + English) Markdown.

    Returns a single string suitable for stdout, a Markdown file, or a
    GitHub issue body. No external claims, no marketing language.
    """
    lines: list[str] = []
    lines.append("# Safety v10 — Red-Team Eval Report / تقرير اختبار الأمان")
    lines.append("")
    lines.append("## Summary / الملخّص")
    lines.append("")
    lines.append(f"- Total cases / مجموع الحالات: **{report.total}**")
    lines.append(f"- Passed / نجح: **{report.passed}**")
    lines.append(f"- Failed / فشل: **{report.failed}**")
    lines.append("")
    lines.append("## By category / حسب الفئة")
    lines.append("")
    lines.append("| Category / الفئة | Total | Passed | Failed |")
    lines.append("| --- | ---: | ---: | ---: |")
    for cat, counts in sorted(report.by_category.items()):
        lines.append(
            f"| `{cat}` | {counts.get('total', 0)} | "
            f"{counts.get('passed', 0)} | {counts.get('failed', 0)} |"
        )
    lines.append("")
    lines.append("## Failures / الإخفاقات")
    lines.append("")
    failures = [r for r in report.results if not r.passed]
    if not failures:
        lines.append("_No failures — every case reached the expected action._")
        lines.append("_لا توجد إخفاقات — كل الحالات وصلت للإجراء المتوقّع._")
    else:
        lines.append("| Case ID | Category | Actual | Reason |")
        lines.append("| --- | --- | --- | --- |")
        for r in failures:
            cat = r.category.value if hasattr(r.category, "value") else str(r.category)
            lines.append(
                f"| `{r.case_id}` | `{cat}` | `{r.actual_action}` | {r.reason} |"
            )
    lines.append("")
    lines.append("## Guardrails / حواجز الأمان")
    lines.append("")
    lines.append("- no_live_send / لا إرسال مباشر")
    lines.append("- no_live_charge / لا خصم تلقائي")
    lines.append("- no_scraping / لا scraping")
    lines.append("- no_linkedin_automation / لا أتمتة LinkedIn")
    lines.append("- no_cold_outreach / لا تواصل بارد")
    lines.append("- approval_required_for_external_actions / موافقة بشرية مطلوبة")
    lines.append("")
    return "\n".join(lines)
