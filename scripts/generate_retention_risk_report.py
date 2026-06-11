"""Generate a retention risk report.

Usage:
    python3 scripts/generate_retention_risk_report.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
EXPORT_DIR = REPO_ROOT / "business" / "retention" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
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

    body = f"""# Retention Risk Report — {today}

## Active clients: TBD (use real data)
## Risk distribution: TBD
"""
    body += "\n## Accounts in deliverable stages\n"
    for a in accounts:
        if a.get("stage") in ("won", "retainer"):
            body += f"- {a['name']} — stage: {a['stage']}\n"
    body += "\n---\n*Draft only.*\n"

    out = EXPORT_DIR / f"retention-risk-report-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
