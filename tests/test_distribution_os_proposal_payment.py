"""Distribution OS — quote-bound proposal factory + payment/delivery handoffs."""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.distribution_os import (
    delivery_handoff,
    payment_handoff,
    proposal,
)
from auto_client_acquisition.distribution_os.payment_handoff import PaymentHandoffStatus


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_PROPOSALS_PATH", str(tmp_path / "proposals.jsonl"))
    monkeypatch.setenv("DEALIX_PAYMENT_HANDOFFS_PATH", str(tmp_path / "pay.jsonl"))
    monkeypatch.setenv("DEALIX_DELIVERY_HANDOFFS_PATH", str(tmp_path / "deliv.jsonl"))
    approvals = get_default_approval_store()
    approvals.clear()
    yield
    approvals.clear()


def _paid_proposal(**overrides):
    payload = {
        "prospect_id": "pros_1",
        "product_id": "prod_sprint_v1",
        "problem": "leak",
        "proposed_solution": "organise",
        "out_of_scope": ["external sending"],
        "discovery_ref": "discovery:pros-1",
        "quote_id": "quote_pros_1",
        "customer_specific_quote_sar": 12500,
    }
    payload.update(overrides)
    return proposal.generate_proposal(**payload)


def _approved_quote_authority(
    *,
    lead_id: str,
    amount_sar: float,
    discovery_ref: str,
    scope_ref: str,
) -> str:
    fingerprint = payment_handoff._quote_authority_fingerprint(
        lead_id=lead_id,
        amount_sar=amount_sar,
        discovery_ref=discovery_ref,
        customer_specific_scope_ref=scope_ref,
    )
    store = get_default_approval_store()
    req = ApprovalRequest(
        object_type="customer_specific_quote",
        object_id=fingerprint,
        action_type="customer_specific_quote",
        action_mode="approval_required",
        channel="finance_manual",
        risk_level="high",
        proof_impact=f"customer_specific_quote:{fingerprint}",
        action_id=f"quote:{fingerprint}",
        lead_id=lead_id,
        audit_ref=discovery_ref,
        proof_target=f"invoice_authority:{fingerprint}",
    )
    stored = store.create(req)
    store.approve(stored.approval_id, "founder-test")
    return stored.approval_id


def _authorized_handoff(**overrides):
    p = _paid_proposal()
    proposal.approve_proposal(p.id)
    scope_ref = "scope:pros-1"
    authority_ref = _approved_quote_authority(
        lead_id=p.prospect_id,
        amount_sar=float(p.customer_specific_quote_sar or 0),
        discovery_ref=p.discovery_ref,
        scope_ref=scope_ref,
    )
    payload = {
        "proposal_id": p.id,
        "customer_id": p.prospect_id,
        "product_id": p.product_id,
        "discovery_ref": p.discovery_ref,
        "quote_id": p.quote_id,
        "quote_authority_ref": authority_ref,
        "customer_specific_scope_ref": scope_ref,
        "amount_sar": float(p.customer_specific_quote_sar or 0),
    }
    payload.update(overrides)
    return payment_handoff.prepare_handoff(**payload)


# ── proposal ─────────────────────────────────────────────────────────────────


def test_paid_proposal_price_comes_from_customer_specific_quote_not_catalog() -> None:
    p = _paid_proposal()
    assert (p.price_min_sar, p.price_max_sar) == (12500, 12500)
    assert p.customer_specific_quote_sar == 12500
    assert p.quote_id == "quote_pros_1"
    assert p.discovery_ref == "discovery:pros-1"
    assert p.price_authority == "customer_specific_quote_after_qualified_discovery"
    assert p.public_fixed_price is False
    assert p.external_send_allowed is False
    assert p.approval_status == "pending_approval"


