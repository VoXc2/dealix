"""Smoke for verify_full_autonomous_ops_stack.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_verify_full_autonomous_ops_stack_skip_api() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify_full_autonomous_ops_stack.py"), "--skip-api"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "DEALIX_FULL_AUTONOMOUS_OPS_STACK=PASS" in proc.stdout
