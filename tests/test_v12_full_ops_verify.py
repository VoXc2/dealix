"""V12 Phase 10 — V12 master verifier presence + smoke."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "v12_full_ops_verify.sh"


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_script_is_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)


def test_script_starts_with_shebang() -> None:
    first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("#!")


def test_run_emits_verdict_block() -> None:
    r = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=600,
    )
    out = r.stdout
    assert "V12 FULL-OPS VERDICT" in out
    assert "V12_FULL_OPS=" in out
    for field in ("GROWTH_OS=", "SALES_OS=", "SUPPORT_OS=",
                  "CUSTOMER_SUCCESS_OS=", "DELIVERY_OS=",
                  "PARTNERSHIP_OS=", "COMPLIANCE_OS=", "EXECUTIVE_OS=",
                  "SELF_IMPROVEMENT_OS=", "WORKITEM_LAYER=",
                  "DAILY_COMMAND_CENTER=", "NO_LIVE_SEND=",
                  "NO_LIVE_CHARGE=", "NO_COLD_WHATSAPP=",
                  "NO_SCRAPING=", "NO_FAKE_PROOF=", "NEXT_ACTION="):
        assert field in out, f"missing verdict field: {field}"


def test_verdict_pass_when_all_checks_pass() -> None:
    r = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=600,
    )
    if "V12_FULL_OPS=PASS" in r.stdout:
        assert r.returncode == 0
    elif "V12_FULL_OPS=FAIL" in r.stdout:
        assert r.returncode == 1


def test_lists_all_9_oses_in_output() -> None:
    r = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=600,
    )
    for os_name in (
        "GROWTH_OS", "SALES_OS", "SUPPORT_OS", "CUSTOMER_SUCCESS_OS",
        "DELIVERY_OS", "PARTNERSHIP_OS", "COMPLIANCE_OS", "EXECUTIVE_OS",
        "SELF_IMPROVEMENT_OS",
    ):
        assert os_name in r.stdout
