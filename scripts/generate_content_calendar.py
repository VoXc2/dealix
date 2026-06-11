"""Generate a content calendar for the next N days.

Usage:
    python3 scripts/generate_content_calendar.py --days 30
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "growth" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


CATEGORIES = [
    "AI Operating Systems",
    "Revenue OS",
    "Review OS",
    "Command Centers",
    "Saudi B2B operations",
    "Follow-up leakage",
    "Proof reports",
    "Human-reviewed AI",
    "PDPL-aware AI operations",
    "Founder execution",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()

    today = dt.date.today()
    lines: list[str] = []
    lines.append(f"# Dealix Content Calendar — {today.isoformat()}")
    lines.append("")
    lines.append(f"Total days: {args.days}")
    lines.append("")
    lines.append("| Day | Date | Category | Title |")
    lines.append("|-----|------|----------|-------|")
    for i in range(args.days):
        d = today + dt.timedelta(days=i)
        cat = CATEGORIES[i % len(CATEGORIES)]
        title = f"{cat} — Day {i + 1} insight"
        lines.append(f"| {i + 1} | {d.isoformat()} | {cat} | {title} |")
    lines.append("")
    lines.append("## Cadence")
    lines.append("- 1 LinkedIn post per day (founder-led)")
    lines.append("- 1 X post per day")
    lines.append("- 1 industry case-card per week")
    lines.append("- 1 proof report per week (real, demo-flagged)")

    out = EXPORT_DIR / f"content-calendar-{today.isoformat()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
