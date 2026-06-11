"""Generate a weekly command report (scaffold).

Usage:
    python3 scripts/generate_weekly_command_report.py
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "delivery" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
    body = f"""# Weekly Command Report — week of {today}

## This week
- 5 metrics snapshot: [TBD]
- 3 biggest risks: [TBD]
- 3 next moves: [TBD]

## Last week outcome
- What shipped: [TBD]
- What slipped: [TBD]
- Why: [TBD]

## Owner map
- [Owner] → [deliverable] → [status]

## Decision log
- [Date] — [Decision] — [Owner] — [Outcome]

---
*Draft only. Founder sign-off required before sending to client.*
"""
    out = EXPORT_DIR / f"weekly-command-report-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
