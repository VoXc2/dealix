"""Smoke tests for commercial expansion orchestrator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_expand_agency_wave2_reaches_120():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/expand_agency_targets_seed.py"), "--wave2"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    from dealix.commercial_ops.targeting_csv import load_targets

    assert len(load_targets()) >= 120


def test_run_commercial_expansion_skip_gates():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/run_commercial_expansion.py"),
            "--wave4",
            "--skip-gates",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        env={**__import__("os").environ, "APP_ENV": "test", "PYTHONIOENCODING": "utf-8"},
    )
    out = proc.stdout or ""
    assert proc.returncode == 0, (proc.stderr or out)[-3000:]
    assert "COMMERCIAL_EXPANSION_VERDICT=PASS" in out
