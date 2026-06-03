"""Delivery Factory v5 — turns a service from the YAML matrix into
a structured delivery plan.

Reads required_inputs + workflow_steps + deliverables from
``docs/registry/SERVICE_READINESS_MATRIX.yaml`` and produces:
  - intake checklist (founder confirms each item is collected)
  - workflow plan (step-by-step, bilingual)
  - QA checklist (what to verify before "client-ready")
  - SLA pointer (read from the matrix `sla:` field)
  - deliverable list (what the customer gets)

Pure read-only — no DB writes, no external sends.
"""
from auto_client_acquisition.delivery_factory.delivery_plan_builder import (
    DeliveryPlan,
    build_delivery_plan,
    list_available_services,
)

__all__ = [
    "DeliveryPlan",
    "build_delivery_plan",
    "list_available_services",
]
