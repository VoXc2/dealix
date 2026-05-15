"""Tests for System 30 — org_graph_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.org_graph_os import (
    GraphEdge,
    GraphError,
    GraphNode,
    NodeType,
    Relation,
    get_org_graph,
    reset_org_graph,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_org_graph()


def _seed_incident() -> None:
    graph = get_org_graph()
    graph.add_node(GraphNode(node_id="inc1", node_type=NodeType.INCIDENT, label="outage"))
    graph.add_node(GraphNode(node_id="risk1", node_type=NodeType.RISK))
    graph.add_node(GraphNode(node_id="wf1", node_type=NodeType.WORKFLOW))
    graph.add_node(GraphNode(node_id="ag1", node_type=NodeType.AGENT))
    graph.add_node(GraphNode(node_id="dept1", node_type=NodeType.DEPARTMENT))
    graph.add_edge(GraphEdge(from_id="risk1", to_id="inc1", relation=Relation.CAUSED))
    graph.add_edge(GraphEdge(from_id="inc1", to_id="wf1", relation=Relation.AFFECTED_BY))
    graph.add_edge(GraphEdge(from_id="inc1", to_id="ag1", relation=Relation.AFFECTED_BY))
    graph.add_edge(GraphEdge(from_id="inc1", to_id="dept1", relation=Relation.AFFECTED_BY))


def test_edge_to_unknown_node_raises() -> None:
    get_org_graph().add_node(GraphNode(node_id="n1", node_type=NodeType.PERSON))
    with pytest.raises(GraphError):
        get_org_graph().add_edge(GraphEdge(from_id="n1", to_id="missing"))


def test_incident_impact_blast_radius() -> None:
    _seed_incident()
    impact = get_org_graph().incident_impact("inc1")
    assert impact.root_cause is not None and impact.root_cause.node_id == "risk1"
    assert impact.related_workflows == ["wf1"]
    assert impact.related_agents == ["ag1"]
    assert [n.node_id for n in impact.affected] == ["dept1"]


def test_dependencies_and_path() -> None:
    graph = get_org_graph()
    graph.add_node(GraphNode(node_id="a", node_type=NodeType.WORKFLOW))
    graph.add_node(GraphNode(node_id="b", node_type=NodeType.WORKFLOW))
    graph.add_edge(GraphEdge(from_id="a", to_id="b", relation=Relation.DEPENDS_ON))
    assert [n.node_id for n in graph.dependencies("a")] == ["b"]
    assert graph.path("a", "b") == ["a", "b"]
