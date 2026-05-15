"""Evidence chain primitives for auditability (parallel to evidence_control_plane_os).

Two layers:

* ``EVIDENCE_CHAIN_STAGES`` + ``evidence_chain_complete`` — the static
  stage-coverage check (unchanged; re-exported by the package ``__init__``).
* ``EvidenceChain`` + ``build_chain`` — derives a procurement-facing chain of
  evidence nodes from the append-only audit log.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    list_events,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import MINI_CHAIN_KEYS

EVIDENCE_CHAIN_STAGES: tuple[str, ...] = MINI_CHAIN_KEYS

_DISCLAIMER = "Estimated outcomes are not guaranteed outcomes."

# Audit-event kind → evidence-chain node type.
_KIND_TO_NODE_TYPE: dict[str, str] = {
    AuditEventKind.SOURCE_PASSPORT_VALIDATED.value: "source",
    AuditEventKind.AI_RUN.value: "ai_run",
    AuditEventKind.GOVERNANCE_DECISION.value: "decision",
    AuditEventKind.APPROVAL.value: "approval",
    AuditEventKind.OUTPUT_DELIVERED.value: "output",
    AuditEventKind.PROOF_PACK_ASSEMBLED.value: "proof_pack",
}


def evidence_chain_complete(present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = tuple(k for k in EVIDENCE_CHAIN_STAGES if k not in present)
    return not missing, missing


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    """One node in the evidence chain, derived from an audit record."""

    event_id: str
    node_type: str
    kind: str
    actor: str
    decision: str
    summary: str
    source_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    occurred_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "node_type": self.node_type,
            "kind": self.kind,
            "actor": self.actor,
            "decision": self.decision,
            "summary": self.summary,
            "source_refs": list(self.source_refs),
            "output_refs": list(self.output_refs),
            "occurred_at": self.occurred_at,
        }


@dataclass(frozen=True, slots=True)
class EvidenceChain:
    """An ordered chain of evidence nodes for one engagement / tenant."""

    customer_id: str
    engagement_id: str
    nodes: list[EvidenceNode] = field(default_factory=list)

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "engagement_id": self.engagement_id,
            "node_count": self.node_count,
            "nodes": [n.to_dict() for n in self.nodes],
            "disclaimer": _DISCLAIMER,
            "governance_decision": "allow",
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Evidence Chain — {self.customer_id}",
            "",
        ]
        if self.engagement_id:
            lines.append(f"Engagement: {self.engagement_id}")
            lines.append("")
        lines.append(f"Nodes: {self.node_count}")
        lines.append("")
        for idx, node in enumerate(self.nodes, start=1):
            lines.append(f"## {idx}. {node.node_type} ({node.kind})")
            lines.append(f"- Actor: {node.actor or 'system'}")
            if node.decision:
                lines.append(f"- Decision: {node.decision}")
            if node.source_refs:
                lines.append(f"- Source refs: {', '.join(node.source_refs)}")
            if node.output_refs:
                lines.append(f"- Output refs: {', '.join(node.output_refs)}")
            if node.summary:
                lines.append(f"- Summary: {node.summary}")
            if node.occurred_at:
                lines.append(f"- At: {node.occurred_at}")
            lines.append("")
        lines.append("---")
        lines.append(_DISCLAIMER)
        return "\n".join(lines)


def build_chain(*, customer_id: str, engagement_id: str = "") -> EvidenceChain:
    """Build an evidence chain for a tenant from the append-only audit log."""
    records = list_events(customer_id=customer_id, engagement_id=engagement_id)
    nodes = [
        EvidenceNode(
            event_id=r.event_id,
            node_type=_KIND_TO_NODE_TYPE.get(r.kind, r.kind),
            kind=r.kind,
            actor=r.actor,
            decision=r.decision,
            summary=r.summary,
            source_refs=list(r.source_refs),
            output_refs=list(r.output_refs),
            occurred_at=r.occurred_at,
        )
        for r in records
    ]
    return EvidenceChain(
        customer_id=customer_id,
        engagement_id=engagement_id,
        nodes=nodes,
    )


__all__ = [
    "EVIDENCE_CHAIN_STAGES",
    "EvidenceChain",
    "EvidenceNode",
    "build_chain",
    "evidence_chain_complete",
]
