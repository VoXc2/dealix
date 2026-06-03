"""Railway production config-as-code checks."""

from __future__ import annotations

from dealix.commercial_ops.railway_production import (
    analyze_railway_production,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
)


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


def test_analyze_skips_live_when_api_base_false() -> None:
    blob = analyze_railway_production(api_base=False)
    assert blob["live_healthz"].get("probed") is False
