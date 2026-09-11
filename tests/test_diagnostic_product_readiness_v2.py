"""Contracts for the readiness-complete universal free diagnostic product.

Every derived value is PATTERN or ESTIMATED. Internal events never count as
pipeline. D0-D2 stay genuinely free; deeper work is quote-only.
"""
from __future__ import annotations

import re

from dealix.commercial.low_touch_products.diagnostic_product import (
    QUOTE_REQUIRED,
    DiagnosticProductEngine,
    DiagnosticProductRequest,
)
from dealix.commercial.universal_diagnostic_factory import DiagnosticDepth

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
FAKE_ROI_RE = re.compile(
    r"will save \d+%|guaranteed \d+%|نضمن|ستوفر \d+٪|\d+٪\s*توفير|توفير مؤكد",
    re.IGNORECASE,
)

READINESS_FIELDS = (
    "problem_map",
    "maturity_score",
    "evidence_gaps",
    "risk_opportunity_map",
    "priority_actions",
    "safe_recommendations",
    "next_step_cta",
    "qualified_discovery_path",
    "opportunity_event",
    "proof_receipt",
)


def _run(**overrides: object):
    payload = {
        "request_id": "req_readiness_1",
        "locale": "ar",
        "sector": "clinics",
        "company_size": "sme",
        "buyer_role": "coo",
        "workflow": "booking_to_followup",
        "problem": "support_backlog",
        "email": "unknown@example.test",
        "consent": True,
    }
    payload.update(overrides)
    return DiagnosticProductEngine().run(DiagnosticProductRequest(**payload))


def test_result_has_full_readiness_contract() -> None:
    result = _run()
    for field in READINESS_FIELDS:
        value = getattr(result, field)
        assert value, field
    assert result.problem_map
    assert all(item["family_id"].startswith("A") for item in result.problem_map)
    assert result.evidence_gaps
    assert result.risk_opportunity_map


def test_arabic_and_english_cta_parity() -> None:
    arabic = _run(locale="ar")
    assert ARABIC_RE.search(arabic.next_step_cta)
    english = _run(locale="en")
    assert english.next_step_cta.isascii()


def test_maturity_score_is_estimated_not_measured() -> None:
    maturity = _run().maturity_score
    assert maturity["truth_class"] == "ESTIMATED"
    assert maturity["is_measured_fact"] is False
    assert 0 <= maturity["score"] <= 100
    assert "تقدير" in maturity["label_ar"]
    assert "ESTIMATED" in maturity["label_en"]


def test_opportunity_event_never_counts_as_pipeline() -> None:
    event = _run().opportunity_event
    assert event["event_type"] == "diagnostic_completed"
    assert event["truth_class"] == "INTERNAL_SIGNAL"
    assert event["counts_as_pipeline"] is False
    assert event["requires_human_review"] is True


def test_proof_receipt_is_pattern_not_customer_fact() -> None:
    receipt = _run().proof_receipt
    assert receipt["truth_class"] == "PATTERN"
    assert receipt["is_customer_fact"] is False
    assert receipt["price_sar"] == 0
    assert receipt["pricing_basis"] == "free_d0_d2"


def test_d0_d2_free_d3_quote_only_with_no_invented_price() -> None:
    engine = DiagnosticProductEngine()
    for depth in (
        DiagnosticDepth.D0_SIGNAL_SCAN,
        DiagnosticDepth.D1_RAPID,
        DiagnosticDepth.D2_FUNCTIONAL,
    ):
        result = _run(depth=depth)
        assert result.price_sar == 0
        assert result.pricing_basis == "free_d0_d2"
    deeper = _run(depth=DiagnosticDepth.D3_CROSS_FUNCTIONAL)
    assert deeper.price_sar == 0
    assert deeper.pricing_basis == QUOTE_REQUIRED
    assert engine.price("clinics", DiagnosticDepth.D3_CROSS_FUNCTIONAL) == 0


def test_consent_controls_qualified_discovery_path() -> None:
    granted = _run(consent=True)
    assert granted.qualified_discovery_path == "discovery"
    assert "consent::not_granted" not in granted.evidence_gaps
    withheld = _run(consent=False)
    assert withheld.qualified_discovery_path == "request_consent_then_discovery"
    assert "consent::not_granted" in withheld.evidence_gaps


def test_safe_recommendations_always_keep_human_approval_gate() -> None:
    result = _run()
    assert "no_automation_without_human_approval_gate" in result.safe_recommendations


def test_serialized_result_has_no_fake_roi_and_labels_estimates() -> None:
    result = _run()
    serialized = result.model_dump_json()
    assert not FAKE_ROI_RE.search(serialized)
    assert "estimate" in result.expected_impact_range.lower()
