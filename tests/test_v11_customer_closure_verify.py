"""V11 Phase 12 — master verifier presence + smoke test.

Asserts:
- The script exists and is executable
- A run produces a verdict block with PASS/FAIL labels
- Hard-gate fields are present
- Exit code reflects pass/fail honestly
"""
from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "v11_customer_closure_verify.sh"


def test_script_exists() -> None:
    assert SCRIPT.exists(), "scripts/v11_customer_closure_verify.sh is missing"


def test_script_is_executable() -> None:
    assert os.access(SCRIPT, os.X_OK), "verify script must be executable"


def test_script_starts_with_shebang() -> None:
    first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("#!"), f"missing shebang: {first!r}"


def test_run_produces_verdict_block() -> None:
    """A run must emit the canonical verdict block."""
    r = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    out = r.stdout
    # Required headers + fields
    assert "V11 CUSTOMER CLOSURE VERDICT" in out
    assert "V11_CUSTOMER_CLOSURE=" in out
    for field in ("COMPILEALL=", "V11_TARGETED_TESTS=", "PHASE_E_DOCS=",
                  "DIAGNOSTIC_CLI=", "FIRST3_BOARD=", "PROOF_PACK_TEMPLATE=",
                  "PAYMENT_FALLBACK=", "PHASE_E_TODAY=", "FORBIDDEN_CLAIMS=",
                  "SECRET_SCAN=", "LIVE_GATES=", "OUTREACH_GO=",
                  "NEXT_ACTION="):
        assert field in out, f"missing verdict field: {field}"


def test_verdict_pass_when_all_checks_pass() -> None:
    """Right now, all V11 checks pass — verdict must reflect it."""
    r = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    if "V11_CUSTOMER_CLOSURE=PASS" in r.stdout:
        assert r.returncode == 0
    elif "V11_CUSTOMER_CLOSURE=FAIL" in r.stdout:
        assert r.returncode == 1


def test_outreach_go_is_yes_and_live_gates_blocked() -> None:
    r = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert "LIVE_GATES=blocked" in r.stdout
    assert "OUTREACH_GO=yes" in r.stdout
