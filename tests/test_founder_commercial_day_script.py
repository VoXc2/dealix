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
    protected_paths = (
        REPO_ROOT / "dealix/config/social_content_queue.yaml",
        REPO_ROOT / "docs/commercial/operations/soft_launch_meetings_tracker.yaml",
    )
    before = {path: path.read_bytes() for path in protected_paths}

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
    assert "Production gates" not in proc.stdout
    assert "Expand stack" not in proc.stdout
    assert {path: path.read_bytes() for path in protected_paths} == before


def test_founder_commercial_day_checks_dry_run_before_side_effects() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    guard = 'if [[ "$DRY_RUN" -eq 1 ]]'
    assert content.index(guard) < content.index("Production gates")
    assert content.index(guard) < content.index("Expand stack")
