"""Contracts for the Dealix Go Resource Broker (deterministic, paid-firewalled)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


broker = _load("go_resource_broker")


def test_route_order_starts_with_no_model_and_ends_with_paid_exception() -> None:
    assert broker.ROUTE_ORDER[0] == "R0_NO_MODEL"
    assert broker.ROUTE_ORDER[-1] == "R6_PAID_EXCEPTION"


def test_deterministic_and_health_tasks_never_reach_models() -> None:
    assert broker.plan_route("HEALTH_CHECK")["route"] == "R0_NO_MODEL"
    assert broker.plan_route("SCHEDULER_AUDIT")["route"] == "R1_DETERMINISTIC"
    assert broker.plan_route("FINGERPRINT")["route"] == "R1_DETERMINISTIC"


def test_complexity_escalates_but_non_architecture_caps_at_included_high() -> None:
    assert broker.plan_route("CODE_ENGINEERING", complexity="low")["route"] == "R4_INCLUDED_HIGH"
    assert broker.plan_route("CODE_ENGINEERING", complexity="critical")["route"] == "R4_INCLUDED_HIGH"
    assert broker.plan_route("ARCHITECTURE", complexity="high")["route"] == "R5_STRONG_REASONING"
    assert broker.plan_route("SECURITY_REVIEW", complexity="high")["route"] == "R5_STRONG_REASONING"


def test_paid_spill_requires_explicit_approval_and_critical_emergency() -> None:
    denied = broker.plan_route(
        "CODE_ENGINEERING", complexity="critical", value="critical", urgency="production_incident"
    )
    assert denied["route"] == "R5_STRONG_REASONING"
    assert denied["paid_spill"] is False
    assert "declined" in denied["reason"]

    approved = broker.plan_route(
        "CODE_ENGINEERING",
        complexity="critical",
        value="critical",
        urgency="production_incident",
        paid_approved=True,
    )
    assert approved["route"] == "R6_PAID_EXCEPTION"
    assert approved["paid_spill"] is True


def test_off_peak_only_for_batchable_non_urgent() -> None:
    batchable = broker.plan_route("CONTENT_DRAFT", value="medium")
    assert batchable["off_peak_preferred"] is True
    urgent = broker.plan_route("CONTENT_DRAFT", value="medium", urgency="customer_obligation")
    assert urgent["off_peak_preferred"] is False
    assert urgent["off_peak_basis"].startswith("UNKNOWN")


def test_headroom_is_unknown_not_fake() -> None:
    plan = broker.plan_route("DIAGNOSTIC_REASONING")
    assert plan["headroom"] == "UNKNOWN"


def test_pick_model_prefers_free_then_included_then_strong() -> None:
    catalog = ["opencode/paid-a", "opencode/some-free", "opencode/deepseek-v4-flash", "opencode/deepseek-v4-pro"]
    assert broker.pick_model("R3_INCLUDED_LIGHT", catalog, [], []) == "opencode/some-free"
    assert broker.pick_model("R4_INCLUDED_HIGH", catalog, [], []) == "opencode/deepseek-v4-flash"
    assert broker.pick_model("R5_STRONG_REASONING", catalog, [], []) == "opencode/deepseek-v4-pro"
    assert broker.pick_model("R2_LOCAL_OLLAMA", catalog, ["qwen3:4b"], []) == "qwen3:4b"
    assert broker.pick_model("R0_NO_MODEL", catalog, [], []) == "none"


def test_daily_envelope_counts_and_reserves() -> None:
    state = {
        "jobs": [
            {"recorded_at": "2026-09-11T08:00:00+00:00", "route": "R4_INCLUDED_HIGH"},
            {"recorded_at": "2026-09-11T09:00:00+00:00", "route": "R5_STRONG_REASONING"},
            {"recorded_at": "2026-09-10T09:00:00+00:00", "route": "R4_INCLUDED_HIGH"},
        ]
    }
    from datetime import UTC, datetime

    envelope = broker.daily_envelope(state, datetime(2026, 9, 11, 12, 0, tzinfo=UTC))
    assert envelope["included_jobs_today"] == 1
    assert envelope["strong_jobs_today"] == 1
    assert envelope["reserved_for_emergency"] >= 1
    assert envelope["headroom_source"].startswith("conservative")


def test_record_job_is_bounded_and_observability_honest(tmp_path: Path) -> None:
    state = {"jobs": []}
    for index in range(2):
        broker.record_job(state, "CODE_ENGINEERING", "R4_INCLUDED_HIGH", "opencode/deepseek-v4-flash")
    assert len(state["jobs"]) == 2
    assert state["jobs"][0]["cost_observable"] is False
    assert state["jobs"][0]["tokens_observable"] is False
    path = tmp_path / "state.json"
    broker.save_state(state, path)
    loaded = broker.load_state(path)
    assert loaded["jobs"]
    assert "updated_at" in loaded
