"""Auto-fill commercial weekly scorecard from evidence CSV (no invented CRM numbers)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    is_placeholder_evidence_row,
    load_evidence_rows,
)
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.targeting_csv import load_targets

KPI_TYPES = [
    "message_sent_manual",
    "reply_received",
    "demo_booked",
    "scope_requested",
    "invoice_sent",
    "payment_received",
    "proof_pack_delivered",
    "partner_intro_created",
]


def build_weekly_scorecard(*, week_end: datetime | None = None) -> dict[str, Any]:
    end = (week_end or datetime.now(UTC)).date()
    start = end - timedelta(days=6)
    rows = load_evidence_rows()

    week_counts: dict[str, int] = dict.fromkeys(KPI_TYPES, 0)
    pilots_proof = 0
    for row in rows:
        if is_placeholder_evidence_row(row):
            continue
        raw = (row.get("event_date") or "").strip()[:10]
        try:
            ed = datetime.fromisoformat(raw).date() if raw else None
        except ValueError:
            ed = None
        if ed is None or not (start <= ed <= end):
            continue
        et = (row.get("event_type") or "").strip()
        if et in week_counts:
            week_counts[et] += 1
        if et == "proof_pack_delivered":
            pilots_proof += 1

    all_targets = load_targets()
    agency_in_pool = sum(
        1
        for r in all_targets
        if (r.get("segment") or "").strip().lower() in ("agency_wedge", "agency", "")
    )

    paid = analyze_first_paid_diagnostic()
    evidence = count_evidence_events(rows, on_date=end, exclude_placeholders=True)

    demo = week_counts.get("demo_booked", 0)
    invoice = week_counts.get("invoice_sent", 0)
    conversion = f"{(invoice / demo * 100):.0f}%" if demo else "n/a"

    return {
        "week_end": end.isoformat(),
        "week_start": start.isoformat(),
        "generated_at": datetime.now(UTC).isoformat(),
        "kpi_week": week_counts,
        "north_star": {
            "pilots_active_note": "املأ يدوياً من التسليم الجاري",
            "proof_packs_delivered_week": pilots_proof,
        },
        "motion_a": {"agencies_in_pool": agency_in_pool},
        "conversion_demo_to_invoice": conversion,
        "first_paid_verdict": paid["verdict"],
        "evidence_today_total": evidence["today_total"],
        "template_doc": "docs/commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md",
    }


def render_weekly_scorecard_markdown(blob: dict[str, Any]) -> str:
    kpi = blob.get("kpi_week") or {}
    ns = blob.get("north_star") or {}
    ma = blob.get("motion_a") or {}
    lines = [
        "# Commercial Weekly Scorecard (auto)",
        "",
        f"**أسبوع ينتهي:** {blob.get('week_end')} · **من:** {blob.get('week_start')}",
        f" · **توليد:** {blob.get('generated_at')}",
        "",
        "## North Star",
        f"- Proof Packs مسلّمة هذا الأسبوع: **{ns.get('proof_packs_delivered_week', 0)}**",
        f"- Pilots نشطة: _{ns.get('pilots_active_note', 'fill')}_",
        "",
        "## Evidence funnel (7 أيام)",
        "",
        "| KPI | الفعلي |",
        "|-----|--------|",
    ]
    for key in KPI_TYPES:
        lines.append(f"| `{key}` | {kpi.get(key, 0)} |")
    lines.extend(
        [
            "",
            f"**معدل تحويل demo → invoice:** {blob.get('conversion_demo_to_invoice')}",
            "",
            "## Motion A",
            f"- وكالات في pool: {ma.get('agencies_in_pool', 0)}",
            "",
            "## First paid Diagnostic",
            f"- verdict: `{blob.get('first_paid_verdict')}`",
            "",
            "> أكمل الأعمدة اليدوية في COMMERCIAL_WEEKLY_SCORECARD_AR.md عند الحاجة.",
            "",
        ]
    )
    return "\n".join(lines)
