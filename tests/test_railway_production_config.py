"""Railway production config-as-code checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from dealix.commercial_ops.railway_production import (
    analyze_railway_production,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
    parse_railway_ui_restart_retries_drift,
)

ROOT = Path(__file__).resolve().parents[1]


def test_repo_railway_config_ok() -> None:
    blob = analyze_railway_production(api_base=False)
    assert blob["repo"]["ok"], blob["repo"]["issues"]
    assert blob["verdict"] == "PASS"


def test_ui_start_command_drift_hint() -> None:
    hint = parse_railway_ui_drift_hint("./start.sh")
    assert hint is not None
    assert "/app/start.sh" in hint


def test_ui_predeploy_drift_no_migration_stub() -> None:
    hint = parse_railway_ui_predeploy_drift('echo "no migration needed"')
    assert hint is not None
    assert "railway_predeploy" in hint


def test_ui_restart_retries_drift_from_uploaded_snapshot() -> None:
    hint = parse_railway_ui_restart_retries_drift("10")
    assert hint is not None
    assert "10" in hint
    assert "3" in hint


def test_ui_restart_retries_canonical_value_has_no_drift() -> None:
    assert parse_railway_ui_restart_retries_drift("3") is None


def test_analyze_skips_live_when_api_base_false() -> None:
    blob = analyze_railway_production(api_base=False)
    assert blob["live_healthz"].get("probed") is False


def _run_verify_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "verify_railway_production_config.py"),
            *args,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_verify_cli_skip_live_does_not_probe_production() -> None:
    proc = _run_verify_cli("--skip-live")
    assert proc.returncode == 0, proc.stderr
    assert "live /healthz: skipped" in proc.stdout
    assert "RAILWAY_PRODUCTION_CONFIG_VERDICT=PASS" in proc.stdout


def test_verify_cli_ui_drift_cannot_report_false_pass() -> None:
    proc = _run_verify_cli(
        "--skip-live",
        "--ui-restart-max-retries",
        "10",
    )
    assert proc.returncode == 0, proc.stderr
    assert "FOUNDER_ACTION (restart)" in proc.stdout
    assert "RAILWAY_PRODUCTION_CONFIG_VERDICT=WARN" in proc.stdout
