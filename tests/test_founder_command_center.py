"""Founder Command Center endpoint — shape, governance, no-build warning.

The command center aggregates real durable state only. With an empty lead
inbox every count must be a real zero — never a fabricated number.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture(autouse=True)
def _isolated_lead_inbox(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "leads.jsonl"))


def _client() -> TestClient:
    return TestClient(app)


def test_command_center_route_resolves() -> None:
    """Must not be swallowed by /founder-summary/{engagement_id}."""
    r = _client().get("/api/v1/founder-summary/command-center")
    assert r.status_code == 200


def test_command_center_shape() -> None:
    body = _client().get("/api/v1/founder-summary/command-center").json()
    cc = body["command_center"]
    for key in (
        "top_actions",
        "new_qualified_leads",
        "new_leads_count",
        "pending_approvals",
        "payments_pending",
        "proof_packs_in_progress",
        "blocked_actions",
        "no_build_warning",
    ):
        assert key in cc
    assert 1 <= len(cc["top_actions"]) <= 3


def test_command_center_carries_governance_status() -> None:
    body = _client().get("/api/v1/founder-summary/command-center").json()
    assert body["governance_decision"] == "ALLOW"


def test_command_center_empty_inbox_no_fabrication() -> None:
    """No leads → all counts are real zeros."""
    cc = _client().get("/api/v1/founder-summary/command-center").json()["command_center"]
    assert cc["new_qualified_leads"]["count"] == 0
    assert cc["new_leads_count"] == 0
    assert cc["blocked_actions"]["count"] == 0


def test_no_build_warning_active_without_paid_proof() -> None:
    """Doctrine L6/L7 — no converted lead means the no-build warning is on."""
    cc = _client().get("/api/v1/founder-summary/command-center").json()["command_center"]
    assert cc["no_build_warning"]["active"] is True
    assert "L6/L7" in cc["no_build_warning"]["reason_en"]


def test_command_center_reflects_captured_lead() -> None:
    """A risk-score submission should surface in the command center."""
    client = _client()
    client.post(
        "/api/v1/public/risk-score",
        json={
            "name": "Sami",
            "company": "Acme Co",
            "email": "sami@acme.com",
            "role": "founder",
            "crm": "yes",
            "biggest_pain": "pipeline",
            "consent_before_external_action": "yes",
            "can_link_workflow_to_value": "yes",
            "budget_range": "5000_25000",
            "urgency": "high",
            "consent": True,
        },
    )
    cc = client.get("/api/v1/founder-summary/command-center").json()["command_center"]
    assert cc["new_qualified_leads"]["count"] >= 1
    assert cc["new_leads_count"] >= 1
