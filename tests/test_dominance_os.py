"""Tests for dominance_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.dominance_os import (
    HOLDING_SEQUENCE_STEP_IDS,
    DominanceScorecard,
    EnterpriseReadinessLevel,
    PostProofDecision,
    ProductizationGateInputs,
    ProofStrengthInputs,
    RetainerEligibilityInputs,
    compute_proof_strength_score,
    holding_sequence_progress,
    infer_enterprise_readiness_level,
    is_retainer_eligible,
    passes_productization_gate,
    proof_usable_for_sales,
    recommend_dominance_focus,
    recommend_post_proof_decision,
)


def test_proof_strength_full() -> None:
    s = compute_proof_strength_score(
        ProofStrengthInputs(100, 100, 100, 100, 100, 100),
    )
    assert s == 100.0


def test_proof_usable_for_sales_threshold() -> None:
    assert proof_usable_for_sales(70.0, minimum=70.0) is True
    assert proof_usable_for_sales(69.0, minimum=70.0) is False


def test_retainer_eligible() -> None:
    assert is_retainer_eligible(
        RetainerEligibilityInputs(
            proof_strength_score=85,
            client_health=75,
            workflow_recurring=True,
            monthly_value_clear=True,
            stakeholder_engaged=True,
        ),
    )


def test_retainer_not_eligible_low_proof() -> None:
    assert not is_retainer_eligible(
        RetainerEligibilityInputs(
            proof_strength_score=70,
            client_health=80,
            workflow_recurring=True,
            monthly_value_clear=True,
            stakeholder_engaged=True,
        ),
    )


def test_productization_gate() -> None:
    assert passes_productization_gate(
        ProductizationGateInputs(
            manual_step_repeated=4,
            time_cost_hours_per_project=3.0,
            linked_to_paid_offer=True,
            reduces_risk_or_improves_margin=True,
            testable=True,
        ),
    )


def test_post_proof_expand() -> None:
    assert (
        recommend_post_proof_decision(
            wants_continue_same_capability=False,
            wants_adjacent_expansion=True,
            value_proven=True,
        )
        == PostProofDecision.EXPAND
    )


def test_dominance_focus_governance_weakest() -> None:
    code = recommend_dominance_focus(
        DominanceScorecard(
            category=90,
            governance=10,
            proof=90,
            offer=90,
            retainer=90,
            product=90,
            market=90,
            standard=90,
            venture=90,
            holding=90,
        ),
    )
    assert code == "governance_weak_stop_expansion"


def test_enterprise_readiness_l2() -> None:
    assert (
        infer_enterprise_readiness_level(
            has_trust_pack=True,
            has_audit_trail=True,
            has_policy_engine=False,
        )
        == EnterpriseReadinessLevel.L2_AUDITABILITY
    )


def test_enterprise_readiness_l5() -> None:
    assert (
        infer_enterprise_readiness_level(
            has_trust_pack=True,
            has_audit_trail=True,
            has_policy_engine=True,
            has_enterprise_platform_features=True,
            has_ai_control_tower=True,
        )
        == EnterpriseReadinessLevel.L5_ENTERPRISE_AI_OS
    )


def test_holding_progress_half() -> None:
    half = set(HOLDING_SEQUENCE_STEP_IDS[:6])
    p = holding_sequence_progress(half)
    assert p > 40.0


def test_proof_strength_invalid_raises() -> None:
    with pytest.raises(ValueError):
        compute_proof_strength_score(ProofStrengthInputs(metric_clarity=101))


def test_holding_progress_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown holding"):
        holding_sequence_progress({"not_a_step"})
