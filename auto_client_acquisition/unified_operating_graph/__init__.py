"""Unified Operating Graph — read-model over existing modules.

NOT a new database. Composes 12 node types + 7 edge types from
existing Wave 3 modules (leadops_spine, customer_brain, service_sessions,
approval_center, payment_ops, support_inbox, proof_ledger,
case_study_engine, executive_pack_v2) using the safe_call adapter.

Empty state returns insufficient_data. Missing module returns degraded.
Customer-facing summary uses customer_safe_label scrubbing.
"""
from auto_client_acquisition.unified_operating_graph.builder import (
    build_graph_for_customer,
    list_known_node_types,
)
from auto_client_acquisition.unified_operating_graph.summarizer import (
    summarize_graph_for_customer,
)

__all__ = [
    "build_graph_for_customer",
    "list_known_node_types",
    "summarize_graph_for_customer",
]
