"""Regression coverage for the repository-level SaaS verifier."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_saas_foundation.py"


def test_saas_foundation_verifier_reports_ready_with_operator_gates() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    failed_checks = [
        f"{check['name']}: {check['evidence']}"
        for check in result["checks"]
        if not check["passed"]
    ]

    assert completed.returncode == 1, (
        "SaaS verifier returned NOT_READY; failed checks: "
        + "; ".join(failed_checks)
        + (f"; stderr={completed.stderr}" if completed.stderr else "")
    )
    assert result["foundation_status"] == "NOT_READY"
    assert result["production_activation_status"] == "OPERATOR_GATES_REQUIRED"
    assert {check["name"] for check in result["checks"] if not check["passed"]} == {"frontend_api_boundary"}
    assert [gate["issue"] for gate in result["operator_gates"]] == [898, 884, 894]
    assert "production-ready requires" in result["claim_boundary"]
