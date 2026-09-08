#!/usr/bin/env python3
"""Compatibility entrypoint for the canonical Dealix Company OS cycle.

This file exists because older VPS orchestration calls this path. It delegates
one-for-one to ``run_self_operating_company_os.py`` and owns no parallel state,
authority model, target source, scheduler, or commercial logic.

Before delegation, it verifies the permanent Dealix operating constitution.
That makes company-law drift fail closed without creating a second Company OS.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "scripts" / "commercial" / "run_self_operating_company_os.py"
CONSTITUTION_VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_operating_constitution.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="dealix", help="Compatibility only; canonical Company OS is company-scoped")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    if not CONSTITUTION_VERIFY.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_CONSTITUTION_VERIFIER_MISSING")
        return 2
    constitution = subprocess.run(
        [sys.executable, str(CONSTITUTION_VERIFY)],
        cwd=ROOT,
        check=False,
    )
    if constitution.returncode != 0:
        print("COMPANY_OS_DAILY=BLOCKED_CONSTITUTION_INVALID")
        return constitution.returncode

    if not CANONICAL.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_CANONICAL_RUNNER_MISSING")
        return 2
    result = subprocess.run(
        [sys.executable, str(CANONICAL), "--mode", args.mode, "--limit", str(args.limit)],
        cwd=ROOT,
        check=False,
    )
    print("COMPANY_OS_DAILY=DELEGATED_TO_CANONICAL_COMPANY_OS")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
