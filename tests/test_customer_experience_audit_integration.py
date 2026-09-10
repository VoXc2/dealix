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


def test_script_checks_current_launch_surfaces() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "customer-portal.html" in content
    assert "executive-command-center.html" in content
    assert "DEALIX_RETIRED_PUBLIC_SURFACE" in content
    assert "url=/proof.html" in content
    assert "enriched_view" in content
