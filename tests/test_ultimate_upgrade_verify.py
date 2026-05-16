"""Phase 14 — ultimate_upgrade_verify.sh script tests."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path("scripts/ultimate_upgrade_verify.sh")


def _system_python_has_pytest() -> bool:
    """The verifier shells out to ``python3 -m pytest``; the sandbox system
    ``python3`` is separate from the project venv and may lack pytest."""
    try:
        return subprocess.run(
            ["python3", "-c", "import pytest"], capture_output=True, timeout=30
        ).returncode == 0
    except Exception:
        return False


_PYTEST_ON_SYSTEM_PYTHON = _system_python_has_pytest()


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_script_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)


def test_script_chains_wave3_and_wave4_verifiers() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "scripts/full_ops_10_layer_verify.sh" in content
    assert "scripts/integration_upgrade_verify.sh" in content
    assert "scripts/customer_experience_final_audit.sh" in content


@pytest.mark.skipif(
    not _PYTEST_ON_SYSTEM_PYTHON,
    reason="verifier shells out to `python3 -m pytest`; system python3 lacks pytest in this sandbox",
)
def test_script_runs_pass() -> None:
    """End-to-end: ultimate verifier must PASS."""
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True, text=True, timeout=600,
    )
    output = result.stdout + result.stderr
    assert "ULTIMATE_UPGRADE=PASS" in output, (
        f"Output:\n{output[-3000:]}"
    )
    assert result.returncode == 0


def test_script_emits_required_pass_lines() -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True, text=True, timeout=600,
    )
    output = result.stdout
    required = [
        "PRODUCT_SIMPLIFICATION=", "EXECUTIVE_COMMAND_CENTER_FINAL=",
        "CUSTOMER_PORTAL_FINAL=", "LEADOPS_RELIABILITY=",
        "FULL_OPS_SCORE_FINAL=", "WEAKNESS_RADAR_FINAL=",
        "REVENUE_PROFITABILITY=", "SUPPORT_JOURNEY=",
        "TOOL_GUARDRAILS=", "AGENT_OBSERVABILITY_FINAL=",
        "FRONTEND_POLISH=", "BACKEND_RELIABILITY=",
        "CUSTOMER_EXPERIENCE_FINAL=",
        "WAVE4_INTEGRATION=", "WAVE3_FULL_OPS_10_LAYER=",
        "CURRENT_CONTRACTS=", "FORBIDDEN_CLAIMS=",
        "NO_LIVE_CHARGE=", "SECRET_SCAN=",
        "NO_INTERNAL_TERMS_PUBLIC=",
        "NO_LIVE_SEND=", "NO_FAKE_PROOF=",
        "NO_BREAKING_CHANGES=",
    ]
    for marker in required:
        assert marker in output, f"missing marker: {marker}"