def test_paid_proposal_requires_discovery_quote_and_closed_scope() -> None:
    with pytest.raises(ValueError):
        _paid_proposal(prospect_id="")
    with pytest.raises(ValueError):
        _paid_proposal(product_id="prod_unknown")
    with pytest.raises(ValueError):
        _paid_proposal(out_of_scope=[])
    with pytest.raises(ValueError, match="discovery_ref"):
        _paid_proposal(discovery_ref="")
    with pytest.raises(ValueError, match="quote_id"):
        _paid_proposal(quote_id="")
    with pytest.raises(ValueError, match="customer_specific_quote"):
        _paid_proposal(customer_specific_quote_sar=None)


def test_free_diagnostic_remains_zero_price_without_paid_quote() -> None:
    p = proposal.generate_proposal(
        prospect_id="p",
        product_id="prod_diagnostic_v1",
        out_of_scope=["external sending"],
    )
    assert p.price_min_sar == 0
    assert p.price_max_sar == 0
    assert p.customer_specific_quote_sar is None
    assert p.public_fixed_price is False


def test_proposal_narrative_with_guarantee_is_blocked() -> None:
    with pytest.raises(ValueError):
        _paid_proposal(problem="نضمن لك مبيعات مضمونة")


def test_proposal_approve_reject() -> None:
    p = _paid_proposal()
    assert proposal.approve_proposal(p.id).approval_status == "approved"
    p2 = _paid_proposal(quote_id="quote_pros_2")
    assert proposal.reject_proposal(p2.id).approval_status == "rejected"


# ── payment handoff ──────────────────────────────────────────────────────────


def test_handoff_requires_all_six_local_approvals_after_quote_authority() -> None:
    h = _authorized_handoff()
    assert h.status == PaymentHandoffStatus.PENDING_APPROVAL.value
    assert h.governance_status == "requires_founder_approval"
    assert h.price_authority == "customer_specific_quote_after_qualified_discovery"
    assert h.public_fixed_price is False
    assert h.live_charge_allowed is False
    assert h.external_send_allowed is False
    assert len(h.quote_fingerprint) == 64
    assert h.quote_authority_ref
    keys = [
        "proposal_approved",
        "scope_confirmed",
        "price_confirmed",
        "decision_maker_confirmed",
        "risk_reviewed",
    ]
    for k in keys:
        h = payment_handoff.set_approval(h.id, k, True)
        assert h.status == PaymentHandoffStatus.PENDING_APPROVAL.value
    h = payment_handoff.set_approval(h.id, "founder_approved", True)
    assert h.status == PaymentHandoffStatus.APPROVED.value
    assert h.governance_status == "approved"


def test_handoff_requires_complete_quote_authority_evidence() -> None:
    with pytest.raises(ValueError, match="discovery_ref"):
        _authorized_handoff(discovery_ref="")
    with pytest.raises(ValueError, match="quote_id"):
        _authorized_handoff(quote_id="")
    with pytest.raises(ValueError, match="quote_authority_ref"):
        _authorized_handoff(quote_authority_ref="")
    with pytest.raises(ValueError, match="customer_specific_scope_ref"):
        _authorized_handoff(customer_specific_scope_ref="")
    with pytest.raises(ValueError, match="invalid_customer_specific_quote_amount"):
        _authorized_handoff(amount_sar=0)


def test_handoff_rejects_nonexistent_or_unapproved_proposal() -> None:
    with pytest.raises(ValueError, match="existing_proposal"):
        payment_handoff.prepare_handoff(
            proposal_id="prop_missing",
            customer_id="pros_1",
            product_id="prod_sprint_v1",
            discovery_ref="discovery:pros-1",
            quote_id="quote_pros_1",
            quote_authority_ref="apr_missing",
            customer_specific_scope_ref="scope:pros-1",
            amount_sar=12500,
        )

    p = _paid_proposal()
    authority_ref = _approved_quote_authority(
        lead_id=p.prospect_id,
        amount_sar=12500,
        discovery_ref=p.discovery_ref,
        scope_ref="scope:pros-1",
    )
    with pytest.raises(ValueError, match="approved_proposal"):
        payment_handoff.prepare_handoff(
            proposal_id=p.id,
            customer_id=p.prospect_id,
            product_id=p.product_id,
            discovery_ref=p.discovery_ref,
            quote_id=p.quote_id,
            quote_authority_ref=authority_ref,
            customer_specific_scope_ref="scope:pros-1",
            amount_sar=12500,
        )


