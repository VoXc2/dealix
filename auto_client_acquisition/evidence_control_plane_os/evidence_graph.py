"""Evidence graph — minimal chain validation + control-graph builder.

:func:`build_control_graph` composes the audit log, the evidence store,
the compliance index and the gap detector into a single control graph
that procurement can read in JSON or markdown.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

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

_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)


def mini_evidence_chain_complete(chain: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in MINI_CHAIN_KEYS if not (chain.get(k) or "").strip()]
    return not missing, tuple(missing)


@dataclass(frozen=True, slots=True)
class ControlGraphNode:
    """A single node in the evidence control graph."""

    node_id: str
    node_type: str
    label: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ControlGraphEdge:
    """A directed edge linking two control-graph nodes."""

    src: str
    dst: str
    relation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EvidenceControlGraph:
    """The assembled evidence control graph for a customer."""

    customer_id: str
    project_id: str
    generated_at: str
    nodes: list[ControlGraphNode] = field(default_factory=list)
    edges: list[ControlGraphEdge] = field(default_factory=list)
    gaps: list[dict[str, Any]] = field(default_factory=list)
    compliance: dict[str, Any] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "project_id": self.project_id,
            "generated_at": self.generated_at,
            "node_count": len(self.nodes),
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "gaps": self.gaps,
            "compliance": self.compliance,
            "governance_decision": self.governance_decision,
            "disclaimer": _DISCLAIMER,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Evidence Control Plane — {self.customer_id}",
            "",
        ]
        if self.project_id:
            lines.append(f"**Project:** {self.project_id}")
        lines.append(f"**Governance:** {self.governance_decision}")
        lines.append(f"**Generated:** {self.generated_at}")
        lines.append("")
        lines.append(f"## Nodes ({len(self.nodes)})")
        for node in self.nodes:
            lines.append(f"- [{node.node_type}] {node.label}")
        if not self.nodes:
            lines.append("- (no evidence recorded yet)")
        lines.append("")
        lines.append("## Compliance Coverage")
        for framework, count in self.compliance.get("by_framework", {}).items():
            lines.append(f"- {framework}: {count} controls")
        lines.append("")
        lines.append(f"## Gaps ({len(self.gaps)})")
        for gap in self.gaps:
            lines.append(f"- [{gap.get('severity')}] {gap.get('label')}")
        if not self.gaps:
            lines.append("- No gaps detected.")
        lines.append("")
        lines.append(f"_{_DISCLAIMER}_")
        return "\n".join(lines)


def build_control_graph(
    *,
    customer_id: str,
    project_id: str = "",
) -> EvidenceControlGraph:
    """Assemble a customer's evidence control graph.

    Composes audit events, evidence items, compliance index and detected
    gaps into a single graph. Each data source is read defensively so a
    missing store degrades the graph rather than raising.
    """
    nodes: list[ControlGraphNode] = []
    edges: list[ControlGraphEdge] = []

    # Audit-log events.
    try:
        from auto_client_acquisition.auditability_os.audit_event import list_events

        for ev in list_events(customer_id=customer_id, limit=500):
            node_id = f"audit:{ev.occurred_at}:{ev.kind}"
            nodes.append(
                ControlGraphNode(
                    node_id=node_id,
                    node_type=f"audit_{ev.kind}",
                    label=ev.summary or ev.kind,
                )
            )
    except Exception:  # noqa: BLE001
        pass

    # Evidence-control-plane items.
    try:
        from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
            list_evidence,
        )

        for item in list_evidence(customer_id=customer_id, limit=500):
            if project_id and item.project_id != project_id:
                continue
            nodes.append(
                ControlGraphNode(
                    node_id=item.evidence_id,
                    node_type=f"evidence_{item.type}",
                    label=item.summary or item.type,
                )
            )
            for src in item.source_ids:
                edges.append(
                    ControlGraphEdge(
                        src=src, dst=item.evidence_id, relation="source_of"
                    )
                )
    except Exception:  # noqa: BLE001
        pass

    # Compliance index.
    compliance: dict[str, Any] = {"by_framework": {}, "items": []}
    try:
        from auto_client_acquisition.evidence_control_plane_os.compliance_index import (
            build_compliance_index,
        )

        idx = build_compliance_index(customer_id=customer_id)
        compliance = idx.to_dict()
    except Exception:  # noqa: BLE001
        pass
    compliance.setdefault("by_framework", {})

    # Gap detection.
    gaps: list[dict[str, Any]] = []
    try:
        from auto_client_acquisition.evidence_control_plane_os.gap_detector import (
            find_gaps,
        )

        gaps = [g.to_dict() for g in find_gaps(customer_id=customer_id, project_id=project_id)]
    except Exception:  # noqa: BLE001
        pass

    has_high_gap = any(g.get("severity") == "high" for g in gaps)
    governance_decision = "allow_with_review" if has_high_gap else "allow"

    return EvidenceControlGraph(
        customer_id=customer_id,
        project_id=project_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        nodes=nodes,
        edges=edges,
        gaps=gaps,
        compliance=compliance,
        governance_decision=governance_decision,
    )


__all__ = [
    "MINI_CHAIN_KEYS",
    "ControlGraphEdge",
    "ControlGraphNode",
    "EvidenceControlGraph",
    "build_control_graph",
    "mini_evidence_chain_complete",
]
