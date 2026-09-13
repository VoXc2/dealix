"""Official-Source Watch contract tests (Omega V3 market intelligence).

Validates current authority: research != relationship, public contact !=
consent, source mention != buyer intent, stale/unknown evidence != fact.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dealix.commercial.official_source_watch import (
    ChangedetectionWatchAdapter,
    CrawlAIExtractAdapter,
    FreshnessState,
    OfficialSourceWatchRegistry,
    build_official_signal,
    compute_dedupe_key,
    compute_evidence_hash,
)
from dealix.company_intelligence.signal_contracts import (
    build_signal,
    is_signal_stale,
    transition_signal,
    SignalStatus,
)


def _zatca_kwargs(**overrides):
    now = datetime.now(UTC)
    base = {
        "source_authority": "ZATCA",
        "canonical_url": "https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx",
        "canonical_ref": "Wave25-E-invoicing",
        "sector": "cross_sector",
        "topic": "e-invoicing Wave 25 compliance mandate",
        "title_en": "ZATCA Wave 25 — E-invoicing Integration Phase",
        "published_at": "2026-07-24",
        "effective_at": "2027-02-01",
        "expires_at": (now + timedelta(days=30)).isoformat(),
        "evidence_excerpt": "Wave 25 criterion: VAT-subject revenue exceeded SAR 187,500 in 2022-2025.",
        "evidence_ref": "zatca-wave25-page-p1",
        "source_registry_id": "zatca_wave25",
        "confidence": 0.9,
        "regulatory_impact": "Notified taxpayers must integrate by 2027-02-01.",
        "commercial_impact": "Internal readiness diagnostic template only.",
    }
    base.update(overrides)
    return base


def test_official_source_validation_known_authority():
    sig = build_official_signal(**_zatca_kwargs())
    assert sig.source_authority == "ZATCA"
    assert sig.canonical_url.startswith("https://")
    assert sig.freshness_state() is FreshnessState.FRESH
    assert sig.is_actionable() is True
    assert sig.evidence_hash == compute_evidence_hash(sig.canonical_url, sig.evidence_excerpt)


def test_unknown_source_metadata_holds_without_invention():
    sig = build_official_signal(**_zatca_kwargs(source_authority="BLOGXYZ", canonical_url=""))
    assert sig.source_authority == "UNKNOWN"
    assert sig.canonical_url == "UNKNOWN"
    assert sig.evidence_hash == "UNKNOWN"
    assert sig.freshness_state() is FreshnessState.HOLD
    assert sig.is_actionable() is False
    assert sig.recommended_internal_action == "HOLD_UNKNOWN_OR_STALE"
    assert sig.confidence <= 0.3


def test_dedupe_repeated_watches_do_not_manufacture_signals():
    registry = OfficialSourceWatchRegistry()
    first, created_first = registry.ingest(build_official_signal(**_zatca_kwargs()))
    second, created_second = registry.ingest(build_official_signal(**_zatca_kwargs()))
    assert created_first is True
    assert created_second is False
    assert second.signal_id == first.signal_id
    assert len(registry.to_dict()["signals"]) == 1
    # Same logical watch -> identical dedupe key and evidence hash.
    assert first.dedupe_key == compute_dedupe_key("ZATCA", "Wave25-E-invoicing",
                                                  "e-invoicing Wave 25 compliance mandate",
                                                  "cross_sector")
    assert first.economic_governor_hint()["creates_opportunity"] is False


def test_stale_evidence_is_never_current_fact():
    now = datetime.now(UTC)
    expired = build_official_signal(
        **_zatca_kwargs(expires_at=(now - timedelta(days=1)).isoformat()),
        now=now,
    )
    assert expired.freshness_state(now=now) is FreshnessState.EXPIRED
    assert expired.is_actionable(now=now) is False
    assert expired.recommended_internal_action == "HOLD_UNKNOWN_OR_STALE"

    stale = build_official_signal(
        **_zatca_kwargs(expires_at=(now + timedelta(days=3)).isoformat()),
        now=now,
    )
    assert stale.freshness_state(now=now) is FreshnessState.STALE
    assert stale.recommended_internal_action == "REFRESH_EVIDENCE_BEFORE_USE"
    assert stale.is_actionable(now=now) is False


def test_public_contact_truth_firewall():
    sig = build_official_signal(
        **_zatca_kwargs(
            evidence_excerpt="Public contact page lists info@zatca.gov.sa and +966112795555; Wave 25 applies.",
        )
    )
    # Public contact inside evidence changes nothing about consent/relationship.
    assert sig.relationship_state == "RESEARCH_ONLY"
    assert sig.consent_state == "NOT_PROVEN"
    assert sig.counts_as_relationship is False
    assert sig.counts_as_consent is False
    assert sig.counts_as_buyer_intent is False
    assert sig.counts_as_pipeline is False
    assert sig.counts_as_revenue is False
    assert sig.allows_external_send is False
    from dealix.commercial.official_source_watch import OfficialSourceSignal

    with pytest.raises(ValueError):
        OfficialSourceSignal.model_validate({**sig.model_dump(), "counts_as_consent": True})
    with pytest.raises(ValueError):
        OfficialSourceSignal.model_validate({**sig.model_dump(), "relationship_state": "REAL_INTERACTION"})


def test_signal_to_internal_action_mapping_never_external():
    sig = build_official_signal(**_zatca_kwargs())
    assert sig.recommended_internal_action == "INTERNAL_REVIEW_OFFICIAL_SOURCE"
    hint = sig.economic_governor_hint()
    assert hint["internal_action"] == "INTERNAL_REVIEW_OFFICIAL_SOURCE"
    assert "external" not in hint["internal_action"].lower()
    assert hint["evidence_class"] == "public_source"

    market = build_official_signal(
        **_zatca_kwargs(topic="SME digitization readiness overview", confidence=0.8)
    )
    assert market.recommended_internal_action == "PREPARE_DIAGNOSTIC_TEMPLATE"


def test_canonical_signal_integration_uses_current_contracts():
    sig = build_official_signal(**_zatca_kwargs())
    kwargs = sig.to_canonical_signal_kwargs(tenant_id="tenant_sa")
    canonical = build_signal(**kwargs)
    assert canonical.consent_status.value == "public_source"
    assert canonical.evidence_ref == sig.evidence_ref
    assert canonical.confidence == pytest.approx(0.9)
    # Lifecycle via current contract: raw -> validated ok; withdrawn blocks link.
    validated = transition_signal(canonical, to_status=SignalStatus.VALIDATED)
    assert validated.status is SignalStatus.VALIDATED
    assert is_signal_stale(validated) is False


def test_radar_admission_stays_research_only():
    sig = build_official_signal(**_zatca_kwargs())
    radar = sig.to_radar_signal()
    assert radar.counts_as_relationship is False
    assert radar.counts_as_consent is False
    assert radar.counts_as_pipeline is False
    assert radar.counts_as_revenue is False
    assert radar.tender_submission_allowed is False
    assert "INTERNAL ONLY" in radar.commercial_implication


def test_adapters_disabled_by_default_no_live_crawl():
    cd = ChangedetectionWatchAdapter()
    crawl = CrawlAIExtractAdapter()
    assert cd.access_state == "BLOCKED_DISABLED_BY_DEFAULT"
    assert crawl.access_state == "BLOCKED_DISABLED_BY_DEFAULT"
    assert cd.fetch(request_id="r1").status == "BLOCKED_DISABLED_BY_DEFAULT"
    assert crawl.fetch(request_id="r1").status == "BLOCKED_DISABLED_BY_DEFAULT"
    for receipt in (cd.plan(request_id="r1"), crawl.plan(request_id="r1")):
        assert receipt.authority["external_send"] is False
        assert receipt.authority["opportunity"] is False
