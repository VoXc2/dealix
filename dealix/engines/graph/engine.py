"""
Organizational Graph Engine (Engine 6).

Net-new domain — relationships across people, decisions, approvals,
workflows, customers, risks, and knowledge. Phase 0 ships a working
in-memory directed graph (Pilot status: built, internal-only, not yet
persisted). Persistence and graph analytics are Planned for phase 3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.engines.base import BaseEngine
from dealix.engines.registry import ENGINE_REGISTRY


@dataclass
class Node:
    node_id: str
    kind: str  # person | decision | approval | workflow | customer | risk | knowledge
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    source_id: str
    target_id: str
    relationship: str
    attributes: dict[str, Any] = field(default_factory=dict)


class GraphEngine(BaseEngine):
    """In-memory organizational relationship graph."""

    spec = ENGINE_REGISTRY.get("graph")

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []

    def add_node(self, node_id: str, kind: str, **attributes: Any) -> Node:
        node = Node(node_id=node_id, kind=kind, attributes=dict(attributes))
        self._nodes[node_id] = node
        return node

    def add_edge(
        self, source_id: str, target_id: str, relationship: str, **attributes: Any
    ) -> Edge:
        if source_id not in self._nodes:
            raise KeyError(f"Unknown source node: {source_id}")
        if target_id not in self._nodes:
            raise KeyError(f"Unknown target node: {target_id}")
        edge = Edge(source_id, target_id, relationship, dict(attributes))
        self._edges.append(edge)
        return edge

    def neighbors(self, node_id: str) -> list[str]:
        if node_id not in self._nodes:
            raise KeyError(f"Unknown node: {node_id}")
        return [e.target_id for e in self._edges if e.source_id == node_id]

    def query(self, *args: Any, **kwargs: Any) -> Any:
        """Graph analytics (centrality, paths) — Planned for phase 3."""
        raise self._planned("query")

    def _domain_report(self) -> dict[str, Any]:
        return {
            "node_count": len(self._nodes),
            "edge_count": len(self._edges),
            "capabilities": {
                "add_node": "built",
                "add_edge": "built",
                "neighbors": "built",
                "query": "planned",
            },
        }
