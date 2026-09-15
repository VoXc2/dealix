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

    assert completed.returncode == 0, (
        "SaaS verifier returned NOT_READY; failed checks: "
        + "; ".join(failed_checks)
        + (f"; stderr={completed.stderr}" if completed.stderr else "")
    )
    assert result["foundation_status"] == "READY"
    assert result["production_activation_status"] == "HOLD_PENDING_EXACT_RUNTIME_EVIDENCE"
    assert not failed_checks
    assert [gate["gate"] for gate in result["operator_gates"]] == [
        "release_identity_parity",
        "tenant_database_safety",
        "tenant_isolation_runtime",
        "commercial_activation",
    ]
    assert "production-ready requires" in result["claim_boundary"]
