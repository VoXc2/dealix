"""Referral program JSONL persistence — Wave 14D.1."""
from __future__ import annotations

import pytest

from auto_client_acquisition.partnership_os.referral_store import (
    REFERRER_CREDIT_SAR,
    ReferralStatus,
    clear_for_test,
    create_referral_code,
    issue_credit,
    list_codes_by_referrer,
    list_referrals,
    lookup_code,
    mark_invoice_paid,
    redeem_referral,
    revoke_code,
)


@pytest.fixture(autouse=True)
def _isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_REFERRAL_CODES_PATH", str(tmp_path / "codes.jsonl"))
    monkeypatch.setenv("DEALIX_REFERRALS_PATH", str(tmp_path / "refs.jsonl"))
    monkeypatch.setenv("DEALIX_REFERRAL_PAYOUTS_PATH", str(tmp_path / "payouts.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_create_and_lookup_code():
    rc = create_referral_code(referrer_id="acme", referrer_email="ceo@acme.sa")
    assert rc.code.startswith("REF-")
    assert rc.referrer_id == "acme"
    looked = lookup_code(rc.code)
    assert looked is not None
    assert looked.code == rc.code


def test_create_requires_referrer_id():
    with pytest.raises(ValueError):
        create_referral_code(referrer_id="")


def test_revoke_code_invalidates_lookup():
    rc = create_referral_code(referrer_id="acme")
    assert revoke_code(rc.code) is True
    assert lookup_code(rc.code) is None


def test_redeem_creates_referral():
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta_corp", referred_email="cto@beta.sa")
    assert r.status == ReferralStatus.REDEEMED.value
    assert r.referrer_id == "acme"
    assert r.referred_id == "beta_corp"


def test_redeem_idempotent():
    rc = create_referral_code(referrer_id="acme")
    r1 = redeem_referral(code=rc.code, referred_id="beta")
    r2 = redeem_referral(code=rc.code, referred_id="beta")
    assert r1.referral_id == r2.referral_id


def test_redeem_self_referral_blocked():
    rc = create_referral_code(referrer_id="acme")
    with pytest.raises(ValueError):
        redeem_referral(code=rc.code, referred_id="acme")


def test_full_lifecycle_to_credit_issued():
    rc = create_referral_code(referrer_id="acme")
    r = redeem_referral(code=rc.code, referred_id="beta")
    mark_invoice_paid(referral_id=r.referral_id, invoice_id="inv_001", amount_sar=2999)
    payout = issue_credit(referral_id=r.referral_id)
    assert payout is not None
    assert payout.credit_sar == REFERRER_CREDIT_SAR
    refs = list_referrals(referrer_id="acme")
    assert refs[0].status == ReferralStatus.CREDIT_ISSUED.value


def test_tenant_isolation_codes_by_referrer():
    create_referral_code(referrer_id="acme")
    create_referral_code(referrer_id="acme")
    create_referral_code(referrer_id="beta")
    acme_codes = list_codes_by_referrer("acme")
    beta_codes = list_codes_by_referrer("beta")
    assert len(acme_codes) == 2
    assert len(beta_codes) == 1
