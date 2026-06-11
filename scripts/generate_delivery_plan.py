"""Generate a delivery plan for a given account + offer.

Usage:
    python3 scripts/generate_delivery_plan.py --account "Demo Company" --offer "Revenue OS" --sector "Marketing Agency"
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "delivery" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


STAGES = [
    ("Day 0 — Intake", "Signed contract, stakeholder map, channel of truth."),
    ("Day 2–4 — Workflow Map", "End-to-end workflow map, pain points tagged."),
    ("Day 5–8 — Command Center Setup", "URL live, owners assigned, cadence defined."),
    ("Day 9–14 — Automation Build", "Top 3 automations live + fallback + audit log."),
    ("Day 15+ — Weekly Review", "Weekly report, sign-off, proof items logged."),
    ("Day 30+ — Expansion", "Quarterly review, expansion offer, case study draft."),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--sector", required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# Delivery Plan — {args.account}")
    lines.append("")
    lines.append(f"**Offer:** {args.offer}")
    lines.append(f"**Sector:** {args.sector}")
    lines.append(f"**Generated:** {today}")
    lines.append("")
    for stage, deliverable in STAGES:
        lines.append(f"## {stage}")
        lines.append(f"- {deliverable}")
        lines.append("")
    lines.append("---")
    lines.append("Draft only. Founder sign-off required.")
    out = EXPORT_DIR / f"delivery-plan-{args.account.lower().replace(' ', '-')}-{today}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
