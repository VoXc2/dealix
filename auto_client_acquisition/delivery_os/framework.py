"""Canonical delivery phases + default checklists for Sprints."""

from __future__ import annotations

from enum import StrEnum


class DeliveryPhase(StrEnum):
    DISCOVER = "discover"
    DIAGNOSE = "diagnose"
    DESIGN = "design"
    BUILD = "build"
    VALIDATE = "validate"
    DELIVER = "deliver"
    PROVE = "prove"
    EXPAND = "expand"


def phases_in_order() -> tuple[DeliveryPhase, ...]:
    return tuple(DeliveryPhase)


DEFAULT_PHASE_CHECKLISTS: dict[DeliveryPhase, list[str]] = {
    DeliveryPhase.DISCOVER: [
        "Confirm sector, team size, tools, pain, and data availability.",
        "Confirm lawful basis / DPA path for customer data.",
    ],
    DeliveryPhase.DIAGNOSE: [
        "Run data quality summary (completeness + duplicate ratio).",
        "List top risks and quick wins.",
    ],
    DeliveryPhase.DESIGN: [
        "Define workflow, approvals, outputs, and success metrics.",
    ],
    DeliveryPhase.BUILD: [
        "Implement minimum viable automation with human-in-the-loop.",
        "Ensure audit logs for sensitive steps.",
    ],
    DeliveryPhase.VALIDATE: [
        "Business QA, Data QA, AI QA, Compliance QA, Delivery QA.",
    ],
    DeliveryPhase.DELIVER: [
        "Executive report, SOP, training, handoff deck.",
    ],
    DeliveryPhase.PROVE: [
        "Before/after metrics and proof pack appendix.",
    ],
    DeliveryPhase.EXPAND: [
        "Renewal / Pilot / Retainer proposal aligned to packages doc.",
    ],
}
