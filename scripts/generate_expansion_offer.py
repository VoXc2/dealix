"""Generate an expansion offer.

Usage:
    python3 scripts/generate_expansion_offer.py --account-id demo-001 --offer "Command Center"
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
    parser.add_argument("--offer", required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Expansion Offer — {args.offer} for {args.account_id}

**Generated:** {today}

## Why now
- Based on the proof report from the last 60 days
- Tied to a measurable workflow gap

## What's included
- Migration to {args.offer}
- New automations (top 3)
- New weekly proof metrics
- No re-onboarding fee

## Pricing
- Migration fee: SAR 0 (waived for existing clients)
- New monthly: SAR +3,000–5,000

## Timeline
- 14 days from approval

## Next step
- 20-min call to confirm
- No obligation

---
*Draft only. Founder sign-off required.*
"""
    out = EXPORT_DIR / f"expansion-offer-{args.account_id}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
