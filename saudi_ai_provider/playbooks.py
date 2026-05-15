"""Delivery playbook access."""

from __future__ import annotations

from typing import Any

from .catalog import load_playbook_catalog
from .pricing import parse_service_id


def playbook_for_service(service_id: str) -> dict[str, Any]:
    engine, tier = parse_service_id(service_id)
    catalog = load_playbook_catalog()
    engine_cfg = catalog.get(engine)
    if not engine_cfg:
        raise ValueError(f"Missing playbook engine: {engine}")

    tier_cfg = engine_cfg.get("tiers", {}).get(tier.lower())
    if not tier_cfg:
        raise ValueError(f"Missing playbook tier {tier} for {engine}")
    return tier_cfg
