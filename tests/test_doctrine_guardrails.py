"""Doctrine guardrails for governed commercial paths."""

from __future__ import annotations

import pytest

from auto_client_acquisition.safe_send_gateway import (
    doctrine_violations_for_revenue_intelligence,
    enforce_doctrine_non_negotiables,
)


def test_doctrine_clean() -> None:
    codes, _reasons = doctrine_violations_for_revenue_intelligence()
    assert codes == ()
    enforce_doctrine_non_negotiables()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"request_cold_whatsapp": True},
        {"request_linkedin_automation": True},
        {"request_scraping": True},
        {"request_bulk_outreach": True},
        {"request_guaranteed_sales_claim": True},
        {"request_fake_proof": True},
        {"request_external_send_without_approval": True},
    ],
)
def test_doctrine_blocks(kwargs: dict) -> None:
    codes, reasons = doctrine_violations_for_revenue_intelligence(**kwargs)
    assert len(codes) >= 1
    assert all(c in reasons for c in codes)
    with pytest.raises(ValueError):
        enforce_doctrine_non_negotiables(**kwargs)


def test_doctrine_multi_violation() -> None:
    codes, _r = doctrine_violations_for_revenue_intelligence(
        request_cold_whatsapp=True,
        request_scraping=True,
    )
    assert "no_cold_whatsapp" in codes
    assert "no_scraping" in codes


def test_doctrine_reasons_bilingual() -> None:
    _codes, reasons = doctrine_violations_for_revenue_intelligence(request_linkedin_automation=True)
    r = reasons["no_linkedin_automation"]
    assert "ar" in r and "en" in r


def test_doctrine_guaranteed_sales() -> None:
    c, _ = doctrine_violations_for_revenue_intelligence(request_guaranteed_sales_claim=True)
    assert c == ("no_guaranteed_sales_claims",)


def test_doctrine_fake_proof() -> None:
    c, _ = doctrine_violations_for_revenue_intelligence(request_fake_proof=True)
    assert c == ("no_fake_proof",)


def test_doctrine_external_without_approval() -> None:
    c, _ = doctrine_violations_for_revenue_intelligence(request_external_send_without_approval=True)
    assert c == ("external_action_requires_approval",)
