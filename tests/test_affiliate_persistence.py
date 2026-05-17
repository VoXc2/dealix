"""Affiliate / Partner Commission Machine — store persistence + scoring."""
from __future__ import annotations

import pytest

from auto_client_acquisition.partnership_os import affiliate_store as store


@pytest.fixture(autouse=True)
def _isolated_store(tmp_path, monkeypatch):
    for env_var in store._PATH_DEFAULTS:
        monkeypatch.setenv(env_var, str(tmp_path / f"{env_var}.jsonl"))
    store.clear_for_test()
    yield
    store.clear_for_test()


def _approved_partner(**signals) -> store.AffiliatePartner:
    partner = store.apply_partner(
        display_name="Acme Consulting",
        email="partner@acme.sa",
        partner_category="consultant",
        plan_text="I run a B2B newsletter and will share Dealix monthly with disclosure.",
        disclosure_accepted=True,
        score_signals=signals or {"audience_is_b2b": True, "audience_is_gcc": True},
    )
    result = store.approve_partner(partner_id=partner.partner_id)
    assert result is not None
    return result[0]


def test_score_partner_additive_weights():
    score, breakdown = store.score_partner(
        audience_is_b2b=True,
        audience_is_gcc=True,
        is_consultant_operator=True,
        has_prior_referrals=True,
        content_quality_good=True,
        trusted_brand=True,
        disclosure_accepted=True,
    )
    assert score == 16
    assert breakdown["audience_is_b2b"] == 4
    assert "no_disclosure" not in breakdown


def test_score_partner_penalties():
    score, breakdown = store.score_partner(
        audience_is_b2b=True,
        spam_history=True,
        fake_audience_suspected=True,
        disclosure_accepted=False,
        plan_is_vague=True,
    )
    # +4 -5 -4 -3 (no_disclosure) -3 (vague_plan) = -11
    assert score == -11
    assert breakdown["no_disclosure"] == -3


def test_tier_from_score_thresholds():
    assert store.tier_from_score(16) == "tier3"
    assert store.tier_from_score(7) == "tier2"
    assert store.tier_from_score(3) == "tier1"
    assert store.tier_from_score(0) == ""


def test_apply_partner_persists_and_scores():
    partner = store.apply_partner(
        display_name="Beta Agency",
        email="hi@beta.sa",
        partner_category="agency",
        plan_text="We resell revenue ops services to GCC founders, disclosed.",
        disclosure_accepted=True,
        score_signals={"audience_is_b2b": True, "audience_is_gcc": True},
    )
    assert partner.partner_id.startswith("apt_")
    assert partner.status == store.PartnerStatus.SCORED.value
    assert store.get_partner(partner.partner_id) is not None


def test_apply_requires_display_name():
    with pytest.raises(ValueError):
        store.apply_partner(display_name="  ", email="x@y.sa")


def test_approve_partner_issues_link():
    partner = store.apply_partner(
        display_name="Gamma", email="g@gamma.sa", disclosure_accepted=True,
        plan_text="GCC operator community, will disclose every referral link.",
    )
    result = store.approve_partner(partner_id=partner.partner_id, tier="tier2")
    assert result is not None
    approved, link = result
    assert approved.status == store.PartnerStatus.APPROVED.value
    assert approved.tier == "tier2"
    assert link.code.startswith("APT-")
    assert store.get_link(link.code) is not None


def test_submit_referral_records_lead():
    partner = _approved_partner()
    link = store.list_links(partner_id=partner.partner_id)[0]
    referral = store.submit_referral(
        code=link.code, lead_company="Prospect Co", lead_email="buyer@prospect.sa"
    )
    assert referral.affiliate_referral_id.startswith("afr_")
    assert referral.status == store.AffiliateReferralStatus.SUBMITTED.value
    assert referral.partner_id == partner.partner_id


def test_submit_referral_is_idempotent_on_duplicate_lead():
    partner = _approved_partner()
    link = store.list_links(partner_id=partner.partner_id)[0]
    r1 = store.submit_referral(
        code=link.code, lead_company="Dup Co", lead_email="same@dup.sa"
    )
    r2 = store.submit_referral(
        code=link.code, lead_company="Dup Co", lead_email="same@dup.sa"
    )
    assert r1.affiliate_referral_id == r2.affiliate_referral_id
    events = store.list_compliance_events(partner_id=partner.partner_id)
    assert any(e.event_type == "duplicate_lead" for e in events)


def test_submit_referral_rejects_self_referral():
    partner = _approved_partner()
    link = store.list_links(partner_id=partner.partner_id)[0]
    with pytest.raises(ValueError):
        store.submit_referral(
            code=link.code, lead_company="Self", lead_email="partner@acme.sa"
        )
    events = store.list_compliance_events(partner_id=partner.partner_id)
    assert any(e.event_type == "self_referral" for e in events)


def test_submit_referral_rejects_unknown_code():
    with pytest.raises(ValueError):
        store.submit_referral(code="APT-NOPE", lead_company="X", lead_email="x@y.sa")


def test_suspended_partner_cannot_submit():
    partner = _approved_partner()
    link = store.list_links(partner_id=partner.partner_id)[0]
    store.suspend_partner(partner_id=partner.partner_id, reason="spam reports")
    with pytest.raises(ValueError):
        store.submit_referral(
            code=link.code, lead_company="X", lead_email="x@y.sa"
        )


def test_partner_isolation_in_listings():
    p1 = _approved_partner()
    p2 = store.apply_partner(
        display_name="Other", email="o@other.sa", disclosure_accepted=True,
        plan_text="Independent operator covering GCC SaaS, discloses links.",
    )
    assert {x.partner_id for x in store.list_partners()} >= {p1.partner_id, p2.partner_id}
    assert store.list_referrals(partner_id=p2.partner_id) == []
