"""Evidence chain primitives for auditability and export APIs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.evidence_control_plane_os.evidence_graph import MINI_CHAIN_KEYS

EVIDENCE_CHAIN_STAGES: tuple[str, ...] = MINI_CHAIN_KEYS


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    node_id: str
    node_type: str
    label: str
    occurred_at: str
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceChain:
    customer_id: str
    engagement_id: str = ""
    nodes: list[EvidenceNode] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "engagement_id": self.engagement_id,
            "generated_at": self.generated_at,
            "node_count": self.node_count,
            "nodes": [n.to_dict() for n in self.nodes],
        }

    def to_markdown(self) -> str:
        lines: list[str] = [
            f"# Evidence Chain — {self.customer_id}",
            "",
            f"_Generated: {self.generated_at}_",
            "",
            "## Nodes",
        ]
        if not self.nodes:
            lines.append("- (no events yet)")
        for n in self.nodes:
            lines.append(f"- [{n.node_type}] {n.label} ({n.occurred_at})")
        lines.extend(
            [
                "",
                "---",
                "_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._",
            ],
        )
        return "\n".join(lines)


def evidence_chain_complete(present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = tuple(k for k in EVIDENCE_CHAIN_STAGES if k not in present)
    return not missing, missing


def _node_type_for_kind(kind: str) -> str:
    k = (kind or "").lower()
    if k == "source_passport_validated":
        return "source"
    if k == "ai_run":
        return "ai_run"
    if k == "governance_decision":
        return "decision"
    return "event"


def build_chain(*, customer_id: str, engagement_id: str = "") -> EvidenceChain:
    """Construct minimal evidence chain from audit log events."""
    from auto_client_acquisition.auditability_os.audit_event import list_events

    events = list_events(customer_id=customer_id, engagement_id=engagement_id, limit=1000)
    nodes: list[EvidenceNode] = []
    for ev in reversed(events):
        label = ev.summary or ev.kind
        if ev.decision:
            label = f"{label} | decision={ev.decision}"
        nodes.append(
            EvidenceNode(
                node_id=ev.event_id,
                node_type=_node_type_for_kind(ev.kind),
                label=label,
                occurred_at=ev.occurred_at,
                meta={
                    "kind": ev.kind,
                    "actor": ev.actor,
                    "source_refs": list(ev.source_refs),
                    "output_refs": list(ev.output_refs),
                },
            ),
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
