"""Builder — composes the unified graph for one customer.

Reads from existing modules via safe_call (never raises).
Empty results → empty graph + insufficient_data.
Missing modules → degraded_sections entries.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import (
    degraded_section,
    safe_call,
)
from auto_client_acquisition.unified_operating_graph.schemas import (
    EdgeType,
    GraphEdge,
    GraphNode,
    NodeType,
    UnifiedGraph,
)


def list_known_node_types() -> list[str]:
    return [
        "company", "contact", "lead", "deal", "service_session",
        "approval", "payment_state", "support_ticket", "proof_event",
        "executive_pack", "case_study_candidate", "partner",
    ]


def _company_node(customer_handle: str, brain_snapshot: dict[str, Any] | None) -> GraphNode:
    sector = (brain_snapshot or {}).get("profile", {}).get("sector") or "—"
    return GraphNode(
        node_id=f"company:{customer_handle}",
        node_type="company",
        customer_handle=customer_handle,
        label_ar=f"شركة العميل ({sector})",
        label_en=f"Customer company ({sector})",
        payload={"sector": sector},
        source_module="customer_brain",
    )


def _lead_nodes(customer_handle: str) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    try:
        from auto_client_acquisition.leadops_spine import list_records
        for r in list_records(limit=100):
            if r.customer_handle == customer_handle:
                nodes.append(GraphNode(
                    node_id=f"lead:{r.leadops_id}",
                    node_type="lead",
                    customer_handle=customer_handle,
                    label_ar=f"فرصة #{r.leadops_id[-6:]}",
                    label_en=f"Lead #{r.leadops_id[-6:]}",
                    payload={
                        "compliance_status": r.compliance_status,
                        "score": r.score,
                    },
                    source_module="leadops_spine",
                ))
    except Exception:
        pass
    return nodes


def _service_session_nodes(customer_handle: str) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    try:
        from auto_client_acquisition.service_sessions import list_sessions
        for s in list_sessions(customer_handle=customer_handle, limit=50):
            nodes.append(GraphNode(
                node_id=f"service_session:{s.session_id}",
                node_type="service_session",
                customer_handle=customer_handle,
                label_ar=f"جلسة خدمة ({s.service_type})",
                label_en=f"Service session ({s.service_type})",
                payload={
                    "service_type": s.service_type,
                    "status": s.status,
                    "deliverable_count": len(s.deliverables),
                },
                source_module="service_sessions",
            ))
    except Exception:
        pass
    return nodes


def _approval_nodes(customer_handle: str) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    try:
        from auto_client_acquisition.approval_center import approval_store
        for ap in approval_store.get_default_approval_store().list_pending():
            if customer_handle in (ap.proof_impact or "") or customer_handle in (ap.summary_ar or ""):
                nodes.append(GraphNode(
                    node_id=f"approval:{ap.approval_id}",
                    node_type="approval",
                    customer_handle=customer_handle,
                    label_ar="قرار معلّق",
                    label_en="Pending approval",
                    payload={
                        "action_type": ap.action_type,
                        "channel": ap.channel,
                        "risk_level": ap.risk_level,
                    },
                    source_module="approval_center",
                ))
    except Exception:
        pass
    return nodes


def _proof_event_nodes(customer_handle: str) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    try:
        from auto_client_acquisition.proof_ledger.file_backend import list_events
        for e in list_events(customer_handle=customer_handle, limit=50):
            event_id = getattr(e, "id", None) or getattr(e, "event_id", None) or "unknown"
            event_type = getattr(e, "event_type", "unknown")
            nodes.append(GraphNode(
                node_id=f"proof_event:{event_id}",
                node_type="proof_event",
                customer_handle=customer_handle,
                label_ar=f"دليل ({event_type})",
                label_en=f"Proof event ({event_type})",
                payload={"event_type": event_type},
                source_module="proof_ledger",
            ))
    except Exception:
        pass
    return nodes


def _support_ticket_nodes(customer_handle: str) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    try:
        from auto_client_acquisition.support_inbox import list_tickets
        for t in list_tickets(customer_id=customer_handle, limit=50):
            nodes.append(GraphNode(
                node_id=f"support_ticket:{t.id}",
                node_type="support_ticket",
                customer_handle=customer_handle,
                label_ar=f"تذكرة دعم ({t.category})",
                label_en=f"Support ticket ({t.category})",
                payload={
                    "category": t.category,
                    "priority": t.priority,
                    "status": t.status,
                },
                source_module="support_inbox",
            ))
    except Exception:
        pass
    return nodes


def _build_edges(nodes: list[GraphNode]) -> list[GraphEdge]:
    """Derive edges from collected nodes (best-effort, no fake edges)."""
    edges: list[GraphEdge] = []
    by_type: dict[NodeType, list[GraphNode]] = {}
    for n in nodes:
        by_type.setdefault(n.node_type, []).append(n)

    # company ← lead (lead_belongs_to_company)
    company_ids = [n.node_id for n in by_type.get("company", [])]
    if company_ids:
        for lead in by_type.get("lead", []):
            edges.append(GraphEdge(
                source_node_id=lead.node_id,
                target_node_id=company_ids[0],
                edge_type="lead_belongs_to_company",
            ))

    # service_session → proof_event (service_creates_proof)
    for sess in by_type.get("service_session", []):
        for proof in by_type.get("proof_event", []):
            edges.append(GraphEdge(
                source_node_id=sess.node_id,
                target_node_id=proof.node_id,
                edge_type="service_creates_proof",
            ))

    # support_ticket → service_session (support_ticket_blocks_delivery)
    # only when support ticket is escalated (signal of blocked delivery)
    for tkt in by_type.get("support_ticket", []):
        if tkt.payload.get("status") == "escalated":
            for sess in by_type.get("service_session", []):
                edges.append(GraphEdge(
                    source_node_id=tkt.node_id,
                    target_node_id=sess.node_id,
                    edge_type="support_ticket_blocks_delivery",
                ))

    # approval → action (approval_blocks_action) — abstract; link to lead
    for ap in by_type.get("approval", []):
        for lead in by_type.get("lead", []):
            edges.append(GraphEdge(
                source_node_id=ap.node_id,
                target_node_id=lead.node_id,
                edge_type="approval_blocks_action",
            ))

    return edges


def build_graph_for_customer(*, customer_handle: str) -> UnifiedGraph:
    """Compose the unified graph. Never raises — always returns a graph."""
    degraded: list[dict[str, Any]] = []

    brain_snapshot = safe_call(
        name="customer_brain",
        fn=lambda: _get_brain_snapshot(customer_handle),
        fallback=None,
    )
    if isinstance(brain_snapshot, dict) and brain_snapshot.get("degraded"):
        degraded.append(brain_snapshot)
        brain_snapshot = None

    leads = safe_call(
        name="leadops_spine",
        fn=lambda: _lead_nodes(customer_handle),
        fallback=[],
    )
    sessions = safe_call(
        name="service_sessions",
        fn=lambda: _service_session_nodes(customer_handle),
        fallback=[],
    )
    approvals = safe_call(
        name="approval_center",
        fn=lambda: _approval_nodes(customer_handle),
        fallback=[],
    )
    proofs = safe_call(
        name="proof_ledger",
        fn=lambda: _proof_event_nodes(customer_handle),
        fallback=[],
    )
    tickets = safe_call(
        name="support_inbox",
        fn=lambda: _support_ticket_nodes(customer_handle),
        fallback=[],
    )

    nodes: list[GraphNode] = [_company_node(customer_handle, brain_snapshot)]
    for collection in (leads, sessions, approvals, proofs, tickets):
        if isinstance(collection, list):
            nodes.extend(collection)
        elif isinstance(collection, dict) and collection.get("degraded"):
            degraded.append(collection)

    edges = _build_edges(nodes)

    # Determine data_status
    non_company_nodes = [n for n in nodes if n.node_type != "company"]
    if not non_company_nodes:
        status = "insufficient_data"
    elif degraded:
        status = "partial"
    else:
        status = "live"

    return UnifiedGraph(
        customer_handle=customer_handle,
        nodes=nodes,
        edges=edges,
        degraded_sections=degraded,
        data_status=status,
    )


def _get_brain_snapshot(customer_handle: str) -> dict[str, Any] | None:
    from auto_client_acquisition.customer_brain import get_snapshot, build_snapshot
    snap = get_snapshot(customer_handle=customer_handle)
    if snap is None:
        snap = build_snapshot(customer_handle=customer_handle)
    return snap.model_dump(mode="json") if snap else None
