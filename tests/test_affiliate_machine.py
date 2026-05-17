"""Affiliate & Partner machine — endpoint coverage.

Exercises the full loop: apply -> approve (queues approval) -> activate
-> link -> referral -> qualify -> commission -> payout -> dashboard ->
portal. Uses the ``async_client`` fixture and an isolated JSONL store
(DEALIX_AFFILIATE_*_PATH env vars set before the app is imported).
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient

_TMP = tempfile.mkdtemp(prefix="affiliate-test-")
for _var in (
    "DEALIX_AFFILIATE_PARTNERS_PATH",
    "DEALIX_AFFILIATE_LINKS_PATH",
    "DEALIX_AFFILIATE_REFERRALS_PATH",
    "DEALIX_AFFILIATE_COMMISSIONS_PATH",
    "DEALIX_AFFILIATE_PAYOUTS_PATH",
    "DEALIX_AFFILIATE_COMPLIANCE_PATH",
):
    os.environ[_var] = os.path.join(_TMP, _var.lower() + ".jsonl")
os.environ.setdefault("DEALIX_FRICTION_LOG_PATH", os.path.join(_TMP, "friction.jsonl"))
os.environ["ADMIN_API_KEYS"] = "test_affiliate_admin_key"

from auto_client_acquisition.partnership_os import affiliate_store  # noqa: E402

_ADMIN = {"X-Admin-API-Key": "test_affiliate_admin_key"}


@pytest.fixture(autouse=True)
def _clean_store() -> Iterator[None]:
    affiliate_store.clear_for_test()
    yield
    affiliate_store.clear_for_test()


def _envelope_ok(payload: dict[str, Any]) -> None:
    assert "hard_gates" in payload
    assert "governance_decision" in payload
    assert payload["hard_gates"]["approval_required_for_partner_activation"] is True


def _good_application() -> dict[str, Any]:
    return {
        "company_name": "Growth Advisors",
        "contact_name": "Sara Ahmed",
        "contact_email": "sara@growthadvisors.sa",
        "country": "sa",
        "audience_type": "b2b",
        "audience_size": 5000,
        "main_channel": "consulting",
        "plan": "Introduce Dealix to our B2B consulting clients via warm intros.",
        "prior_referrals": 3,
        "content_quality": True,
        "trusted_brand": True,
        "disclosure_accepted": True,
    }


async def _apply(client: AsyncClient) -> str:
    resp = await client.post("/api/v1/public/partner-apply", json=_good_application())
    assert resp.status_code == 200, resp.text
    body = resp.json()
    _envelope_ok(body)
    return body["partner_id"]


@pytest.mark.asyncio
async def test_public_tiers_endpoint(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/affiliate/tiers")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["tiers"]) == 4
    _envelope_ok(body)


@pytest.mark.asyncio
async def test_approved_assets_endpoint(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/affiliate/approved-assets")
    assert resp.status_code == 200
    body = resp.json()
    assert body["disclosure_mandatory"] is True
    assert any(a["asset_type"] == "disclosure" for a in body["assets"])


@pytest.mark.asyncio
async def test_partner_apply_creates_scored_partner(async_client: AsyncClient) -> None:
    resp = await async_client.post(
        "/api/v1/public/partner-apply", json=_good_application()
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "application_received"
    assert body["score"]["score"] > 0
    partner = affiliate_store.get("partners", body["partner_id"])
    assert partner is not None
    # No raw email is ever stored — only a hash.
    assert "contact_email" not in partner
    assert partner["contact_email_hash"]


@pytest.mark.asyncio
async def test_full_loop_apply_to_portal(async_client: AsyncClient) -> None:
    partner_id = await _apply(async_client)

    # Approve — queues an ApprovalRequest, partner NOT yet active.
    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/approve",
        json={"approver": "founder", "tier": "qualified_referral"},
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "approval_queued"
    assert affiliate_store.get("partners", partner_id)["status"] == "pending_activation"

    # Activation refused while approval pending.
    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/activate", headers=_ADMIN
    )
    assert resp.status_code == 409

    # Approve the queued request in the Approval Center, then activate.
    from auto_client_acquisition.approval_center import get_default_approval_store

    pending = [
        r
        for r in get_default_approval_store().list_pending()
        if r.object_id == partner_id
    ]
    assert pending, "partner approval was not queued"
    get_default_approval_store().approve(pending[0].approval_id, "founder")

    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/activate", headers=_ADMIN
    )
    assert resp.status_code == 200, resp.text
    activated = resp.json()
    assert activated["status"] == "activated"
    assert activated["referral_code"]

    # Create a tracked link.
    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/links",
        json={"utm_campaign": "spring", "target_url": "https://dealix.me/pricing"},
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text

    # Log a referral.
    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/referrals",
        json={
            "contact_email": "lead@prospect.sa",
            "tier": "qualified_referral",
            "lead_id": "lead_99",
        },
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text
    referral_id = resp.json()["referral"]["id"]

    # Qualify it.
    resp = await async_client.post(
        f"/api/v1/referrals/{referral_id}/qualify", headers=_ADMIN
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["referral"]["qualified"] is True

    # Calculate commission for a paid deal.
    from datetime import datetime, timezone

    resp = await async_client.post(
        "/api/v1/commissions/calculate",
        json={
            "referral_id": referral_id,
            "deal_id": "deal_99",
            "amount_sar": 12000,
            "invoice_paid": True,
            "invoice_paid_at": datetime.now(timezone.utc).isoformat(),
            "tier": "qualified_referral",
        },
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text
    commission = resp.json()["commission"]
    assert commission["amount_sar"] == 1200.0

    # Build a payout.
    resp = await async_client.post(
        "/api/v1/payouts/build",
        json={"partner_id": partner_id, "period": "2026-05"},
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text
    payout_id = resp.json()["payout"]["id"]

    # Dashboard.
    resp = await async_client.get("/api/v1/ops/partners/dashboard", headers=_ADMIN)
    assert resp.status_code == 200, resp.text
    dash = resp.json()
    assert dash["active_partners"] >= 1
    assert dash["referrals_qualified"] >= 1

    # Portal.
    resp = await async_client.get(f"/api/v1/partner/{partner_id}/portal")
    assert resp.status_code == 200, resp.text
    portal = resp.json()
    assert portal["partner"]["status"] == "active"
    assert portal["commission_earned_sar"] == 1200.0
    assert any(p["id"] == payout_id for p in portal["payouts"])
    _envelope_ok(portal)


@pytest.mark.asyncio
async def test_unknown_partner_returns_404(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/partner/ptn_missing/portal")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_compliance_event_recorded(async_client: AsyncClient) -> None:
    partner_id = await _apply(async_client)
    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/compliance-event",
        json={"kind": "no_disclosure", "severity": "med", "notes": "missing disclosure"},
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["event"]["kind"] == "no_disclosure"
