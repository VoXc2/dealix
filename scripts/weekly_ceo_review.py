#!/usr/bin/env python3
"""Weekly CEO Review generator — Dealix Execution Assurance System.

Reads the machine registry and prints the founder's Weekly CEO Review as
markdown: the 12 standing questions (with what the system can already
answer pre-filled), the flagged machines below their acceptance gate, and
the standing weekly decision checklist.

Usage:
  python scripts/weekly_ceo_review.py            # print markdown
  python scripts/weekly_ceo_review.py --json     # print raw JSON

No file writes, no external sends. Read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_client_acquisition.execution_assurance_os import (
    generate_weekly_ceo_review,
    load_machine_registry,
    render_ceo_review_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Weekly CEO Review")
    parser.add_argument("--json", action="store_true", help="emit raw JSON")
    args = parser.parse_args()

    report = generate_weekly_ceo_review(load_machine_registry())
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_ceo_review_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
