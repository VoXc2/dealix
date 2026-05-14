"""Evidence Control Graph — wraps auditability_os.evidence_chain + adds
gap detection + compliance summary.

Returns a single composite object used by the enterprise Trust Pack PDF.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class EvidenceControlGraph:
    customer_id: str
    project_id: str
    generated_at: str
    nodes: list[dict[str, Any]] = field(default_factory=list)
    edges: list[dict[str, Any]] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    compliance: dict[str, Any] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Evidence Control Plane — {self.customer_id}")
        if self.project_id:
            lines.append(f"_Project: {self.project_id}_")
        lines.append(f"_Generated: {self.generated_at}_")
        lines.append(f"_Governance: {self.governance_decision}_")
        lines.append(f"_Nodes: {len(self.nodes)} | Edges: {len(self.edges)}_")
        lines.append("")
        if self.gaps:
            lines.append(f"## Gaps detected ({len(self.gaps)})")
            for g in self.gaps:
                lines.append(f"- {g}")
            lines.append("")
        if self.compliance:
            lines.append("## Compliance summary")
            for k, v in self.compliance.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")
        if self.nodes:
            lines.append(f"## Nodes by type")
            by_type: dict[str, int] = {}
            for n in self.nodes:
                t = n.get("node_type") or n.get("type") or "unknown"
                by_type[t] = by_type.get(t, 0) + 1
            for k, v in by_type.items():
                lines.append(f"- {k}: {v}")
            lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated outcomes are not guaranteed outcomes / "
            "النتائج التقديرية ليست نتائج مضمونة._"
        )
        return "\n".join(lines)


def build_control_graph(
    *, customer_id: str, project_id: str = ""
) -> EvidenceControlGraph:
    """Compose the canonical evidence control graph.

    Best-effort composition — never raises. Missing data sources surface
    as gaps instead of exceptions.
    """
    from auto_client_acquisition.auditability_os.evidence_chain import build_chain
    from auto_client_acquisition.evidence_control_plane_os.compliance_index import (
        build_compliance_index,
    )
    from auto_client_acquisition.evidence_control_plane_os.gap_detector import find_gaps

    base = build_chain(customer_id=customer_id, engagement_id=project_id)
    base_dict = base.to_dict()
    gaps = find_gaps(customer_id=customer_id, project_id=project_id)
    compliance = build_compliance_index(customer_id=customer_id).to_dict()

    return EvidenceControlGraph(
        customer_id=customer_id,
        project_id=project_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        nodes=base_dict.get("nodes", []),
        edges=base_dict.get("edges", []),
        gaps=[g.label for g in gaps],
        compliance=compliance,
        governance_decision=base_dict.get("governance_decision", "allow_with_review"),
    )


__all__ = ["EvidenceControlGraph", "build_control_graph"]
