"""Tests for risk_resilience_os."""

from __future__ import annotations

from auto_client_acquisition.risk_resilience_os import (
    CLIENT_INCIDENT_PHASES,
    FORBIDDEN_CHANNEL_AUTOMATIONS,
    STRATEGIC_DRIFT_WARNING_SIGNALS,
    ClientRiskSignals,
    PartnerCovenantSignals,
    ai_output_qa_band,
    autonomy_level_allowed_in_mvp,
    channel_automation_forbidden,
    claim_may_appear_in_case_study,
    client_risk_tier,
    drift_freeze_new_features_recommended,
    drift_warning_signal_valid,
    governance_failure_playbook_steps,
    incident_response_phases_complete,
    partner_should_suspend,
    resilience_shock_valid,
    risk_register_metadata_complete,
    risk_taxonomy_category_valid,
    whatsapp_client_use_allowed,
)


def test_risk_taxonomy() -> None:
    assert risk_taxonomy_category_valid("data_risk")
    assert not risk_taxonomy_category_valid("unknown_risk")


def test_risk_register_metadata() -> None:
    ok, missing = risk_register_metadata_complete(frozenset())
    assert not ok and missing


def test_ai_output_qa_band() -> None:
    assert ai_output_qa_band(92) == "client_ready"
    assert ai_output_qa_band(85) == "review"
    assert ai_output_qa_band(75) == "revise"
    assert ai_output_qa_band(50) == "reject"


def test_autonomy_mvp() -> None:
    assert autonomy_level_allowed_in_mvp(3) is True
    assert autonomy_level_allowed_in_mvp(4) is False


def test_channel_policy() -> None:
    assert channel_automation_forbidden("cold_whatsapp")
    assert len(FORBIDDEN_CHANNEL_AUTOMATIONS) >= 3
    assert whatsapp_client_use_allowed(relationship_or_consent=True, approved_external=False) is False


def test_claim_safety() -> None:
    assert claim_may_appear_in_case_study("verified", client_permission=True) is True
    assert claim_may_appear_in_case_study("estimated", client_permission=True) is False


def test_client_risk_tier() -> None:
    high = ClientRiskSignals(
        unclear_data_ownership=False,
        governance_rejects_approval=False,
        wants_guaranteed_outcomes=True,
        open_ended_scope=False,
        no_executive_owner=False,
        requests_unsafe_automation=False,
    )
    assert client_risk_tier(high) == "high_reject_or_reframe"


def test_partner_suspend() -> None:
    bad = PartnerCovenantSignals(
        scraping_systems=True,
        cold_whatsapp_automation=False,
        linkedin_automation=False,
        fake_proof=False,
        guaranteed_outcome_claims=False,
        client_output_without_qa=False,
        external_action_without_approval=False,
    )
    assert partner_should_suspend(bad) is True


def test_strategic_drift_freeze() -> None:
    w = frozenset(STRATEGIC_DRIFT_WARNING_SIGNALS[:3])
    assert drift_freeze_new_features_recommended(w) is True
    assert drift_warning_signal_valid("no_proof_packs")


def test_incident_and_resilience() -> None:
    ok, _ = incident_response_phases_complete(frozenset(CLIENT_INCIDENT_PHASES))
    assert ok
    assert resilience_shock_valid("governance_failure")
    assert len(governance_failure_playbook_steps()) == 5
