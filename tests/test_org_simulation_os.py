"""Tests for System 32 — org_simulation_os.

Also guards `no_live_send` — every simulation kind routes through the sandbox
and never touches production.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.org_graph_os import (
    GraphEdge,
    GraphNode,
    NodeType,
    Relation,
    get_org_graph,
    reset_org_graph,
)
from auto_client_acquisition.org_simulation_os import (
    ScenarioKind,
    SimulationError,
    SimulationScenario,
    get_org_simulator,
    reset_org_simulator,
)
from auto_client_acquisition.sandbox_os import get_sandbox_engine, reset_sandbox_engine


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_org_simulator()
    reset_sandbox_engine()
    reset_org_graph()


def test_workflow_simulation_routes_through_sandbox() -> None:
    scenario = SimulationScenario(
        kind=ScenarioKind.WORKFLOW,
        parameters={"workflow_id": "wf1", "steps": [{"action_type": "noop"}]},
    )
    result = get_org_simulator().simulate(scenario)
    assert result.kind == "workflow"
    # the sandbox produced a non-production run
    runs = [
        r for r in get_sandbox_engine()._runs.values() if r.workflow_id == "wf1"
    ]
    assert runs and all(not r.is_production for r in runs)


def test_failure_simulation_flags_bottleneck() -> None:
    scenario = SimulationScenario(
        kind=ScenarioKind.FAILURE,
        parameters={"workflow_id": "wf1", "fail_step": "s2", "steps": []},
    )
    result = get_org_simulator().simulate(scenario)
    assert result.bottlenecks == ["s2"]
    assert result.risk_score > 0.0


def test_scale_simulation_detects_overload() -> None:
    scenario = SimulationScenario(
        kind=ScenarioKind.SCALE,
        parameters={"current_load": 100, "target_load": 1000},
    )
    result = get_org_simulator().simulate(scenario)
    assert "capacity" in result.bottlenecks


def test_incident_simulation_uses_graph() -> None:
    graph = get_org_graph()
    graph.add_node(GraphNode(node_id="inc1", node_type=NodeType.INCIDENT))
    graph.add_node(GraphNode(node_id="wf1", node_type=NodeType.WORKFLOW))
    graph.add_edge(GraphEdge(from_id="inc1", to_id="wf1", relation=Relation.AFFECTED_BY))
    result = get_org_simulator().simulate(
        SimulationScenario(kind=ScenarioKind.INCIDENT, parameters={"incident_id": "inc1"})
    )
    assert result.bottlenecks == ["wf1"]


def test_incident_simulation_without_id_raises() -> None:
    with pytest.raises(SimulationError):
        get_org_simulator().simulate(
            SimulationScenario(kind=ScenarioKind.INCIDENT, parameters={})
        )
