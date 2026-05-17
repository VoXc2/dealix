"""Affiliate / Partner Commission Machine — doctrine guardrails.

Enforces the non-negotiables for the partner program:
  - No raw PII in storage (emails are hashed).
  - No guaranteed-outcome language in approved partner messaging.
  - Commission is gated strictly on a recorded invoice_paid event.
  - Every state change leaves a ledger trail.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.partnership_os import affiliate_store as store


@pytest.fixture(autouse=True)
def _isolated_store(tmp_path, monkeypatch):
    for env_var in store._PATH_DEFAULTS:
        monkeypatch.setenv(env_var, str(tmp_path / f"{env_var}.jsonl"))
    store.clear_for_test()
    yield
    store.clear_for_test()


def test_partner_email_is_never_stored_raw():
    raw_email = "ceo@secret-company.sa"
    partner = store.apply_partner(
        display_name="Secret Co",
        email=raw_email,
        disclosure_accepted=True,
        plan_text="GCC operator promoting Dealix with disclosure on every link.",
    )
    content = store._partners_path().read_text(encoding="utf-8")
    assert raw_email not in content
    assert partner.email_hash and len(partner.email_hash) == 16
    assert partner.email_hash != raw_email


def test_lead_email_is_never_stored_raw():
    partner = store.apply_partner(
        display_name="P", email="p@p.sa", disclosure_accepted=True,
        plan_text="GCC consultant promoting Dealix monthly with disclosure.",
    )
    store.approve_partner(partner_id=partner.partner_id, tier="tier1")
    link = store.list_links(partner_id=partner.partner_id)[0]
    lead_email = "buyer@lead-company.sa"
    store.submit_referral(
        code=link.code, lead_company="Lead Co", lead_email=lead_email
    )
    content = store._referrals_path().read_text(encoding="utf-8")
    assert lead_email not in content


def test_guaranteed_claims_blocked_for_partner_assets():
    # The /assets admin endpoint runs every partner asset through this gate.
    assert policy_check_draft("نضمن لك نتائج مبيعات خلال أسبوع").allowed is False
    assert policy_check_draft("We guarantee ROI in 30 days").allowed is False
    # Honest, source-bound partner copy passes.
    assert policy_check_draft(
        "Dealix runs governed revenue and AI workflows for GCC teams."
    ).allowed is True


def test_commission_requires_invoice_paid_event():
    partner = store.apply_partner(
        display_name="P", email="p@p.sa", disclosure_accepted=True,
        plan_text="GCC consultant promoting Dealix monthly with disclosure.",
    )
    store.approve_partner(partner_id=partner.partner_id, tier="tier2")
    link = store.list_links(partner_id=partner.partner_id)[0]
    referral = store.submit_referral(
        code=link.code, lead_company="Buyer", lead_email="b@b.sa"
    )
    # submitted, not even qualified — commission must be impossible.
    with pytest.raises(ValueError):
        store.calculate_commission(
            affiliate_referral_id=referral.affiliate_referral_id
        )


def test_payout_cannot_settle_unapproved_commission():
    partner = store.apply_partner(
        display_name="P", email="p@p.sa", disclosure_accepted=True,
        plan_text="GCC consultant promoting Dealix monthly with disclosure.",
    )
    store.approve_partner(partner_id=partner.partner_id, tier="tier2")
    link = store.list_links(partner_id=partner.partner_id)[0]
    referral = store.submit_referral(
        code=link.code, lead_company="Buyer", lead_email="b@b.sa"
    )
    store.qualify_referral(
        affiliate_referral_id=referral.affiliate_referral_id, disclosure_present=True
    )
    store.mark_invoice_paid(
        affiliate_referral_id=referral.affiliate_referral_id,
        invoice_id="inv_1",
        deal_amount_sar=5_000,
    )
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    with pytest.raises(ValueError):
        store.mark_payout_paid(
            partner_id=partner.partner_id,
            commission_ids=[commission.commission_id],
        )


def test_every_partner_mutation_leaves_a_ledger_trail():
    partner = store.apply_partner(
        display_name="Ledger Co", email="l@l.sa", disclosure_accepted=True,
        plan_text="GCC operator promoting Dealix with disclosure on every link.",
    )
    assert store._partners_path().exists()
    store.approve_partner(partner_id=partner.partner_id, tier="tier1")
    # The referral link issued on approval is appended to the links ledger.
    assert store.list_links(partner_id=partner.partner_id)
    assert store._links_path().read_text(encoding="utf-8").strip()