def test_handoff_rejects_forged_customer_amount_and_quote_authority() -> None:
    with pytest.raises(ValueError, match="customer_mismatch"):
        _authorized_handoff(customer_id="invented-customer")
    with pytest.raises(ValueError, match="amount_mismatch"):
        _authorized_handoff(amount_sar=12000)
    with pytest.raises(ValueError, match="quote_authority_not_found"):
        _authorized_handoff(quote_authority_ref="apr_invented")


def test_handoff_rejects_quote_fingerprint_substitution() -> None:
    p = _paid_proposal()
    proposal.approve_proposal(p.id)
    wrong_authority = _approved_quote_authority(
        lead_id=p.prospect_id,
        amount_sar=13000,
        discovery_ref=p.discovery_ref,
        scope_ref="scope:pros-1",
    )
    with pytest.raises(ValueError, match="fingerprint_mismatch"):
        payment_handoff.prepare_handoff(
            proposal_id=p.id,
            customer_id=p.prospect_id,
            product_id=p.product_id,
            discovery_ref=p.discovery_ref,
            quote_id=p.quote_id,
            quote_authority_ref=wrong_authority,
            customer_specific_scope_ref="scope:pros-1",
            amount_sar=12500,
        )


def test_free_diagnostic_has_no_payment_handoff() -> None:
    with pytest.raises(ValueError, match="free_diagnostic_has_no_payment_handoff"):
        payment_handoff.prepare_handoff(
            proposal_id="x",
            customer_id="x",
            product_id="prod_diagnostic_v1",
            discovery_ref="discovery:x",
            quote_id="quote_x",
            quote_authority_ref="apr_x",
            customer_specific_scope_ref="scope:x",
            amount_sar=1,
        )


def test_handoff_rejects_unknown_product_and_missing_proposal_id() -> None:
    with pytest.raises(ValueError, match="proposal_id"):
        payment_handoff.prepare_handoff(
            proposal_id="",
            customer_id="c",
            product_id="prod_sprint_v1",
            discovery_ref="discovery:c",
            quote_id="quote_c",
            quote_authority_ref="apr_c",
            customer_specific_scope_ref="scope:c",
            amount_sar=12500,
        )
    with pytest.raises(ValueError, match="unknown_product"):
        payment_handoff.prepare_handoff(
            proposal_id="x",
            customer_id="c",
            product_id="nope",
            discovery_ref="discovery:c",
            quote_id="quote_c",
            quote_authority_ref="apr_c",
            customer_specific_scope_ref="scope:c",
            amount_sar=12500,
        )


def test_handoff_has_no_charge_capability() -> None:
    public = set(payment_handoff.__all__)
    assert not any(
        w in name.lower() for name in public for w in ("charge", "send", "link", "moyasar")
    )


def test_set_unknown_approval_raises() -> None:
    h = _authorized_handoff()
    with pytest.raises(ValueError):
        payment_handoff.set_approval(h.id, "wishful_thinking", True)


# ── delivery handoff ─────────────────────────────────────────────────────────


def test_delivery_handoff_requires_success_metric_and_valid_product() -> None:
    with pytest.raises(ValueError):
        delivery_handoff.create_handoff(
            customer_id="c", product_sold="prod_sprint_v1", success_metric=""
        )
    with pytest.raises(ValueError):
        delivery_handoff.create_handoff(customer_id="c", product_sold="nope", success_metric="x")
    h = delivery_handoff.create_handoff(
        customer_id="c",
        product_sold="prod_sprint_v1",
        success_metric="reply rate up",
        first_workflow="followups",
    )
    assert h.status == "queued"
    assert delivery_handoff.update_status(h.id, "active").status == "active"