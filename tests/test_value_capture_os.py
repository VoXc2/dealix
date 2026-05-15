"""Tests for value_capture_os."""

from __future__ import annotations

from auto_client_acquisition.value_capture_os import (
    TRACK_REVENUE_INTELLIGENCE,
    VALUE_CAPTURE_DASHBOARD_SIGNALS,
    ChangeRequestClass,
    ClientQualityDimensions,
    MonetizationOfferKind,
    ProofCommercialSignal,
    RevenueQualityDimensions,
    classify_change_request,
    client_quality_band,
    client_quality_score,
    gross_margin_meets_target,
    recommended_expansion_offer,
    revenue_quality_band,
    revenue_quality_score,
    upsell_from_proof_signal,
    value_capture_dashboard_coverage_score,
)


def test_revenue_quality_score() -> None:
    hi = RevenueQualityDimensions(90, 90, 90, 90, 90, 90)
    s = revenue_quality_score(hi)
    assert s == 90
    assert revenue_quality_band(s) == "excellent_revenue"


def test_client_quality_score() -> None:
    mid = ClientQualityDimensions(70, 70, 70, 70, 70, 70, 70)
    s = client_quality_score(mid)
    assert s == 70
    assert client_quality_band(s) == "good_client"


def test_gross_margin_targets() -> None:
    assert gross_margin_meets_target(MonetizationOfferKind.DIAGNOSTIC, 75.0)
    assert not gross_margin_meets_target(MonetizationOfferKind.DIAGNOSTIC, 74.0)
    assert gross_margin_meets_target(MonetizationOfferKind.SPRINT, 65.0)
    assert gross_margin_meets_target(MonetizationOfferKind.ENTERPRISE, 50.0)


def test_expansion_map() -> None:
    assert (
        recommended_expansion_offer(
            track=TRACK_REVENUE_INTELLIGENCE,
            current_stage="capability_diagnostic",
        )
        == "revenue_intelligence_sprint"
    )
    assert (
        recommended_expansion_offer(
            track=TRACK_REVENUE_INTELLIGENCE,
            current_stage="dealix_revenue_os",
        )
        is None
    )
    assert recommended_expansion_offer(track="unknown", current_stage="x") is None


def test_upsell_logic() -> None:
    assert (
        upsell_from_proof_signal(ProofCommercialSignal.DATA_ISSUES)
        == "data_readiness_retainer"
    )
    assert upsell_from_proof_signal("unknown") is None


def test_scope_control() -> None:
    assert (
        classify_change_request(
            in_written_scope=True,
            estimated_additional_hours=0.0,
            introduces_new_capability_outside_scope=False,
            aligns_with_retainer_backlog_item=False,
            requests_unapproved_outbound_execution=True,
        )
        is ChangeRequestClass.REJECTED
    )
    assert (
        classify_change_request(
            in_written_scope=True,
            estimated_additional_hours=1.0,
            introduces_new_capability_outside_scope=False,
            aligns_with_retainer_backlog_item=False,
            requests_unapproved_outbound_execution=False,
        )
        is ChangeRequestClass.MINOR_ADJUSTMENT
    )


def test_value_capture_dashboard() -> None:
    assert (
        value_capture_dashboard_coverage_score(frozenset(VALUE_CAPTURE_DASHBOARD_SIGNALS))
        == 100
    )
