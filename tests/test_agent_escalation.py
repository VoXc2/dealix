"""Agent OS — escalation rules to human supervisor (task 6)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    EscalationTrigger,
    clear_for_test,
    evaluate_escalation,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_high_risk_escalates():
    decision = evaluate_escalation(
        agent_id="a1", risk_level="high", supervisor="founder",
    )
    assert decision.escalate is True
    assert decision.trigger == EscalationTrigger.HIGH_RISK.value


def test_repeated_failure_escalates():
    decision = evaluate_escalation(
        agent_id="a1", failure_count=3, supervisor="founder",
    )
    assert decision.escalate is True
    assert decision.trigger == EscalationTrigger.REPEATED_FAILURE.value


def test_low_confidence_escalates():
    decision = evaluate_escalation(
        agent_id="a1", confidence=0.4, supervisor="founder",
    )
    assert decision.escalate is True
    assert decision.trigger == EscalationTrigger.LOW_CONFIDENCE.value


def test_forbidden_tool_takes_precedence():
    decision = evaluate_escalation(
        agent_id="a1",
        risk_level="high",
        failure_count=9,
        forbidden_tool_attempted=True,
        supervisor="founder",
    )
    assert decision.escalate is True
    assert decision.trigger == EscalationTrigger.FORBIDDEN_TOOL.value


def test_no_escalation_when_healthy():
    decision = evaluate_escalation(agent_id="a1", supervisor="founder")
    assert decision.escalate is False
    assert decision.trigger == EscalationTrigger.NONE.value


def test_missing_supervisor_flagged_in_reason():
    decision = evaluate_escalation(agent_id="a1", risk_level="high", supervisor="")
    assert decision.escalate is True
    assert "no_supervisor_assigned" in decision.reason
