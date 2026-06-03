#!/usr/bin/env python3
"""
Dealix Delivery Report Generator
================================
Reads the delivery data files and renders the post-win operating reports:

  - reports/delivery/DELIVERY_PIPELINE_STATUS.md
  - reports/delivery/DELIVERY_BLOCKERS.md
  - reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md

Core gate: delivery cannot start before the five required things exist —
system, scope, success_metric, delivery_owner, and all required_inputs provided.
"""

import json
from pathlib import Path

RUN_DATE = "2026-06-03"

STAGE_ORDER = [
    "interested",
    "qualified",
    "mini_proposal_ready",
    "proposal_sent",
    "payment_handoff",
    "won",
    "intake_required",
    "delivery_started",
    "first_output_ready",
    "client_review",
    "accepted",
    "weekly_value_report",
    "renewal_candidate",
]

# Stages at which a not-ready pipeline counts as an active delivery blocker.
BLOCKER_STAGES = {"won", "intake_required", "delivery_started", "first_output_ready", "client_review"}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    except FileNotFoundError:
        print(f"Warning: {path} not found.")
    return rows


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def cell(value: str) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def stage_index(stage: str) -> int:
    return STAGE_ORDER.index(stage) if stage in STAGE_ORDER else -1


def missing_requirements(p: dict) -> list[str]:
    """Return which of the five required things are missing for a pipeline."""
    missing = []
    if not str(p.get("system", "")).strip():
        missing.append("system")
    if not str(p.get("scope", "")).strip():
        missing.append("scope")
    if not str(p.get("success_metric", "")).strip():
        missing.append("success_metric")
    if not str(p.get("delivery_owner", "")).strip():
        missing.append("delivery_owner")
    inputs = p.get("required_inputs", [])
    not_provided = [ri.get("name") for ri in inputs if not ri.get("provided")]
    if not inputs or not_provided:
        missing.append("required_inputs (" + ", ".join(not_provided) + ")" if not_provided else "required_inputs")
    return missing


