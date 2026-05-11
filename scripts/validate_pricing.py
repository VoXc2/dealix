#!/usr/bin/env python3
"""Validate pricing model and segment package consistency."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import (
    load_packaging_matrix,
    load_pricing_model,
    load_roi_formulas,
    load_segment_rules,
    load_sla_matrix,
)
from saudi_ai_provider.pricing import parse_service_id


def main() -> int:
    pricing = load_pricing_model()
    rules = load_segment_rules()
    packaging = load_packaging_matrix()
    roi_formulas = load_roi_formulas()
    sla_matrix = load_sla_matrix()
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

    for service_family, tiers in packaging.get("services", {}).items():
        if service_family not in pricing["service_matrix"]:
            errors.append(f"packaging: unknown service family {service_family}")
        for tier_name, cfg in tiers.items():
            if tier_name not in {"bronze", "silver", "gold"}:
                errors.append(f"{service_family}: invalid tier name {tier_name}")
            for key in ("segment", "setup_fee_sar", "monthly_sar", "deployment_days", "support_sla"):
                if key not in cfg:
                    errors.append(f"{service_family}_{tier_name}: missing packaging field {key}")
            if cfg.get("support_sla") not in {"business_hours", "24_7", "dedicated"}:
                errors.append(f"{service_family}_{tier_name}: invalid support_sla")

    if "formulas" not in roi_formulas or not roi_formulas["formulas"]:
        errors.append("roi_formulas: formulas section missing")
    else:
        for engine, formula_cfg in roi_formulas["formulas"].items():
            if engine not in pricing["service_matrix"] and engine != "AI_REVENUE_COMMAND_CENTER":
                errors.append(f"roi_formulas: unknown engine {engine}")
            for key in ("inputs", "monthly_savings_formula", "annual_roi_formula"):
                if key not in formula_cfg:
                    errors.append(f"roi_formulas[{engine}]: missing {key}")

    if "tiers" not in sla_matrix:
        errors.append("sla_matrix: missing tiers")
    else:
        for tier in ("bronze", "silver", "gold"):
            if tier not in sla_matrix["tiers"]:
                errors.append(f"sla_matrix: missing tier {tier}")

    if errors:
        print("PRICING_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PRICING_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
