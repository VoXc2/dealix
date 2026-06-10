"""Client workspace MVP: GET /api/v1/customer-portal/{handle}/workspace.

Returns a bundle of ~10 panels driven by value_os, friction_log, etc.
Must be null-safe for empty customers and prioritize governance blocks
in the 'next_action' panel.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.friction_log.schemas import FrictionKind, FrictionSeverity
from auto_client_acquisition.friction_log.store import (
    clear_for_test as clear_friction,
)
from auto_client_acquisition.friction_log.store import emit as emit_friction
from auto_client_acquisition.value_os.value_ledger import (
    add_event as add_value_event,
)
from auto_client_acquisition.value_os.value_ledger import (
    clear_for_test as clear_value_for_test,
)

EXPECTED_PANEL_KEYS = {
    "capability_score",
    "data_readiness",
    "governance_status",
    "ranked_opportunities",
    "draft_packs_pending_approval",
    "proof_timeline",
    "adoption_score",
    "friction_summary",
    "latest_monthly_value_report",
    "next_action",
}


@pytest.fixture(autouse=True)
def isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    for cid in ("populated", "empty_handle", "gov_block_cust", "missing_passport_cust"):
        try:
            clear_friction()
        except Exception:
            pass
        try:
            clear_value_for_test(cid)
        except Exception:
            pass
    yield


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_workspace_returns_10_panels_for_populated_customer(client: TestClient) -> None:
    add_value_event(
        customer_id="populated",
        kind="revenue_uplift",
        amount=500.0,
        tier="estimated",
    )
    emit_friction(
        customer_id="populated",
        kind=FrictionKind.APPROVAL_DELAY,
        severity=FrictionSeverity.LOW,
    )

    resp = client.get("/api/v1/customer-portal/populated/workspace")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    missing = EXPECTED_PANEL_KEYS - set(body.keys())
    assert not missing, f"workspace missing panels: {missing}"


def test_workspace_null_safe_for_empty_customer(client: TestClient) -> None:
    resp = client.get("/api/v1/customer-portal/empty_handle/workspace")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    # Panels exist; nullable values are fine.
    for key in EXPECTED_PANEL_KEYS:
        assert key in body, f"missing panel key {key}"


def test_workspace_next_action_priority_governance_block_first(
    client: TestClient,
) -> None:
    emit_friction(
        customer_id="gov_block_cust",
        kind=FrictionKind.GOVERNANCE_BLOCK,
        severity=FrictionSeverity.HIGH,
    )
    resp = client.get(
        "/api/v1/customer-portal/gov_block_cust/workspace"
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    next_action = body.get("next_action") or {}
    assert isinstance(next_action, dict)
    assert next_action.get("kind") == "resolve_governance_block"


def test_workspace_emits_friction_for_missing_panel(client: TestClient) -> None:
    # Brand-new customer with no source_passport — the workspace itself should
    # log a missing_source_passport friction event and surface it in the panel.
    resp = client.get(
        "/api/v1/customer-portal/missing_passport_cust/workspace"
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    friction_summary = body.get("friction_summary") or {}

    # Either the aggregator surface or the by_kind dict should mention the
    # missing_source_passport friction kind.
    serialized = repr(friction_summary).lower()
    assert "missing_source_passport" in serialized
