"""Customer Brain — per-customer operational memory.

Aggregates from existing modules (crm_v10, customer_loop,
proof_ledger, support_os, market_intelligence, leadops_spine).

Read-only composition — never writes back to the source modules.
"""
from auto_client_acquisition.customer_brain.builder import (
    build_snapshot,
    get_snapshot,
    list_known_customers,
)
from auto_client_acquisition.customer_brain.context_pack import context_pack

__all__ = [
    "build_snapshot",
    "context_pack",
    "get_snapshot",
    "list_known_customers",
]
