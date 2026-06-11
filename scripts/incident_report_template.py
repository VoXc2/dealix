"""Generate an incident report template (filled by founder).

Usage:
    python3 scripts/incident_report_template.py --severity P0 --summary "..."
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "reports" / "incidents"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=["P0", "P1", "P2", "P3"], default="P2")
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    body = f"""# Incident Report — {today}

## Summary
{args.summary}

## Severity
{args.severity}

## Timeline
- T0: Incident detected
- T+15m: Investigation started
- T+?: Mitigated
- T+?: Resolved

## Root cause
TBD

## Impact
- Users affected: TBD
- Data loss: TBD
- Revenue impact: TBD

## Action items
- [ ] TBD
- [ ] TBD

## Lessons
TBD
"""
    out = OUT_DIR / f"incident-{today}-{args.severity}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
