"""Tests for proof_architecture_os."""

from __future__ import annotations

from auto_client_acquisition.proof_architecture_os import (
    OFFER_REVENUE_INTELLIGENCE_SPRINT,
    PROOF_DASHBOARD_SIGNALS,
    PROOF_LEVELS,
    PROOF_PACK_V2_SECTIONS,
    VALUE_METRICS_BY_OFFER,
    EnterpriseProofDimensions,
    RetainerGateInput,
    RetainerPath,
    RoiConfidence,
    ValueLedgerEvent,
    VentureFactoryGateV2Input,
    case_safe_public_summary_ok,
    enterprise_proof_score,
    proof_allows_case_study,
    proof_allows_retainer_pitch,
    proof_allows_sales_asset,
    proof_dashboard_coverage_score,
    proof_level_opens_retainer_path,
    proof_level_valid,
    proof_pack_v2_sections_complete,
    proof_score_band,
    retainer_gate_passes,
    retainer_path_recommendation,
    roi_must_label_distinct,
    roi_observed_ok_for_internal_report,
    roi_safe_for_public_case,
    value_ledger_event_valid,
    value_metrics_for_offer,
    venture_factory_gate_v2_passes,
)


def test_proof_pack_v2() -> None:
    full = dict.fromkeys(PROOF_PACK_V2_SECTIONS, "x")
    assert proof_pack_v2_sections_complete(full) == (True, ())


def test_proof_levels() -> None:
    assert len(PROOF_LEVELS) == 5
    assert proof_level_valid(3)
    assert not proof_level_valid(6)
    assert not proof_level_opens_retainer_path(4)
    assert proof_level_opens_retainer_path(5)


def test_value_metrics_by_offer() -> None:
    m = value_metrics_for_offer(OFFER_REVENUE_INTELLIGENCE_SPRINT)
    assert "accounts_scored" in m
    assert len(VALUE_METRICS_BY_OFFER) == 5
    assert value_metrics_for_offer("unknown_offer") == ()


def test_enterprise_proof_score_bands() -> None:
    hi = EnterpriseProofDimensions(90, 90, 90, 90, 90, 90, 90, 100)
    s = enterprise_proof_score(hi)
    assert s == 90
    assert proof_score_band(s) == "case_candidate"
    assert proof_allows_case_study(s)
    assert proof_allows_retainer_pitch(s)
    mid = EnterpriseProofDimensions(75, 75, 75, 75, 75, 70, 70, 80)
    s2 = enterprise_proof_score(mid)
    assert proof_score_band(s2) == "sales_support"
    assert proof_allows_sales_asset(s2)
    assert not proof_allows_case_study(84)


def test_value_ledger() -> None:
    ev = ValueLedgerEvent(
        value_event_id="V1",
        project_id="P1",
        client_id="C1",
        value_type="Revenue Proof",
        metric="accounts_scored",
        before=0,
        after=50,
        evidence="report",
        confidence="high",
        limitations="no external sends",
    )
    assert value_ledger_event_valid(ev)


def test_roi_discipline() -> None:
    assert roi_safe_for_public_case(RoiConfidence.VERIFIED)
    assert not roi_safe_for_public_case(RoiConfidence.ESTIMATED)
    assert not roi_safe_for_public_case(RoiConfidence.OBSERVED)
    assert roi_observed_ok_for_internal_report(RoiConfidence.OBSERVED)
    assert roi_observed_ok_for_internal_report(RoiConfidence.VERIFIED)
    assert not roi_observed_ok_for_internal_report(RoiConfidence.ESTIMATED)
    assert not roi_must_label_distinct(True, True)[0]


def test_case_safe() -> None:
    ok, _ = case_safe_public_summary_ok(
        mentions_client_name=False,
        includes_confidential_metrics=False,
        includes_sector_pattern=True,
        includes_work_performed_summary=True,
    )
    assert ok


def test_proof_dashboard() -> None:
    assert proof_dashboard_coverage_score(frozenset(PROOF_DASHBOARD_SIGNALS)) == 100


def test_retainer_and_venture() -> None:
    g = RetainerGateInput(
        proof_score=85,
        client_health=75,
        workflow_recurring=True,
        owner_exists=True,
        monthly_value_clear=True,
        governance_risk_controlled=True,
    )
    assert retainer_gate_passes(g)[0]
    assert retainer_path_recommendation(
        retainer_gate_ok=True,
        adjacent_capability_ready=False,
    ) == RetainerPath.CONTINUE
    assert (
        retainer_path_recommendation(
            retainer_gate_ok=True,
            adjacent_capability_ready=True,
        )
        == RetainerPath.EXPAND
    )
    v = VentureFactoryGateV2Input(
        paid_clients=5,
        retainers=2,
        proof_packs_count=10,
        avg_proof_score=82.0,
        repeatable_delivery=True,
        product_module_used=True,
        playbook_maturity=85.0,
        owner_exists=True,
        healthy_margin=True,
        core_os_dependency_documented=True,
    )
    assert venture_factory_gate_v2_passes(v)[0]
