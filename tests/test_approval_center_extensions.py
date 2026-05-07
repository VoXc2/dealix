"""Phase 5 — Approval Center extensions (per-channel policy + expiry + bulk).

Existing tests in tests/test_approval_center.py still pass; this file
adds coverage for the new features.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.approval_center.approval_policy import (
    CHANNEL_POLICY,
    can_auto_approve,
)
from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


def _make(approval_id: str, **kw) -> ApprovalRequest:
    defaults: dict = {
        "approval_id": approval_id,
        "object_type": "outreach_draft",
        "object_id": f"obj_{approval_id}",
        "action_type": "send_whatsapp",
        "action_mode": "approval_required",
        "channel": "whatsapp",
        "summary_ar": "ملخّص",
        "summary_en": "summary",
        "risk_level": "medium",
        "proof_impact": "leadops:lops_test",
    }
    defaults.update(kw)
    return ApprovalRequest(**defaults)


def test_channel_policy_table_exists() -> None:
    """Per-channel policy table is required for the spine to enforce
    that LinkedIn and WhatsApp can never auto-approve."""
    assert CHANNEL_POLICY["whatsapp"]["max_auto_approve_risk"] is None
    assert CHANNEL_POLICY["linkedin"]["max_auto_approve_risk"] is None
    assert CHANNEL_POLICY["phone"]["max_auto_approve_risk"] is None
    assert CHANNEL_POLICY["email"]["max_auto_approve_risk"] == "low"
    assert CHANNEL_POLICY["dashboard"]["max_auto_approve_risk"] == "medium"


def test_can_auto_approve_whatsapp_always_false() -> None:
    req = _make("apv_w1", channel="whatsapp", risk_level="low")
    assert can_auto_approve(req) is False
    req = _make("apv_w2", channel="whatsapp", risk_level="medium")
    assert can_auto_approve(req) is False


def test_can_auto_approve_linkedin_always_false() -> None:
    req = _make("apv_l1", channel="linkedin", risk_level="low")
    assert can_auto_approve(req) is False


def test_can_auto_approve_email_low_risk_only() -> None:
    assert can_auto_approve(_make("apv_e1", channel="email", risk_level="low")) is True
    assert can_auto_approve(_make("apv_e2", channel="email", risk_level="medium")) is False
    assert can_auto_approve(_make("apv_e3", channel="email", risk_level="high")) is False


def test_evaluate_safety_strips_auto_execute_from_linkedin() -> None:
    from auto_client_acquisition.approval_center.approval_policy import evaluate_safety
    req = _make("apv_li", channel="linkedin", action_mode="approved_execute", risk_level="low")
    evaluate_safety(req)
    # LinkedIn must never be auto-executed
    assert req.action_mode == "approval_required"


def test_expire_overdue_flips_pending_to_expired() -> None:
    store = ApprovalStore()
    past = datetime.now(timezone.utc) - timedelta(hours=1)
    future = datetime.now(timezone.utc) + timedelta(hours=1)

    expired_req = _make("apv_old", expires_at=past)
    fresh_req = _make("apv_new", expires_at=future)
    no_expiry_req = _make("apv_forever", expires_at=None)

    store.create(expired_req)
    store.create(fresh_req)
    store.create(no_expiry_req)

    count = store.expire_overdue()
    assert count == 1
    assert store.get("apv_old").status == ApprovalStatus.EXPIRED
    assert store.get("apv_new").status == ApprovalStatus.PENDING
    assert store.get("apv_forever").status == ApprovalStatus.PENDING


def test_bulk_approve_by_proof_impact_prefix() -> None:
    store = ApprovalStore()
    store.create(_make("apv_a", proof_impact="leadops:lops_X"))
    store.create(_make("apv_b", proof_impact="leadops:lops_X"))
    store.create(_make("apv_c", proof_impact="leadops:lops_Y"))  # different prefix

    result = store.bulk_approve(who="founder", proof_impact_prefix="leadops:lops_X")
    assert len(result["approved"]) == 2
    assert "apv_a" in result["approved"]
    assert "apv_b" in result["approved"]
    assert store.get("apv_c").status == ApprovalStatus.PENDING


def test_bulk_approve_by_explicit_ids() -> None:
    store = ApprovalStore()
    store.create(_make("apv_x"))
    store.create(_make("apv_y"))
    store.create(_make("apv_z"))

    result = store.bulk_approve(who="founder", approval_ids=["apv_x", "apv_z"])
    assert len(result["approved"]) == 2
    assert store.get("apv_x").status == ApprovalStatus.APPROVED
    assert store.get("apv_y").status == ApprovalStatus.PENDING
    assert store.get("apv_z").status == ApprovalStatus.APPROVED


@pytest.mark.asyncio
async def test_expire_sweep_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/approvals/expire-sweep")
    assert r.status_code == 200
    body = r.json()
    assert "expired_count" in body
    assert body["guardrails"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_bulk_approve_endpoint_requires_who() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/approvals/bulk-approve", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_bulk_approve_endpoint_requires_selection() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/approvals/bulk-approve", json={"who": "founder"})
    assert r.status_code == 422
