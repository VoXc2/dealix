"""Executive Weekly Pack generator.

Wraps ``executive_reporting.build_weekly_report`` markdown_ar +
markdown_en in design-system HTML + bilingual markdown.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)


def generate_executive_weekly_pack(week_label: str = "") -> dict[str, Any]:
    """Compose a bilingual executive weekly pack artifact."""
    markdown_ar = ""
    markdown_en = ""
    label = week_label or ""
    risks_count = 0
    decisions_count = 0
    proof_count = 0
    try:
        from auto_client_acquisition.executive_reporting import (
            build_weekly_report,
        )

        report = build_weekly_report(week_label=week_label)
        markdown_ar = report.markdown_ar or ""
        markdown_en = report.markdown_en or ""
        label = report.week_label or label
        risks_count = len(report.risks or [])
        decisions_count = len(report.decisions or [])
        proof_total = (report.proof or {}).get("total", 0)
        try:
            proof_count = int(proof_total or 0)
        except Exception:  # noqa: BLE001
            proof_count = 0
    except Exception:  # noqa: BLE001 — defensive
        markdown_ar = "لا بيانات بعد / no data yet"
        markdown_en = "no data yet"

    title_ar = f"التقرير التنفيذي الأسبوعي — {label or 'هذا الأسبوع'}"
    title_en = f"Executive Weekly Pack — {label or 'this week'}"

    sections_ar = [
        {
            "title": "السياق",
            "body": (
                f"الأسبوع: {label or '—'}\n"
                f"عدد المخاطر: {risks_count}\n"
                f"عدد القرارات المعلّقة: {decisions_count}\n"
                f"أحداث الإثبات: {proof_count}"
            ),
        },
        {"title": "التقرير", "body": markdown_ar or "لا بيانات بعد / no data yet"},
    ]
    sections_en = [
        {
            "title": "Context",
            "body": (
                f"Week: {label or '-'}\n"
                f"Risks: {risks_count}\n"
                f"Pending decisions: {decisions_count}\n"
                f"Proof events: {proof_count}"
            ),
        },
        {"title": "Report", "body": markdown_en or "no data yet"},
    ]

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs = [
        "executive_reporting.build_weekly_report",
        f"week_label={label}",
        f"risks={risks_count}",
        f"decisions={decisions_count}",
    ]

    md_full = render_artifact_markdown(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )
    html = render_artifact_html(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )

    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "manifest": {
            "artifact_type": "executive_weekly_pack",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "week_label": label,
        },
    }
