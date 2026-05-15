"""Adoption score — usage/cadence signals weighted 0–100 + retainer readiness."""
from __future__ import annotations

from auto_client_acquisition.adoption_os.adoption_score import (
    AdoptionDimensions,
    adoption_band,
    adoption_score,
)
from auto_client_acquisition.adoption_os.retainer_readiness import (
    AdoptionRetainerReadiness,
    adoption_retainer_readiness_passes,
    wave2_retainer_eligibility,
)


def _dims(value: int) -> AdoptionDimensions:
    return AdoptionDimensions(
        executive_sponsor=value,
        workflow_owner=value,
        data_readiness=value,
        user_engagement=value,
        approval_completion=value,
        proof_visibility=value,
        monthly_cadence=value,
        expansion_pull=value,
    )


def test_all_max_signals_score_100():
    assert adoption_score(_dims(100)) == 100


def test_all_zero_signals_score_0():
    assert adoption_score(_dims(0)) == 0


def test_score_is_bounded_when_inputs_exceed_range():
    # Out-of-range values are clamped to 0–100 before weighting.
    assert adoption_score(_dims(500)) == 100


def test_adoption_band_thresholds():
    assert adoption_band(90) == "scale_account"
    assert adoption_band(75) == "retainer_ready"
    assert adoption_band(60) == "needs_enablement"
    assert adoption_band(20) == "risky_adoption"


def test_partial_signals_land_mid_range():
    score = adoption_score(_dims(50))
    assert 0 < score < 100


def test_retainer_readiness_passes_when_all_conditions_met():
    ok, errs = adoption_retainer_readiness_passes(
        AdoptionRetainerReadiness(
            workflow_owner_exists=True,
            outputs_used=True,
            approval_path_works=True,
            proof_score=85,
            client_asks_continuation=True,
            monthly_value_exists=True,
            governance_risk_controlled=True,
        )
    )
    assert ok is True
    assert errs == ()


def test_retainer_readiness_lists_every_gap():
    ok, errs = adoption_retainer_readiness_passes(
        AdoptionRetainerReadiness(
            workflow_owner_exists=False,
            outputs_used=False,
            approval_path_works=False,
            proof_score=10,
            client_asks_continuation=False,
            monthly_value_exists=False,
            governance_risk_controlled=False,
        )
    )
    assert ok is False
    assert "workflow_owner_missing" in errs
    assert "proof_score_below_80" in errs
    assert len(errs) == 7


def test_wave2_eligibility_gate_passes_and_fails():
    ok, errs = wave2_retainer_eligibility(
        proof_score=85,
        adoption_score=75,
        workflow_owner_exists=True,
        monthly_workflow_exists=True,
        governance_risk_controlled=True,
    )
    assert ok is True and errs == ()

    ok, errs = wave2_retainer_eligibility(
        proof_score=50,
        adoption_score=40,
        workflow_owner_exists=False,
        monthly_workflow_exists=False,
        governance_risk_controlled=False,
    )
    assert ok is False
    assert "proof_score_below_80" in errs
    assert "adoption_score_below_70" in errs
