#!/usr/bin/env python3
"""
Dealix Acquisition Report Generator
===================================
Reads the acquisition data files and renders the daily operating reports:

  - reports/acquisition/DAILY_COMPANY_INTELLIGENCE_PACKS.md
  - reports/acquisition/CALL_FOLLOWUP_QUEUE.md
  - reports/acquisition/MINI_PROPOSAL_QUEUE.md
  - reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md

Every email/proposal is shown as a DRAFT pending founder approval — nothing in
these reports is auto-sent.
"""

import json
from datetime import datetime
from pathlib import Path

RUN_DATE = "2026-06-03"


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
    """Make a string safe for a single markdown table cell."""
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def report_company_intelligence(packs: list[dict]) -> str:
    md = [
        "# Dealix — Daily Company Intelligence Packs",
        f"*Date: {RUN_DATE} | Packs: {len(packs)} | Status: every outreach is a DRAFT pending founder approval*",
        "",
        "> القاعدة: لا يُرسل أي بريد قبل موافقة المؤسس. هذا التقرير للتجهيز والتوجيه فقط.",
        "",
        "| # | Company | Sector | Recommended System | First Contact | Likely Pain | Risk | Approval | Next Action |",
        "|---|---------|--------|--------------------|---------------|-------------|------|----------|-------------|",
    ]
    for i, p in enumerate(packs, start=1):
        approval = "🟡 Draft — needs approval" if p.get("approval_required") else "✅"
        md.append(
            f"| {i} | {cell(p.get('company'))} | {cell(p.get('sector'))} | "
            f"{cell(p.get('recommended_system'))} | {cell(p.get('best_contact_role'))} | "
            f"{cell(p.get('likely_pain'))} | {cell(p.get('risk_level'))} | {approval} | "
            f"{cell(p.get('next_action'))} |"
        )
    # System distribution
    counts: dict[str, int] = {}
    for p in packs:
        s = p.get("recommended_system", "—")
        counts[s] = counts.get(s, 0) + 1
    md += ["", "## System Distribution", "", "| System | Companies |", "|--------|-----------:|"]
    for s, c in sorted(counts.items(), key=lambda x: -x[1]):
        md.append(f"| {cell(s)} | {c} |")
    md += ["", f"*Generated from data/acquisition/company_intelligence_packs.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def report_call_followup_queue(briefs: list[dict]) -> str:
    md = [
        "# Dealix — Call Follow-up Queue",
        f"*Date: {RUN_DATE} | Briefs: {len(briefs)} | Caller: human only (no automated calling)*",
        "",
        "> كل Call Brief مخصص لمتصل بشري. لا يوجد اتصال آلي بالعملاء.",
        "",
        "| # | Company | Contact Role | System | Call Objective | Opening Line | Next Step |",
        "|---|---------|--------------|--------|----------------|--------------|-----------|",
    ]
    for i, b in enumerate(briefs, start=1):
        md.append(
            f"| {i} | {cell(b.get('company'))} | {cell(b.get('contact_role'))} | "
            f"{cell(b.get('recommended_system'))} | {cell(b.get('call_objective'))} | "
            f"{cell(b.get('opening_line'))} | {cell(b.get('next_step'))} |"
        )
    md += ["", "## Discovery Questions per Company", ""]
    for b in briefs:
        md.append(f"### {b.get('company')} — {b.get('recommended_system')}")
        md.append(f"- **Opening:** {b.get('opening_line')}")
        for q in b.get("discovery_questions", []):
            md.append(f"- Q: {q}")
        if b.get("expected_objection"):
            md.append(f"- **Expected objection:** {b.get('expected_objection')}")
            md.append(f"- **Best response:** {b.get('best_response')}")
        md.append(f"- **Next step:** {b.get('next_step')}")
        md.append("")
    md += [f"*Generated from data/acquisition/call_briefs.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def report_mini_proposal_queue(proposals: list[dict]) -> str:
    md = [
        "# Dealix — Mini Proposal Queue",
        f"*Date: {RUN_DATE} | Proposals: {len(proposals)} | Every proposal needs founder approval before sending*",
        "",
        "> لا يُرسل أي عرض قبل موافقة المؤسس. لا توجد وعود عائد مضمونة في أي عرض.",
        "",
        "| # | Title | Company | System | First Sprint | Timeline | Starter Price | Approval |",
        "|---|-------|---------|--------|--------------|----------|---------------|----------|",
    ]
    for i, p in enumerate(proposals, start=1):
        approval = "🟡 Needs approval" if p.get("approval_required") else "✅"
        md.append(
            f"| {i} | {cell(p.get('title'))} | {cell(p.get('company'))} | "
            f"{cell(p.get('recommended_system'))} | {cell(p.get('first_sprint'))} | "
            f"{cell(p.get('timeline'))} | {cell(p.get('starter_price'))} | {approval} |"
        )
    md += ["", "## Deliverables per Proposal", ""]
    for p in proposals:
        md.append(f"### {p.get('title')}")
        md.append(f"- **Pain:** {p.get('current_likely_pain')}")
        md.append(f"- **Deliverables:** {', '.join(p.get('deliverables', []))}")
        md.append(f"- **Expected first proof:** {p.get('expected_first_proof')}")
        md.append(f"- **Next step:** {p.get('next_step')}")
        md.append("")
    md += [f"*Generated from data/acquisition/mini_proposals.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def report_email_to_call_handoff(packs: list[dict], briefs: list[dict]) -> str:
    briefs_by_company = {b.get("company"): b for b in briefs}
    md = [
        "# Dealix — Email → Call Handoff Queue",
        f"*Date: {RUN_DATE} | Companies: {len(packs)}*",
        "",
        "> المسار: مسودة بريد (بانتظار موافقة المؤسس) ← Call Brief جاهز لمتصل بشري.",
        "",
        "| # | Company | System | Email Subject (draft) | Email Status | Call Brief | Contact Role | Next Step |",
        "|---|---------|--------|-----------------------|--------------|-----------|--------------|-----------|",
    ]
    for i, p in enumerate(packs, start=1):
        b = briefs_by_company.get(p.get("company"), {})
        email_status = "🟡 Draft — awaiting approval" if p.get("approval_required") else "✅ Approved"
        md.append(
            f"| {i} | {cell(p.get('company'))} | {cell(p.get('recommended_system'))} | "
            f"{cell(p.get('email_subject'))} | {email_status} | {cell(b.get('brief_id', '—'))} | "
            f"{cell(b.get('contact_role', p.get('best_contact_role')))} | {cell(b.get('next_step', p.get('next_action')))} |"
        )
    md += ["", f"*Generated from company_intelligence_packs.jsonl + call_briefs.jsonl on {RUN_DATE}*", ""]
    return "\n".join(md)


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    data = base / "data" / "acquisition"
    out = base / "reports" / "acquisition"

    packs = load_jsonl(data / "company_intelligence_packs.jsonl")
    briefs = load_jsonl(data / "call_briefs.jsonl")
    proposals = load_jsonl(data / "mini_proposals.jsonl")

    write(out / "DAILY_COMPANY_INTELLIGENCE_PACKS.md", report_company_intelligence(packs))
    write(out / "CALL_FOLLOWUP_QUEUE.md", report_call_followup_queue(briefs))
    write(out / "MINI_PROPOSAL_QUEUE.md", report_mini_proposal_queue(proposals))
    write(out / "EMAIL_TO_CALL_HANDOFF_QUEUE.md", report_email_to_call_handoff(packs, briefs))

    print("✅ Acquisition reports generated")
    print(f"   Packs: {len(packs)} | Briefs: {len(briefs)} | Proposals: {len(proposals)}")
    print(f"   Output: {out}")


if __name__ == "__main__":
    main()
