from dealix.commercial.best_free_diagnostic import BEST_OFFERS, BestFreeDiagnosticEngine
from dealix.commercial.low_touch_products.diagnostic_product import (
    FREE_ALL_DEPTHS,
    DiagnosticProductEngine,
    DiagnosticProductRequest,
)
from dealix.commercial.universal_diagnostic_factory import FREE_DEPTHS, DiagnosticDepth


def test_every_diagnostic_depth_is_free() -> None:
    engine = DiagnosticProductEngine()

    assert frozenset(DiagnosticDepth) == FREE_DEPTHS
    for depth in DiagnosticDepth:
        assert engine.price("technology_saas_si", depth) == 0
        assert engine.pricing_basis(depth) == FREE_ALL_DEPTHS


def test_missing_economic_basis_produces_unknown_not_fake_roi() -> None:
    result = DiagnosticProductEngine().run(
        DiagnosticProductRequest(
            request_id="truth-gate",
            sector="professional_services",
            buyer_role="ceo",
            problem="revenue_leakage",
            consent=False,
        )
    )

    assert result.expected_impact_range == "UNKNOWN"
    assert result.impact_truth_class == "UNKNOWN"
    assert result.opportunity_event["counts_as_relationship"] is False
    assert result.opportunity_event["counts_as_pipeline"] is False
    assert result.opportunity_event["counts_as_revenue"] is False
    assert "consent::not_granted" in result.evidence_gaps


def test_estimate_requires_full_explicit_basis() -> None:
    result = DiagnosticProductEngine().run(
        DiagnosticProductRequest(
            request_id="basis-gate",
            sector="industrial_manufacturing",
            buyer_role="coo",
            problem="repetitive_manual_work",
            workflow="exception_to_resolution",
            cost_hypothesis_sar=10_000,
            impact_basis={
                "source_value": "10000 SAR/month stated operating cost",
                "source_type": "CUSTOMER_PROVIDED",
                "calculation": "10%-30% scenario only",
                "assumptions": "scope remains constant",
                "timeframe": "monthly",
                "confidence": "LOW",
                "owner": "customer operations owner",
            },
        )
    )

    assert result.impact_truth_class == "ESTIMATED"
    assert "ESTIMATED" in result.expected_impact_range


def test_free_offer_copy_contains_no_fabricated_result_claim() -> None:
    all_copy = " ".join(
        offer.title_ar + " " + offer.title_en + " " + offer.value_ar + " " + offer.value_en
        for offer in BEST_OFFERS
    )

    assert "18%" not in all_copy
    assert all(offer.price == "مجاني" for offer in BEST_OFFERS)


def test_best_free_diagnostic_does_not_invent_consent_or_pipeline() -> None:
    result = BestFreeDiagnosticEngine().run(
        "technology_saas_si",
        "ceo",
        "revenue_leakage",
    )

    assert result["counts_as_relationship"] is False
    assert result["counts_as_pipeline"] is False
    assert result["result"]["price_sar"] == 0
    assert "consent::not_granted" in result["result"]["evidence_gaps"]
    assert result["quality_claim"] == "NOT_ASSERTED_WITHOUT_EVIDENCE"
