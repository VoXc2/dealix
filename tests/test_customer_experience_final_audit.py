"""Phase 12 — Customer Experience Final Audit script tests."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

SCRIPT = Path("scripts/customer_experience_final_audit.sh")


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_script_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)


def test_script_runs_pass() -> None:
    """End-to-end: script must PASS after Wave 5 build."""
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True, text=True, timeout=60,
    )
    output = result.stdout + result.stderr
    assert "CUSTOMER_EXPERIENCE_FINAL=PASS" in output
    assert result.returncode == 0


def test_script_calls_wave4_sub_audit() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "scripts/customer_experience_audit.sh" in content


def test_script_checks_8_wave5_items() -> None:
    """The script must perform at least 8 distinct Wave 5 checks."""
    content = SCRIPT.read_text(encoding="utf-8")
    # Heuristic: count `ok_msg` calls in the Wave 5 section
    wave5_section = content.split("Wave 5 Final CX Audit")[-1]
    pass_count = wave5_section.count("ok_msg")
    assert pass_count >= 8


def test_script_checks_revenue_playbook() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "DEALIX_REVENUE_PLAYBOOK_FINAL.md" in content


def test_revenue_playbook_doc_exists() -> None:
    assert Path("docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md").exists()
