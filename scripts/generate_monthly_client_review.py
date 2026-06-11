"""Generate a monthly client review (scaffold).

Usage:
    python3 scripts/generate_monthly_client_review.py --account-id demo-001 --lang both
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "retention" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Monthly Client Review — {args.account_id} ({today})

## What shipped
- TBD

## Outcomes
- Metric 1: TBD
- Metric 2: TBD
- Metric 3: TBD
- Metric 4: TBD
- Metric 5: TBD

## What slipped
- TBD

## Decisions
- TBD

## Next 30 days
- TBD

## Expansion offer (if applicable)
- TBD

## Client sign-off
- [ ] Approved
- [ ] Comments

---
*Draft only. Founder + client sign-off required.*
"""
    out = EXPORT_DIR / f"monthly-review-{args.account_id}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
