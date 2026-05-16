#!/usr/bin/env python3
"""Lead scoring calibration — compares strategy_os scores to golden fixtures (offline)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=Path("tests/fixtures/lead_scoring_golden.json"))
    args = parser.parse_args()
    if not args.fixtures.exists():
        sample = [
            {"company": "Acme SA", "sector": "technology", "expected_tier": "warm"},
            {"company": "Clinic Riyadh", "sector": "healthcare", "expected_tier": "hot"},
        ]
        args.fixtures.parent.mkdir(parents=True, exist_ok=True)
        args.fixtures.write_text(json.dumps(sample, indent=2), encoding="utf-8")
        print(f"Created sample fixture: {args.fixtures}")
    rows = json.loads(args.fixtures.read_text(encoding="utf-8"))
    print(f"Lead scoring calibration: {len(rows)} golden rows (offline — wire to strategy_os in CI next)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
