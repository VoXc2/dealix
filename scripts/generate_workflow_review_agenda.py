"""Generate a workflow review agenda (20-min diagnostic).

Usage:
    python3 scripts/generate_workflow_review_agenda.py --account "Demo Company"
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
    parser.add_argument("--account", required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Workflow Review Agenda — {args.account}

**Date:** {today}
**Duration:** 20 minutes
**Facilitator:** Founder

## 1. Context (3 min)
- What does {args.account} ship today?
- Where is the founder the bottleneck?

## 2. Visible signals (5 min)
- Inbound response window
- Reputation / review response
- Reporting cadence

## 3. Offer fit (7 min)
- Which Dealix OS matches?
- Setup + monthly range
- 14-day onboarding scope

## 4. Risks & non-fit (3 min)
- Things Dealix does NOT do
- Things we always say no to

## 5. Next step (2 min)
- Sign or pass
- Diagnostic next steps if interested
- Never pressure

---
*Draft only. Founder-led call.*
"""
    out = EXPORT_DIR / f"workflow-review-agenda-{args.account.lower().replace(' ', '-')}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
