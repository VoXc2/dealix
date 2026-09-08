#!/usr/bin/env python3
"""Compatibility entrypoint for the canonical Dealix Company OS cycle.

This file exists because older VPS orchestration calls this path. It delegates
one-for-one to ``run_self_operating_company_os.py`` and then runs the bounded
Strategy Execution Orchestrator. Neither layer owns a parallel state store,
authority model, target source, scheduler, CRM, approval system, or proof ledger.

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
ORCHESTRATOR = ROOT / "scripts" / "commercial" / "run_strategy_execution_orchestrator_v1.py"
VERIFIER = ROOT / "scripts" / "commercial" / "verify_strategy_execution_orchestrator_v1.py"


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="dealix", help="Compatibility only; canonical Company OS is company-scoped")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    if not CONSTITUTION_VERIFY.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_CONSTITUTION_VERIFIER_MISSING")
        return 2
    constitution_rc = run([sys.executable, str(CONSTITUTION_VERIFY)])
    if constitution_rc != 0:
        print("COMPANY_OS_DAILY=BLOCKED_CONSTITUTION_INVALID")
        return constitution_rc

    if not CANONICAL.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_CANONICAL_RUNNER_MISSING")
        return 2
    if not ORCHESTRATOR.is_file() or not VERIFIER.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_STRATEGY_ORCHESTRATOR_MISSING")
        return 2

    canonical_rc = run([
        sys.executable,
        str(CANONICAL),
        "--mode",
        args.mode,
        "--limit",
        str(args.limit),
    ])
    if canonical_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_CANONICAL_RC_{canonical_rc}")
        return canonical_rc

    verify_rc = run([sys.executable, str(VERIFIER)])
    if verify_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_STRATEGY_VERIFY_RC_{verify_rc}")
        return verify_rc

    orchestrator_rc = run([sys.executable, str(ORCHESTRATOR), "--mode", args.mode])
    if orchestrator_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_STRATEGY_ORCHESTRATOR_RC_{orchestrator_rc}")
        return orchestrator_rc

    print("COMPANY_OS_DAILY=DELEGATED_TO_CANONICAL_COMPANY_OS")
    print("STRATEGY_EXECUTION_ORCHESTRATOR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
