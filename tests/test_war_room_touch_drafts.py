"""Smoke tests for governed War Room touch draft batch script."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generate_war_room_touch_drafts_dry_run() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/generate_war_room_touch_drafts.py"), "--dry-run"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert r.returncode == 0, r.stderr or r.stdout
    assert "WAR_ROOM_TOUCH_DRAFTS" in r.stdout
