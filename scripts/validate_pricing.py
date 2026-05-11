#!/usr/bin/env python3
"""Validate pricing model and segment package consistency."""

from __future__ import annotations

import sys

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_pricing_model, load_segment_rules
from saudi_ai_provider.pricing import parse_service_id


def main() -> int:
    pricing = load_pricing_model()
    rules = load_segment_rules()
    errors: list[str] = []

    for engine, cfg in pricing["service_matrix"].items():
        tiers = cfg.get("tiers", {})
        for tier in ("bronze", "silver", "gold"):
            if tier not in tiers:
                errors.append(f"{engine}: missing tier {tier}")
                continue
            for field in (
                "setup_fee_sar",
                "monthly_retainer_sar",
                "gross_margin_target",
                "delivery_hours_estimate",
                "minimum_contract_months",
                "discount_floor",
            ):
                if field not in tiers[tier]:
                    errors.append(f"{engine}_{tier}: missing field {field}")

    for segment, services in rules["package_recommendations"].items():
        for service_id in services:
            engine, tier = parse_service_id(service_id)
            if engine not in pricing["service_matrix"]:
                errors.append(f"{segment}: unknown service engine {engine}")
            elif tier.lower() not in pricing["service_matrix"][engine]["tiers"]:
                errors.append(f"{segment}: unknown service tier {service_id}")

    if errors:
        print("PRICING_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PRICING_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
