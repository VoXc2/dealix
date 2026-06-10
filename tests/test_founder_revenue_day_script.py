"""Smoke tests for founder revenue day runner."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_founder_revenue_day_dry_run():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/founder_revenue_day_runner.py"), "--dry-run"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout + proc.stderr
    assert "War Room" in out or "war room" in out.lower()
    assert "evidence" in out.lower()
    assert "FOUNDER_REVENUE_DAY_VERDICT=READY" in out


def test_aeo_week_parser():
    import importlib.util

    mod_path = REPO_ROOT / "scripts" / "founder_revenue_day_runner.py"
    spec = importlib.util.spec_from_file_location("founder_revenue_day_runner", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    row = mod.parse_aeo_row(1)
    if row:
        assert "post-lead" in row.get("slug", "").lower() or row.get("title_ar")
