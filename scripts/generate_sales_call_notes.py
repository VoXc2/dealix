"""Generate a sales call notes template.

Usage:
    python3 scripts/generate_sales_call_notes.py --account-id demo-acc-001
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "conversion" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Sales Call Notes — {args.account_id} ({today})

## Attendees
- Founder:
- Client:

## Context
- How did they hear about us:
- What triggered this call:

## Pain (in their words)
- Pain 1:
- Pain 2:
- Pain 3:

## Visible signals confirmed
- Signal 1:
- Signal 2:

## Offer fit
- Recommended: TBD
- Reasoning: TBD

## Decision criteria
- Who decides:
- Timeline:
- Budget range:

## Risks / non-fit
- Risk 1:
- Risk 2:

## Next step
- [ ] Send proposal
- [ ] Book follow-up
- [ ] Disqualify (with reason)

---
*Draft only. Founder sign-off required.*
"""
    out = EXPORT_DIR / f"sales-call-notes-{args.account_id}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
