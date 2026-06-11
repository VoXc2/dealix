"""Generate the ultimate Dealix sales OS pack (Markdown + JSON).

Usage:
    python3 scripts/generate_ultimate_sales_os_pack.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "sales-machine" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


OFFERS = [
    ("Diagnostic Sprint", "Free", "20-min workflow review"),
    ("Revenue OS", "SAR 18,000 setup + 5,000/mo", "Lead flow + outreach drafts + proof"),
    ("Command Center OS", "SAR 35,000 setup + 9,000/mo", "One-page decision view"),
    ("Delivery OS", "SAR 25,000 setup + 6,000/mo", "Workflow map + automation build"),
    ("Review & Reputation", "SAR 12,000 setup + 3,500/mo", "Review monitoring + replies"),
    ("Custom Enterprise", "SAR 80,000+", "Architecture + custom modules"),
    ("Managed Retainer", "SAR 4,000–12,000/mo", "Ongoing ops + reviews"),
]

INDUSTRIES = [
    ("Marketing Agency", "Revenue OS", "Slow response window + multiple campaigns live"),
    ("Training / Consulting", "Delivery OS", "Cohort follow-up + renewal cycle"),
    ("Clinic / Local Service", "Review & Reputation OS", "Google reviews + reply cadence"),
    ("Real Estate", "Revenue OS + Command Center", "Listing rotation + agent consistency"),
    ("Logistics / B2B", "Command Center OS", "Manual dispatch + SLA reporting"),
    ("Consulting Firm", "Command Center OS", "Pipeline velocity + senior utilization"),
]


def main() -> int:
    today = dt.date.today()
    md = EXPORT_DIR / f"dealix-ultimate-sales-os-pack-{today.isoformat()}.md"
    js = EXPORT_DIR / f"dealix-ultimate-sales-os-pack-{today.isoformat()}.json"

    lines: list[str] = []
    lines.append(f"# Dealix Ultimate Sales OS Pack — {today.isoformat()}")
    lines.append("")
    lines.append("## Offers")
    for o, p, s in OFFERS:
        lines.append(f"- **{o}** — {p} — {s}")
    lines.append("")
    lines.append("## Industry plays")
    for i, o, s in INDUSTRIES:
        lines.append(f"- **{i}** → {o} — signal: {s}")
    lines.append("")
    lines.append("## Safety")
    lines.append("- No auto-send. Drafts only. Human review required.")
    lines.append("- No scraping. No spam. No fake ROI.")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    js.write_text(
        json.dumps(
            {
                "date": today.isoformat(),
                "offers": [{"name": o, "price": p, "scope": s} for o, p, s in OFFERS],
                "industries": [{"industry": i, "offer": o, "signal": s} for i, o, s in INDUSTRIES],
                "safety": {"auto_send": False, "human_review": True, "no_scraping": True},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"wrote {md}")
    print(f"wrote {js}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
