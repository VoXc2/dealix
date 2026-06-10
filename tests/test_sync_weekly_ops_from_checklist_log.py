"""Tests for scripts/sync_weekly_ops_from_checklist_log.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _minimal_baselines() -> str:
    return """version: 1
program: global_ai_transformation
notes_ar: >-
  x
updated_period_iso: ""

weekly_ops:
  last_checklist_run_iso: ""
  checklist_script: scripts/run_executive_weekly_checklist.sh

snapshots:
  measured_customer_value_sar:
    value_numeric: null
    source_ref: ""
"""


def test_sync_script_updates_last_checklist_date(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    ev = root / "docs/transformation/evidence"
    ev.mkdir(parents=True)
    (ev / "weekly_ops_checklist.log").write_text(
        "2026-05-20T10:00:00Z verify_global_ai_transformation=PASS\n", encoding="utf-8"
    )
    kb = root / "dealix/transformation"
    kb.mkdir(parents=True)
    base = kb / "kpi_baselines.yaml"
    base.write_text(_minimal_baselines(), encoding="utf-8")

    script = Path(__file__).resolve().parents[1] / "scripts" / "sync_weekly_ops_from_checklist_log.py"
    r = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    text = base.read_text(encoding="utf-8")
    assert 'last_checklist_run_iso: "2026-05-20"' in text
