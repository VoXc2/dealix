from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.targeting import (
    Actionability,
    ChannelEligibility,
    CommercialOutcome,
    ConsentState,
    EvidenceItem,
    EvidenceTier,
    PriorityBand,
    RelationshipState,
    SignalFamily,
    TargetDossier,
    TargetValueFeatures,
    deterministic_entity_key,
    evidence_expiry,
    normalize_company_name,
    normalize_domain,
    outcome_learning_row,
    possible_duplicate,
    rank_dossiers,
    score_target,
)


def evidence(*, stale: bool = False) -> EvidenceItem:
    observed = datetime.now(UTC) - (timedelta(days=90) if stale else timedelta(days=1))
    return EvidenceItem(
        source_id="official-company-newsroom",
        source_url="https://example.sa/news",
        tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
        observed_at=observed,
        expires_at=observed + timedelta(days=45),
        claim="Company announced an operating transition with measurable workflow impact.",
        confidence=0.9,
    )


def dossier(**overrides) -> TargetDossier:
    values = dict(
        company_id="company_123",
        company_name="Example Saudi Co",
        canonical_domain="example.sa",
        signal_family=SignalFamily.REVENUE_LEAKAGE,
        why_them="Visible multi-step commercial workflow.",
        why_now="Official trigger observed this week.",
        problem_hypothesis="Manual handoffs may delay follow-up.",
        business_cost_hypothesis="Delay may reduce conversion and proof quality.",
        offer_route="Execution Diagnostic",
        proof_baseline="Measure enquiry-to-next-action latency before/after.",
        evidence=(evidence(),),
        features=TargetValueFeatures(
            icp_saudi_fit=1.0,
            problem_evidence=0.9,
            why_now_trigger=0.9,
            offer_fit=0.9,
            buyer_or_partner_route=0.7,
            proofability=0.9,
            expected_economic_value=0.8,
            evidence_confidence=0.9,
            semantic_fit=0.8,
        ),
        actionability=Actionability(
            relationship=RelationshipState.RESEARCH_ONLY,
            consent=ConsentState.NOT_REQUIRED_FOR_INTERNAL_RESEARCH,
            email=ChannelEligibility.DRAFT_ONLY,
            whatsapp=ChannelEligibility.INBOUND_ONLY,
            voice=ChannelEligibility.INBOUND_ONLY,
        ),
    )
    values.update(overrides)
    return TargetDossier(**values)


def test_target_value_and_actionability_are_separate():
    target = dossier()
    result = score_target(target)
    assert result.total >= 85
    assert result.priority_band == PriorityBand.P0
    assert result.eligible_for_draft is True
    assert target.actionability.can_execute_live("email") is False
    assert target.actionability.can_execute_live("whatsapp") is False


def test_suppression_blocks_live_execution_and_draft_gate():
    target = dossier(
        actionability=Actionability(
            relationship=RelationshipState.KNOWN,
            consent=ConsentState.OPTED_OUT,
            email=ChannelEligibility.ELIGIBLE,
            suppressed=True,
        )
    )
    result = score_target(target)
    assert result.eligible_for_draft is False
    assert "suppressed" in result.hold_reasons
    assert "opted_out_or_suppressed" in result.hold_reasons
    assert target.actionability.can_execute_live("email") is False


def test_stale_only_evidence_holds_draft():
    target = dossier(evidence=(evidence(stale=True),))
    result = score_target(target)
    assert result.stale_evidence_count == 1
    assert result.eligible_for_draft is False
    assert "no_fresh_credible_evidence" in result.hold_reasons


def test_duplicate_active_thread_holds_new_draft():
    result = score_target(dossier(active_thread_or_opportunity=True))
    assert result.eligible_for_draft is False
    assert "duplicate_active_thread_or_opportunity" in result.hold_reasons


def test_domain_and_company_normalization_are_deterministic():
    assert normalize_domain("https://WWW.Example.SA/path") == "example.sa"
    assert normalize_company_name("Example Company LLC") == "example"
    assert deterministic_entity_key(domain="www.Example.sa", legal_name="Ignored LLC") == "domain:example.sa"


def test_duplicate_detector_prefers_domain_then_conservative_fuzzy_name():
    assert possible_duplicate(
        left_domain="example.sa",
        left_name="Different Name",
        right_domain="www.example.sa",
        right_name="Another Name",
    )
    assert possible_duplicate(
        left_domain="",
        left_name="Acme Saudi Technology LLC",
        right_domain="",
        right_name="Acme Saudi Technology",
        fuzzy_threshold=0.90,
    )
    assert not possible_duplicate(
        left_domain="alpha.sa",
        left_name="Alpha Holdings",
        right_domain="beta.sa",
        right_name="Beta Logistics",
    )


def test_outcome_truth_cannot_skip_economic_stages():
    with pytest.raises(ValueError, match="cannot skip evidence"):
        CommercialOutcome(
            dossier_id=dossier().dossier_id,
            real_interaction=False,
            payment_verified=True,
        )


def test_learning_row_attributes_cash_and_proof_to_originating_dossier():
    target = dossier()
    score = score_target(target)
    outcome = CommercialOutcome(
        dossier_id=target.dossier_id,
        real_interaction=True,
        qualified_problem=True,
        quote_created=True,
        payment_verified=True,
        outcome_delivered=True,
        proof_validated=True,
        founder_minutes=20,
        cost_sar=15,
    )
    row = outcome_learning_row(dossier=target, score=score, outcome=outcome)
    assert row["company_id"] == target.company_id
    assert row["payment_verified"] is True
    assert row["proof_validated"] is True
    assert row["target_value_score"] == score.total


def test_rank_dossiers_prioritizes_eligible_high_value_targets():
    strong = dossier(company_id="company_strong")
    held = dossier(company_id="company_held", active_thread_or_opportunity=True)
    ranked = rank_dossiers([held, strong])
    assert ranked[0][0].company_id == "company_strong"
    assert ranked[0][1].eligible_for_draft is True


def test_evidence_expiry_is_tier_specific():
    observed = datetime(2026, 9, 6, tzinfo=UTC)
    assert evidence_expiry(observed_at=observed, tier=EvidenceTier.FIRST_PARTY_OFFICIAL) == observed + timedelta(days=45)
    assert evidence_expiry(observed_at=observed, tier=EvidenceTier.SOCIAL_CHATTER) == observed + timedelta(days=14)
