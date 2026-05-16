"""Tests for the governed-revenue service catalog pricing modes."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_client_acquisition.service_catalog.registry import (
    get_offering,
    list_offerings,
)
from auto_client_acquisition.service_catalog.schemas import ServiceOffering


def test_diagnostic_is_a_range_4999_to_25000() -> None:
    diagnostic = get_offering("governed_revenue_ops_diagnostic")
    assert diagnostic is not None
    assert diagnostic.price_mode == "range"
    assert diagnostic.price_sar_min == 4999.0
    assert diagnostic.price_sar_max == 25000.0
    # `price_sar` stays valid (equal to the min) so consumers do not break.
    assert diagnostic.price_sar == 4999.0


def test_sprint_and_retainer_are_recommended_draft() -> None:
    for service_id in ("revenue_intelligence_sprint", "governed_ops_retainer"):
        offering = get_offering(service_id)
        assert offering is not None
        assert offering.price_mode == "recommended_draft"
        assert offering.price_mode != "fixed"
        assert offering.price_sar == 0.0


def test_every_offering_is_an_estimate() -> None:
    offerings = list_offerings()
    assert len(offerings) == 7
    for o in offerings:
        assert o.is_estimate is True, f"{o.id} must be is_estimate=True"


def test_only_diagnostic_uses_range_mode() -> None:
    for o in list_offerings():
        if o.id == "governed_revenue_ops_diagnostic":
            assert o.price_mode == "range"
        else:
            assert o.price_mode == "recommended_draft"


def test_range_mode_requires_min_and_max() -> None:
    with pytest.raises(ValidationError):
        ServiceOffering(
            id="bad_range",
            name_ar="نطاق غير صالح",
            name_en="Bad Range",
            price_sar=100.0,
            price_mode="range",  # missing min/max
            duration_days=1,
            deliverables=("x",),
            kpi_commitment_ar="x",
            kpi_commitment_en="x",
            refund_policy_ar="x",
            refund_policy_en="x",
            action_modes_used=("draft_only",),
            hard_gates=("no_live_send",),
            customer_journey_stage="discovery",
        )


def test_range_mode_rejects_min_greater_than_max() -> None:
    with pytest.raises(ValidationError):
        ServiceOffering(
            id="bad_range2",
            name_ar="نطاق مقلوب",
            name_en="Inverted Range",
            price_sar=100.0,
            price_mode="range",
            price_sar_min=500.0,
            price_sar_max=100.0,
            duration_days=1,
            deliverables=("x",),
            kpi_commitment_ar="x",
            kpi_commitment_en="x",
            refund_policy_ar="x",
            refund_policy_en="x",
            action_modes_used=("draft_only",),
            hard_gates=("no_live_send",),
            customer_journey_stage="discovery",
        )
