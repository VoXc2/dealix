"""Thin adapters that re-export builder helpers as a stable surface
for tests and the router."""
from auto_client_acquisition.unified_operating_graph.builder import (
    build_graph_for_customer,
    list_known_node_types,
)

__all__ = ["build_graph_for_customer", "list_known_node_types"]
