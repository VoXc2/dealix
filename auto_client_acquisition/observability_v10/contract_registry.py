"""Telemetry contract registry and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_FIELDS: tuple[str, ...] = (
    "tenant_id",
    "correlation_id",
    "run_id",
    "event_type",
    "source_module",
    "actor",
    "occurred_at",
    "payload_schema_version",
)

ALLOWED_EVENT_TYPES: tuple[str, ...] = (
    "workflow.registered",
    "workflow.paused",
    "workflow.rollback.finalized",
    "approval.submitted",
    "approval.granted",
    "approval.rejected",
    "runtime_safety.kill_switch.activated",
    "value.metric.recorded",
    "self_evolving.proposal.submitted",
    "self_evolving.proposal.approved",
    "self_evolving.proposal.applied",
)


@dataclass(frozen=True, slots=True)
class ContractValidation:
    valid: bool
    errors: tuple[str, ...]


def validate_observability_event(event: dict[str, Any]) -> ContractValidation:
    errors: list[str] = []
    for key in REQUIRED_FIELDS:
        value = event.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"missing:{key}")
    event_type = str(event.get("event_type", ""))
    if event_type and event_type not in ALLOWED_EVENT_TYPES:
        errors.append(f"unknown_event_type:{event_type}")
    return ContractValidation(valid=not errors, errors=tuple(errors))


__all__ = [
    "ALLOWED_EVENT_TYPES",
    "REQUIRED_FIELDS",
    "ContractValidation",
    "validate_observability_event",
]
