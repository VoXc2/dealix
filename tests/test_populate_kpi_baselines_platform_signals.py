"""Platform KPI baseline updater must fail closed without explicit evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "populate_kpi_baselines_platform_signals.py"


def _minimal_baselines() -> str:
    return '''version: 1
program: global_ai_transformation
updated_period_iso: "2026-08-31"
snapshots:
  reliability_posture_score:
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
  gross_margin_by_offer:
    value_numeric: null
    source_ref: ""
'''


def _repo(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "repo"
    base = root / "dealix/transformation/kpi_baselines.yaml"
    base.parent.mkdir(parents=True)
    base.write_text(_minimal_baselines(), encoding="utf-8")
    return root, base


def _run(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), *extra],
        check=False, capture_output=True, text=True,
    )


def _receipt(tmp_path: Path, signals: dict) -> Path:
    path = tmp_path / "signals.json"
    path.write_text(json.dumps({"schema": "dealix.kpi_platform_signals.v1", "signals": signals}), encoding="utf-8")
    return path


def test_default_without_verified_input_is_noop(tmp_path: Path) -> None:
    root, base = _repo(tmp_path)
    before = base.read_text(encoding="utf-8")
    result = _run(root)
    assert result.returncode == 0
    assert "PLATFORM_SIGNALS=NO_VERIFIED_INPUT" in result.stdout
    assert base.read_text(encoding="utf-8") == before


def test_verified_platform_signal_updates_key_but_not_global_freshness(tmp_path: Path) -> None:
    root, base = _repo(tmp_path)
    receipt = _receipt(tmp_path, {"reliability_posture_score": {"value_numeric": 87, "source_ref": "platform:runtime-audit:2026-09-15:receipt-abc"}})
    result = _run(root, "--verified-signals-json", str(receipt))
    assert result.returncode == 0, result.stdout + result.stderr
    text = base.read_text(encoding="utf-8")
    assert "value_numeric: 87.0" in text
    assert "platform:runtime-audit:2026-09-15:receipt-abc" in text
    assert 'updated_period_iso: "2026-08-31"' in text
    assert "GLOBAL_UPDATED_PERIOD=UNCHANGED" in result.stdout


def test_unverified_source_is_rejected(tmp_path: Path) -> None:
    root, base = _repo(tmp_path)
    before = base.read_text(encoding="utf-8")
    receipt = _receipt(tmp_path, {"unauthorized_external_action_count": {"value_numeric": 0, "source_ref": "platform:guardrail:PASS_required"}})
    result = _run(root, "--verified-signals-json", str(receipt))
    assert result.returncode == 2
    assert "REJECTED" in result.stdout
    assert base.read_text(encoding="utf-8") == before


def test_finance_metric_cannot_enter_through_platform_updater(tmp_path: Path) -> None:
    root, base = _repo(tmp_path)
    before = base.read_text(encoding="utf-8")
    receipt = _receipt(tmp_path, {"gross_margin_by_offer": {"value_numeric": 43.33, "source_ref": "finance:ledger:2026-09-15"}})
    result = _run(root, "--verified-signals-json", str(receipt))
    assert result.returncode == 2
    assert "not platform-owned" in result.stdout
    assert base.read_text(encoding="utf-8") == before
