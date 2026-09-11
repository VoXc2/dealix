"""Wave 13 Phase 13 — Master verifier wrapper test.

Asserts:
  - The master verifier script exists and is executable
  - It exits 0 (i.e. all technical checks PASS) when run on this branch
  - Output preserves the boundary between technical contract PASS and
    unproven customer/commercial readiness

Sandbox-safe: invokes the bash verifier as a subprocess.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VERIFIER = _REPO_ROOT / "scripts" / "dealix_full_ops_productization_verify.sh"


def _verifier_env() -> dict[str, str]:
    """Keep nested verifier pytest calls on the same accepted interpreter."""
    env = os.environ.copy()
    env["DEALIX_PYTHON_BIN"] = sys.executable
    return env


def test_verifier_script_exists_and_executable():
    assert _VERIFIER.is_file(), f"missing verifier: {_VERIFIER}"
    assert os.access(_VERIFIER, os.X_OK), f"not executable: {_VERIFIER}"


def test_verifier_exits_zero_on_clean_branch():
    """Technical verification may pass without claiming customer readiness."""
    if shutil.which("bash") is None:
        pytest.skip("bash not available in this environment")
    result = subprocess.run(
        ["bash", str(_VERIFIER)],
        cwd=str(_REPO_ROOT),
        env=_verifier_env(),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"verifier failed (exit={result.returncode})\n"
        f"--- stdout (tail) ---\n{result.stdout[-2000:]}\n"
        f"--- stderr (tail) ---\n{result.stderr[-2000:]}"
    )


def test_verifier_output_contains_verdict_line():
    if shutil.which("bash") is None:
        pytest.skip("bash not available in this environment")
    result = subprocess.run(
        ["bash", str(_VERIFIER)],
        cwd=str(_REPO_ROOT),
        env=_verifier_env(),
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = result.stdout
    assert "DEALIX_WAVE13_FULL_OPS_PRODUCTIZATION_VERDICT=PASS" in out, (
        f"missing PASS verdict line in output:\n{out[-2000:]}"
    )
    # Historical Wave13 technical contract can pass while current launch,
    # customer, revenue, and sellability authority remain explicitly unproven.
    expected = [
        "NO_LIVE_SEND_IN_WAVE13=PASS",
        "NO_LIVE_CHARGE_IN_WAVE13=PASS",
        "NO_FAKE_REVENUE=PASS",
        "PORTAL_RETIREMENT_INVARIANT=PASS",
        "TECHNICAL_WAVE13_CONTRACT=PASS",
        "CUSTOMER_READY=NOT_PROVEN_BY_THIS_VERIFIER",
        "FIRST_3_PAID_PILOTS_READY=NOT_PROVEN_BY_THIS_VERIFIER",
        "SELLABLE_NOW=NOT_PROVEN_BY_THIS_VERIFIER",
    ]
    for line in expected:
        assert line in out, f"missing '{line}' in verifier output"
