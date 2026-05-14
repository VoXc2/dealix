"""Adoption friction log — repeated friction drives productization."""

from __future__ import annotations

from dataclasses import dataclass

FRICTION_TYPES: tuple[str, ...] = (
    "data_friction",
    "approval_friction",
    "user_confusion",
    "workflow_ambiguity",
    "trust_concern",
    "arabic_quality_issue",
    "integration_issue",
    "pricing_concern",
)


@dataclass(frozen=True, slots=True)
class FrictionEvent:
    friction_id: str
    client_id: str
    friction_type: str
    description: str
    impact: str
    response: str
    product_signal: str


def friction_event_valid(event: FrictionEvent) -> bool:
    return all(
        (
            event.friction_id.strip(),
            event.client_id.strip(),
            event.friction_type.strip(),
            event.description.strip(),
            event.impact.strip(),
            event.response.strip(),
            event.product_signal.strip(),
        ),
    )


def friction_type_known(friction_type: str) -> bool:
    return friction_type in FRICTION_TYPES
