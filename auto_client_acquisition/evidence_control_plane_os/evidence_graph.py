"""Evidence graph — minimal chain validation + control-graph assembly.

Two layers live here:

* ``mini_evidence_chain_complete`` — validates a minimal auditable story
  (unchanged; used by existing callers).
* ``build_control_graph`` — assembles a tenant-scoped ``ControlGraph`` from the
  persisted audit log, evidence store, compliance index and gap detector for
  the Evidence Control Plane.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
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


def mini_evidence_chain_complete(chain: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in MINI_CHAIN_KEYS if not (chain.get(k) or "").strip()]
    return not missing, tuple(missing)


@dataclass
class ControlGraphNode:
    """One node in the evidence control graph (an audit / evidence row)."""

    node_id: str
    kind: str
    summary: str
    source_refs: list[str] = field(default_factory=list)
    recorded_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "summary": self.summary,
            "source_refs": list(self.source_refs),
            "recorded_at": self.recorded_at,
        }


@dataclass
class ControlGraph:
    """Tenant-scoped evidence control graph for the Evidence Control Plane."""

    customer_id: str
    generated_at: str
    governance_decision: str
    nodes: list[ControlGraphNode] = field(default_factory=list)
    gaps: list[dict[str, Any]] = field(default_factory=list)
    compliance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "generated_at": self.generated_at,
            "governance_decision": self.governance_decision,
            "nodes": [n.to_dict() for n in self.nodes],
            "gaps": list(self.gaps),
            "compliance": dict(self.compliance),
        }

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Evidence Control Plane — {self.customer_id}")
        lines.append("")
        lines.append(f"**Generated:** {self.generated_at}")
        lines.append(f"**Governance decision:** {self.governance_decision}")
        lines.append("")
        lines.append("## Audit Nodes")
        if self.nodes:
            for n in self.nodes:
                refs = ", ".join(n.source_refs) if n.source_refs else "(none)"
                lines.append(f"- **{n.kind}** — {n.summary} [sources: {refs}]")
        else:
            lines.append("- (no audit events recorded yet)")
        lines.append("")
        lines.append("## Compliance Coverage")
        by_fw = self.compliance.get("by_framework", {})
        if by_fw:
            for framework, count in sorted(by_fw.items()):
                lines.append(f"- {framework}: {count} item(s)")
        else:
            lines.append("- (no compliance items)")
        lines.append("")
        lines.append("## Evidence Gaps")
        if self.gaps:
            for g in self.gaps:
                lines.append(
                    f"- [{g.get('severity', 'low')}] {g.get('label', '')}"
                )
        else:
            lines.append("- (no gaps detected)")
        lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated outcomes are not guaranteed outcomes. "
            "النتائج التقديرية ليست نتائج مضمونة._"
        )
        return "\n".join(lines)


def build_control_graph(*, customer_id: str, project_id: str = "") -> ControlGraph:
    """Assemble the evidence control graph for one tenant.

    Reads from the persisted audit log, compliance index and gap detector.
    Deterministic and defensive — never raises on missing stores.
    """
    if not customer_id:
        raise ValueError("customer_id is required")

    nodes: list[ControlGraphNode] = []
    try:
        from auto_client_acquisition.auditability_os.audit_event import list_events

        for entry in list_events(customer_id=customer_id, limit=500):
            nodes.append(
                ControlGraphNode(
                    node_id=getattr(entry, "event_id", ""),
                    kind=getattr(entry, "kind", ""),
                    summary=getattr(entry, "summary", ""),
                    source_refs=list(getattr(entry, "source_refs", []) or []),
                    recorded_at=getattr(entry, "occurred_at", "")
                    or getattr(entry, "recorded_at", ""),
                )
            )
    except Exception:  # noqa: BLE001
        pass

    compliance: dict[str, Any] = {}
    try:
        from auto_client_acquisition.evidence_control_plane_os.compliance_index import (
            build_compliance_index,
        )

        compliance = build_compliance_index(customer_id=customer_id).to_dict()
    except Exception:  # noqa: BLE001
        compliance = {"by_framework": {}, "items": []}

    gaps: list[dict[str, Any]] = []
    try:
        from auto_client_acquisition.evidence_control_plane_os.gap_detector import (
            find_gaps,
        )

        gaps = [g.to_dict() for g in find_gaps(customer_id=customer_id, project_id=project_id)]
    except Exception:  # noqa: BLE001
        gaps = []

    high_gaps = sum(1 for g in gaps if g.get("severity") == "high")
    governance_decision = "allow_with_review" if (high_gaps or gaps) else "allow"

    return ControlGraph(
        customer_id=customer_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        governance_decision=governance_decision,
        nodes=nodes,
        gaps=gaps,
        compliance=compliance,
    )


__all__ = [
    "MINI_CHAIN_KEYS",
    "ControlGraph",
    "ControlGraphNode",
    "build_control_graph",
    "mini_evidence_chain_complete",
]
