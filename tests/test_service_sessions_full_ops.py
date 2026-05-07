"""Phase 4 — Service Sessions tests.

Asserts:
- start_session creates draft
- transition_session validates state machine + requires approval_id for active
- attach_deliverable links proof_event_ids
- complete_session reaches terminal state
- HARD_GATES present + approval_required_for_active_state
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.service_sessions import (
    advance_session,
    is_transition_allowed,
)


def test_transition_allowed_truth_table() -> None:
    # Forward path
    assert is_transition_allowed(current="draft", target="waiting_for_approval")
    assert is_transition_allowed(current="waiting_for_approval", target="active")
    assert is_transition_allowed(current="active", target="delivered")
    assert is_transition_allowed(current="delivered", target="proof_pending")
    assert is_transition_allowed(current="proof_pending", target="complete")
    # Cannot go backwards
    assert not is_transition_allowed(current="active", target="draft")
    # Cannot leave terminal
    assert not is_transition_allowed(current="complete", target="active")
    assert not is_transition_allowed(current="blocked", target="active")


def test_advance_to_active_requires_approval() -> None:
    ok, reason = advance_session(
        current="waiting_for_approval", target="active", approval_id=None,
    )
    assert ok is False
    assert "approval_id_required" in reason

    ok, reason = advance_session(
        current="waiting_for_approval", target="active", approval_id="apv_xyz",
    )
    assert ok is True


@pytest.mark.asyncio
async def test_start_session_returns_draft() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "session-test-1",
            "service_type": "diagnostic",
            "inputs": {"sector": "real_estate"},
        })
    assert r.status_code == 200
    body = r.json()
    sess = body["session"]
    assert sess["status"] == "draft"
    assert sess["customer_handle"] == "session-test-1"
    assert sess["service_type"] == "diagnostic"
    assert sess["next_step"]["action"] == "request_approval_to_activate"


@pytest.mark.asyncio
async def test_advance_session_through_lifecycle() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Start
        r = await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "lifecycle-test",
            "service_type": "leadops_sprint",
        })
        sid = r.json()["session"]["session_id"]

        # draft → waiting_for_approval
        r = await c.post(f"/api/v1/service-sessions/{sid}/advance", json={
            "target": "waiting_for_approval",
        })
        assert r.status_code == 200

        # waiting_for_approval → active (requires approval_id)
        r = await c.post(f"/api/v1/service-sessions/{sid}/advance", json={
            "target": "active",
        })
        assert r.status_code == 409  # approval_id required

        r = await c.post(f"/api/v1/service-sessions/{sid}/advance", json={
            "target": "active", "approval_id": "apv_test_1",
        })
        assert r.status_code == 200
        assert r.json()["session"]["status"] == "active"
        assert "apv_test_1" in r.json()["session"]["approval_ids"]

        # active → delivered
        r = await c.post(f"/api/v1/service-sessions/{sid}/advance", json={
            "target": "delivered",
        })
        assert r.status_code == 200

        # Attach a deliverable
        r = await c.post(f"/api/v1/service-sessions/{sid}/attach-deliverable", json={
            "deliverable": {
                "type": "diagnostic_report",
                "proof_event_id": "pe_test_1",
            },
        })
        assert r.status_code == 200
        assert "pe_test_1" in r.json()["session"]["proof_event_ids"]

        # delivered → proof_pending → complete
        r = await c.post(f"/api/v1/service-sessions/{sid}/advance", json={
            "target": "proof_pending",
        })
        assert r.status_code == 200

        r = await c.post(f"/api/v1/service-sessions/{sid}/complete")
        assert r.status_code == 200
        assert r.json()["session"]["status"] == "complete"
        assert r.json()["session"]["completed_at"] is not None


@pytest.mark.asyncio
async def test_invalid_transition_rejected() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "invalid-test",
            "service_type": "diagnostic",
        })
        sid = r.json()["session"]["session_id"]
        # Try draft → complete (skip many steps)
        r = await c.post(f"/api/v1/service-sessions/{sid}/advance", json={
            "target": "complete",
        })
    assert r.status_code == 409
    assert "transition_not_allowed" in r.json()["detail"]


@pytest.mark.asyncio
async def test_unknown_session_404() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/service-sessions/sess_doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_invalid_service_type_422() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "x",
            "service_type": "made_up_type",
        })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_hard_gates_present() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "gates-test",
            "service_type": "proof_pack",
        })
    gates = r.json()["hard_gates"]
    assert gates["no_live_send"] is True
    assert gates["no_live_charge"] is True
    assert gates["approval_required_for_active_state"] is True
