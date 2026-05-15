"""Tests for endgame_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.endgame_os import (
    GOVERNANCE_RUNTIME_COMPONENTS,
    CapabilityDiagnosticProfile,
    GovernanceDecision,
    KillServiceSignals,
    ProofKind,
    VentureGateChecklist,
    autonomy_allowed,
    can_enter_step,
    governance_runtime_maturity_score,
    proof_to_retainer_hint,
    recommended_sprints,
    recurring_offer_for_proof,
    should_kill_service,
    validate_agent_card,
    venture_gate_passes,
)
from auto_client_acquisition.endgame_os.agent_control import AgentControlCard


def test_chain_requires_order() -> None:
    assert can_enter_step(frozenset(), "signal") is True
    assert can_enter_step(frozenset({"signal"}), "capability_diagnostic") is True
    assert can_enter_step(frozenset(), "capability_diagnostic") is False


def test_governance_maturity() -> None:
    half = frozenset(GOVERNANCE_RUNTIME_COMPONENTS[:5])
    assert 40 <= governance_runtime_maturity_score(half) <= 60


def test_agent_card() -> None:
    ok, err = validate_agent_card(
        AgentControlCard(
            agent_id="AGT-1",
            name="R",
            owner="Dealix",
            purpose="score",
            autonomy_level=2,
            audit_required=True,
        ),
    )
    assert ok and not err


def test_autonomy_enterprise_vs_mvp() -> None:
    assert autonomy_allowed(4, enterprise_tier=False) is False
    assert autonomy_allowed(4, enterprise_tier=True) is True


def test_capability_recommendations() -> None:
    p = CapabilityDiagnosticProfile(revenue=1, data=2, governance=0)
    sprints = recommended_sprints(p)
    assert "Revenue Intelligence Sprint" in sprints
    assert "AI Governance Review" in sprints


def test_proof_recurring_mapping() -> None:
    assert "RevOps" in recurring_offer_for_proof(ProofKind.REVENUE)


def test_proof_to_retainer_hint() -> None:
    assert proof_to_retainer_hint("strong") == "expand"


def test_venture_gate() -> None:
    full = VentureGateChecklist(*(True,) * 9)
    assert venture_gate_passes(full)
    bad = VentureGateChecklist(*(False,) * 9)
    assert not venture_gate_passes(bad)


def test_kill_service() -> None:
    assert should_kill_service(
        KillServiceSignals(True, True, True, False, False, False, False),
    )


def test_governance_decision_enum() -> None:
    assert GovernanceDecision.BLOCK == "BLOCK"
