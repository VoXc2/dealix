"""Smoke test for founder commercial day shell script (--dry-run)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "run_founder_commercial_day.sh"


def test_founder_commercial_day_dry_run_exits_zero() -> None:
    if not SCRIPT.is_file():
        raise AssertionError(f"missing script: {SCRIPT}")
    if sys.platform == "win32":
        # On Windows CI, bash may be unavailable; skip gracefully.
        import shutil

        if not shutil.which("bash"):
            return
    proc = subprocess.run(
        ["bash", str(SCRIPT), "--dry-run"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "FOUNDER_COMMERCIAL_DAY: OK" in proc.stdout
