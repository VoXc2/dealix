"""Tests for operating_empire_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.market_power_os import PartnerGateSignals
from auto_client_acquisition.operating_empire_os import (
    DealixBusinessUnit,
    TrustInfrastructureAttestation,
    benchmark_publish_ok,
    can_make_public_claim,
    can_publish_case_study,
    can_push_retainer,
    escape_commodity_framing,
    get_unit_profile,
    market_language_coverage_score,
    partner_empire_gate_readiness,
    trust_infrastructure_score,
)


def test_market_language_score() -> None:
    s = market_language_coverage_score("governed ai operations proof pack revenue intelligence")
    assert 0 < s <= 100


def test_trust_infrastructure_full() -> None:
    att = TrustInfrastructureAttestation(
        no_scraping=True,
        no_cold_whatsapp=True,
        no_linkedin_automation=True,
        no_fake_proof=True,
        no_guaranteed_sales_claims=True,
        no_pii_in_logs=True,
        no_sourceless_answers=True,
        no_external_action_without_approval=True,
    )
    assert trust_infrastructure_score(att) == 100


def test_proof_economy_rules() -> None:
    assert can_make_public_claim(has_substantiating_proof=False) is False
    assert can_publish_case_study(has_proof_pack=True, client_authorized=False) is False
    assert can_push_retainer(proof_strength_score=85) is True


def test_unit_registry() -> None:
    p = get_unit_profile(DealixBusinessUnit.REVENUE)
    assert "Revenue Intelligence" in p.primary_offer


def test_benchmark_publish() -> None:
    ok = benchmark_publish_ok(dict.fromkeys(("anonymized", "aggregated", "no_pii", "no_client_confidential", "permission_aware"), True))
    assert ok


def test_benchmark_unknown_rule() -> None:
    with pytest.raises(ValueError):
        benchmark_publish_ok({"anonymized": True, "bad": True})


def test_partner_gate_facade() -> None:
    assert partner_empire_gate_readiness(
        PartnerGateSignals(
            understands_dealix_method=True,
            respects_no_unsafe_automation=True,
            commits_to_proof_pack=True,
            accepts_qa=True,
            accepts_audit_rights=True,
            no_guaranteed_claims=True,
        ),
    ) == 100


def test_no_commodity_escape() -> None:
    assert escape_commodity_framing("chatbot") == "company_brain_governed"
    assert escape_commodity_framing("unknown") == "governed_ai_operating_capability"
