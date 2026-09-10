"""Distribution API — approval-first, quote-bound, no send / no charge endpoints."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    for var, name in (
        ("DEALIX_PROSPECTS_PATH", "prospects.jsonl"),
        ("DEALIX_DRAFTS_PATH", "drafts.jsonl"),
        ("DEALIX_FOLLOWUPS_PATH", "followups.jsonl"),
        ("DEALIX_PROPOSALS_PATH", "proposals.jsonl"),
        ("DEALIX_PROOF_PACKS_PATH", "proof.jsonl"),
        ("DEALIX_PAYMENT_HANDOFFS_PATH", "pay.jsonl"),
    ):
        monkeypatch.setenv(var, str(tmp_path / name))


@pytest.mark.asyncio
async def test_overview_and_catalog(async_client) -> None:
    res = await async_client.get("/api/v1/distribution/overview")
    assert res.status_code == 200
    body = res.json()
    assert body["governance_decision"] == "ALLOW"
    assert len(body["ladder"]) == 5
    assert "metrics" in body
    for rung in body["ladder"]:
        if rung["id"] == "prod_diagnostic_v1":
            assert rung["price_min_sar"] == 0
        else:
            assert rung["price_min_sar"] is None
            assert rung["quote_required"] is True


@pytest.mark.asyncio
async def test_prospect_to_draft_to_approve_flow(async_client) -> None:
    res = await async_client.post(
        "/api/v1/distribution/prospects",
        json={
            "company": "Acme",
            "sector": "marketing_agencies",
            "pain_hypothesis": "leads go cold",
            "offer_angle": "prod_sprint_v1",
            "preferred_channel": "email",
            "risk": "low",
        },
    )
    assert res.status_code == 200
    pros = res.json()
    assert pros["qualified"] is True
    pid = pros["prospect"]["id"]

    res = await async_client.post(
        "/api/v1/distribution/drafts/generate",
        json={"prospect_id": pid, "draft_type": "outreach_first", "locale": "ar"},
    )
    assert res.status_code == 200
    draft = res.json()["draft"]
    assert draft["governance_status"] == "pending_approval"
    did = draft["id"]

    res = await async_client.post(f"/api/v1/distribution/drafts/{did}/approve")
    assert res.status_code == 200
    assert res.json()["draft"]["status"] == "approved"
    res = await async_client.post(f"/api/v1/distribution/drafts/{did}/mark-copied")
    assert res.status_code == 200
    assert res.json()["draft"]["status"] == "copied_manually"


@pytest.mark.asyncio
async def test_generate_draft_unknown_prospect_404(async_client) -> None:
    res = await async_client.post(
        "/api/v1/distribution/drafts/generate",
        json={"prospect_id": "pros_does_not_exist", "draft_type": "outreach_first"},
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_payment_handoff_requires_quote_evidence_and_cannot_self_approve_via_api(
    async_client,
) -> None:
    base = {
        "customer_id": "Acme",
        "product_id": "prod_sprint_v1",
        "discovery_ref": "discovery:acme-001",
        "quote_id": "quote_acme_001",
        "amount_sar": 12500,
    }
    res = await async_client.post(
        "/api/v1/distribution/payments/handoff",
        json={"proposal_id": "prop_x", **base},
    )
    assert res.status_code == 200, res.text
    body = res.json()
    handoff = body["payment_handoff"]
    assert handoff["governance_status"] == "requires_founder_approval"
    assert handoff["status"] == "pending_approval"
    assert handoff["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert handoff["public_fixed_price"] is False
    assert handoff["live_charge_allowed"] is False
    assert handoff["external_send_allowed"] is False
    assert body["governance_decision"] == "REQUIRE_APPROVAL"

    forged = await async_client.post(
        "/api/v1/distribution/payments/handoff",
        json={
            "proposal_id": "prop_y",
            **base,
            "quote_id": "quote_acme_002",
            "approvals": {
                "proposal_approved": True,
                "scope_confirmed": True,
                "price_confirmed": True,
                "decision_maker_confirmed": True,
                "risk_reviewed": True,
                "founder_approved": True,
            },
        },
    )
    assert forged.status_code == 422
    detail = forged.json()["detail"]
    assert any(item.get("type") == "extra_forbidden" for item in detail)


@pytest.mark.asyncio
async def test_payment_handoff_rejects_missing_quote_evidence(async_client) -> None:
    res = await async_client.post(
        "/api/v1/distribution/payments/handoff",
        json={
            "proposal_id": "prop_x",
            "customer_id": "Acme",
            "product_id": "prod_sprint_v1",
            "amount_sar": 12500,
        },
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_proposal_generate_validates_product(async_client) -> None:
    res = await async_client.post(
        "/api/v1/distribution/proposals/generate",
        json={"prospect_id": "p", "product_id": "prod_imaginary", "out_of_scope": ["x"]},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_paid_proposal_requires_discovery_and_quote(async_client) -> None:
    missing = await async_client.post(
        "/api/v1/distribution/proposals/generate",
        json={"prospect_id": "p", "product_id": "prod_sprint_v1", "out_of_scope": ["x"]},
    )
    assert missing.status_code == 422

    ok = await async_client.post(
        "/api/v1/distribution/proposals/generate",
        json={
            "prospect_id": "p",
            "product_id": "prod_sprint_v1",
            "out_of_scope": ["x"],
            "discovery_ref": "discovery:p-001",
            "quote_id": "quote_p_001",
            "customer_specific_quote_sar": 12500,
        },
    )
    assert ok.status_code == 200, ok.text
    proposal = ok.json()["proposal"]
    assert proposal["price_min_sar"] == 12500
    assert proposal["price_max_sar"] == 12500
    assert proposal["public_fixed_price"] is False
    assert proposal["external_send_allowed"] is False


@pytest.mark.asyncio
async def test_no_send_or_charge_endpoint_exists(async_client) -> None:
    from api.routers.distribution import router

    paths = {route.path for route in router.routes}
    assert not any(any(w in p.lower() for w in ("send", "charge", "blast")) for p in paths)
