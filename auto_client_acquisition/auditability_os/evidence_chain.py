"""Evidence Chain — builds the full audit graph for one engagement.

Composes:
  Source Passport → AI Run → Policy Check → Governance Decision →
  Human Review → Approval → Output → Proof Pack → Value Event → Capital Asset

Returns a single EvidenceChain with all nodes + edges. Markdown render
supported for enterprise procurement reports.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.auditability_os.audit_event import list_events as list_audit
from auto_client_acquisition.capital_os.capital_ledger import list_assets
from auto_client_acquisition.friction_log.aggregator import aggregate as friction_agg
from auto_client_acquisition.value_os.value_ledger import list_events as list_value


@dataclass
class EvidenceNode:
    node_id: str
    node_type: str  # source / ai_run / policy / decision / approval / output / proof / value / capital / friction
    label: str
    timestamp: str = ""
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceEdge:
    from_node: str
    to_node: str
    relation: str  # "produced" | "checked" | "approved" | "linked"


@dataclass
class EvidenceChain:
    customer_id: str
    engagement_id: str
    generated_at: str
    nodes: list[EvidenceNode] = field(default_factory=list)
    edges: list[EvidenceEdge] = field(default_factory=list)
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "engagement_id": self.engagement_id,
            "generated_at": self.generated_at,
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
            "governance_decision": self.governance_decision,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
        }

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Evidence Chain — {self.customer_id} / {self.engagement_id}")
        lines.append(f"_Generated: {self.generated_at}_")
        lines.append(f"_Governance: {self.governance_decision}_")
        lines.append(f"_Nodes: {len(self.nodes)} | Edges: {len(self.edges)}_")
        lines.append("")
        groups: dict[str, list[EvidenceNode]] = {}
        for n in self.nodes:
            groups.setdefault(n.node_type, []).append(n)
        for node_type in (
            "source", "ai_run", "policy", "decision", "approval",
            "output", "proof", "value", "capital", "friction",
        ):
            items = groups.get(node_type, [])
            if not items:
                continue
            lines.append(f"## {node_type.title()} ({len(items)})")
            for n in items[:20]:
                lines.append(f"- `{n.node_id}` — {n.label} ({n.timestamp})")
            lines.append("")
        if self.edges:
            lines.append(f"## Edges ({len(self.edges)})")
            for e in self.edges[:50]:
                lines.append(f"- `{e.from_node}` --[{e.relation}]--> `{e.to_node}`")
            lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._"
        )
        return "\n".join(lines)


def build_chain(*, customer_id: str, engagement_id: str = "") -> EvidenceChain:
    """Compose the evidence chain from existing ledgers."""
    nodes: list[EvidenceNode] = []
    edges: list[EvidenceEdge] = []

    # Audit events as decision/policy/approval nodes
    audit = list_audit(
        customer_id=customer_id, engagement_id=engagement_id or None, limit=500
    )
    for ev in audit:
        ntype = _audit_kind_to_node_type(ev.kind)
        node = EvidenceNode(
            node_id=ev.event_id,
            node_type=ntype,
            label=f"{ev.kind} by {ev.actor or 'system'}",
            timestamp=ev.occurred_at,
            payload={
                "decision": ev.decision,
                "policy_checked": ev.policy_checked,
                "summary": ev.summary,
            },
        )
        nodes.append(node)
        for src in ev.source_refs:
            edges.append(EvidenceEdge(from_node=src, to_node=ev.event_id, relation="checked"))
        for out in ev.output_refs:
            edges.append(EvidenceEdge(from_node=ev.event_id, to_node=out, relation="produced"))

    # Proof ledger events
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger
        ledger = get_default_ledger()
        proof_events = ledger.list_events(customer_handle=customer_id, limit=50)
        for pe in proof_events:
            nodes.append(EvidenceNode(
                node_id=pe.id,
                node_type="proof",
                label=f"{pe.event_type}",
                timestamp=pe.created_at.isoformat(),
                payload={"approval_status": pe.approval_status, "risk_level": pe.risk_level},
            ))
    except Exception:  # noqa: BLE001
        pass

    # Value events
    try:
        value_events = list_value(customer_id=customer_id, limit=50)
        for ve in value_events:
            nodes.append(EvidenceNode(
                node_id=ve.event_id,
                node_type="value",
                label=f"{ve.kind} ({ve.tier}) = {ve.amount}",
                timestamp=ve.occurred_at,
                payload={"tier": ve.tier, "source_ref": ve.source_ref, "amount": ve.amount},
            ))
            if ve.source_ref:
                edges.append(EvidenceEdge(
                    from_node=ve.source_ref, to_node=ve.event_id, relation="linked"
                ))
    except Exception:  # noqa: BLE001
        pass

    # Capital assets
    try:
        assets = list_assets(customer_id=customer_id, engagement_id=engagement_id or None, limit=50)
        for a in assets:
            nodes.append(EvidenceNode(
                node_id=a.asset_id,
                node_type="capital",
                label=f"{a.asset_type} owned by {a.owner}",
                timestamp=a.created_at,
                payload={"asset_type": a.asset_type, "asset_ref": a.asset_ref, "reusable": a.reusable},
            ))
    except Exception:  # noqa: BLE001
        pass

    # Friction summary as a single node
    try:
        fagg = friction_agg(customer_id=customer_id, window_days=90)
        if fagg.total > 0:
            nodes.append(EvidenceNode(
                node_id=f"friction_{customer_id}_summary",
                node_type="friction",
                label=f"{fagg.total} friction events / cost {fagg.total_cost_minutes}min",
                timestamp=datetime.now(timezone.utc).isoformat(),
                payload=fagg.to_dict(),
            ))
    except Exception:  # noqa: BLE001
        pass

    return EvidenceChain(
        customer_id=customer_id,
        engagement_id=engagement_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        nodes=nodes,
        edges=edges,
        governance_decision="allow_with_review",
    )


def _audit_kind_to_node_type(kind: str) -> str:
    if kind == "source_passport_validated":
        return "source"
    if kind == "ai_run":
        return "ai_run"
    if kind == "policy_check":
        return "policy"
    if kind == "governance_decision":
        return "decision"
    if kind in ("human_review", "approval_granted", "approval_rejected"):
        return "approval"
    if kind == "output_delivered":
        return "output"
    if kind == "proof_pack_assembled":
        return "proof"
    if kind == "value_event_recorded":
        return "value"
    if kind == "capital_asset_registered":
        return "capital"
    return "ai_run"


__all__ = ["EvidenceChain", "EvidenceEdge", "EvidenceNode", "build_chain"]
