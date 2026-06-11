"""Generate a quote (price + scope + status) for an account.

Usage:
    python3 scripts/generate_quote.py --account-id demo-001 --offer "Revenue OS" --setup-price 18000 --monthly-price 5000
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "closing" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--setup-price", type=int, required=True)
    parser.add_argument("--monthly-price", type=int, required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Quote — {args.offer} for {args.account_id}

- Setup: SAR {args.setup_price:,}
- Monthly: SAR {args.monthly_price:,}
- Generated: {today}
- Status: draft
- Review: required (founder)

Includes:
- Workflow map
- Command center setup
- Top 3 automations
- Weekly proof report
- Quarterly review

Excludes:
- Financial/legal decision automation
- Private data scraping

Next step: 60-min Day 0 — Intake call.

---
*Draft only.*
"""
    out = EXPORT_DIR / f"quote-{args.account_id}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
