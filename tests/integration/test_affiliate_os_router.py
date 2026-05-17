"""Integration tests for the Affiliate OS router — Dealix Full Ops.

Exercises the public application + compliance endpoints and the
admin-gated, approval-gated commission payout flow.
"""
from __future__ import annotations

import pytest

ADMIN_KEY = "test_admin_affiliate"
ADMIN_HEADER = {"X-Admin-API-Key": ADMIN_KEY}


@pytest.fixture()
def affiliate_env(tmp_path, monkeypatch):
    """Isolate the affiliate JSONL store and the approval singleton."""
    monkeypatch.setenv("DEALIX_AFFILIATES_PATH", str(tmp_path / "aff.jsonl"))
    monkeypatch.setenv(
        "DEALIX_AFFILIATE_COMMISSIONS_PATH", str(tmp_path / "com.jsonl")
    )
    monkeypatch.setenv(
        "DEALIX_AFFILIATE_PAYOUTS_PATH", str(tmp_path / "pay.jsonl")
    )
    monkeypatch.setenv(
        "DEALIX_EVIDENCE_CONTROL_PATH", str(tmp_path / "ev.jsonl")
    )
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    from auto_client_acquisition.affiliate_os import store
    from auto_client_acquisition.approval_center.approval_store import (
        get_default_approval_store,
    )

    store.clear_for_test()
    get_default_approval_store().clear()
    yield
    store.clear_for_test()
    get_default_approval_store().clear()


# ─────────────── Public endpoints ───────────────


@pytest.mark.asyncio
async def test_status_public(async_client, affiliate_env):
    res = await async_client.get("/api/v1/affiliate-os/status")
    assert res.status_code == 200
    body = res.json()
    assert body["module"] == "affiliate_os"
    assert body["guardrails"]["no_llm_calls"] is True
    assert body["hard_gates"]["no_payout_without_founder_approval"] is True


@pytest.mark.asyncio
async def test_program_terms_lists_four_tiers(async_client, affiliate_env):
    res = await async_client.get("/api/v1/affiliate-os/program-terms")
    assert res.status_code == 200
    body = res.json()
    assert len(body["tiers"]) == 4
    assert body["disclosure_ar"]
    assert body["disclosure_en"]


