"""Generate a prospect pack for the founder.

Usage:
    python3 scripts/generate_prospect_pack.py
"""
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCORED_PATH = REPO_ROOT / "business" / "_data" / "scored_leads.json"
EXPORT_DIR = REPO_ROOT / "business" / "crm" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    if not SCORED_PATH.exists():
        print(f"missing: {SCORED_PATH} (run scripts/score_leads.py first)")
        return 1
    data = json.loads(SCORED_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])

    lines: list[str] = []
    lines.append("# Dealix Daily Prospect Pack")
    lines.append("")
    lines.append("## Top 10 by score")
    for a in accounts[:10]:
        lines.append(f"- **{a['score']}** · {a['name']} · {a.get('segment', '')} · signal: {a.get('visibleSignal', '')}")

    lines.append("")
    lines.append("## Pipeline value (top 10)")
    total = 0
    for a in accounts[:10]:
        v = (a.get("setupValue") or 0) + (a.get("monthlyValue") or 0) * 3
        total += v
        lines.append(f"- {a['name']} · SAR {v:,}")
    lines.append("")
    lines.append(f"**Total pipeline value (top 10): SAR {total:,}**")
    lines.append("")
    lines.append("---")
    lines.append("Draft only. Founder must approve each outreach draft before any send.")

    out = EXPORT_DIR / "dealix-daily-prospect-pack.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
