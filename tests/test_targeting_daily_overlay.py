from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.targeting import (
    Actionability,
    ChannelEligibility,
    ConsentState,
    EvidenceItem,
    EvidenceTier,
    RelationshipState,
    SignalFamily,
    TargetDossier,
    TargetValueFeatures,
)
from dealix.company_intelligence.targeting_daily_overlay import (
    daily_targeting_overlay_payload,
    select_evidence_first_daily_drafts,
)


def _evidence(*, stale: bool = False):
    observed = datetime.now(UTC) - (timedelta(days=90) if stale else timedelta(days=1))
    return EvidenceItem(
        source_id="official",
        source_url="https://example.sa/news",
        tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
        observed_at=observed,
        expires_at=observed + timedelta(days=45),
        claim="Official operating change with a measurable commercial implication.",
        confidence=0.9,
    )


def _dossier(*, company_id: str, score_bias: float = 1.0, stale: bool = False, suppressed: bool = False):
    return TargetDossier(
        company_id=company_id,
        company_name=company_id,
        canonical_domain=f"{company_id}.sa",
        signal_family=SignalFamily.REVENUE_LEAKAGE,
        why_them="Visible multi-step commercial workflow.",
        why_now="Fresh first-party operating trigger.",
        problem_hypothesis="Manual handoffs may delay next action.",
        business_cost_hypothesis="Delay may reduce conversion and proof quality.",
        offer_route="Execution Diagnostic",
        proof_baseline="Measure enquiry-to-next-action latency.",
        evidence=(_evidence(stale=stale),),
        features=TargetValueFeatures(
            icp_saudi_fit=score_bias,
            problem_evidence=score_bias,
            why_now_trigger=score_bias,
            offer_fit=score_bias,
            buyer_or_partner_route=score_bias,
            proofability=score_bias,
            expected_economic_value=score_bias,
            evidence_confidence=score_bias,
        ),
        actionability=Actionability(
            relationship=RelationshipState.RESEARCH_ONLY,
            consent=ConsentState.NOT_REQUIRED_FOR_INTERNAL_RESEARCH,
            email=ChannelEligibility.DRAFT_ONLY,
            whatsapp=ChannelEligibility.INBOUND_ONLY,
            voice=ChannelEligibility.INBOUND_ONLY,
            suppressed=suppressed,
        ),
    )


def test_research_only_high_score_can_be_draft_candidate_but_never_live_authority():
    payload = daily_targeting_overlay_payload(
        [_dossier(company_id="strong", score_bias=1.0)],
        target_count=20,
    )
    assert payload["selected_count"] == 1
    row = payload["selected"][0]
    assert row["priority_band"] == "P0"
    assert row["relationship_state"] == "research_only"
    assert row["email_eligibility"] == "draft_only"
    assert row["approval_required"] is True
    assert row["live_execution_authorized"] is False
    assert payload["live_execution_authorized"] is False
    assert payload["external_effects"] == "NONE"


def test_stale_and_suppressed_dossiers_do_not_enter_daily_draft_queue():
    selected = select_evidence_first_daily_drafts(
        [
            _dossier(company_id="stale", stale=True),
            _dossier(company_id="suppressed", suppressed=True),
            _dossier(company_id="good", score_bias=0.8),
        ],
        target_count=20,
    )
    assert [candidate.company_id for candidate in selected] == ["good"]


def test_daily_overlay_respects_value_ranking_and_capacity_bound():
    selected = select_evidence_first_daily_drafts(
        [
            _dossier(company_id="mid", score_bias=0.7),
            _dossier(company_id="high", score_bias=1.0),
            _dossier(company_id="low", score_bias=0.6),
        ],
        target_count=2,
    )
    assert [candidate.company_id for candidate in selected] == ["high", "mid"]


def test_zero_capacity_returns_no_candidates():
    assert select_evidence_first_daily_drafts(
        [_dossier(company_id="strong")],
        target_count=0,
    ) == []


def test_negative_capacity_fails_closed():
    with pytest.raises(ValueError, match="non-negative"):
        select_evidence_first_daily_drafts([], target_count=-1)
