"""Generate a weekly operating review (scaffold).

Usage:
    python3 scripts/generate_weekly_operating_review.py
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "reports" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
    body = f"""# Weekly Operating Review — {today}

## 1. Pipeline health
- Total accounts: TBD
- New this week: TBD
- Moved forward: TBD
- Stuck > 14 days: TBD

## 2. Sales
- Drafts generated: TBD
- Approved: TBD
- Rejected: TBD
- Average time in review: TBD

## 3. Delivery
- Active clients: TBD
- Proof items logged: TBD
- Open risks: TBD

## 4. Money
- New MRR added: TBD
- Setup invoiced: TBD
- Outstanding: TBD

## 5. Decisions
- TBD

## 6. Next week
- TBD

---
*Draft only. Founder sign-off required.*
"""
    out = EXPORT_DIR / f"weekly-operating-review-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
