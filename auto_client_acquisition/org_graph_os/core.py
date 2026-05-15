"""System 30 — the Operational Memory Graph.

A graph of people, workflows, approvals, incidents, risks, departments and
agents. For any incident it answers: what caused it, who was affected, which
workflows and agents are related, and which risks resulted.

Plain in-memory adjacency — no graph database in v1.
"""

from __future__ import annotations

from collections import deque

from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit
from auto_client_acquisition.org_graph_os.schemas import (
    GraphEdge,
    GraphNode,
    IncidentImpact,
    NodeType,
    Relation,
)

_MODULE = "org_graph_os"


class GraphError(ValueError):
    """Raised on an invalid graph operation — never swallowed."""


class OrgGraph:
    """In-memory operational memory graph."""

    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: list[GraphEdge] = []

    # ── construction ─────────────────────────────────────────────
    def add_node(self, node: GraphNode) -> GraphNode:
        self._nodes[node.node_id] = node
        emit(
            event_type=ControlEventType.GRAPH_NODE_ADDED,
            source_module=_MODULE,
            subject_type=str(node.node_type),
            subject_id=node.node_id,
            payload={"label": node.label},
        )
        return node

    def add_edge(self, edge: GraphEdge) -> GraphEdge:
        if edge.from_id not in self._nodes:
            raise GraphError(f"unknown from_id: {edge.from_id}")
        if edge.to_id not in self._nodes:
            raise GraphError(f"unknown to_id: {edge.to_id}")
        self._edges.append(edge)
        emit(
            event_type=ControlEventType.GRAPH_EDGE_ADDED,
            source_module=_MODULE,
            subject_type="edge",
            subject_id=edge.edge_id,
            payload={
                "from_id": edge.from_id,
                "to_id": edge.to_id,
                "relation": str(edge.relation),
            },
        )
        return edge

    def get_node(self, node_id: str) -> GraphNode | None:
        return self._nodes.get(node_id)

    # ── traversal ────────────────────────────────────────────────
    def neighbors(
        self, node_id: str, *, relation: str | None = None
    ) -> list[GraphNode]:
        """Adjacent nodes (both edge directions), optionally filtered by relation."""
        self._require(node_id)
        adjacent: list[str] = []
        for edge in self._edges:
            if relation and str(edge.relation) != relation:
                continue
            if edge.from_id == node_id:
                adjacent.append(edge.to_id)
            elif edge.to_id == node_id:
                adjacent.append(edge.from_id)
        seen: set[str] = set()
        out: list[GraphNode] = []
        for nid in adjacent:
            if nid not in seen and nid in self._nodes:
                seen.add(nid)
                out.append(self._nodes[nid])
        return out

    def dependencies(self, node_id: str) -> list[GraphNode]:
        """Nodes this node depends on (outgoing `depends_on` edges)."""
        self._require(node_id)
        return [
            self._nodes[e.to_id]
            for e in self._edges
            if e.from_id == node_id
            and str(e.relation) == Relation.DEPENDS_ON.value
            and e.to_id in self._nodes
        ]

    def path(self, from_id: str, to_id: str) -> list[str]:
        """Shortest path of node IDs between two nodes (BFS), or [] if none."""
        self._require(from_id)
        self._require(to_id)
        if from_id == to_id:
            return [from_id]
        queue: deque[list[str]] = deque([[from_id]])
        visited: set[str] = {from_id}
        while queue:
            trail = queue.popleft()
            for neighbor in self.neighbors(trail[-1]):
                if neighbor.node_id == to_id:
                    return trail + [to_id]
                if neighbor.node_id not in visited:
                    visited.add(neighbor.node_id)
                    queue.append(trail + [neighbor.node_id])
        return []

    def incident_impact(self, incident_id: str) -> IncidentImpact:
        """Compute the blast radius of an incident node."""
        node = self._require(incident_id)
        if str(node.node_type) != NodeType.INCIDENT.value:
            raise GraphError(f"node {incident_id} is not an incident")

        root_cause: GraphNode | None = None
        for edge in self._edges:
            if (
                edge.to_id == incident_id
                and str(edge.relation) == Relation.CAUSED.value
                and edge.from_id in self._nodes
            ):
                root_cause = self._nodes[edge.from_id]
                break

        neighbors = self.neighbors(incident_id)
        affected = [
            n
            for n in neighbors
            if str(n.node_type)
            in (NodeType.PERSON.value, NodeType.DEPARTMENT.value)
        ]
        related_workflows = [
            n.node_id for n in neighbors if str(n.node_type) == NodeType.WORKFLOW.value
        ]
        related_agents = [
            n.node_id for n in neighbors if str(n.node_type) == NodeType.AGENT.value
        ]
        resulting_risks = [
            n.node_id for n in neighbors if str(n.node_type) == NodeType.RISK.value
        ]
        return IncidentImpact(
            incident_id=incident_id,
            root_cause=root_cause,
            affected=affected,
            related_workflows=related_workflows,
            related_agents=related_agents,
            resulting_risks=resulting_risks,
        )

    def _require(self, node_id: str) -> GraphNode:
        node = self._nodes.get(node_id)
        if node is None:
            raise GraphError(f"node not found: {node_id}")
        return node


_GRAPH: OrgGraph | None = None


def get_org_graph() -> OrgGraph:
    """Return the process-scoped operational memory graph singleton."""
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = OrgGraph()
    return _GRAPH


def reset_org_graph() -> None:
    """Test helper: drop the cached graph."""
    global _GRAPH
    _GRAPH = None


__all__ = [
    "GraphError",
    "OrgGraph",
    "get_org_graph",
    "reset_org_graph",
]
