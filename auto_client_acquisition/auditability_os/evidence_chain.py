"""Evidence chain primitives for auditability (parallel to evidence_control_plane_os).

Two layers:

  * :data:`EVIDENCE_CHAIN_STAGES` / :func:`evidence_chain_complete` — the
    static stage contract for a minimal auditable story.
  * :func:`build_chain` — assembles a customer evidence chain from the
    recorded audit events (JSONL ledger), for procurement-grade export.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    AuditLogEntry,
    list_events,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import MINI_CHAIN_KEYS

EVIDENCE_CHAIN_STAGES: tuple[str, ...] = MINI_CHAIN_KEYS

_DISCLAIMER = "Estimated outcomes are not guaranteed outcomes — النتائج المقدّرة ليست نتائج مضمونة"

# Audit event kind -> evidence chain node type.
_KIND_TO_NODE_TYPE: dict[str, str] = {
    AuditEventKind.SOURCE_PASSPORT_VALIDATED.value: "source",
    AuditEventKind.AI_RUN.value: "ai_run",
    AuditEventKind.GOVERNANCE_DECISION.value: "decision",
    AuditEventKind.HUMAN_REVIEW.value: "review",
    AuditEventKind.APPROVAL.value: "approval",
    AuditEventKind.EXTERNAL_SEND.value: "output",
    AuditEventKind.OUTPUT_PUBLISHED.value: "output",
}


def evidence_chain_complete(present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = tuple(k for k in EVIDENCE_CHAIN_STAGES if k not in present)
    return not missing, missing


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    """A single node in a customer evidence chain, derived from an audit event."""

    node_type: str
    kind: str
    actor: str
    summary: str
    source_refs: tuple[str, ...]
    output_refs: tuple[str, ...]
    decision: str
    occurred_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_type": self.node_type,
            "kind": self.kind,
            "actor": self.actor,
            "summary": self.summary,
            "source_refs": list(self.source_refs),
            "output_refs": list(self.output_refs),
            "decision": self.decision,
            "occurred_at": self.occurred_at,
        }


@dataclass(frozen=True, slots=True)
class EvidenceChain:
    """A customer's ordered evidence chain assembled from audit events."""

    customer_id: str
    engagement_id: str = ""
    nodes: list[EvidenceNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "engagement_id": self.engagement_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "node_count": len(self.nodes),
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Evidence Chain — {self.customer_id}",
            "",
        ]
        if self.engagement_id:
            lines.append(f"Engagement: {self.engagement_id}")
            lines.append("")
        lines.append(f"Nodes: {len(self.nodes)}")
        lines.append("")
        for idx, node in enumerate(self.nodes, start=1):
            lines.append(f"## {idx}. {node.node_type} ({node.kind})")
            lines.append(f"- Actor: {node.actor}")
            if node.decision:
                lines.append(f"- Decision: {node.decision}")
            if node.source_refs:
                lines.append(f"- Source refs: {', '.join(node.source_refs)}")
            if node.output_refs:
                lines.append(f"- Output refs: {', '.join(node.output_refs)}")
            if node.summary:
                lines.append(f"- Summary: {node.summary}")
            lines.append(f"- Recorded: {node.occurred_at}")
            lines.append("")
        lines.append("---")
        lines.append(f"_{_DISCLAIMER}_")
        return "\n".join(lines)


def _to_node(entry: AuditLogEntry) -> EvidenceNode:
    return EvidenceNode(
        node_type=_KIND_TO_NODE_TYPE.get(entry.kind, "event"),
        kind=entry.kind,
        actor=entry.actor,
        summary=entry.summary,
        source_refs=tuple(entry.source_refs),
        output_refs=tuple(entry.output_refs),
        decision=entry.decision,
        occurred_at=entry.occurred_at,
    )


def build_chain(*, customer_id: str, engagement_id: str = "") -> EvidenceChain:
    """Assemble a customer evidence chain from recorded audit events."""
    entries = list_events(
        customer_id=customer_id,
        engagement_id=engagement_id or None,
    )
    return EvidenceChain(
        customer_id=customer_id,
        engagement_id=engagement_id,
        nodes=[_to_node(e) for e in entries],
    )


__all__ = [
    "EVIDENCE_CHAIN_STAGES",
    "EvidenceChain",
    "EvidenceNode",
    "build_chain",
    "evidence_chain_complete",
]
