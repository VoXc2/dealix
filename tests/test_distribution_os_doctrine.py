"""Doctrine guards for the Distribution OS compatibility layer.

The layer may prepare drafts/proposals/handoffs internally but cannot send,
charge, scrape, invent a price, or grant commercial authority from the legacy
catalog. Paid proposals and payment handoffs require explicit discovery +
customer-specific quote evidence.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.distribution_os import (
    catalog,
    delivery_handoff,
    draft_factory,
    payment_handoff,
    proposal,
    prospect,
)
from auto_client_acquisition.distribution_os.draft_factory import DraftStatus, DraftType

_FORBIDDEN_VERBS = ("send", "charge", "scrape", "automate", "blast", "moyasar", "link")


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    for var, name in (
        ("DEALIX_PROSPECTS_PATH", "prospects.jsonl"),
        ("DEALIX_DRAFTS_PATH", "drafts.jsonl"),
        ("DEALIX_PROPOSALS_PATH", "proposals.jsonl"),
        ("DEALIX_PAYMENT_HANDOFFS_PATH", "pay.jsonl"),
        ("DEALIX_DELIVERY_HANDOFFS_PATH", "deliv.jsonl"),
    ):
        monkeypatch.setenv(var, str(tmp_path / name))
    approvals = get_default_approval_store()
    approvals.clear()
    yield
    approvals.clear()


def _prospect(**over):
    base = {
        "company": "Acme",
        "sector": "marketing_agencies",
        "pain_hypothesis": "leaks",
        "offer_angle": "prod_sprint_v1",
        "preferred_channel": "email",
        "risk": "low",
    }
    base.update(over)
    return prospect.add_prospect(**base)


def _authorized_payment_handoff():
    discovery_ref = "discovery:c-001"
    scope_ref = "scope:c-001"
    quote_id = "quote_c_001"
    amount = 12500
    prop = proposal.generate_proposal(
        prospect_id="c",
        product_id="prod_sprint_v1",
        out_of_scope=["external send"],
        discovery_ref=discovery_ref,
        quote_id=quote_id,
        customer_specific_quote_sar=amount,
    )
    proposal.approve_proposal(prop.id)
    fingerprint = payment_handoff._quote_authority_fingerprint(
        lead_id=prop.prospect_id,
        amount_sar=amount,
        discovery_ref=discovery_ref,
        customer_specific_scope_ref=scope_ref,
    )
    approvals = get_default_approval_store()
    req = ApprovalRequest(
        object_type="customer_specific_quote",
        object_id=fingerprint,
        action_type="customer_specific_quote",
        action_mode="approval_required",
        channel="finance_manual",
        risk_level="high",
        proof_impact=f"customer_specific_quote:{fingerprint}",
        action_id=f"quote:{fingerprint}",
        lead_id=prop.prospect_id,
        audit_ref=discovery_ref,
        proof_target=f"invoice_authority:{fingerprint}",
    )
    stored = approvals.create(req)
    approvals.approve(stored.approval_id, "founder-test")
    return payment_handoff.prepare_handoff(
        proposal_id=prop.id,
        customer_id=prop.prospect_id,
        product_id=prop.product_id,
        discovery_ref=discovery_ref,
        quote_id=quote_id,
        quote_authority_ref=stored.approval_id,
        customer_specific_scope_ref=scope_ref,
        amount_sar=amount,
    )


def test_no_external_send_capability_in_any_submodule() -> None:
    for module in (draft_factory, proposal, payment_handoff, delivery_handoff):
        for name in module.__all__:
            lowered = name.lower()
            assert not any(verb in lowered for verb in _FORBIDDEN_VERBS), (
                f"{module.__name__}.{name}"
            )


def test_every_generated_draft_carries_a_governance_status() -> None:
    p = _prospect()
    for dtype in DraftType:
        d = draft_factory.generate_draft(prospect=p, draft_type=dtype)
        assert d.governance_status in {"pending_approval", "needs_edit", "blocked"}
        assert d.status == d.governance_status


def test_no_draft_is_ever_auto_sent_on_generation() -> None:
    p = _prospect()
    d = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FIRST)
    assert d.status != DraftStatus.SENT_VIA_INTEGRATION.value
    assert d.status != DraftStatus.APPROVED.value


def test_guaranteed_claim_draft_cannot_reach_approved() -> None:
    bad = _prospect(company="B", pain_hypothesis="نضمن لك نتائج مبيعات مضمونة 100%")
    d = draft_factory.generate_draft(prospect=bad, draft_type=DraftType.DIAGNOSTIC_SUMMARY)
    assert d.governance_status == "blocked"
    with pytest.raises(ValueError):
        draft_factory.approve_draft(d.id)


def test_legacy_catalog_never_grants_paid_price_authority() -> None:
    free = catalog.product_by_id("prod_diagnostic_v1")
    assert free is not None
    assert catalog.price_band(free.id) == (0, 0)

    for product in catalog.all_products():
        if product.id == free.id:
            continue
        assert product.quote_required is True
        assert product.price_authorized is False
        with pytest.raises(PermissionError, match="CUSTOMER_SPECIFIC_QUOTE_REQUIRED"):
            catalog.price_band(product.id)


def test_paid_proposal_requires_customer_specific_quote_evidence() -> None:
    with pytest.raises(ValueError, match="discovery_ref"):
        proposal.generate_proposal(
            prospect_id="p",
            product_id="prod_sprint_v1",
            out_of_scope=["external send"],
        )

    prop = proposal.generate_proposal(
        prospect_id="p",
        product_id="prod_sprint_v1",
        out_of_scope=["external send"],
        discovery_ref="discovery:p-001",
        quote_id="quote_p_001",
        customer_specific_quote_sar=12500,
    )
    assert prop.price_min_sar == 12500
    assert prop.price_max_sar == 12500
    assert prop.public_fixed_price is False
    assert prop.external_send_allowed is False


def test_off_catalog_product_cannot_produce_proposal_or_handoff() -> None:
    with pytest.raises(ValueError):
        proposal.generate_proposal(
            prospect_id="p",
            product_id="prod_imaginary",
            out_of_scope=["x"],
        )
    with pytest.raises(ValueError):
        payment_handoff.prepare_handoff(
            proposal_id="x",
            customer_id="c",
            product_id="prod_imaginary",
            discovery_ref="discovery:x",
            quote_id="quote_x",
            amount_sar=10000,
        )


def test_payment_handoff_defaults_to_requiring_founder_approval() -> None:
    h = _authorized_payment_handoff()
    assert h.governance_status == "requires_founder_approval"
    assert h.approvals["founder_approved"] is False
    assert h.live_charge_allowed is False
    assert h.external_send_allowed is False
    assert h.public_fixed_price is False
    assert h.quote_authority_ref
    assert len(h.quote_fingerprint) == 64