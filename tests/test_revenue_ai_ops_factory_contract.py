"""Revenue + AI Ops Factory contract integrity tests."""

from __future__ import annotations

from pathlib import Path

import yaml


def _load_contract() -> dict:
    root = Path(__file__).resolve().parents[1]
    path = root / "dealix/transformation/revenue_ai_ops_factory.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_contract_enforces_non_autonomous_external_send() -> None:
    data = _load_contract()
    policies = data.get("policies") or {}
    assert policies.get("no_autonomous_external_send") is True
    assert policies.get("external_send_requires_human_approval") is True


def test_contract_has_required_approval_and_evidence_minimums() -> None:
    data = _load_contract()
    approval_center = data.get("approval_center") or {}
    approval_types = set(approval_center.get("approval_types") or [])
    assert {"external_message", "scope_send", "invoice_send", "security_claim"} <= approval_types

    ledger = data.get("evidence_ledger") or {}
    required_fields = set(ledger.get("required_fields") or [])
    assert {"event_type", "source", "approval_required", "created_by"} <= required_fields


def test_agent_contracts_define_forbidden_actions() -> None:
    data = _load_contract()
    agents = data.get("agents") or []
    assert len(agents) >= 10
    for row in agents:
        assert row.get("id")
        assert row.get("mission")
        forbidden_actions = row.get("forbidden_actions") or []
        assert isinstance(forbidden_actions, list)
        assert forbidden_actions
