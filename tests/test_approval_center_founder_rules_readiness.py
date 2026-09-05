from __future__ import annotations

import json

import pytest

import scripts.verify_approval_center_backend as verifier


class _FakeRuleEngine:
    configured = []
    active = []

    def list_rules(self):
        return list(self.configured)

    def list_active_rules(self):
        return list(self.active)


def _postgres_ready():
    return {
        "verdict": "PASS",
        "backend": "postgres",
        "process_scoped": False,
        "database_url_configured": True,
        "schema_ready": True,
        "reason": "approval_center_postgres_ready",
    }


@pytest.fixture(autouse=True)
def _patch_backend(monkeypatch):
    monkeypatch.setattr(verifier, "FounderRuleEngine", _FakeRuleEngine)
    monkeypatch.setattr(verifier, "approval_store_backend_status", _postgres_ready)
    _FakeRuleEngine.configured = []
    _FakeRuleEngine.active = []


def test_readiness_passes_with_postgres_and_no_active_founder_rules(
    monkeypatch,
    capsys,
) -> None:
    _FakeRuleEngine.configured = [object()]
    _FakeRuleEngine.active = []
    monkeypatch.setattr("sys.argv", ["verify_approval_center_backend.py", "--json"])

    assert verifier.main() == 0
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["verdict"] == "PASS"
    assert receipt["founder_rules_storage"] == "local_jsonl"
    assert receipt["founder_rules_configured_count"] == 1
    assert receipt["founder_rules_active_count"] == 0
    assert receipt["founder_rules_auto_approval_ready"] is False
    assert receipt["founder_rules_reason"] == "no_active_founder_rules_manual_approval_only"


def test_readiness_holds_when_any_active_founder_rule_is_local_only(
    monkeypatch,
    capsys,
) -> None:
    _FakeRuleEngine.configured = [object()]
    _FakeRuleEngine.active = [object()]
    monkeypatch.setattr("sys.argv", ["verify_approval_center_backend.py", "--json"])

    assert verifier.main() == 1
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["verdict"] == "HOLD"
    assert receipt["reason"] == "active_founder_rules_not_shared_durable"
    assert receipt["founder_rules_active_count"] == 1
    assert receipt["founder_rules_auto_approval_ready"] is False
