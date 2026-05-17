"""Affiliate OS — acceptance tests for the governed affiliate program.

The four hard gates under test:
  1. Affiliate copy with a guaranteed/forbidden claim is BLOCKED.
  2. A commission never accrues without invoice-paid evidence.
  3. A payout never settles without human approval.
  4. The happy path settles and writes an audit trail.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.affiliate_os import (
    affiliate_store,
    asset_registry,
    commission_engine,
    payout_gate,
    referral_links,
)
from auto_client_acquisition.affiliate_os.affiliate_profile import AffiliateApplication
from auto_client_acquisition.affiliate_os.asset_registry import AssetSubmission
from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.auditability_os import audit_event
from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.revops import payment_confirmation


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    """Point every JSONL store at a temp dir and wipe shared in-memory state."""
    monkeypatch.setenv("DEALIX_AFFILIATES_PATH", str(tmp_path / "affiliates.jsonl"))
    monkeypatch.setenv("DEALIX_AFFILIATE_LINKS_PATH", str(tmp_path / "links.jsonl"))
    monkeypatch.setenv("DEALIX_AFFILIATE_ASSETS_PATH", str(tmp_path / "assets.jsonl"))
    monkeypatch.setenv(
        "DEALIX_AFFILIATE_COMMISSIONS_PATH", str(tmp_path / "commissions.jsonl")
    )
    monkeypatch.setenv("DEALIX_AFFILIATE_PAYOUTS_PATH", str(tmp_path / "payouts.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    payment_confirmation.reset_confirmations()
    get_default_approval_store().clear()
    yield
    payment_confirmation.reset_confirmations()
    get_default_approval_store().clear()


def _approved_affiliate(affiliate_id: str = "aff_001") -> str:
    affiliate_store.submit_application(
        AffiliateApplication(
            affiliate_id=affiliate_id,
            placeholder_name="Affiliate-A",
            affiliate_type="agency",
            region="riyadh",
        )
    )
    affiliate_store.set_status(affiliate_id=affiliate_id, status="approved")
    return affiliate_id


def _paid_invoice(invoice_id: str, amount_sar: int = 10000) -> None:
    payment_confirmation.record_payment_confirmation(
        invoice_id=invoice_id,
        customer_handle="customer-handle-x",
        amount_sar=amount_sar,
        payment_method="bank_transfer",
        evidence_reference=f"bank_statement_{invoice_id}.pdf",
    )


# ── Gate 1: forbidden / guaranteed claims are blocked ────────────────


def test_affiliate_copy_with_guarantee_claim_is_blocked() -> None:
    affiliate_id = _approved_affiliate()
    result = asset_registry.review_asset_copy(
        AssetSubmission(
            asset_id="asset_bad",
            affiliate_id=affiliate_id,
            copy_text="Use Dealix for guaranteed sales and guaranteed ROI every month.",
        )
    )
    assert result.decision == GovernanceDecision.BLOCK
    assert result.approved_asset is None
    assert result.issues
    assert asset_registry.list_approved_assets(affiliate_id=affiliate_id) == []


def test_clean_affiliate_copy_is_approved_with_disclosure() -> None:
    affiliate_id = _approved_affiliate()
    result = asset_registry.review_asset_copy(
        AssetSubmission(
            asset_id="asset_ok",
            affiliate_id=affiliate_id,
            copy_text="Dealix helps Saudi B2B teams organize their revenue operations.",
        )
    )
    assert result.decision == GovernanceDecision.ALLOW
    assert result.approved_asset is not None
    assert result.approved_asset.disclosure_text  # disclosure is mandatory


@pytest.mark.asyncio
async def test_assets_submit_endpoint_blocks_guarantee_claim() -> None:
    from httpx import ASGITransport, AsyncClient

    from api.main import app

    affiliate_id = _approved_affiliate()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/affiliate-os/assets/submit",
            json={
                "asset_id": "asset_api_bad",
                "affiliate_id": affiliate_id,
                "copy_text": "guaranteed revenue for all Dealix affiliates",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["approved"] is False
    assert body["governance_decision"] == GovernanceDecision.BLOCK.value


# ── Gate 2: commission requires invoice-paid evidence ────────────────


def test_commission_not_created_without_invoice_paid_evidence() -> None:
    affiliate_id = _approved_affiliate()
    link = referral_links.create_affiliate_link(affiliate_id=affiliate_id)

    no_commission = commission_engine.calculate_commission(
        affiliate_id=affiliate_id,
        referral_code=link.code,
        invoice_id="inv_unpaid",
        deal_amount_sar=10000,
    )
    assert no_commission is None
    assert commission_engine.list_commissions() == []

    _paid_invoice("inv_unpaid")
    commission = commission_engine.calculate_commission(
        affiliate_id=affiliate_id,
        referral_code=link.code,
        invoice_id="inv_unpaid",
        deal_amount_sar=10000,
    )
    assert commission is not None
    assert commission.commission_amount_sar > 0
    assert commission.evidence_reference


# ── Gate 3: payout requires human approval ───────────────────────────


def test_payout_blocked_without_approval() -> None:
    affiliate_id = _approved_affiliate()
    link = referral_links.create_affiliate_link(affiliate_id=affiliate_id)
    _paid_invoice("inv_payout")
    commission = commission_engine.calculate_commission(
        affiliate_id=affiliate_id,
        referral_code=link.code,
        invoice_id="inv_payout",
        deal_amount_sar=10000,
    )
    assert commission is not None

    payout = payout_gate.request_payout(commission_id=commission.commission_id)
    assert payout.status == "pending_approval"

    # Finalize WITHOUT approving the underlying ApprovalRequest.
    still_pending = payout_gate.finalize_payout(
        payout_id=payout.payout_id, approver="founder"
    )
    assert still_pending is not None
    assert still_pending.status == "pending_approval"
    assert all(p.status != "paid" for p in payout_gate.list_payouts())


# ── Gate 4: happy path settles + writes an audit trail ───────────────


def test_happy_path_end_to_end() -> None:
    affiliate_id = _approved_affiliate()
    link = referral_links.create_affiliate_link(affiliate_id=affiliate_id)
    _paid_invoice("inv_happy")
    commission = commission_engine.calculate_commission(
        affiliate_id=affiliate_id,
        referral_code=link.code,
        invoice_id="inv_happy",
        deal_amount_sar=10000,
    )
    assert commission is not None

    payout = payout_gate.request_payout(commission_id=commission.commission_id)
    settled = payout_gate.approve_payout(
        payout_id=payout.payout_id, approver="founder"
    )
    assert settled is not None
    assert settled.status == "paid"
    assert settled.paid_at

    events = audit_event.list_events(
        customer_id=affiliate_store.AFFILIATE_OPS_TENANT
    )
    kinds = {e.kind for e in events}
    assert audit_event.AuditEventKind.OUTPUT_DELIVERED.value in kinds
    assert audit_event.AuditEventKind.APPROVAL.value in kinds


# ── Misc gates ───────────────────────────────────────────────────────


def test_link_generation_requires_approved_affiliate() -> None:
    affiliate_store.submit_application(
        AffiliateApplication(
            affiliate_id="aff_pending",
            placeholder_name="Affiliate-P",
            affiliate_type="newsletter",
            region="jeddah",
        )
    )
    with pytest.raises(ValueError):
        referral_links.create_affiliate_link(affiliate_id="aff_pending")


@pytest.mark.asyncio
async def test_status_endpoint_reports_hard_gates() -> None:
    from httpx import ASGITransport, AsyncClient

    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/affiliate-os/status")
    assert r.status_code == 200
    gates = r.json()["hard_gates"]
    assert gates["commission_requires_invoice_paid"] is True
    assert gates["payout_requires_human_approval"] is True
    assert gates["no_guaranteed_claims"] is True
