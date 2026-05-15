"""Agentic Enterprise OS — continuous-evolution loop and unified agent view."""

from __future__ import annotations

from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agentic_enterprise_os.evaluation_harness import (
    EvalDimensionResult,
    run_evaluation_harness,
)
from auto_client_acquisition.agentic_enterprise_os.evolution_loop import (
    FrictionEntry,
    run_evolution_loop,
)
from auto_client_acquisition.agentic_enterprise_os.unified_agent_view import (
    build_unified_agent_view,
)


def test_evolution_loop_empty_inputs_yield_no_recommendations() -> None:
    result = run_evolution_loop()
    assert result.recommendations == ()
    assert result.sources_present == {
        "evaluation_harness": False,
        "friction_log": False,
        "learning_flywheel": False,
    }


def test_evolution_loop_surfaces_evaluation_gaps_first() -> None:
    evaluation = run_evaluation_harness(())  # all six dimensions are gaps
    result = run_evolution_loop(evaluation=evaluation)
    assert len(result.recommendations) == 6
    assert all(r.priority == 1 for r in result.recommendations)
    assert all(r.source == "evaluation_harness" for r in result.recommendations)
    assert result.sources_present["evaluation_harness"] is True


def test_evolution_loop_friction_threshold() -> None:
    friction = [
        FrictionEntry("import", "Slow import", "بطء الاستيراد", occurrences=4),
        FrictionEntry("billing", "Rare hiccup", "عطل نادر", occurrences=1),
    ]
    result = run_evolution_loop(friction_log=friction)
    # Only the entry with >= 3 occurrences becomes a recommendation.
    assert len(result.recommendations) == 1
    assert result.recommendations[0].area == "friction:import"
    assert result.recommendations[0].source == "friction_log"


def test_evolution_loop_priority_ordering() -> None:
    evaluation = run_evaluation_harness(
        (EvalDimensionResult("grounding", 90.0, sample_size=5),)
    )
    friction = [FrictionEntry("crm", "CRM lag", "تأخر النظام", occurrences=3)]
    result = run_evolution_loop(evaluation=evaluation, friction_log=friction)
    priorities = [r.priority for r in result.recommendations]
    assert priorities == sorted(priorities)


def test_unified_agent_view_no_fabricated_risk() -> None:
    card = AgentCard(
        agent_id="a1",
        name="Intake Agent",
        owner="ops",
        purpose="triage inbound",
        autonomy_level=1,
        status="active",
    )
    view = build_unified_agent_view(card)
    assert view.agent_id == "a1"
    # Governance / risk fields stay None unless explicitly supplied.
    assert view.risk_score is None
    assert view.risk_band is None
    assert view.governance_decision is None
