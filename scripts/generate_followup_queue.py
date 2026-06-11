"""Generate the follow-up queue for the next 7 days.

Usage:
    python3 scripts/generate_followup_queue.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
EXPORT_DIR = REPO_ROOT / "business" / "crm" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    if not LEADS_PATH.exists():
        print(f"missing: {LEADS_PATH}")
        return 1
    data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])
    today = dt.date.today()

    lines: list[str] = []
    lines.append("# Dealix Follow-up Queue")
    lines.append("")
    lines.append(f"Generated: {today.isoformat()}")
    lines.append("")
    due: list[dict] = []
    upcoming: list[dict] = []
    for a in accounts:
        na = a.get("nextAction")
        nd = a.get("nextActionDate")
        if not (na and nd):
            continue
        try:
            d = dt.date.fromisoformat(nd)
        except ValueError:
            continue
        if d <= today:
            due.append({"name": a["name"], "action": na, "date": nd})
        elif (d - today).days <= 7:
            upcoming.append({"name": a["name"], "action": na, "date": nd})

    lines.append(f"## Due today ({len(due)})")
    for x in due:
        lines.append(f"- {x['name']} — {x['action']} (was {x['date']})")
    lines.append("")
    lines.append(f"## Upcoming (next 7 days) ({len(upcoming)})")
    for x in upcoming:
        lines.append(f"- {x['name']} — {x['action']} on {x['date']}")
    lines.append("")
    lines.append("---")
    lines.append("Reminder: do NOT auto-send. Approve each draft via approve_outreach_draft.py first.")

    out = EXPORT_DIR / "dealix-followup-queue.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out} (due={len(due)} upcoming={len(upcoming)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
