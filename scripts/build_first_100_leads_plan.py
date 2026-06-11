"""Build the first 100 leads execution plan (demo).

Usage:
    python3 scripts/build_first_100_leads_plan.py --mode demo
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "lead-lists" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


SEGMENTS = [
    ("marketing_agency", 25),
    ("training", 20),
    ("clinic", 15),
    ("real_estate", 15),
    ("logistics", 15),
    ("partner", 10),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# First 100 Leads Execution Plan — {today}")
    lines.append("")
    lines.append(f"Mode: {args.mode}")
    lines.append("")
    lines.append("## Segment split")
    for s, n in SEGMENTS:
        lines.append(f"- {s}: {n} leads")
    lines.append("")
    lines.append("## Per-segment plan")
    for s, n in SEGMENTS:
        lines.append(f"### {s} ({n} leads)")
        lines.append("- Source: manual research + open data + founder-supplied CSV")
        lines.append("- Visible signals to look for: weakness in workflow, slow response, scattered reporting")
        lines.append("- Recommended offer: based on weakness")
        lines.append("- Review gate: every draft")
        lines.append("")

    lines.append("## Daily cadence")
    lines.append("- Monday: 25 leads researched")
    lines.append("- Tuesday: drafts generated for top 10")
    lines.append("- Wednesday: review queue cleared")
    lines.append("- Thursday: 25 more leads researched")
    lines.append("- Friday: 25 more leads researched + Friday review")
    lines.append("")

    lines.append("## Safety")
    lines.append("- No auto-send. Every draft needs human review.")
    lines.append("- Demo data is marked demo=true.")
    lines.append("- Source URL/quote required for every lead.")

    out = EXPORT_DIR / f"first-100-leads-plan-{today}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
