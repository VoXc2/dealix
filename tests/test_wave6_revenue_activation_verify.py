"""Wave 6 Phase 10 — revenue activation verifier tests."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

SCRIPT = Path("scripts/wave6_revenue_activation_verify.sh")


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_script_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)


def test_script_runs_pass() -> None:
    """End-to-end: revenue activation verifier must PASS."""
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True, text=True, timeout=600,
    )
    output = result.stdout + result.stderr
    assert "WAVE6_REVENUE_ACTIVATION=PASS" in output, (
        f"Output:\n{output[-3000:]}"
    )
    assert result.returncode == 0


def test_script_chains_wave5_verifier() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "scripts/ultimate_upgrade_verify.sh" in content


def test_script_emits_required_pass_lines() -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True, text=True, timeout=600,
    )
    output = result.stdout
    required = [
        "FIRST_PROSPECT_INTAKE=", "AI_OPS_DIAGNOSTIC=",
        "PILOT_BRIEF=", "PAYMENT_CONFIRMATION=",
        "DELIVERY_KICKOFF=", "PROOF_PACK=",
        "DEMO_OUTCOME_LOGGER=", "DEMO_RUNBOOK=",
        "UPSELL_SCRIPT=", "PAYMENT_CHECKLIST=",
        "INTAKE_TEMPLATE=", "LIVE_DATA_GITIGNORED=",
        "FORBIDDEN_CLAIMS=", "SECRET_SCAN=",
        "NO_LIVE_SEND=", "NO_LIVE_CHARGE=",
        "NO_COLD_WHATSAPP=", "NO_FAKE_PROOF=",
    ]
    for marker in required:
        assert marker in output, f"missing marker: {marker}"


def test_script_emits_final_status_line() -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True, text=True, timeout=600,
    )
    assert "WAVE6_REVENUE_ACTIVATION=" in result.stdout
