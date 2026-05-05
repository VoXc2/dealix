"""Tests for the Approval Command Center (v6 Phase 5).

Covers:
  - Store-level CRUD + state transitions + audit trail
  - Policy: blocked / non-pending requests cannot be approved
  - Renderer: bilingual card with buttons
  - Router: /create + /approve + /history happy path
  - Router: extra='forbid' rejects rogue fields with 422
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    ApprovalStatus,
    ApprovalStore,
    get_default_approval_store,
    render_approval_card,
)


# ─── Fixtures ────────────────────────────────────────────────────


@pytest.fixture()
def store() -> ApprovalStore:
    """Fresh isolated store per test (avoids cross-pollination)."""
    return ApprovalStore()


@pytest.fixture()
def client() -> TestClient:
    # Reset the process-wide default store so router tests start clean.
    get_default_approval_store().clear()
    return TestClient(create_app())


def _sample_payload(**overrides: object) -> dict:
    base = {
        "object_type": "draft_message",
        "object_id": "msg_001",
        "action_type": "send_email",
        "action_mode": "approval_required",
        "channel": "email",
        "summary_ar": "مسودة بريد للعميل",
        "summary_en": "Draft email to customer",
        "risk_level": "low",
        "proof_impact": "Records 1 outreach event in proof ledger",
    }
    base.update(overrides)
    return base


# ─── Store / model tests ─────────────────────────────────────────


def test_create_then_list_pending_returns_it(store: ApprovalStore) -> None:
    req = ApprovalRequest.model_validate(_sample_payload())
    store.create(req)
    pending = store.list_pending()
    assert len(pending) == 1
    assert pending[0].approval_id == req.approval_id
    assert ApprovalStatus(pending[0].status) == ApprovalStatus.PENDING


def test_approve_flips_status(store: ApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_sample_payload()))
    out = store.approve(req.approval_id, who="sami")
    assert ApprovalStatus(out.status) == ApprovalStatus.APPROVED
    assert any(e["action"] == "approve" and e["who"] == "sami" for e in out.edit_history)
    assert store.list_pending() == []


def test_reject_records_reason(store: ApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_sample_payload()))
    out = store.reject(req.approval_id, who="sami", reason="tone is off")
    assert ApprovalStatus(out.status) == ApprovalStatus.REJECTED
    assert out.reject_reason == "tone is off"
    assert out.edit_history[-1]["action"] == "reject"
    assert out.edit_history[-1]["reason"] == "tone is off"


def test_edit_appends_to_history_without_rewriting_prior(
    store: ApprovalStore,
) -> None:
    req = store.create(ApprovalRequest.model_validate(_sample_payload()))
    first = store.edit(req.approval_id, who="sami", patch={"summary_en": "Edit 1"})
    snapshot_first_entry = dict(first.edit_history[0])

    second = store.edit(req.approval_id, who="sami", patch={"summary_en": "Edit 2"})
    assert len(second.edit_history) == 2
    # The earlier entry must remain byte-identical.
    assert second.edit_history[0] == snapshot_first_entry
    assert second.edit_history[1]["patch"] == {"summary_en": "Edit 2"}
    assert second.summary_en == "Edit 2"


def test_approving_blocked_request_raises(store: ApprovalStore) -> None:
    req = store.create(
        ApprovalRequest.model_validate(_sample_payload(action_mode="blocked"))
    )
    assert ApprovalStatus(req.status) == ApprovalStatus.BLOCKED
    with pytest.raises(ValueError, match="blocked"):
        store.approve(req.approval_id, who="sami")


def test_approving_already_approved_raises(store: ApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_sample_payload()))
    store.approve(req.approval_id, who="sami")
    with pytest.raises(ValueError, match="approved"):
        store.approve(req.approval_id, who="sami")


def test_approving_rejected_raises(store: ApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_sample_payload()))
    store.reject(req.approval_id, who="sami", reason="nope")
    with pytest.raises(ValueError, match="rejected"):
        store.approve(req.approval_id, who="sami")


def test_blocked_via_risk_level_also_blocks(store: ApprovalStore) -> None:
    req = store.create(
        ApprovalRequest.model_validate(_sample_payload(risk_level="blocked"))
    )
    assert ApprovalStatus(req.status) == ApprovalStatus.BLOCKED


# ─── Renderer tests ──────────────────────────────────────────────


def test_renderer_returns_bilingual_card_with_buttons() -> None:
    req = ApprovalRequest.model_validate(_sample_payload())
    card = render_approval_card(req)

    # Bilingual fields populated
    for key in (
        "title_ar",
        "title_en",
        "summary_ar",
        "summary_en",
        "risk_badge_ar",
        "risk_badge_en",
        "recommended_action_ar",
        "recommended_action_en",
        "why_now_ar",
        "why_now_en",
    ):
        assert key in card and card[key], f"missing or empty: {key}"

    assert isinstance(card["buttons"], list)
    button_ids = {b["id"] for b in card["buttons"]}
    assert button_ids == {"approve", "reject", "edit"}
    assert all(b["enabled"] for b in card["buttons"])


def test_renderer_disables_buttons_for_blocked() -> None:
    req = ApprovalRequest.model_validate(_sample_payload(action_mode="blocked"))
    # mimic what the store does at create-time
    from auto_client_acquisition.approval_center.approval_policy import evaluate_safety
    evaluate_safety(req)
    card = render_approval_card(req)
    assert card["status"] == "blocked"
    assert all(not b["enabled"] for b in card["buttons"])


# ─── Router tests ────────────────────────────────────────────────


def test_router_create_approve_history_happy_path(client: TestClient) -> None:
    # 1) Create
    resp = client.post("/api/v1/approvals/create", json=_sample_payload())
    assert resp.status_code == 200, resp.text
    body = resp.json()
    approval_id = body["approval"]["approval_id"]
    assert body["approval"]["status"] == "pending"
    assert body["card"]["title_en"].startswith("Approval needed")

    # 2) /pending shows it
    pending = client.get("/api/v1/approvals/pending").json()
    assert pending["count"] == 1
    assert pending["approvals"][0]["approval_id"] == approval_id

    # 3) Approve
    resp = client.post(
        f"/api/v1/approvals/{approval_id}/approve",
        json={"who": "sami"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["approval"]["status"] == "approved"

    # 4) /history shows it as approved
    hist = client.get("/api/v1/approvals/history?limit=10").json()
    assert hist["count"] >= 1
    assert any(
        a["approval_id"] == approval_id and a["status"] == "approved"
        for a in hist["approvals"]
    )

    # 5) Re-approving must 400
    resp = client.post(
        f"/api/v1/approvals/{approval_id}/approve",
        json={"who": "sami"},
    )
    assert resp.status_code == 400


def test_router_create_with_rogue_field_returns_422(client: TestClient) -> None:
    payload = _sample_payload()
    payload["unexpected_evil_field"] = "boom"
    resp = client.post("/api/v1/approvals/create", json=payload)
    assert resp.status_code == 422, resp.text


def test_router_reject_records_reason(client: TestClient) -> None:
    resp = client.post("/api/v1/approvals/create", json=_sample_payload())
    approval_id = resp.json()["approval"]["approval_id"]

    resp = client.post(
        f"/api/v1/approvals/{approval_id}/reject",
        json={"who": "sami", "reason": "wrong tone"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["approval"]["status"] == "rejected"
    assert body["approval"]["reject_reason"] == "wrong tone"


def test_router_blocked_request_cannot_be_approved(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/approvals/create",
        json=_sample_payload(action_mode="blocked"),
    )
    assert resp.status_code == 200
    approval_id = resp.json()["approval"]["approval_id"]
    assert resp.json()["approval"]["status"] == "blocked"

    resp = client.post(
        f"/api/v1/approvals/{approval_id}/approve",
        json={"who": "sami"},
    )
    assert resp.status_code == 400
    assert "blocked" in resp.json()["detail"].lower()


def test_router_status_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/approvals/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "approval_center"
    assert body["guardrails"]["blocked_cannot_be_approved"] is True
