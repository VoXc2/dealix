"""Generate the daily Dealix CEO brief in Markdown.

Usage:
    python3 scripts/generate_daily_ceo_brief.py

Outputs:
    business/reports/exports/dealix-daily-ceo-brief-YYYY-MM-DD.txt
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "reports" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


ACQUISITION_FUNNEL = [
    ("Discover", "اكتشاف", "Identify companies with visible operational leakage."),
    ("Qualify", "تأهيل", "Score against BANT, segment, weakness severity."),
    ("Outreach (Drafts Only)", "تواصل (مسوّدة فقط)", "Generate bilingual drafts."),
    ("Human Review Gate", "بوابة المراجعة البشرية", "Approve/reject every draft."),
    ("Workflow Review Call", "مكالمة مراجعة سير العمل", "20-min diagnostic call."),
    ("Proposal", "عرض رسمي", "Generate bilingual proposal."),
    ("Close", "إغلاق", "Convert to won deal with setup + retainer."),
    ("Deliver", "تسليم", "Run Delivery OS end-to-end."),
    ("Retain & Expand", "احتفاظ وتوسعة", "Monthly review + expansion offer."),
]

DELIVERY_PIPELINE = [
    ("Day 0 — Intake", "0–1", "Signed contract, stakeholder map, channel of truth."),
    ("Workflow Map", "2–4", "End-to-end workflow map, pain points tagged."),
    ("Command Center Setup", "5–8", "URL live, owners assigned, cadence defined."),
    ("Automation Build", "9–14", "Top 3 automations live + fallback + audit log."),
    ("Weekly Executive Review", "15+", "Weekly report, sign-off, proof items logged."),
    ("Expansion", "30+", "Quarterly review, expansion offer, case study draft."),
]

KPIS = [
    ("MRR (SAR)", 250000, 42000, "monthly", "watch"),
    ("Active Retainers", 12, 3, "monthly", "on_track"),
    ("Proposal → Close %", 35, 22, "monthly", "watch"),
    ("Drafts Pending Review", 0, 14, "daily", "off_track"),
    ("Follow-ups Due Today", 5, 8, "daily", "on_track"),
    ("Proof Items Logged", 20, 7, "monthly", "watch"),
]

PRIORITIES = [
    (1, "Clear the review queue", 1),
    (2, "Ship launch brief + CEO brief", 1),
    (3, "First 100 leads plan", 3),
    (4, "Deployment readiness", 5),
    (5, "First retainer contract", 14),
]


def render_brief(date: dt.date) -> str:
    lines: list[str] = []
    lines.append(f"# Dealix Daily CEO Brief — {date.isoformat()}")
    lines.append("")
    lines.append("## 1. Acquisition Moves")
    for title, title_ar, goal in ACQUISITION_FUNNEL[:5]:
        lines.append(f"- **{title}** ({title_ar}): {goal}")
    lines.append("")
    lines.append("## 2. Delivery Moves")
    for title, day_range, deliverable in DELIVERY_PIPELINE[:3]:
        lines.append(f"- **{title}** ({day_range}) — {deliverable}")
    lines.append("")
    lines.append("## 3. KPI Checks")
    for label, target, current, cadence, status in KPIS:
        gap = 0 if target == 0 else round(((current - target) / max(1, target)) * 100)
        arrow = "OK" if gap >= 0 else "GAP"
        lines.append(
            f"- [{arrow}] {label}: target {target}, current {current} ({gap}%) — {cadence} · {status}"
        )
    lines.append("")
    lines.append("## 4. Risks")
    lines.append("- Review queue not cleared → no outreach should be sent.")
    lines.append("- Conversion rate below 35% — tighten close criteria and proposal quality.")
    lines.append("- Proof vault underused — coach delivery lead to log proof items weekly.")
    lines.append("- MRR target not met — slow expansion, speed up retainer conversion.")
    lines.append("")
    lines.append("## 5. Operating Focus")
    for rank, title, due in PRIORITIES:
        lines.append(f"- [P{rank}] {title} — due in {due}d")
    lines.append("")
    lines.append("---")
    lines.append("Draft only. Human review required before any external action.")
    return "\n".join(lines) + "\n"


def main() -> None:
    today = dt.date.today()
    out_path = EXPORT_DIR / f"dealix-daily-ceo-brief-{today.isoformat()}.txt"
    out_path.write_text(render_brief(today), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
