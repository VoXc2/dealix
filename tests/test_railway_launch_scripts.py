"""Smoke tests for Railway launch orchestration scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_railway_launch_env_check_runs():
    env = {**dict(__import__("os").environ), "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "railway_launch_env_check.py")],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=env,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert proc.returncode in (0, 1)
    assert "RAILWAY_ENV_CHECK" in combined or "Railway API" in combined


def test_validate_warm_csv_allow_replace():
    env = {**dict(__import__("os").environ), "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "validate_warm_targeting_csv.py"),
            "--max-replace-top",
            "99",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=env,
    )
    assert proc.returncode == 0
    assert "WARM_CSV_VALIDATION=PASS" in proc.stdout


def test_railway_launch_module_import():
    from dealix.commercial_ops.railway_launch import check_railway_api_env

    out = check_railway_api_env()
    assert "ready_for_api_deploy" in out
