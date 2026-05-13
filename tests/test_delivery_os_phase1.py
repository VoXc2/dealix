"""Phase-1 Delivery OS smoke tests — happy-path coverage for the new modules.

اختبارات تدخين Phase 1 — تغطية المسار السعيد للوحدات الجديدة.

These tests guard the contract relied on by the 3 runnable demos and the
verify_company_ready.py script. They use only the in-memory event store, no
external services, so they run in any CI environment.
"""
from __future__ import annotations

import pytest

pytest.importorskip("pydantic", reason="pydantic required for Phase-1 OS modules")


def test_intake_happy_path():
    from auto_client_acquisition.delivery_factory.client_intake import (
        CustomerTier,
        IntakeRequest,
        StartingOffer,
        Vertical,
        process_intake,
    )

    intake = IntakeRequest(
        company_name_ar="شركة الاختبار",
        vertical=Vertical.BFSI,
        tier=CustomerTier.MID_MARKET,
        primary_pain_ar="بيانات مبعثرة.",
        requested_offer=StartingOffer.REVENUE_INTELLIGENCE,
        contact_name="اختبار",
        contact_role="CEO",
        contact_email="t@ex.sa",
        pdpl_acknowledged=True,
        commercial_registration="1234567890",
    )
    res = process_intake(intake)
    assert res.accepted
    assert res.matched_offer == StartingOffer.REVENUE_INTELLIGENCE
    assert res.estimated_price_sar == 9_500
    assert res.estimated_duration_days == 10


def test_intake_pdpl_gate_blocks():
    from auto_client_acquisition.delivery_factory.client_intake import (
        CustomerTier,
        IntakeRequest,
        StartingOffer,
        Vertical,
        process_intake,
    )

    intake = IntakeRequest(
        company_name_ar="شركة الاختبار",
        vertical=Vertical.RETAIL_ECOMM,
        tier=CustomerTier.SME,
        primary_pain_ar="...",
        requested_offer=StartingOffer.AI_QUICK_WIN,
        contact_name="ت",
        contact_role="CEO",
        contact_email="t@ex.sa",
        pdpl_acknowledged=False,
    )
    res = process_intake(intake)
    assert not res.accepted
    assert "PDPL" in (res.rejection_reason_en or "")


def test_scope_builder_pricing():
    from auto_client_acquisition.delivery_factory.client_intake import (
        CustomerTier,
        IntakeRequest,
        StartingOffer,
        Vertical,
        process_intake,
    )
    from auto_client_acquisition.delivery_factory.scope_builder import build_scope

    intake = IntakeRequest(
        company_name_ar="ش",
        vertical=Vertical.HEALTHCARE,
        tier=CustomerTier.MID_MARKET,
        primary_pain_ar="...",
        requested_offer=StartingOffer.COMPANY_BRAIN,
        contact_name="ت",
        contact_role="CEO",
        contact_email="t@ex.sa",
        pdpl_acknowledged=True,
        commercial_registration="1010088888",
    )
    res = process_intake(intake)
    sow = build_scope(intake, res)
    assert sow.price_sar == 20_000
    assert sow.vat_sar == 3_000
    assert sow.total_sar == 23_000
    assert sow.duration_days == 21
    assert len(sow.deliverables) >= 6


def test_qa_quality_floor():
    from auto_client_acquisition.delivery_factory.qa_review import (
        QUALITY_FLOOR,
        QualityScore,
        build_blank_gates,
        evaluate,
    )

    gates = build_blank_gates()
    for g in gates:
        for c in g.checks:
            c.passed = True

    # Score below floor → ships=False
    low = QualityScore(
        business_impact=10,
        data_quality=10,
        output_quality_ar_en=10,
        customer_usability=5,
        safety_compliance=10,
        productization=10,
        retainer_upgradeability=5,
    )
    rep_low = evaluate("prj_x", gates, low, reviewer="test")
    assert rep_low.score.total < QUALITY_FLOOR
    assert not rep_low.ships

    # Score above floor + all gates pass → ships=True
    high = QualityScore(
        business_impact=18,
        data_quality=14,
        output_quality_ar_en=13,
        customer_usability=9,
        safety_compliance=14,
        productization=12,
        retainer_upgradeability=8,
    )
    rep_high = evaluate("prj_x", gates, high, reviewer="test")
    assert rep_high.score.total >= QUALITY_FLOOR
    assert rep_high.ships


def test_lead_scoring_rationale_present():
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    record = {
        "vertical": "bfsi",
        "headcount": 250,
        "annual_revenue_sar": 300_000_000,
        "triggers": ["funding", "tender"],
        "data_quality_score": 88,
    }
    ls = score_account(record)
    assert ls.band in ("A", "B", "C", "D")
    assert 0 <= ls.score <= 100
    # Every feature has a rationale
    assert all(f.rationale_en for f in ls.features)


def test_forbidden_claims_block():
    from dealix.trust.forbidden_claims import assert_clean, scan_text

    assert scan_text("regular professional message").has_forbidden is False
    assert scan_text("we guarantee results").has_forbidden is True
    assert scan_text("نضمن لك نتائج").has_forbidden is True
    with pytest.raises(ValueError):
        assert_clean("we are the best in saudi with risk-free guarantee")


def test_stage_machine_no_skip():
    from auto_client_acquisition.delivery_factory.stage_machine import (
        Stage,
        TransitionError,
        start_project,
        transition,
    )

    state = start_project(actor="ceo")
    # Skipping a stage is not allowed
    with pytest.raises(TransitionError):
        transition(state, Stage.BUILD, actor="ceo")
    # Validate -> Deliver requires ships=True
    state = transition(state, Stage.DIAGNOSE, actor="ceo")
    state = transition(state, Stage.DESIGN, actor="ceo")
    state = transition(state, Stage.BUILD, actor="ceo")
    state = transition(state, Stage.VALIDATE, actor="ceo")
    with pytest.raises(TransitionError):
        transition(state, Stage.DELIVER, actor="ceo", ships=False)
    state = transition(state, Stage.DELIVER, actor="ceo", ships=True)
    assert state.current_stage == Stage.DELIVER
    assert state.ships is True


def test_roi_calculator_scenarios():
    from auto_client_acquisition.revenue_os.roi_calculator import (
        ROIInputs,
        compute_all,
    )

    results = compute_all(ROIInputs())
    assert set(results) == {"conservative", "mid", "optimistic"}
    # Optimistic should beat conservative on every metric
    c = results["conservative"]
    o = results["optimistic"]
    assert o.total_annual_value_sar >= c.total_annual_value_sar
    assert o.annual_revenue_uplift_sar >= c.annual_revenue_uplift_sar
    # All scenarios should have positive ROI multiple if inputs are non-trivial
    assert results["mid"].roi_multiple > 0
