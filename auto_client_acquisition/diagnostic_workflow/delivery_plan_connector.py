"""Connector — pick a service in a bundle and build a DeliveryPlan.

Wraps ``delivery_factory.build_delivery_plan`` so the workflow can
return a structured plan for the recommended bundle without leaking
the YAML matrix shape outside of ``delivery_factory``.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.delivery_factory import (
    build_delivery_plan,
    list_available_services,
)
from auto_client_acquisition.self_growth_os.service_activation_matrix import (
    load_matrix,
)


def _first_service_in_bundle(bundle_id: str) -> str:
    matrix = load_matrix()
    for s in matrix.get("services") or []:
        if s.get("bundle") == bundle_id:
            sid = s.get("service_id")
            if sid:
                return str(sid)
    services = list_available_services()
    if not services:
        raise KeyError("matrix has no services")
    return services[0]


def build_delivery_plan_for_recommendation(recommended_bundle_id: str) -> dict[str, Any]:
    """Build a DeliveryPlan for one service inside the recommended bundle."""
    service_id = _first_service_in_bundle(recommended_bundle_id)
    plan = build_delivery_plan(service_id)
    return plan.to_dict()
