"""Phase 15 — integration_upgrade_verify.sh script tests."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

SCRIPT = Path("scripts/integration_upgrade_verify.sh")


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_script_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)


def test_script_runs_pass() -> None:
    """End-to-end run must pass after Wave 4 build."""
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = result.stdout + result.stderr
    assert "INTEGRATION_UPGRADE=PASS" in output
    assert result.returncode == 0


def test_script_emits_required_pass_lines() -> None:
    """The output table must include all required check names."""
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = result.stdout
    required = [
        "ADAPTERS=", "UNIFIED_OPERATING_GRAPH=",
        "FULL_OPS_SCORE=", "WEAKNESS_RADAR=",
        "EXECUTIVE_COMMAND_CENTER=", "EXECUTIVE_DASHBOARD_FRONTEND=",
        "WHATSAPP_DECISION=", "CHANNEL_POLICY=",
        "RADAR_EVENTS=", "CUSTOMER_PORTAL_COMPAT=",
        "AGENT_OBSERVABILITY=", "CUSTOMER_EXPERIENCE=",
        "CURRENT_CONTRACTS=", "FORBIDDEN_CLAIMS=",
        "NO_LIVE_CHARGE=", "PROOF_REDACTS_ON_EXPORT=",
        "NO_INTERNAL_TERMS_PUBLIC=", "SECRET_SCAN=",
        "NO_LIVE_SEND=", "NO_COLD_WHATSAPP=",
        "NO_FAKE_PROOF=", "NO_BREAKING_CHANGES=",
    ]
    for marker in required:
        assert marker in output, f"missing check marker: {marker}"


def test_script_checks_compile() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "compileall" in content


def test_script_calls_full_ops_10_layer_verify() -> None:
    """Wave 4 verifier must call into Wave 3 verifier (no duplication)."""
    content = SCRIPT.read_text(encoding="utf-8")
    assert "scripts/full_ops_10_layer_verify.sh" in content


def test_script_calls_customer_experience_audit() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "scripts/customer_experience_audit.sh" in content
