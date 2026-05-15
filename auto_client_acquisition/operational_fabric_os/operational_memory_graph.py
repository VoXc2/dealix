"""System 30 — Operational memory graph for incident reasoning."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphEdge:
    source_id: str
    relation: str
    target_id: str


class OperationalMemoryGraph:
    def __init__(self) -> None:
        self._edges: list[GraphEdge] = []

    def add_edge(self, *, source_id: str, relation: str, target_id: str) -> None:
        src = source_id.strip()
        rel = relation.strip()
        tgt = target_id.strip()
        if not src or not rel or not tgt:
            raise ValueError("graph_edge_fields_required")
        self._edges.append(GraphEdge(source_id=src, relation=rel, target_id=tgt))

    def related(self, source_id: str, *, relation: str | None = None) -> tuple[str, ...]:
        src = source_id.strip()
        rel = (relation or "").strip()
        out = [
            edge.target_id
            for edge in self._edges
            if edge.source_id == src and (not rel or edge.relation == rel)
        ]
        return tuple(sorted(set(out)))

    def incident_context(self, incident_id: str) -> dict[str, tuple[str, ...]]:
        incident = incident_id.strip()
        return {
            "root_causes": self.related(incident, relation="caused_by"),
            "impacted_entities": self.related(incident, relation="impacts"),
            "linked_workflows": self.related(incident, relation="linked_workflow"),
            "linked_agents": self.related(incident, relation="linked_agent"),
            "resulting_risks": self.related(incident, relation="introduces_risk"),
        }
