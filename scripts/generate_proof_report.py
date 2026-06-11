"""Generate the proof report (scaffold).

Usage:
    python3 scripts/generate_proof_report.py --account-id demo-001 --lang both
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "proof" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Proof Report — {args.account_id} ({today})

## Outcomes (5 metrics, owner per metric)
- [Metric 1] target / current / trend — TBD
- [Metric 2] — TBD
- [Metric 3] — TBD
- [Metric 4] — TBD
- [Metric 5] — TBD

## Workflow health
- Automations running: TBD
- Automations in fallback: TBD
- Audit log entries: TBD

## Risks raised this period
- TBD

## Decisions made
- TBD

## Next 30 days
- TBD

## Client sign-off
- [ ] Approved as delivered
- [ ] Comments attached

---
*Draft only. Founder + client sign-off required.*
"""
    out = EXPORT_DIR / f"proof-report-{args.account_id}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
