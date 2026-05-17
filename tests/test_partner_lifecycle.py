"""Full Ops 2.0 — partner/affiliate lifecycle + payout safety + clawback."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.partnership_os import (
    PartnerStage,
    PartnerTier,
    can_advance,
    compute_payout,
    flag_forbidden_claims,
    next_stage,
)
from auto_client_acquisition.partnership_os.referral_store import (
    ReferralStatus,
    clawback_credit,
    clear_for_test,
    create_referral_code,
    issue_credit,
    mark_invoice_paid,
    redeem_referral,
)


# ── lifecycle stages + tiers ─────────────────────────────────────


def test_next_stage_progression() -> None:
    assert next_stage(PartnerStage.APPLY) == PartnerStage.SCORE
    assert next_stage(PartnerStage.PAY) is None


def test_partner_tiers_are_zero_to_four() -> None:
    assert PartnerTier.APPLICANT == 0
    assert PartnerTier.IMPLEMENTATION_PARTNER == 4


def test_can_advance_forward_only() -> None:
    # skipping a stage is rejected
    res = can_advance(from_stage=PartnerStage.APPLY, to_stage=PartnerStage.APPROVE)
    assert res.allowed is False


def test_can_advance_requires_fit_score_for_approval() -> None:
    low = can_advance(
        from_stage=PartnerStage.SCORE, to_stage=PartnerStage.APPROVE, fit_score=20
    )
    assert low.allowed is False
    ok = can_advance(
        from_stage=PartnerStage.SCORE, to_stage=PartnerStage.APPROVE, fit_score=70
    )
    assert ok.allowed is True


def test_can_advance_pay_blocked_on_compliance_violation() -> None:
    res = can_advance(
        from_stage=PartnerStage.REVIEW,
        to_stage=PartnerStage.PAY,
        has_clean_compliance=False,
    )
    assert res.allowed is False


# ── forbidden claims guard ───────────────────────────────────────


def test_flag_forbidden_claims_catches_guarantee() -> None:
    res = flag_forbidden_claims("Dealix guarantees revenue for every client.")
    assert res.is_clean is False
    assert res.requires_review is True
    assert any("guarantees revenue" in c for c in res.flagged_claims)


def test_flag_forbidden_claims_clean_copy() -> None:
    res = flag_forbidden_claims("Dealix helps Saudi B2B teams reply to leads faster.")
    assert res.is_clean is True
    assert res.flagged_claims == []


# ── payout rules ─────────────────────────────────────────────────


def test_compute_payout_blocked_before_invoice_paid() -> None:
    d = compute_payout(
        motion="affiliate_lead", deal_amount_sar=10000, invoice_paid=False
    )
    assert d.eligible is False


def test_compute_payout_affiliate_five_percent() -> None:
    d = compute_payout(
        motion="affiliate_lead", deal_amount_sar=10000, invoice_paid=True
    )
    assert d.eligible is True
    assert d.commission_pct == 5.0
    assert d.commission_sar == 500


def test_compute_payout_blocks_self_referral() -> None:
    d = compute_payout(
        motion="warm_qualified_intro",
        deal_amount_sar=10000,
        invoice_paid=True,
        is_self_referral=True,
    )
    assert d.eligible is False


def test_compute_payout_blocks_duplicate() -> None:
    d = compute_payout(
        motion="warm_qualified_intro",
        deal_amount_sar=10000,
        invoice_paid=True,
        is_duplicate=True,
    )
    assert d.eligible is False


def test_compute_payout_blocks_compliance_violation() -> None:
    d = compute_payout(
        motion="strategic_partner_deal",
        deal_amount_sar=50000,
        invoice_paid=True,
        compliance_violation=True,
    )
    assert d.eligible is False


def test_compute_payout_strategic_band() -> None:
    d = compute_payout(
        motion="strategic_partner_deal",
        deal_amount_sar=50000,
        invoice_paid=True,
        approved_pct=18.0,
    )
    assert d.eligible is True
    assert d.commission_pct == 18.0


# ── referral-store clawback ──────────────────────────────────────


@pytest.fixture(autouse=True)
def _isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_REFERRAL_CODES_PATH", str(tmp_path / "codes.jsonl"))
    monkeypatch.setenv("DEALIX_REFERRALS_PATH", str(tmp_path / "refs.jsonl"))
    monkeypatch.setenv("DEALIX_REFERRAL_PAYOUTS_PATH", str(tmp_path / "payouts.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_issue_credit_blocked_before_invoice_paid() -> None:
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta")
    # No invoice paid — no credit.
    assert issue_credit(referral_id=r.referral_id) is None


def test_clawback_reverses_issued_credit() -> None:
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta")
    mark_invoice_paid(referral_id=r.referral_id, invoice_id="inv1", amount_sar=2999)
    payout = issue_credit(referral_id=r.referral_id)
    assert payout is not None
    reversal = clawback_credit(referral_id=r.referral_id, reason="refund")
    assert reversal is not None
    assert reversal.credit_sar == -payout.credit_sar


def test_clawback_noop_when_no_credit_issued() -> None:
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta")
    assert clawback_credit(referral_id=r.referral_id) is None


def test_clawback_outside_window_rejected() -> None:
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta")
    mark_invoice_paid(referral_id=r.referral_id, invoice_id="inv1", amount_sar=2999)
    issue_credit(referral_id=r.referral_id)
    # Request 60 days after issuance — outside the 30-day window.
    late = clawback_credit(
        referral_id=r.referral_id, requested_at="2099-12-31T00:00:00+00:00"
    )
    assert late is None


def test_clawback_transitions_status() -> None:
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta")
    mark_invoice_paid(referral_id=r.referral_id, invoice_id="inv1", amount_sar=2999)
    issue_credit(referral_id=r.referral_id)
    clawback_credit(referral_id=r.referral_id)
    from auto_client_acquisition.partnership_os.referral_store import get_referral

    ref = get_referral(r.referral_id)
    assert ref is not None
    assert ref.status == ReferralStatus.CLAWED_BACK.value


# ── router endpoints ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_router_lifecycle_overview() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/partnership-os/lifecycle")
    body = r.json()
    assert "apply" in body["stages"]
    assert body["tiers"]["0"]["en"] == "Applicant"


@pytest.mark.asyncio
async def test_router_claim_scan_blocks_forbidden() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/partnership-os/claim-scan",
            json={"partner_copy": "Dealix guarantees compliance for you."},
        )
    body = r.json()
    assert body["is_clean"] is False
    assert body["governance_decision"] == "blocked"


@pytest.mark.asyncio
async def test_router_payout_blocked_without_invoice() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/partnership-os/payout/compute",
            json={
                "motion": "affiliate_lead",
                "deal_amount_sar": 10000,
                "invoice_paid": False,
            },
        )
    body = r.json()
    assert body["eligible"] is False
    assert body["governance_decision"] == "blocked"
