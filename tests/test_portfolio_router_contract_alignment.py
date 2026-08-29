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
        "signal_id": "route-contract-1",
        "company_name": "Example Co",
        "observed_at": "2026-08-29T10:00:00+00:00",
        "source_ref": "source://1",
        "real_interaction_ref": "interaction://1",
        "relationship_state": UNKNOWN,
        "consent_state": "CONSENTED",
        "problem_statement": "We have a revenue follow-up problem.",
        "problem_tags": ["revenue", "follow_up"],
        "urgency": "HIGH",
        "economic_relevance": "HIGH",
        "risk_class": "STANDARD",
    }
    values.update(overrides)
    return DemandSignal(**values)  # type: ignore[arg-type]


def _assert_no_authority(decision: object) -> None:
    assert all(value is False for value in decision.authority.values())
    assert decision.confidence_semantics == "ROUTING_CLARITY_ONLY_NOT_PURCHASE_PROBABILITY"


def test_crm_or_public_source_cannot_self_promote_even_if_relationship_is_claimed() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            real_interaction_ref="",
            explicit_inbound_ref="",
            source_ref="crm://research-row/1",
            relationship_state="VERIFIED_RELATIONSHIP",
        )
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.status == "RESEARCH_ONLY"
    assert decision.relationship_state == UNKNOWN
    assert "RESEARCH_IS_NOT_RELATIONSHIP_OR_LEGITIMATE_DEMAND" in decision.reason_codes
    _assert_no_authority(decision)


def test_interaction_reference_is_evidence_presence_not_relationship_truth() -> None:
    decision = PortfolioPackageRouter().route(_signal())
    assert decision.recommended_package == EntryPackage.REVENUE_COMMAND
    assert decision.relationship_state == INTERACTION_EVIDENCE_PRESENT
    assert "INTERACTION_REFERENCE_IS_NOT_VERIFIED_RELATIONSHIP" in decision.reason_codes
    assert "canonical verified relationship state" in decision.missing_evidence
    assert decision.authority_class == "PACKAGE_HYPOTHESIS_ONLY"
    _assert_no_authority(decision)


def test_canonical_verified_relationship_requires_supporting_interaction_evidence() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(relationship_state="VERIFIED_RELATIONSHIP")
    )
    assert decision.relationship_state == "VERIFIED_RELATIONSHIP"
    assert decision.recommended_package == EntryPackage.REVENUE_COMMAND
    assert decision.status == "INTERNAL_ROUTING_RECOMMENDATION"
    _assert_no_authority(decision)


def test_multiple_package_families_require_diagnostic_discovery() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            problem_statement="We need sales automation and a governed company brain.",
            problem_tags=["revenue", "automation", "company_brain"],
        )
    )
    assert decision.recommended_package == EntryPackage.DIAGNOSTIC_DISCOVERY
    assert decision.status == "DISCOVERY_REQUIRED"
    assert "MULTIPLE_PACKAGE_FAMILIES_REQUIRE_DISCOVERY" in decision.reason_codes
    assert "primary problem and scope priority" in decision.missing_evidence
    _assert_no_authority(decision)


def test_high_risk_requires_governance_before_package_progression() -> None:
    decision = PortfolioPackageRouter().route(_signal(risk_class="HIGH"))
    assert decision.recommended_package == EntryPackage.REVENUE_COMMAND
    assert decision.status == "GOVERNANCE_REVIEW_REQUIRED"
    assert decision.authority_class == "GOVERNANCE_REVIEW_REQUIRED"
    assert decision.owner == "governance"
    assert "HIGH_RISK_REQUIRES_GOVERNANCE_REVIEW" in decision.reason_codes
    _assert_no_authority(decision)


def test_prohibited_risk_suppresses_commercial_progression() -> None:
    decision = PortfolioPackageRouter().route(_signal(risk_class="PROHIBITED"))
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.status == "GOVERNANCE_BLOCKED"
    assert decision.expiry_hours == 0
    assert "PROHIBITED_RISK_CLASS" in decision.reason_codes
    _assert_no_authority(decision)


def test_opt_out_overrides_partner_and_market_access_interest() -> None:
    decision = PortfolioPackageRouter().route(
        _signal(
            consent_state="OPTED_OUT",
            partner_intent=True,
            ksa_market_entry_intent=True,
        )
    )
    assert decision.recommended_package == EntryPackage.RESEARCH_NURTURE_SUPPRESS
    assert decision.status == "SUPPRESSED"
    assert decision.owner == "governance"
    assert decision.expiry_hours == 0
    _assert_no_authority(decision)


def test_runtime_exposes_contract_fields_and_remains_deterministic() -> None:
    router = PortfolioPackageRouter()
    signal = _signal()
    first = router.route(signal)
    second = router.route(signal)
    payload = first.to_dict()
    for field in (
        "recommended_package",
        "routing_reason",
        "confidence",
        "input_evidence_refs",
        "missing_evidence",
        "next_evidence_required",
        "next_action",
        "owner",
        "sla_minutes",
        "expiry_hours",
        "authority_class",
        "risk_class",
    ):
        assert field in payload
    assert payload["input_evidence_refs"] == payload["evidence_refs"]
    assert first.decision_id == second.decision_id
    assert first.to_dict() == second.to_dict()
    _assert_no_authority(first)
