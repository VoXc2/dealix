"""Tests for adoption_os."""

from __future__ import annotations

from auto_client_acquisition.adoption_os import (
    ADOPTION_DASHBOARD_SIGNALS,
    ADOPTION_REVIEW_SIGNALS,
    CLIENT_ADOPTION_ROLES,
    ENABLEMENT_KIT_ITEMS,
    FRICTION_TYPES,
    ONBOARDING_PHASES,
    TRAINING_PRODUCT_SLUGS,
    AdoptionDimensions,
    AdoptionOutcome,
    AdoptionRetainerReadiness,
    FrictionEvent,
    adoption_band,
    adoption_dashboard_coverage_score,
    adoption_retainer_readiness_passes,
    adoption_review_coverage_score,
    adoption_score,
    enablement_kit_coverage_score,
    friction_event_valid,
    friction_type_known,
    onboarding_phase_index,
    training_product_known,
)


def test_adoption_score() -> None:
    d = AdoptionDimensions(80, 80, 80, 80, 80, 80, 80, 80)
    s = adoption_score(d)
    assert s == 80
    assert adoption_band(s) == "retainer_ready"


def test_enablement_kit() -> None:
    assert enablement_kit_coverage_score(frozenset(ENABLEMENT_KIT_ITEMS)) == 100


def test_friction() -> None:
    ev = FrictionEvent(
        friction_id="F1",
        client_id="C1",
        friction_type="approval_friction",
        description="d",
        impact="i",
        response="r",
        product_signal="approval_center",
    )
    assert friction_event_valid(ev)
    assert friction_type_known("approval_friction")


def test_adoption_review() -> None:
    assert adoption_review_coverage_score(frozenset(ADOPTION_REVIEW_SIGNALS)) == 100
    assert onboarding_phase_index("proof_pack") == 7


def test_dashboard() -> None:
    assert adoption_dashboard_coverage_score(frozenset(ADOPTION_DASHBOARD_SIGNALS)) == 100


def test_retainer_readiness() -> None:
    r = AdoptionRetainerReadiness(
        workflow_owner_exists=True,
        outputs_used=True,
        approval_path_works=True,
        proof_score=85,
        client_asks_continuation=True,
        monthly_value_exists=True,
        governance_risk_controlled=True,
    )
    assert adoption_retainer_readiness_passes(r)[0]


def test_training_products() -> None:
    assert training_product_known(TRAINING_PRODUCT_SLUGS[0])


def test_roles() -> None:
    assert len(CLIENT_ADOPTION_ROLES) == 5
    assert len(FRICTION_TYPES) == 8
    assert AdoptionOutcome.NOT_ADOPTED.value == "not_adopted"
