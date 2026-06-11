"""Generate a client brief for a given account + signal.

Usage:
    python3 scripts/generate_client_brief.py --account-id demo-acc-001 --sector "Marketing Agency" --signal "No booking flow"
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "delivery" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--signal", required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Client Brief — {args.account}

**Sector:** {args.sector}
**Signal:** {args.signal}
**Generated:** {today}

## 1. What we observed
{args.signal}

## 2. What we propose
Install a Dealix OS that closes this gap with a measurable workflow.

## 3. Day 0 plan
- 60-min intake call
- Stakeholder map
- Single communication channel
- Confidential data scope document

## 4. Day 7 deliverable
Workflow Map (as-is) + 3 first automation candidates.

## 5. Day 14 deliverable
Command Center URL + top 3 automations live + audit log.

## 6. Day 30 deliverable
First monthly proof report + expansion offer if applicable.

---
*Draft only. Founder sign-off required before sending.*
"""
    out = EXPORT_DIR / f"client-brief-{args.account.lower().replace(' ', '-')}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
