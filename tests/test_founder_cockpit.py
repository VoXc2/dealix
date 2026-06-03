"""Founder unified cockpit — autonomous ops aggregation."""

from __future__ import annotations

from dealix.commercial_ops.founder_cockpit import build_founder_cockpit, run_cockpit_morning


def test_build_founder_cockpit_shape() -> None:
    snap = build_founder_cockpit(top_n=5, strongest_ops_mode="morning")
    assert snap.get("cockpit_verdict")
    assert snap.get("strongest_ops", {}).get("tasks_today_count", 0) >= 0
    assert snap.get("max_ops_backlog", {}).get("total", 0) >= 0
    assert snap.get("benchmark_rows")
    assert snap.get("automation_readiness", {}).get("verdict")
    assert snap.get("full_autonomous_ops", {}).get("schema_version")
    assert "GET /api/v1/ops-autopilot/founder/cockpit" in (
        snap.get("commands", {}).get("cockpit_api") or ""
    )


def test_run_cockpit_evening_shape(monkeypatch) -> None:
    monkeypatch.setattr(
        "dealix.commercial_ops.founder_strongest_ops.write_strongest_ops_brief",
        lambda **_: {"markdown": "x.md", "json": "x.json"},
    )
    monkeypatch.setattr(
        "dealix.commercial_ops.founder_strongest_ops.build_strongest_ops_snapshot",
        lambda **_: {"verdict": "OK", "cadence": {"evidence_logged_today": False}},
    )
    snap = __import__(
        "dealix.commercial_ops.founder_cockpit", fromlist=["run_cockpit_evening"]
    ).run_cockpit_evening(top_n=3)
    assert snap.get("evening_run")


def test_run_cockpit_morning_returns_morning_run(monkeypatch) -> None:
    monkeypatch.setattr(
        "dealix.commercial_ops.founder_cockpit.run_morning_core",
        lambda **_: {"verdict": "PASS", "steps": []},
    )
    snap = run_cockpit_morning(top_n=5, run_optional_scripts=False)
    assert snap["morning_run"]["verdict"] == "PASS"
    assert snap.get("cockpit_verdict") == "AUTONOMOUS_READY"