def report_pipeline_status(pipelines: list[dict]) -> str:
    md = [
        "# Dealix — Delivery Pipeline Status",
        f"*Date: {RUN_DATE} | Pipelines: {len(pipelines)}*",
        "",
        "| # | Company | System | Stage | Owner | Inputs | Ready to deliver? |",
        "|---|---------|--------|-------|-------|--------|-------------------|",
    ]
    for i, p in enumerate(pipelines, start=1):
        inputs = p.get("required_inputs", [])
        provided = sum(1 for ri in inputs if ri.get("provided"))
        missing = missing_requirements(p)
        ready = "✅ Ready" if not missing else "🔴 Not ready"
        owner = p.get("delivery_owner") or "—"
        md.append(
            f"| {i} | {cell(p.get('company'))} | {cell(p.get('system'))} | "
            f"{cell(p.get('stage'))} | {cell(owner)} | {provided}/{len(inputs)} | {ready} |"
        )
    # Stage counts
    counts: dict[str, int] = {}
    for p in pipelines:
        counts[p.get("stage", "—")] = counts.get(p.get("stage", "—"), 0) + 1
    md += ["", "## Stage Distribution", "", "| Stage | Count |", "|-------|------:|"]
    for s in STAGE_ORDER:
        if s in counts:
            md.append(f"| {s} | {counts[s]} |")
    md += ["", f"*Generated from data/delivery/pipelines.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def report_blockers(pipelines: list[dict]) -> str:
    blocked = []
    for p in pipelines:
        missing = missing_requirements(p)
        if missing and p.get("stage") in BLOCKER_STAGES:
            blocked.append((p, missing))
    md = [
        "# Dealix — Delivery Blockers",
        f"*Date: {RUN_DATE} | Blocked pipelines: {len(blocked)}*",
        "",
        "> القاعدة: لا يبدأ التسليم قبل توفر الخمسة: النظام، Scope، المدخلات المطلوبة، success metric، مسؤول التسليم.",
        "",
    ]
    if not blocked:
        md += ["✅ لا توجد عوائق تسليم حالياً — كل خط نشط جاهز للبدء.", ""]
    else:
        md += [
            "| # | Company | System | Stage | Missing (Delivery Not Ready) | Listed Blockers |",
            "|---|---------|--------|-------|------------------------------|-----------------|",
        ]
        for i, (p, missing) in enumerate(blocked, start=1):
            md.append(
                f"| {i} | {cell(p.get('company'))} | {cell(p.get('system'))} | "
                f"{cell(p.get('stage'))} | {cell('; '.join(missing))} | "
                f"{cell('; '.join(p.get('blockers', [])) or '—')} |"
            )
        md += ["", "## Action per Blocker", ""]
        for p, missing in blocked:
            md.append(f"### {p.get('company')} — {p.get('system')} → `Delivery Not Ready`")
            md.append(f"- **Stage:** {p.get('stage')}")
            md.append(f"- **Missing:** {', '.join(missing)}")
            md.append(f"- **Action:** اجمع النواقص أعلاه قبل الانتقال إلى `delivery_started`.")
            md.append("")
    md += [f"*Generated from data/delivery/pipelines.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def report_weekly_value_queue(reports: list[dict]) -> str:
    pending = [r for r in reports if r.get("acceptance_status") == "pending"]
    md = [
        "# Dealix — Weekly Value Report Queue",
        f"*Date: {RUN_DATE} | Reports: {len(reports)} | Pending approval: {len(pending)}*",
        "",
        "> كل تقرير قيمة أسبوعي يبقى مسودة حتى موافقة المؤسس قبل الإرسال للعميل.",
        "",
        "| # | Company | System | Week Of | Value Delivered | Acceptance | Approval |",
        "|---|---------|--------|---------|-----------------|------------|----------|",
    ]
    status_emoji = {"accepted": "✅ Accepted", "pending": "🟡 Pending", "changes_requested": "🟠 Changes requested"}
    for i, r in enumerate(reports, start=1):
        acceptance = status_emoji.get(r.get("acceptance_status"), r.get("acceptance_status"))
        approval = "🟡 Needs approval" if r.get("approval_required") else "✅"
        md.append(
            f"| {i} | {cell(r.get('company'))} | {cell(r.get('system'))} | "
            f"{cell(r.get('week_of'))} | {cell(r.get('value_delivered'))} | {acceptance} | {approval} |"
        )
    md += ["", "## Report Detail", ""]
    for r in reports:
        md.append(f"### {r.get('company')} — Week of {r.get('week_of')}")
        md.append(f"- **Deliverables:** {', '.join(r.get('deliverables_completed', []))}")
        for m in r.get("metrics", []):
            md.append(f"- **{m.get('name')}:** {m.get('value')}")
        md.append(f"- **Next week:** {r.get('next_week_focus')}")
        if r.get("blockers"):
            md.append(f"- **Blockers:** {', '.join(r.get('blockers'))}")
        md.append("")
    md += [f"*Generated from data/delivery/weekly_value_reports.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    data = base / "data" / "delivery"
    out = base / "reports" / "delivery"

    pipelines = load_jsonl(data / "pipelines.jsonl")
    reports = load_jsonl(data / "weekly_value_reports.jsonl")

    write(out / "DELIVERY_PIPELINE_STATUS.md", report_pipeline_status(pipelines))
    write(out / "DELIVERY_BLOCKERS.md", report_blockers(pipelines))
    write(out / "WEEKLY_VALUE_REPORT_QUEUE.md", report_weekly_value_queue(reports))

    print("✅ Delivery reports generated")
    print(f"   Pipelines: {len(pipelines)} | Weekly value reports: {len(reports)}")
    print(f"   Output: {out}")


if __name__ == "__main__":
    main()
