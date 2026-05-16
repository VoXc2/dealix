"""Tests for populate_kpi_baselines_platform_signals.py."""

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
  reliability_posture_score:
    value_numeric: null
    source_ref: ""
  gross_margin_by_offer:
    value_numeric: null
    source_ref: ""
  unauthorized_external_action_count:
    value_numeric: null
    source_ref: ""
  measured_metric_without_source_ref_count:
    value_numeric: null
    source_ref: ""
  tenant_isolation_violation_count:
    value_numeric: null
    source_ref: ""
  measured_customer_value_sar:
    value_numeric: null
    source_ref: ""
"""


def test_populate_sets_platform_keys(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    kb = root / "dealix/transformation"
    kb.mkdir(parents=True)
    base = kb / "kpi_baselines.yaml"
    base.write_text(_minimal_baselines(), encoding="utf-8")

    script = Path(__file__).resolve().parents[1] / "scripts" / "populate_kpi_baselines_platform_signals.py"
    r = subprocess.run(
        [sys.executable, str(script), "--repo-root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    text = base.read_text(encoding="utf-8")
    assert "reliability_posture_score:" in text
    assert "value_numeric: 100.0" in text or "value_numeric: 100" in text
    assert "computed:weekly_cross_os_snapshot" in text
    assert 'updated_period_iso: "' in text
