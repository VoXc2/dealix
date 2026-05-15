"""Roadmap generator for execution phases."""

from __future__ import annotations

from typing import Any


ROADMAP_PHASES = [
    {
        "name": "P0 Foundation Gate",
        "start_day": 1,
        "end_day": 30,
        "outcomes": [
            "Pricing + sellable rules + KPI tree + risk register published",
            "CLI verify/package/quote commands live",
            "Playbook catalog and strict validators in CI",
        ],
    },
    {
        "name": "P1 Sales and Delivery Enablement",
        "start_day": 31,
        "end_day": 90,
        "outcomes": [
            "Offer generator and SOW templates shipped",
            "Intake forms + demo scripts ready for sales",
            "First paid pilots run on standard playbooks",
        ],
    },
    {
        "name": "P2 Scale and Productization",
        "start_day": 91,
        "end_day": 180,
        "outcomes": [
            "ROI calculator + proposal customization",
            "Dashboard export for executive reporting",
            "Continuous learning loop tied to pricing and packaging",
        ],
    },
]


def roadmap_for_days(days: int) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for phase in ROADMAP_PHASES:
        if phase["start_day"] <= days:
            items.append(phase)
    return items
