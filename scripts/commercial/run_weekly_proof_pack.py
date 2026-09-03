#!/usr/bin/env python3
"""Compatibility adapter to the canonical Weekly Operating Proof Pack generator."""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts" / "generate_weekly_operating_proof_pack.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="dealix", help="Compatibility only")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    if not GENERATOR.is_file():
        print("WEEKLY_PROOF=BLOCKED_CANONICAL_GENERATOR_MISSING")
        return 2
    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    out = ROOT / "reports" / "company_os" / "weekly" / f"OPERATING_PROOF_{stamp}.md"
    command = [sys.executable, str(GENERATOR), "--repo-root", str(ROOT), "--out", str(out)]
    if args.strict:
        command.append("--strict")
    result = subprocess.run(command, cwd=ROOT, check=False)
    print(f"WEEKLY_PROOF_REPORT={out.relative_to(ROOT)}")
    print("WEEKLY_PROOF=DELEGATED_TO_CANONICAL_OPERATING_PROOF_GENERATOR")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
