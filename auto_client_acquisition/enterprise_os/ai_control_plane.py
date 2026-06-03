"""Enterprise AI Control Plane product phases (group-level packaging)."""

from __future__ import annotations

CONTROL_PLANE_PRODUCT_PHASES: tuple[str, ...] = (
    "internal_operating_visibility",
    "client_visible_dashboards",
    "enterprise_policy_registry",
    "agent_registry_integrated",
    "audit_exports_and_risk_indexing",
)

CONTROL_PLANE_ENTERPRISE_MODULES: tuple[str, ...] = (
    "policy_registry",
    "agent_registry",
    "ai_run_ledger",
    "risk_index",
    "audit_exports",
    "approval_center",
    "cost_and_model_routing",
)
