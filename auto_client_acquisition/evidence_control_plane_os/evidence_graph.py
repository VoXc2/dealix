"""Evidence graph — minimal chain validation + control-plane graph builder.

Two layers:

  * :data:`MINI_CHAIN_KEYS` / :func:`mini_evidence_chain_complete` — the
    static minimal-chain contract for linked artifacts.
  * :func:`build_control_graph` — assembles a customer evidence control
    graph (nodes + edges + gaps + compliance summary) for the control-plane
    endpoints, reusing audit events, gap detection, and the compliance index.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.evidence_control_plane_os.compliance_index import (
    build_compliance_index,
)
from auto_client_acquisition.evidence_control_plane_os.gap_detector import find_gaps

# Keys for a minimal auditable story (see docs/evidence_control_plane/EVIDENCE_GRAPH.md)
MINI_CHAIN_KEYS: tuple[str, ...] = (
    "source",
    "used_by",
    "produced",
    "governed_by",
    "reviewed_by",
    "supports",
    "created_value",
)

_DISCLAIMER = "Estimated outcomes are not guaranteed outcomes — النتائج المقدّرة ليست نتائج مضمونة"

# Audit event kind -> control-graph node type.
_KIND_TO_NODE_TYPE: dict[str, str] = {
    "source_passport_validated": "source",
    "ai_run": "ai_run",
    "governance_decision": "decision",
    "human_review": "review",
    "approval": "approval",
    "external_send": "output",
    "output_published": "output",
}


def mini_evidence_chain_complete(chain: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in MINI_CHAIN_KEYS if not (chain.get(k) or "").strip()]
    return not missing, tuple(missing)


@dataclass(frozen=True, slots=True)
class ControlGraphNode:
    """A node in the evidence control graph, derived from an audit event."""

    node_id: str
    node_type: str
    kind: str
    actor: str
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "kind": self.kind,
            "actor": self.actor,
            "summary": self.summary,
        }


@dataclass(frozen=True, slots=True)
class ControlGraphEdge:
    """A directed edge linking two control-graph nodes."""

    src: str
    dst: str
    relation: str

    def to_dict(self) -> dict[str, Any]:
        return {"src": self.src, "dst": self.dst, "relation": self.relation}


@dataclass(frozen=True, slots=True)
class ControlGraph:
    """A customer evidence control graph: nodes + edges + gaps + compliance."""

    customer_id: str
    project_id: str = ""
    nodes: list[ControlGraphNode] = field(default_factory=list)
    edges: list[ControlGraphEdge] = field(default_factory=list)
    gaps: list[dict[str, Any]] = field(default_factory=list)
    compliance: dict[str, Any] = field(default_factory=dict)
    governance_decision: str = "allow"

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "project_id": self.project_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "gaps": self.gaps,
            "gap_count": len(self.gaps),
            "compliance": self.compliance,
            "governance_decision": self.governance_decision,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Evidence Control Plane — {self.customer_id}",
            "",
        ]
        if self.project_id:
            lines.append(f"Project: {self.project_id}")
            lines.append("")
        lines.append(f"Governance decision: {self.governance_decision}")
        lines.append(f"Nodes: {len(self.nodes)} | Edges: {len(self.edges)} "
                      f"| Gaps: {len(self.gaps)}")
        lines.append("")
        lines.append("## Nodes")
        if self.nodes:
            for idx, node in enumerate(self.nodes, start=1):
                lines.append(f"{idx}. {node.node_type} ({node.kind}) — {node.actor}")
        else:
            lines.append("_No recorded evidence nodes._")
        lines.append("")
        lines.append("## Gaps")
        if self.gaps:
            for gap in self.gaps:
                lines.append(f"- [{gap.get('severity', '?')}] {gap.get('label', '')}")
        else:
            lines.append("_No gaps detected._")
        lines.append("")
        lines.append("## Compliance")
        for framework, count in self.compliance.get("by_framework", {}).items():
            lines.append(f"- {framework}: {count} items")
        lines.append("")
        lines.append("---")
        lines.append(f"_{_DISCLAIMER}_")
        return "\n".join(lines)


def _governance_decision(gaps: list[dict[str, Any]]) -> str:
    """Derive a governance status: high-severity gaps need a human review."""
    if any(g.get("severity") == "high" for g in gaps):
        return "allow_with_review"
    return "allow"


def build_control_graph(*, customer_id: str, project_id: str = "") -> ControlGraph:
    """Assemble a customer evidence control graph.

    Nodes are derived from recorded audit events; edges chain consecutive
    nodes; gaps come from :func:`find_gaps`; the compliance summary comes
    from :func:`build_compliance_index`.
    """
    from auto_client_acquisition.auditability_os.audit_event import list_events

    events = list_events(
        customer_id=customer_id,
        engagement_id=project_id or None,
    )
    nodes: list[ControlGraphNode] = []
    for idx, event in enumerate(events):
        nodes.append(
            ControlGraphNode(
                node_id=f"n{idx}",
                node_type=_KIND_TO_NODE_TYPE.get(event.kind, "event"),
                kind=event.kind,
                actor=event.actor,
                summary=event.summary,
            ),
        )
    edges = [
        ControlGraphEdge(src=nodes[i].node_id, dst=nodes[i + 1].node_id, relation="precedes")
        for i in range(len(nodes) - 1)
    ]
    gaps = [g.to_dict() for g in find_gaps(customer_id=customer_id, project_id=project_id)]
    compliance = build_compliance_index(customer_id=customer_id).to_dict()
    return ControlGraph(
        customer_id=customer_id,
        project_id=project_id,
        nodes=nodes,
        edges=edges,
        gaps=gaps,
        compliance=compliance,
        governance_decision=_governance_decision(gaps),
    )


__all__ = [
    "MINI_CHAIN_KEYS",
    "ControlGraph",
    "ControlGraphEdge",
    "ControlGraphNode",
    "build_control_graph",
    "mini_evidence_chain_complete",
]
