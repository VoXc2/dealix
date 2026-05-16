"""The 11 codified non-negotiables — 7 outreach/claims + 4 proof-progression."""

from __future__ import annotations

import pytest

from auto_client_acquisition.proof_engine.evidence import (
    EvidenceLevel,
    assert_public_proof_allowed,
)
from auto_client_acquisition.safe_send_gateway import (
    doctrine_violations_for_revenue_intelligence,
    enforce_doctrine_non_negotiables,
)

ALL_11 = (
    "no_cold_whatsapp",
    "no_linkedin_automation",
    "no_scraping",
    "no_bulk_outreach",
    "no_guaranteed_sales_claims",
    "no_fake_proof",
    "external_action_requires_approval",
    "no_revenue_before_invoice_paid",
    "no_l5_before_meeting",
    "no_l7_confirmed_before_payment",
    "no_unconsented_public_proof",
)


def test_clean_request_raises_nothing() -> None:
    codes, _ = doctrine_violations_for_revenue_intelligence()
    assert codes == ()
    enforce_doctrine_non_negotiables()


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"request_revenue_before_invoice_paid": True}, "no_revenue_before_invoice_paid"),
        ({"request_l5_before_meeting": True}, "no_l5_before_meeting"),
        ({"request_l7_confirmed_before_payment": True}, "no_l7_confirmed_before_payment"),
        ({"request_unconsented_public_proof": True}, "no_unconsented_public_proof"),
    ],
)
def test_new_non_negotiables_block(kwargs: dict, expected: str) -> None:
    codes, reasons = doctrine_violations_for_revenue_intelligence(**kwargs)
    assert expected in codes
    assert "ar" in reasons[expected] and "en" in reasons[expected]
    with pytest.raises(ValueError):
        enforce_doctrine_non_negotiables(**kwargs)


def test_all_eleven_codes_reachable() -> None:
    codes, _ = doctrine_violations_for_revenue_intelligence(
        request_cold_whatsapp=True,
        request_linkedin_automation=True,
        request_scraping=True,
        request_bulk_outreach=True,
        request_guaranteed_sales_claim=True,
        request_fake_proof=True,
        request_external_send_without_approval=True,
        request_revenue_before_invoice_paid=True,
        request_l5_before_meeting=True,
        request_l7_confirmed_before_payment=True,
        request_unconsented_public_proof=True,
    )
    assert set(codes) == set(ALL_11)
    assert len(codes) == 11


def test_unconsented_public_proof_guard_in_evidence_module() -> None:
    # L4 reached but no consent → blocked.
    with pytest.raises(ValueError):
        assert_public_proof_allowed(EvidenceLevel.L4_PUBLIC_APPROVED, consent_public=False)
    # L4 + consent → allowed.
    assert_public_proof_allowed(EvidenceLevel.L4_PUBLIC_APPROVED, consent_public=True)


def test_existing_callers_unaffected() -> None:
    # Old 7-arg call signature still works with defaults.
    enforce_doctrine_non_negotiables(
        request_cold_whatsapp=False,
        request_linkedin_automation=False,
        request_scraping=False,
        request_bulk_outreach=False,
        request_guaranteed_sales_claim=False,
        request_fake_proof=False,
        request_external_send_without_approval=False,
    )
