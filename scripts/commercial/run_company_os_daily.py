#!/usr/bin/env python3
"""Compatibility entrypoint for the canonical Dealix Company OS cycle.

This file exists because older VPS orchestration calls this path. It verifies
company law and the company-wide Arm/Portfolio contracts, materializes the real
website-diagnostic intake bridge from the existing Revenue Ops store, delegates
one-for-one to ``run_self_operating_company_os.py``, then runs the bounded
Strategy Execution Orchestrator and President Portfolio Command. No layer owns
a parallel state store, authority model, target source, scheduler, CRM, approval
system, proof ledger, model router, or permanent agent fleet.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "scripts" / "commercial" / "run_self_operating_company_os.py"
CONSTITUTION_VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_operating_constitution.py"
ARM_REGISTRY_VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_arm_registry.py"
INBOUND_DIAGNOSTIC_BRIDGE = ROOT / "scripts" / "commercial" / "run_inbound_execution_diagnostic_bridge_v1.py"
ORCHESTRATOR = ROOT / "scripts" / "commercial" / "run_strategy_execution_orchestrator_v1.py"
VERIFIER = ROOT / "scripts" / "commercial" / "verify_strategy_execution_orchestrator_v1.py"
PRESIDENT_PORTFOLIO_COMMAND = ROOT / "scripts" / "commercial" / "run_president_portfolio_command_v1.py"
PRESIDENT_PORTFOLIO_VERIFY = ROOT / "scripts" / "commercial" / "verify_president_portfolio_command_v1.py"


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

    if not ARM_REGISTRY_VERIFY.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_ARM_REGISTRY_VERIFIER_MISSING")
        return 2
    arm_registry_rc = run([sys.executable, str(ARM_REGISTRY_VERIFY)])
    if arm_registry_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_ARM_REGISTRY_RC_{arm_registry_rc}")
        return arm_registry_rc

    if not PRESIDENT_PORTFOLIO_COMMAND.is_file() or not PRESIDENT_PORTFOLIO_VERIFY.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_PRESIDENT_PORTFOLIO_COMMAND_MISSING")
        return 2
    president_verify_rc = run([sys.executable, str(PRESIDENT_PORTFOLIO_VERIFY)])
    if president_verify_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_PRESIDENT_PORTFOLIO_VERIFY_RC_{president_verify_rc}")
        return president_verify_rc

    if not INBOUND_DIAGNOSTIC_BRIDGE.is_file():
        print("COMPANY_OS_DAILY=BLOCKED_INBOUND_DIAGNOSTIC_BRIDGE_MISSING")
        return 2
    inbound_rc = run([sys.executable, str(INBOUND_DIAGNOSTIC_BRIDGE)])
    if inbound_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_INBOUND_DIAGNOSTIC_BRIDGE_RC_{inbound_rc}")
        return inbound_rc

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

    president_rc = run([sys.executable, str(PRESIDENT_PORTFOLIO_COMMAND)])
    if president_rc != 0:
        print(f"COMPANY_OS_DAILY=BLOCKED_PRESIDENT_PORTFOLIO_RC_{president_rc}")
        return president_rc

    print("INBOUND_EXECUTION_DIAGNOSTIC_BRIDGE=PASS")
    print("COMPANY_OS_DAILY=DELEGATED_TO_CANONICAL_COMPANY_OS")
    print("STRATEGY_EXECUTION_ORCHESTRATOR=PASS")
    print("COMPANY_ARM_PORTFOLIO_REGISTRY=PASS")
    print("PRESIDENT_PORTFOLIO_COMMAND=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
