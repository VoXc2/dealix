"""Tests for scale_os gates and scoring helpers."""

from __future__ import annotations

import pytest

from auto_client_acquisition.scale_os import (
    Gate1FounderToProductized,
    Gate2ProductizedToTool,
    Gate6PlatformToAcademy,
    HiringSignals,
    PartnerReadinessInputs,
    PricingSignals,
    SaasTransitionSignals,
    compute_partner_readiness_score,
    compute_saas_transition_score,
    evaluate_gate1,
    evaluate_gate2,
    evaluate_gate6,
    infer_pricing_stage,
    recommend_hires,
    saas_readiness_band,
)
from auto_client_acquisition.scale_os.pricing_stage import PricingEvolutionStage


def test_gate1_passes() -> None:
    ok, failed = evaluate_gate1(
        Gate1FounderToProductized(
            same_service_sold_count=3,
            same_pain_repeated=True,
            same_deliverables_repeated=True,
        ),
    )
    assert ok and failed == []


def test_gate1_fails_low_sales() -> None:
    ok, failed = evaluate_gate1(Gate1FounderToProductized(same_service_sold_count=1))
    assert not ok
    assert "same_service_sold_count_lt_2" in failed


def test_gate2_passes() -> None:
    ok, failed = evaluate_gate2(
        Gate2ProductizedToTool(
            manual_step_repeats=5,
            hours_per_manual_step=2.5,
            affects_quality_or_margin=True,
        ),
    )
    assert ok and failed == []


def test_gate2_fails_hours() -> None:
    ok, failed = evaluate_gate2(
        Gate2ProductizedToTool(
            manual_step_repeats=4,
            hours_per_manual_step=2.0,
            affects_quality_or_margin=True,
        ),
    )
    assert not ok
    assert "manual_step_hours_not_gt_2" in failed


def test_gate6_academy_thresholds() -> None:
    ok, _ = evaluate_gate6(
        Gate6PlatformToAcademy(
            project_count=11,
            proof_backed_cases=4,
            method_stable=True,
            templates_stable=True,
        ),
    )
    assert ok


def test_partner_score_perfect() -> None:
    s, miss = compute_partner_readiness_score(
        PartnerReadinessInputs(
            trust_pack_acknowledged=True,
            governance_rules_acknowledged=True,
            qa_review_required_acknowledged=True,
            proof_pack_required_acknowledged=True,
            no_guaranteed_claims_acknowledged=True,
            no_unsafe_automation_acknowledged=True,
            no_fake_proof_acknowledged=True,
            certification_path_defined=True,
            audit_rights_defined=True,
            delivery_standard_documented=True,
        ),
    )
    assert s == 100 and miss == []


def test_saas_score_all_signals() -> None:
    assert compute_saas_transition_score(
        SaasTransitionSignals(
            workflow_stable_repeat=True,
            client_asks_access=True,
            high_manual_delivery_time=True,
            internal_module_in_production_use=True,
            retainers_need_dashboard=True,
        ),
    ) == 100


def test_saas_band_boundaries() -> None:
    assert saas_readiness_band(0) == "hold"
    assert saas_readiness_band(39) == "hold"
    assert saas_readiness_band(40) == "pilot"
    assert saas_readiness_band(69) == "pilot"
    assert saas_readiness_band(70) == "accelerate"


def test_saas_band_invalid() -> None:
    with pytest.raises(ValueError):
        saas_readiness_band(101)


def test_pricing_stage_precedence() -> None:
    assert (
        infer_pricing_stage(
            PricingSignals(
                enterprise_contract=True,
                subscription_plus_managed_service=True,
                has_mrr_retainers_material=False,
                repeatable_sprint_catalog_live=False,
                founder_proof_engagements=False,
            ),
        )
        == PricingEvolutionStage.ENTERPRISE
    )


def test_hiring_empty_when_offer_unclear() -> None:
    assert recommend_hires(HiringSignals(offer_clear=False, founder_bottleneck=True)) == []

def test_hiring_ordered_basic() -> None:
    roles = recommend_hires(
        HiringSignals(
            offer_clear=True,
            checklists_exist=True,
            repeated_projects=True,
            founder_bottleneck=True,
            manual_steps_repeat=True,
            modules_needed=True,
            retainers_active=True,
            workspace_critical=True,
            sensitive_data_or_enterprise=True,
            high_ai_output_review_load=True,
        ),
    )
    assert len(roles) == 4
