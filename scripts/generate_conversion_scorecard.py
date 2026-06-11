"""Generate the conversion scorecard.

Usage:
    python3 scripts/generate_conversion_scorecard.py
"""
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
EXPORT_DIR = REPO_ROOT / "business" / "conversion" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    accounts: list[dict] = []
    if LEADS_PATH.exists():
        try:
            accounts = json.loads(LEADS_PATH.read_text(encoding="utf-8")).get("accounts", [])
        except json.JSONDecodeError:
            pass
    if not accounts:
        seed = REPO_ROOT / "business" / "crm" / "prospects.seed.json"
        if seed.exists():
            accounts = json.loads(seed.read_text(encoding="utf-8")).get("accounts", [])

    total = len(accounts)
    by_stage: dict[str, int] = {}
    for a in accounts:
        s = a.get("stage", "unknown")
        by_stage[s] = by_stage.get(s, 0) + 1

    proposals = by_stage.get("proposal", 0) + by_stage.get("won", 0)
    won = by_stage.get("won", 0)
    conversion = 0 if proposals == 0 else round(won / proposals * 100, 1)
    status = "off_track" if conversion < 20 else ("watch" if conversion < 35 else "on_track")

    body = f"""# Dealix Conversion Scorecard

## Pipeline
- Total accounts: {total}
- New: {by_stage.get('new', 0)}
- Qualified: {by_stage.get('qualified', 0)}
- Drafted: {by_stage.get('drafted', 0)}
- In review: {by_stage.get('review', 0)}
- Meeting: {by_stage.get('meeting', 0)}
- Proposal: {by_stage.get('proposal', 0)}
- Won: {by_stage.get('won', 0)}
- Lost: {by_stage.get('lost', 0)}
- Retainer: {by_stage.get('retainer', 0)}

## Conversion
- Proposal → Close: {conversion}% ({status})

## Action
"""
    if status == "off_track":
        body += "- Tighten close criteria + revisit offer matching"
    elif status == "watch":
        body += "- Focus on top 3 accounts + tighten proposal quality"
    else:
        body += "- Expand to next segment"
    body += "\n\n---\n*Draft only.*\n"

    out = EXPORT_DIR / "dealix-conversion-scorecard.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out} (status: {status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
