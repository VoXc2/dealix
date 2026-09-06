#!/usr/bin/env python3
"""Bounded executable acceptance for Targeting Intelligence V1.

Read-only / no external effects. This verifier exercises the production
contracts directly without requiring pytest or any network/provider access.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dealix.company_intelligence.signal_contracts import SignalType, build_signal
from dealix.company_intelligence.targeting import (
    Actionability,
    ChannelEligibility,
    CommercialOutcome,
    ConsentState,
    DuplicateMatchKind,
    EvidenceItem,
    EvidenceTier,
    RelationshipState,
    SignalFamily,
    TargetValueFeatures,
    classify_duplicate,
    score_target,
)
from dealix.company_intelligence.targeting_bridge import (
    TargetingDossierContext,
    TargetingSignalBinding,
    build_target_dossier_from_canonical_signals,
)
from dealix.company_intelligence.targeting_daily_overlay import (
    daily_targeting_overlay_payload,
)


def _features() -> TargetValueFeatures:
    return TargetValueFeatures(
        icp_saudi_fit=1.0,
        problem_evidence=0.9,
        why_now_trigger=0.9,
        offer_fit=0.9,
        buyer_or_partner_route=0.7,
        proofability=0.9,
        expected_economic_value=0.8,
        evidence_confidence=0.9,
    )


def _context(*, suppressed: bool = False) -> TargetingDossierContext:
    return TargetingDossierContext(
        company_name="Verifier Company",
        canonical_domain="verifier.example.sa",
        why_them="A measurable commercial workflow is visible.",
        why_now="A fresh first-party operating signal was observed.",
        problem_hypothesis="A handoff may delay next action.",
        business_cost_hypothesis="The delay may reduce conversion and proof quality.",
        offer_route="Execution Diagnostic",
        proof_baseline="Measure next-action latency before and after.",
        features=_features(),
        actionability=Actionability(
            relationship=RelationshipState.RESEARCH_ONLY,
            consent=ConsentState.NOT_REQUIRED_FOR_INTERNAL_RESEARCH,
            email=ChannelEligibility.DRAFT_ONLY,
            whatsapp=ChannelEligibility.INBOUND_ONLY,
            voice=ChannelEligibility.INBOUND_ONLY,
            suppressed=suppressed,
        ),
    )


def _signal():
    return build_signal(
        tenant_id="dealix_internal",
        deduplication_key="verifier:money:official",
        company_id="company_verifier",
        source_id="official_company_source",
        signal_type=SignalType.MONEY,
        claim="Official evidence indicates a measurable commercial handoff gap.",
        evidence_ref="https://verifier.example.sa/news",
        confidence=0.9,
        observed_at=datetime.now(UTC) - timedelta(days=1),
    )


def _dossier(*, suppressed: bool = False):
    return build_target_dossier_from_canonical_signals(
        [
            TargetingSignalBinding(
                signal=_signal(),
                evidence_tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
            )
        ],
        context=_context(suppressed=suppressed),
    )


def main() -> int:
    checks = 0

    target = _dossier()
    score = score_target(target)
    assert score.total >= 70.0
    assert score.eligible_for_draft is True
    assert target.actionability.can_execute_live("email") is False
    checks += 1

    held = _dossier(suppressed=True)
    held_score = score_target(held)
    assert held_score.eligible_for_draft is False
    assert "suppressed" in held_score.hold_reasons
    assert held.actionability.can_execute_live("email") is False
    checks += 1

    assert classify_duplicate(
        left_domain="alpha.sa",
        left_name="Acme Saudi Technology LLC",
        right_domain="beta.sa",
        right_name="Acme Saudi Technology",
        fuzzy_threshold=0.90,
    ) == DuplicateMatchKind.FUZZY_NAME_CANDIDATE
    checks += 1

    stale_observed = datetime.now(UTC) - timedelta(days=90)
    stale = EvidenceItem(
        source_id="official",
        source_url="https://example.sa",
        tier=EvidenceTier.FIRST_PARTY_OFFICIAL,
        observed_at=stale_observed,
        expires_at=stale_observed + timedelta(days=45),
        claim="Old official claim",
        confidence=0.9,
    )
    stale_target = type(target)(
        **{
            **target.__dict__,
            "evidence": (stale,),
        }
    )
    stale_score = score_target(stale_target)
    assert stale_score.eligible_for_draft is False
    assert "no_fresh_credible_evidence" in stale_score.hold_reasons
    checks += 1

    try:
        CommercialOutcome(
            dossier_id=target.dossier_id,
            real_interaction=False,
            payment_verified=True,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("commercial outcome chain allowed payment without prior evidence")
    checks += 1

    try:
        EvidenceItem(
            source_id="source",
            source_url="",
            tier=EvidenceTier.OPEN_WEB_ARCHIVE,
            observed_at=datetime(2026, 9, 6),
            claim="naive timestamp",
            confidence=0.7,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("timezone-naive evidence timestamp was accepted")
    checks += 1

    assert target.signal_family == SignalFamily.REVENUE_LEAKAGE
    checks += 1

    overlay = daily_targeting_overlay_payload([target, held], target_count=20)
    assert overlay["mode"] == "targeting_v1_evidence_overlay"
    assert overlay["selected_count"] == 1
    assert overlay["approval_required"] is True
    assert overlay["live_execution_authorized"] is False
    assert overlay["external_effects"] == "NONE"
    row = overlay["selected"][0]
    assert row["dossier_id"] == target.dossier_id
    assert row["approval_required"] is True
    assert row["live_execution_authorized"] is False
    checks += 1

    print(f"TARGETING_INTELLIGENCE_V1_CHECKS={checks}")
    print("TARGETING_INTELLIGENCE_V1_PASS")
    print("EXTERNAL_EFFECTS=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
