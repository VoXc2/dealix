"""Agent OS — agent-to-agent handoff protocol (task 7)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    accept_handoff,
    clear_for_test,
    new_handoff,
    validate_handoff,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_handoff_requires_evidence_ref():
    with pytest.raises(ValueError):
        new_handoff(
            from_agent="intake",
            to_agent="scoring",
            state="ranked",
            evidence_ref="",
        )


def test_handoff_rejects_same_from_to_agent():
    with pytest.raises(ValueError):
        new_handoff(
            from_agent="intake",
            to_agent="intake",
            state="ranked",
            evidence_ref="proof/P-001",
        )


def test_handoff_requires_state():
    with pytest.raises(ValueError):
        new_handoff(
            from_agent="intake",
            to_agent="scoring",
            state="",
            evidence_ref="proof/P-001",
        )


def test_validate_handoff_flags_pii_in_context():
    env = new_handoff(
        from_agent="intake",
        to_agent="scoring",
        state="ranked",
        evidence_ref="proof/P-001",
        context={"contact_email": "lead@example.com"},
    )
    result = validate_handoff(env)
    assert result.ok is False
    assert any(i.startswith("pii_in_context") for i in result.issues)


def test_accept_handoff_wrong_receiver_rejected():
    env = new_handoff(
        from_agent="intake",
        to_agent="scoring",
        state="ranked",
        evidence_ref="proof/P-001",
    )
    with pytest.raises(ValueError):
        accept_handoff(env, receiving_agent_id="outreach")


def test_new_handoff_roundtrip_to_dict():
    env = new_handoff(
        from_agent="intake",
        to_agent="scoring",
        state="ranked",
        evidence_ref="proof/P-001",
        context={"account_count": 10},
    )
    d = env.to_dict()
    assert d["from_agent"] == "intake"
    assert d["to_agent"] == "scoring"
    assert d["evidence_ref"] == "proof/P-001"
    assert validate_handoff(env).ok is True
    accepted = accept_handoff(env, receiving_agent_id="scoring")
    assert accepted.accepted_by == "scoring"
