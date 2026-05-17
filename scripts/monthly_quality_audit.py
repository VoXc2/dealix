#!/usr/bin/env python3
"""Monthly Quality Audit generator — Dealix Execution Assurance System.

Reconciles the machine registry's declared Definition-of-Done claims
against what the Evidence Ledger actually contains. A machine claiming
Automated maturity while its expected evidence is entirely absent is
flagged as a contradiction — the registry claim is not backed by proof.

Usage:
  python scripts/monthly_quality_audit.py                  # print markdown
  python scripts/monthly_quality_audit.py --json           # print raw JSON
  python scripts/monthly_quality_audit.py --evidence PATH  # custom ledger

No file writes, no external sends. Read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_client_acquisition.execution_assurance_os import (
    generate_monthly_quality_audit,
    load_machine_registry,
    render_audit_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Monthly Quality Audit")
    parser.add_argument("--json", action="store_true", help="emit raw JSON")
    parser.add_argument(
        "--evidence",
        default=None,
        help="path to the Evidence Ledger JSONL (defaults to the live ledger)",
    )
    args = parser.parse_args()

    report = generate_monthly_quality_audit(
        load_machine_registry(), evidence_path=args.evidence
    )
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_audit_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
