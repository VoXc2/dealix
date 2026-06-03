"""Tests for moat_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.moat_os import (
    AntiMoatRisk,
    MoatScoreDimensions,
    PartnerMoatSignals,
    detect_anti_moat_risks,
    governance_moat_loop_complete,
    moat_compound_index,
    moat_market_language_adoption_score,
    moat_tier,
    partner_moat_score,
    proof_moat_loop_complete,
    proof_to_moat_progress,
    risk_to_seed_artifacts,
    weighted_moat_score,
)


def test_weighted_moat_score_mid() -> None:
    d = MoatScoreDimensions(*(80,) * 7)
    assert weighted_moat_score(d) == 80
    assert moat_tier(80) == "emerging"


def test_moat_tier_edges() -> None:
    assert moat_tier(90) == "strong"
    assert moat_tier(74) == "emerging"
    assert moat_tier(55) == "weak"
    assert moat_tier(40) == "commodity_risk"


def test_moat_dimensions_validation() -> None:
    with pytest.raises(ValueError):
        MoatScoreDimensions(101, 0, 0, 0, 0, 0, 0)


def test_moat_compound_index_penalizes_weak_link() -> None:
    high = MoatScoreDimensions(*(90,) * 7)
    mixed = MoatScoreDimensions(90, 90, 90, 90, 90, 90, 20)
    assert moat_compound_index(mixed) < moat_compound_index(high)


def test_proof_to_moat_progress() -> None:
    done, missing = proof_to_moat_progress(frozenset({"client_expansion"}))
    assert done == 1
    assert "anonymized_insight" in missing


def test_proof_moat_loop_complete() -> None:
    assert proof_moat_loop_complete(frozenset()) is False
    full = {
        "client_expansion",
        "anonymized_insight",
        "benchmark_update",
        "sales_asset",
        "product_signal",
        "market_content",
        "trust_increase",
    }
    assert proof_moat_loop_complete(frozenset(full)) is True


def test_governance_moat_loop() -> None:
    assert governance_moat_loop_complete(frozenset()) is False


def test_risk_to_seed_artifacts() -> None:
    arts = risk_to_seed_artifacts("client asks for cold whatsapp")
    assert "no_cold_whatsapp_rule" in arts


def test_partner_moat_score() -> None:
    full = PartnerMoatSignals(
        certified_method=True,
        qa_standard_accepted=True,
        governance_rules_accepted=True,
        proof_pack_required=True,
        co_sell_playbook=True,
        partner_dashboard=True,
        audit_rights_accepted=True,
        zero_compliance_incidents=True,
    )
    assert partner_moat_score(full) == 100


def test_market_language_adoption_wraps() -> None:
    s = moat_market_language_adoption_score("governed ai operations proof pack revenue intelligence")
    assert 0 < s <= 100


def test_anti_moat() -> None:
    hits = detect_anti_moat_risks(delivery_without_proof_pack=True)
    assert hits[0].risk == AntiMoatRisk.WEAK_PROOF
