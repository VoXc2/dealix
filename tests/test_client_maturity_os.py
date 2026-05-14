"""Tests for client_maturity_os — ladder, score, offers, playbooks."""

from __future__ import annotations

from auto_client_acquisition.client_maturity_os.maturity_dashboard import build_maturity_dashboard
from auto_client_acquisition.client_maturity_os.maturity_engine import (
    ClientMaturityInputs,
    maturity_engine_result,
)
from auto_client_acquisition.client_maturity_os.maturity_score import (
    ClientMaturityDimensions,
    client_maturity_band,
    client_maturity_score,
)
from auto_client_acquisition.client_maturity_os.offer_matrix import (
    blocked_offers_for_level,
    level1_first_track,
    retainer_eligibility_met,
)
from auto_client_acquisition.client_maturity_os.progression_playbooks import progression_deliverables


def _dims(**kwargs: int) -> ClientMaturityDimensions:
    base = dict(
        leadership_alignment=50,
        data_readiness=50,
        workflow_ownership=50,
        governance_coverage=50,
        proof_discipline=50,
        adoption=50,
        operating_cadence=50,
    )
    base.update(kwargs)
    return ClientMaturityDimensions(**base)


def test_client_maturity_score_weights() -> None:
    d = ClientMaturityDimensions(
        leadership_alignment=100,
        data_readiness=100,
        workflow_ownership=100,
        governance_coverage=100,
        proof_discipline=100,
        adoption=100,
        operating_cadence=100,
    )
    assert client_maturity_score(d) == 100


def test_client_maturity_bands() -> None:
    assert client_maturity_band(90) == "enterprise_expansion_ready"
    assert client_maturity_band(75) == "retainer_workspace_ready"
    assert client_maturity_band(60) == "sprint_enablement"
    assert client_maturity_band(40) == "diagnostic_readiness"
    assert client_maturity_band(20) == "do_not_deploy_ai_workflow"


def test_level0_blocks_agents() -> None:
    b = blocked_offers_for_level(0)
    assert "Autonomous Agents" in b


def test_level3_blocks_external_automation() -> None:
    b = blocked_offers_for_level(3)
    assert "External Automation Without Approval" in b


def test_derive_readiness_blockers_includes_shadow() -> None:
    from auto_client_acquisition.client_maturity_os.maturity_dashboard import derive_readiness_blockers

    inp = ClientMaturityInputs(
        dimensions=_dims(),
        proof_score=50,
        adoption_score=50,
        workflow_count=0,
        workflow_owner_exists=False,
        monthly_cadence_active=False,
        governance_risk_controlled=False,
        shadow_ai_uncontrolled=True,
        has_executive_sponsor=False,
        has_governance_owner=False,
        requires_audit=False,
        clear_budget=False,
    )
    bl = derive_readiness_blockers(inp)
    assert "shadow_ai_uncontrolled" in bl
    assert "workflow_owner_missing" in bl


def test_retainer_eligibility() -> None:
    assert retainer_eligibility_met(
        proof_score=82,
        adoption_score=72,
        workflow_owner_exists=True,
        monthly_cadence_active=True,
        governance_risk_controlled=True,
    )
    assert not retainer_eligibility_met(
        proof_score=70,
        adoption_score=72,
        workflow_owner_exists=True,
        monthly_cadence_active=True,
        governance_risk_controlled=True,
    )


def test_progression_0_to_1() -> None:
    assert "ai_inventory" in progression_deliverables(0, 1)


def test_maturity_engine_chaos_shadow() -> None:
    inp = ClientMaturityInputs(
        dimensions=_dims(governance_coverage=30, proof_discipline=40),
        proof_score=40,
        adoption_score=40,
        workflow_count=0,
        workflow_owner_exists=False,
        monthly_cadence_active=False,
        governance_risk_controlled=False,
        shadow_ai_uncontrolled=True,
        has_executive_sponsor=False,
        has_governance_owner=False,
        requires_audit=False,
        clear_budget=False,
    )
    r = maturity_engine_result("CL-1", inp)
    assert r.maturity_level <= 1
    assert "Autonomous Agents" in r.blocked_offers


def test_maturity_engine_blocks_retainer_without_gates() -> None:
    inp = ClientMaturityInputs(
        dimensions=_dims(
            leadership_alignment=75,
            data_readiness=75,
            workflow_ownership=75,
            governance_coverage=75,
            proof_discipline=75,
            adoption=65,
            operating_cadence=70,
        ),
        proof_score=75,
        adoption_score=65,
        workflow_count=1,
        workflow_owner_exists=True,
        monthly_cadence_active=False,
        governance_risk_controlled=True,
        shadow_ai_uncontrolled=False,
        has_executive_sponsor=True,
        has_governance_owner=True,
        requires_audit=False,
        clear_budget=True,
    )
    r = maturity_engine_result("CL-2", inp)
    assert "Monthly Retainer" in r.blocked_offers


def test_level1_first_track_priority() -> None:
    assert (
        level1_first_track(
            pain_near_revenue=True,
            risk_higher_than_value=True,
            scattered_knowledge=True,
        )
        == "AI Governance Review"
    )
    assert (
        level1_first_track(
            pain_near_revenue=True,
            risk_higher_than_value=False,
            scattered_knowledge=True,
        )
        == "Company Brain Sprint"
    )
    assert (
        level1_first_track(
            pain_near_revenue=True,
            risk_higher_than_value=False,
            scattered_knowledge=False,
        )
        == "Revenue Intelligence Sprint"
    )
    assert "defer" in level1_first_track(
        pain_near_revenue=False,
        risk_higher_than_value=False,
        scattered_knowledge=False,
    )


def test_build_maturity_dashboard() -> None:
    inp = ClientMaturityInputs(
        dimensions=_dims(governance_coverage=72, proof_discipline=72),
        proof_score=72,
        adoption_score=65,
        workflow_count=1,
        workflow_owner_exists=True,
        monthly_cadence_active=True,
        governance_risk_controlled=True,
        shadow_ai_uncontrolled=False,
        has_executive_sponsor=False,
        has_governance_owner=False,
        requires_audit=False,
        clear_budget=False,
    )
    view = build_maturity_dashboard(
        "CL-3",
        inp,
        target_level=5,
        platform_pull_signals=("approvals_repeat",),
    )
    assert view.client_id == "CL-3"
    assert view.target_level == 5
    assert view.platform_pull_signals == ("approvals_repeat",)
    assert view.proof_score == 72
    assert view.adoption_score == 65
    assert view.governance_score == 72
    assert isinstance(view.readiness_blockers, tuple)
