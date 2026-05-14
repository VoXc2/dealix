"""Tests for client_os."""

from __future__ import annotations

from auto_client_acquisition.client_os import (
    CLIENT_OS_USAGE_SIGNALS,
    DATA_READINESS_PANEL_SIGNALS,
    GOVERNANCE_PANEL_SIGNALS,
    MONTHLY_VALUE_REPORT_SECTIONS,
    PROOF_TIMELINE_SIGNALS,
    TRUST_OUTPUT_STRIP_SIGNALS,
    AgentTransparencyCard,
    ClientExpansionSignal,
    ClientHealthDimensions,
    agent_transparency_card_valid,
    capability_level_valid,
    client_expansion_recommendation,
    client_health_band,
    client_health_score,
    client_os_usage_coverage_score,
    data_readiness_panel_coverage_score,
    governance_panel_coverage_score,
    monthly_value_report_sections_complete,
    proof_timeline_coverage_score,
    trust_output_strip_coverage_score,
)


def test_client_health() -> None:
    d = ClientHealthDimensions(80, 80, 80, 80, 80, 80, 80)
    s = client_health_score(d)
    assert s == 80
    assert client_health_band(s) == "offer_retainer"


def test_capability_levels() -> None:
    assert capability_level_valid(0)
    assert capability_level_valid(5)
    assert not capability_level_valid(6)


def test_panel_coverage_scores() -> None:
    assert data_readiness_panel_coverage_score(frozenset(DATA_READINESS_PANEL_SIGNALS)) == 100
    assert governance_panel_coverage_score(frozenset(GOVERNANCE_PANEL_SIGNALS)) == 100
    assert trust_output_strip_coverage_score(frozenset(TRUST_OUTPUT_STRIP_SIGNALS)) == 100
    assert proof_timeline_coverage_score(frozenset(PROOF_TIMELINE_SIGNALS)) == 100
    assert client_os_usage_coverage_score(frozenset(CLIENT_OS_USAGE_SIGNALS)) == 100


def test_monthly_value_report() -> None:
    full = dict.fromkeys(MONTHLY_VALUE_REPORT_SECTIONS, "x")
    assert monthly_value_report_sections_complete(full) == (True, ())


def test_expansion_engine() -> None:
    assert (
        client_expansion_recommendation(ClientExpansionSignal.LOW_DATA_READINESS)
        == "data_readiness_retainer"
    )
    assert client_expansion_recommendation("unknown") is None


def test_agent_transparency() -> None:
    ok = AgentTransparencyCard(
        agent="RevenueAgent",
        task="rank_accounts",
        autonomy_level=2,
        human_owner="Dealix Revenue",
        external_action_allowed=False,
        approval_required=True,
        audit_event="AUD-003",
    )
    assert agent_transparency_card_valid(ok)
    bad = AgentTransparencyCard(
        agent="",
        task="t",
        autonomy_level=2,
        human_owner="h",
        external_action_allowed=True,
        approval_required=False,
        audit_event="A",
    )
    assert not agent_transparency_card_valid(bad)
