"""Smoke tests for founder closure env merge (no secrets required)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/apply_founder_closure_env.py"


def test_apply_founder_closure_env_dry_run() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode in (0, 1)
    # Script prints either the merge header or a SKIP/INCOMPLETE status line
    assert "apply_founder_closure_env" in proc.stdout or "FOUNDER_CLOSURE_ENV=" in proc.stdout
