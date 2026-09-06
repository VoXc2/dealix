from datetime import UTC, datetime

import pytest

from dealix.company_intelligence.signal_contracts import (
    ConsentStatus as SignalConsentStatus,
    SignalType,
    build_signal,
)
from dealix.company_intelligence.targeting import (
    Actionability,
    ChannelEligibility,
    ConsentState,
    EvidenceTier,
    RelationshipState,
    SignalFamily,
    TargetValueFeatures,
    score_target,
)
from dealix.company_intelligence.targeting_bridge import (
    TargetingDossierContext,
    TargetingSignalBinding,
    build_target_dossier_from_canonical_signals,
    evidence_from_canonical_signal,
    suggested_signal_family,
)


def signal(
    *,
    signal_type: SignalType = SignalType.MONEY,
    company_id: str = "company_123",
    consent_status: SignalConsentStatus = SignalConsentStatus.UNKNOWN,
    claim: str = "Commercial workflow shows a measurable revenue handoff gap.",
):
    return build_signal(
        tenant_id="dealix_internal",
        deduplication_key=f"{company_id}:{signal_type.value}:official",
        company_id=company_id,
        source_id="official_company_source",
        signal_type=signal_type,
        consent_status=consent_status,
        claim=claim,
        evidence_ref="https://example.sa/news",
        confidence=0.9,
        observed_at=datetime(2026, 9, 6, 12, 0, tzinfo=UTC),
    )


def context(**overrides):
    values = dict(
        company_name="Example Saudi Co",
        canonical_domain="example.sa",
        why_them="A multi-step commercial workflow is visible.",
        why_now="A first-party operating change was observed this week.",
        problem_hypothesis="Manual handoffs may delay next action.",
        business_cost_hypothesis="Delay may reduce conversion and proof quality.",
        offer_route="Execution Diagnostic",
        proof_baseline="Measure enquiry-to-next-action latency before and after.",
        features=TargetValueFeatures(
            icp_saudi_fit=1.0,
            problem_evidence=0.9,
            why_now_trigger=0.9,
            offer_fit=0.9,
            buyer_or_partner_route=0.7,
            proofability=0.9,
            expected_economic_value=0.8,
            evidence_confidence=0.9,
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
    return TargetingDossierContext(**values)


def test_bridge_preserves_canonical_signal_evidence_without_granting_authority():
    binding = TargetingSignalBinding(
        signal=signal(),
        evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
    )
    dossier = build_target_dossier_from_canonical_signals(
        [binding],
        context=context(),
    )
    result = score_target(dossier)

    assert dossier.company_id == "company_123"
    assert dossier.signal_family == SignalFamily.REVENUE_LEAKAGE
    assert dossier.evidence[0].source_id == "official_company_source"
    assert dossier.evidence[0].tier == EvidenceTier.FIRST_PARTY_OFFICIAL
    assert dossier.evidence[0].expires_at is not None
    assert result.eligible_for_draft is True
    assert dossier.actionability.can_execute_live("email") is False


def test_bridge_requires_one_canonical_company():
    left = TargetingSignalBinding(signal=signal(company_id="left"), evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL)
    right = TargetingSignalBinding(signal=signal(company_id="right"), evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL)
    with pytest.raises(ValueError, match="one canonical company"):
        build_target_dossier_from_canonical_signals([left, right], context=context())


def test_mixed_signal_families_require_explicit_commercial_classification():
    money = TargetingSignalBinding(signal=signal(signal_type=SignalType.MONEY), evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL)
    customer = TargetingSignalBinding(signal=signal(signal_type=SignalType.CUSTOMER), evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL)

    with pytest.raises(ValueError, match="mixed canonical signal families"):
        build_target_dossier_from_canonical_signals([money, customer], context=context())

    dossier = build_target_dossier_from_canonical_signals(
        [money, customer],
        context=context(),
        signal_family=SignalFamily.REVENUE_LEAKAGE,
    )
    assert dossier.signal_family == SignalFamily.REVENUE_LEAKAGE
    assert len(dossier.evidence) == 2


def test_withdrawn_signal_cannot_be_reused_as_targeting_evidence():
    binding = TargetingSignalBinding(
        signal=signal(consent_status=SignalConsentStatus.WITHDRAWN),
        evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
    )
    with pytest.raises(ValueError, match="withdrawn-consent"):
        evidence_from_canonical_signal(binding)


def test_personal_signal_type_is_not_silently_promoted_into_b2b_targeting():
    with pytest.raises(ValueError, match="not eligible for B2B targeting"):
        suggested_signal_family(SignalType.PERSONAL)


def test_empty_canonical_claim_fails_closed():
    binding = TargetingSignalBinding(
        signal=signal(claim=""),
        evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
    )
    with pytest.raises(ValueError, match="non-empty claim"):
        evidence_from_canonical_signal(binding)
