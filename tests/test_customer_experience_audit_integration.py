"""Phase 12 — Customer Experience Audit script tests."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

SCRIPT = Path("scripts/customer_experience_audit.sh")


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_script_executable() -> None:
    assert os.access(SCRIPT, os.X_OK), "script should be chmod +x"


def test_script_runs_and_passes() -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = result.stdout + result.stderr
    assert "CUSTOMER_EXPERIENCE_AUDIT=PASS" in output
    assert result.returncode == 0


def test_script_checks_required_pages() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "customer-portal.html" in content
    assert "executive-command-center.html" in content
    assert "customer-dashboard.js" in content
    assert "executive-command-center.js" in content


def test_script_checks_internal_terms() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "v11" in content
    assert "v12" in content
    assert "growth_beast" in content
    assert "stacktrace" in content


def test_script_checks_forbidden_claims() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "guaranteed" in content.lower() or "guaranteed" in content
    assert "blast" in content
    assert "scraping" in content
    assert "نضمن" in content
    assert "cold" in content.lower()
