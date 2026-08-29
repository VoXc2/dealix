from __future__ import annotations

import pytest

from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier
from auto_client_acquisition.distribution_os.catalog import ladder_summary, price_band


def test_legacy_paid_catalog_has_no_price_authority() -> None:
    for tier in (
        ProductTier.SPRINT,
        ProductTier.DATA_PACK,
        ProductTier.MANAGED_OPS,
        ProductTier.CUSTOM_AI,
    ):
        product = PRODUCT_CATALOG[tier]
        assert product.price_sar == 0
        assert product.price_max_sar == 0
        assert product.active_offer is False
        assert product.quote_required is True
        assert product.price_authorized is False
        assert product.delivery_authorized is False
        assert product.commercial_authority == "RETIRED_COMPATIBILITY_NOT_OFFER_AUTHORITY"


def test_legacy_catalog_adapter_cannot_quote_paid_tier() -> None:
    with pytest.raises(PermissionError, match="CUSTOMER_SPECIFIC_QUOTE_REQUIRED"):
        price_band("prod_sprint_v1")
    assert price_band("prod_diagnostic_v1") == (0, 0)


def test_ladder_summary_hides_paid_prices_and_delivery_commitments() -> None:
    rows = ladder_summary()
    paid = [row for row in rows if row["tier"] != ProductTier.FREE_DIAGNOSTIC.value]
    assert paid
    assert all(row["price_min_sar"] is None for row in paid)
    assert all(row["price_max_sar"] is None for row in paid)
    assert all(row["delivery_days"] is None for row in paid)
    assert all(row["active_offer"] is False for row in paid)


def test_proposal_builder_never_renders_legacy_price_or_delivery() -> None:
    from autonomous_growth.agents.proposal_sender import ProposalSenderAgent

    product = PRODUCT_CATALOG[ProductTier.SPRINT]
    body_en = ProposalSenderAgent._build_body_en(
        product=product,
        lead_name="Example Buyer",
        company="Example Co",
        pain_text="handoff friction",
        cta_url="",
    )
    body_ar = ProposalSenderAgent._build_body_ar(
        product=product,
        lead_name="عميل تجريبي",
        company="شركة تجريبية",
        pain_text="مشكلة في التسليم بين الفرق",
        cta_url="",
    )
    combined = f"{body_en}\n{body_ar}".lower()
    assert "499" not in combined
    assert "7-day" not in combined
    assert "14-day" not in combined
    assert "price:" not in combined
    assert "**السعر:**" not in combined
    assert "delivery:" not in combined
    assert "free mini diagnostic" in combined
