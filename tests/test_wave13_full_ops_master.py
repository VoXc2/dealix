"""Wave 13 Phase 13 — Master verifier wrapper test.

Asserts:
  - The master verifier script exists and is executable
  - It exits 0 (i.e. all checks PASS) when run on this branch
  - Output contains the expected verdict line

Sandbox-safe: invokes the bash verifier as a subprocess.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VERIFIER = _REPO_ROOT / "scripts" / "dealix_full_ops_productization_verify.sh"


# ── Test 1 ────────────────────────────────────────────────────────────
def test_verifier_script_exists_and_executable():
    assert _VERIFIER.is_file(), f"missing verifier: {_VERIFIER}"
    assert os.access(_VERIFIER, os.X_OK), f"not executable: {_VERIFIER}"


# ── Test 2 ────────────────────────────────────────────────────────────
def test_verifier_exits_zero_on_clean_branch():
    """Run verifier; expect exit 0 (all PASS).

    Sandbox-safe: bash + python3 are available; the verifier itself
    invokes pytest (which works in sandbox).
    """
    if shutil.which("bash") is None:
        pytest.skip("bash not available in this environment")
    result = subprocess.run(
        ["bash", str(_VERIFIER)],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"verifier failed (exit={result.returncode})\n"
        f"--- stdout (tail) ---\n{result.stdout[-2000:]}\n"
        f"--- stderr (tail) ---\n{result.stderr[-2000:]}"
    )


# ── Test 3 ────────────────────────────────────────────────────────────
def test_verifier_output_contains_verdict_line():
    if shutil.which("bash") is None:
        pytest.skip("bash not available in this environment")
    result = subprocess.run(
        ["bash", str(_VERIFIER)],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = result.stdout
    assert "DEALIX_WAVE13_FULL_OPS_PRODUCTIZATION_VERDICT=PASS" in out, (
        f"missing PASS verdict line in output:\n{out[-2000:]}"
    )
    # Expected PASS lines from each phase
    expected = [
        "SERVICE_CATALOG=PASS",
        "SERVICE_SESSION_RUNTIME=PASS",
        "DELIVERABLES=PASS",
        "WEEKLY_EXECUTIVE_PACK=PASS",
        "CUSTOMER_PORTAL_FULL_OPS=PASS",
        "WHATSAPP_DECISION_FULL_OPS=PASS",
        "CUSTOMER_SUCCESS_SCORES=PASS",
        "BOTTLENECK_RADAR=PASS",
        "INTEGRATION_CAPABILITY_REGISTRY=PASS",
        "BUSINESS_METRICS_BOARD=PASS",
    ]
    for line in expected:
        assert line in out, f"missing '{line}' in verifier output"