@pytest.mark.asyncio
async def test_apply_creates_pending_affiliate_and_approval(
    async_client, affiliate_env
):
    res = await async_client.post(
        "/api/v1/affiliate-os/apply",
        json={
            "handle": "b2b_creator",
            "email": "creator@example.com",
            "audience_type": "b2b",
            "audience_in_gcc": True,
            "is_consultant_or_operator": True,
            "promotion_plan_clear": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "received_pending_approval"
    assert body["affiliate_status"] == "pending"
    assert body["approval_id"].startswith("apr_")
    assert body["application_score"] >= 10


@pytest.mark.asyncio
async def test_compliance_check_flags_and_passes(async_client, affiliate_env):
    bad = await async_client.post(
        "/api/v1/affiliate-os/compliance/check",
        json={"text": "Dealix gives guaranteed ROI, sign up!!!"},
    )
    assert bad.status_code == 200
    assert bad.json()["compliant"] is False

    good = await async_client.post(
        "/api/v1/affiliate-os/compliance/check",
        json={"text": "تنويه: قد أحصل على عمولة إحالة. أوصي بـDealix."},
    )
    assert good.status_code == 200
    assert good.json()["compliant"] is True


# ─────────────── Admin gating ───────────────


@pytest.mark.asyncio
async def test_compute_requires_admin(async_client, affiliate_env):
    res = await async_client.post(
        "/api/v1/affiliate-os/commission/compute",
        json={
            "affiliate_id": "aff_1",
            "tier": "tier_1_affiliate_lead",
            "deal_amount_sar": 499,
        },
    )
    assert res.status_code in (401, 403)


# ─────────────── Commission payout flow ───────────────


@pytest.mark.asyncio
async def test_compute_eligible_when_invoice_paid(async_client, affiliate_env):
    res = await async_client.post(
        "/api/v1/affiliate-os/commission/compute",
        headers=ADMIN_HEADER,
        json={
            "affiliate_id": "aff_1",
            "tier": "tier_2_qualified_referral",
            "deal_amount_sar": 4999,
            "invoice_status": "paid",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["commission"]["status"] == "eligible"
    assert body["eligible_for_payout_request"] is True


@pytest.mark.asyncio
async def test_compute_voids_disqualified_lead(async_client, affiliate_env):
    res = await async_client.post(
        "/api/v1/affiliate-os/commission/compute",
        headers=ADMIN_HEADER,
        json={
            "affiliate_id": "aff_1",
            "tier": "tier_1_affiliate_lead",
            "deal_amount_sar": 499,
            "invoice_status": "paid",
            "lead_flags": ["duplicate"],
        },
    )
    assert res.status_code == 200
    assert res.json()["commission"]["status"] == "void"


@pytest.mark.asyncio
async def test_request_payout_refused_when_not_eligible(
    async_client, affiliate_env
):
    compute = await async_client.post(
        "/api/v1/affiliate-os/commission/compute",
        headers=ADMIN_HEADER,
        json={
            "affiliate_id": "aff_1",
            "tier": "tier_1_affiliate_lead",
            "deal_amount_sar": 499,
            "invoice_status": "draft",
        },
    )
    commission_id = compute.json()["commission"]["commission_id"]
    res = await async_client.post(
        f"/api/v1/affiliate-os/commission/{commission_id}/request-payout",
        headers=ADMIN_HEADER,
        json={"requested_by": "founder"},
    )
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_full_payout_flow_requires_approval(async_client, affiliate_env):
    from auto_client_acquisition.approval_center.approval_store import (
        get_default_approval_store,
    )

    # 1. compute an eligible commission
    compute = await async_client.post(
        "/api/v1/affiliate-os/commission/compute",
        headers=ADMIN_HEADER,
        json={
            "affiliate_id": "aff_1",
            "tier": "tier_2_qualified_referral",
            "deal_amount_sar": 4999,
            "invoice_status": "paid",
        },
    )
    commission_id = compute.json()["commission"]["commission_id"]

    # 2. request payout → opens an ApprovalRequest
    req = await async_client.post(
        f"/api/v1/affiliate-os/commission/{commission_id}/request-payout",
        headers=ADMIN_HEADER,
        json={"requested_by": "founder"},
    )
    assert req.status_code == 200
    approval_id = req.json()["approval_id"]

    # 3. confirm-payout BEFORE approval → blocked
    early = await async_client.post(
        f"/api/v1/affiliate-os/commission/{commission_id}/confirm-payout",
        headers=ADMIN_HEADER,
        json={"confirmed_by": "founder"},
    )
    assert early.status_code == 409

    # 4. founder approves the request through the Approval Command Center
    get_default_approval_store().approve(approval_id, "founder")

    # 5. confirm-payout now succeeds
    done = await async_client.post(
        f"/api/v1/affiliate-os/commission/{commission_id}/confirm-payout",
        headers=ADMIN_HEADER,
        json={"confirmed_by": "founder"},
    )
    assert done.status_code == 200
    body = done.json()
    assert body["status"] == "paid"
    assert body["payout"]["approval_id"] == approval_id


@pytest.mark.asyncio
async def test_clawback_on_refund_in_window(async_client, affiliate_env):
    compute = await async_client.post(
        "/api/v1/affiliate-os/commission/compute",
        headers=ADMIN_HEADER,
        json={
            "affiliate_id": "aff_1",
            "tier": "tier_1_affiliate_lead",
            "deal_amount_sar": 499,
            "invoice_status": "paid",
        },
    )
    commission_id = compute.json()["commission"]["commission_id"]
    res = await async_client.post(
        f"/api/v1/affiliate-os/commission/{commission_id}/clawback",
        headers=ADMIN_HEADER,
        json={
            "invoice_status": "refunded",
            "paid_at": "2026-01-01T00:00:00+00:00",
            "refunded_at": "2026-01-15T00:00:00+00:00",
        },
    )
    assert res.status_code == 200
    assert res.json()["status"] == "clawed_back"
