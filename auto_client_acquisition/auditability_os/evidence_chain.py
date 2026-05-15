"""Evidence chain primitives for auditability (parallel to evidence_control_plane_os).

The :func:`build_chain` builder turns the customer-scoped audit log into a
linked evidence chain — source passports, AI runs, governance decisions —
that procurement can read in JSON or markdown.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    list_events,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import (
    MINI_CHAIN_KEYS,
)

EVIDENCE_CHAIN_STAGES: tuple[str, ...] = MINI_CHAIN_KEYS

_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)

# Maps audit event kinds to evidence-chain node types.
_NODE_TYPE_BY_KIND: dict[str, str] = {
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
    """A single node in a customer's evidence chain."""

    node_type: str
    kind: str
    actor: str
    summary: str
    decision: str
    occurred_at: str
    source_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EvidenceChain:
    """A customer's full evidence chain assembled from the audit log."""

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
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Evidence Chain — {self.customer_id}",
            "",
        ]
        if self.engagement_id:
            lines.append(f"**Engagement:** {self.engagement_id}")
            lines.append("")
        lines.append(f"**Nodes:** {self.node_count}")
        lines.append("")
        for i, node in enumerate(self.nodes, start=1):
            lines.append(f"## {i}. {node.node_type} ({node.kind})")
            lines.append(f"- Actor: {node.actor}")
            if node.decision:
                lines.append(f"- Decision: {node.decision}")
            if node.summary:
                lines.append(f"- Summary: {node.summary}")
            if node.source_refs:
                lines.append(f"- Sources: {', '.join(node.source_refs)}")
            if node.output_refs:
                lines.append(f"- Outputs: {', '.join(node.output_refs)}")
            lines.append(f"- When: {node.occurred_at}")
            lines.append("")
        lines.append(f"_{_DISCLAIMER}_")
        return "\n".join(lines)


def build_chain(*, customer_id: str, engagement_id: str = "") -> EvidenceChain:
    """Assemble a customer's evidence chain from the audit log.

    When ``engagement_id`` is given, only events for that engagement are
    included; otherwise every audit event for the customer is used.
    """
    events = list_events(customer_id=customer_id, limit=1000)
    nodes: list[EvidenceNode] = []
    for ev in events:
        if engagement_id and ev.engagement_id != engagement_id:
            continue
        nodes.append(
            EvidenceNode(
                node_type=_NODE_TYPE_BY_KIND.get(ev.kind, ev.kind),
                kind=ev.kind,
                actor=ev.actor,
                summary=ev.summary,
                decision=ev.decision,
                occurred_at=ev.occurred_at,
                source_refs=list(ev.source_refs),
                output_refs=list(ev.output_refs),
            )
        )
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
