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


def test_script_checks_current_public_surface_contracts() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "DEALIX_RETIRED_PUBLIC_SURFACE" in content
    assert "index.html" in content
    assert "diagnostic.html" in content
    assert "pricing.html" in content
    assert "proof.html" in content


def test_script_checks_revenue_playbook() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "DEALIX_REVENUE_PLAYBOOK_FINAL.md" in content


def test_revenue_playbook_doc_exists() -> None:
    assert Path("docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md").exists()
