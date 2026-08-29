from __future__ import annotations

from dealix.commercial.portfolio_router import (
    INTERACTION_EVIDENCE_PRESENT,
    UNKNOWN,
    DemandSignal,
    EntryPackage,
    PortfolioPackageRouter,
)


def _signal(**overrides: object) -> DemandSignal:
    values: dict[str, object] = {
        "signal_id": "router-truth-1",
        "company_name": "Example Co",
        "observed_at": "2026-08-29T10:00:00+00:00",
        "source_ref": "source://account-research/1",
        "real_interaction_state": "REAL_INTERACTION",
        "real_interaction_ref": "interaction://event/1",
        "relationship_state": UNKNOWN,
        "consent_state": "UNKNOWN",
        "problem_statement": "Revenue follow-up is leaking qualified opportunities.",
        "problem_tags": ["revenue", "follow_up"],
        "urgency": "HIGH",
        "economic_relevance": "HIGH",
        "risk_class": "STANDARD",
    }
    values.update(overrides)
    return DemandSignal(**values)  # type: ignore[arg-type]


def test_public_or_crm_research_never_routes_itself_into_commercial_package() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            real_interaction_state="UNKNOWN",
            real_interaction_ref="",
            explicit_inbound_ref="",
            relationship_state="VERIFIED_RELATIONSHIP",
            source_ref="crm://research-row/1",
        )
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.status == "RESEARCH_ONLY"
    assert decision.relationship_state == UNKNOWN
    assert "RESEARCH_IS_NOT_RELATIONSHIP_OR_LEGITIMATE_DEMAND" in decision.reason_codes
    assert "supporting canonical interaction state and evidence" in decision.missing_evidence
    assert all(value is False for value in decision.authority.values())


def test_raw_interaction_reference_without_canonical_state_stays_research_only() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(real_interaction_state="UNKNOWN")
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.status == "RESEARCH_ONLY"
    assert decision.relationship_state == UNKNOWN
    assert "RAW_INTERACTION_REFERENCE_NOT_CANONICAL_STATE" in decision.reason_codes
    assert all(value is False for value in decision.authority.values())


def test_mismatched_interaction_state_and_reference_fail_closed() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            real_interaction_state="EXPLICIT_INBOUND",
            real_interaction_ref="interaction://wrong-kind",
            explicit_inbound_ref="",
        )
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.status == "RESEARCH_ONLY"
    assert decision.relationship_state == UNKNOWN
    assert "matching interaction evidence reference" in decision.missing_evidence
    assert all(value is False for value in decision.authority.values())


def test_canonical_interaction_state_and_ref_create_internal_hypothesis_not_relationship() -> None:
    decision = PortfolioPackageRouter().route(_signal())
    assert decision.recommended_package == EntryPackage.REVENUE_COMMAND
    assert decision.relationship_state == INTERACTION_EVIDENCE_PRESENT
    assert decision.authority_class == "PACKAGE_HYPOTHESIS_ONLY"
    assert "INTERACTION_EVIDENCE_IS_NOT_VERIFIED_RELATIONSHIP" in decision.reason_codes
    assert "canonical verified relationship state" in decision.missing_evidence
    assert decision.authority["relationship"] is False
    assert decision.authority["external_send"] is False


def test_verified_relationship_requires_canonical_state_and_matching_interaction_evidence() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(relationship_state="VERIFIED_RELATIONSHIP")
    )
    assert decision.relationship_state == "VERIFIED_RELATIONSHIP"
    assert "canonical verified relationship state" not in decision.missing_evidence
    assert decision.authority["relationship"] is False
    assert decision.authority["offer"] is False
    assert decision.authority["external_send"] is False


def test_explicit_inbound_requires_matching_state_and_ref() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            real_interaction_state="EXPLICIT_INBOUND",
            real_interaction_ref="",
            explicit_inbound_ref="inbound://diagnostic/1",
        )
    )
    assert decision.recommended_package == EntryPackage.REVENUE_COMMAND
    assert decision.relationship_state == INTERACTION_EVIDENCE_PRESENT
    assert decision.status == "INTERNAL_ROUTING_RECOMMENDATION"
    assert decision.authority_class == "PACKAGE_HYPOTHESIS_ONLY"
    assert all(value is False for value in decision.authority.values())


def test_multiple_package_families_fall_back_to_diagnostic_discovery() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            problem_statement="We need sales automation and a governed company brain.",
            problem_tags=["revenue", "automation", "company_brain"],
        )
    )
    assert decision.recommended_package == EntryPackage.DIAGNOSTIC_DISCOVERY
    assert decision.status == "DISCOVERY_REQUIRED"
    assert "MULTIPLE_PACKAGE_FAMILIES_REQUIRE_DISCOVERY" in decision.reason_codes
    assert all(value is False for value in decision.authority.values())


def test_suppression_and_prohibited_risk_override_package_fit() -> None:
    suppressed = PortfolioPackageRouter().route(_signal(consent_state="SUPPRESSED"))
    assert suppressed.status == "SUPPRESSED"
    assert suppressed.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert all(value is False for value in suppressed.authority.values())

    prohibited = PortfolioPackageRouter().route(_signal(risk_class="PROHIBITED"))
    assert prohibited.status == "GOVERNANCE_BLOCKED"
    assert prohibited.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert all(value is False for value in prohibited.authority.values())


def test_decision_is_deterministic() -> None:
    router = PortfolioPackageRouter()
    signal = _signal()
    first = router.route(signal)
    second = router.route(signal)
    assert first.decision_id == second.decision_id
    assert first.to_dict() == second.to_dict()
