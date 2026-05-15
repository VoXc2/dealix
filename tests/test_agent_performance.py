"""Agent OS — performance dashboard data layer (task 8)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    clear_for_test,
    kill_agent,
    new_card,
    register_agent,
    summarize_agent,
    summarize_all,
)
from auto_client_acquisition.friction_log import emit


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def _register(agent_id: str = "agt-perf"):
    return register_agent(
        new_card(
            agent_id=agent_id,
            name="Perf Agent",
            owner="founder",
            purpose="rank accounts",
        ),
    )


def test_summarize_unknown_agent_returns_none():
    assert summarize_agent("does-not-exist") is None


def test_summarize_agent_basic_fields():
    _register()
    summary = summarize_agent("agt-perf")
    assert summary is not None
    assert summary.agent_id == "agt-perf"
    assert summary.quality_score == 1.0
    assert summary.compliance_ok is True


def test_friction_events_lower_quality_score():
    _register()
    emit(customer_id="dealix_internal", kind="manual_override", workflow_id="agt-perf")
    summary = summarize_agent("agt-perf")
    assert summary is not None
    assert summary.friction_count == 1
    assert summary.quality_score < 1.0


def test_killed_agent_compliance_not_ok():
    _register()
    kill_agent("agt-perf", reason="manual override")
    summary = summarize_agent("agt-perf")
    assert summary is not None
    assert summary.compliance_ok is False


def test_summarize_all_covers_registered_agents():
    _register("agt-1")
    _register("agt-2")
    summaries = summarize_all()
    assert {s.agent_id for s in summaries} == {"agt-1", "agt-2"}


def test_no_observability_data_yields_zero_cost_latency():
    _register()
    summary = summarize_agent("agt-perf")
    assert summary is not None
    assert summary.cost_estimate_total == 0.0
    assert summary.latency_ms_avg == 0.0
    assert summary.trace_count == 0
