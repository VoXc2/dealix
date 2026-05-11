"""Pricing and packaging logic for Saudi AI provider services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .catalog import (
    load_discount_policy,
    load_margin_guardrails,
    load_pricing_model,
    load_segment_rules,
)


@dataclass(frozen=True)
class Quote:
    service_id: str
    segment: str
    setup_fee_sar: float
    monthly_retainer_sar: float
    implementation_fee_sar: float
    annual_contract_value_sar: float
    discount_applied: float
    gross_margin_target: float
    sellable: bool
    reasons: list[str]


def parse_service_id(service_id: str) -> tuple[str, str]:
    normalized = service_id.strip().upper()
    if "_" not in normalized:
        raise ValueError("Service ID must be ENGINE_TIER, e.g. CUSTOMER_PORTAL_GOLD")
    engine, tier = normalized.rsplit("_", 1)
    if tier not in {"BRONZE", "SILVER", "GOLD"}:
        raise ValueError("Tier must be BRONZE, SILVER, or GOLD")
    return engine, tier


def resolve_segment_by_employees(employees: int) -> str:
    rules = load_segment_rules()
    for segment, cfg in rules["segments"].items():
        min_emp = int(cfg["employees_min"])
        max_emp = int(cfg["employees_max"])
        if min_emp <= employees <= max_emp:
            return segment
    return "enterprise"


def get_service_pricing(service_id: str, segment: str) -> dict[str, Any]:
    engine, tier = parse_service_id(service_id)
    model = load_pricing_model()
    engine_cfg = model["service_matrix"].get(engine)
    if not engine_cfg:
        raise ValueError(f"Unknown engine in service id: {engine}")

    tier_cfg = engine_cfg["tiers"].get(tier.lower())
    if not tier_cfg:
        raise ValueError(f"Unknown tier for {engine}: {tier}")

    segment_multiplier = load_segment_rules()["segments"][segment]["price_multiplier"]
    setup_fee = round(tier_cfg["setup_fee_sar"] * segment_multiplier, 2)
    monthly_retainer = round(tier_cfg["monthly_retainer_sar"] * segment_multiplier, 2)
    delivery_hours = int(tier_cfg["delivery_hours_estimate"] * segment_multiplier)

    return {
        "service_id": service_id.upper(),
        "segment": segment,
        "engine": engine,
        "tier": tier,
        "setup_fee_sar": setup_fee,
        "monthly_retainer_sar": monthly_retainer,
        "gross_margin_target": tier_cfg["gross_margin_target"],
        "delivery_hours_estimate": delivery_hours,
        "minimum_contract_months": tier_cfg["minimum_contract_months"],
        "discount_floor": tier_cfg["discount_floor"],
        "requires": engine_cfg["requires"],
        "not_sellable_if": engine_cfg["not_sellable_if"],
    }


def quote_service(
    service_id: str,
    employees: int,
    discount: float = 0.0,
    segment: str | None = None,
) -> Quote:
    resolved_segment = segment or resolve_segment_by_employees(employees)
    pricing = get_service_pricing(service_id, resolved_segment)
    discount_policy = load_discount_policy()
    margin_policy = load_margin_guardrails()

    floor = max(pricing["discount_floor"], discount_policy["global_discount_floor"])
    cap = discount_policy["max_discount_with_founder_approval"]
    bounded_discount = max(0.0, min(discount, cap))
    implementation_fee = round(pricing["setup_fee_sar"] * (1 - bounded_discount), 2)
    annual_contract = round(
        implementation_fee
        + (pricing["monthly_retainer_sar"] * pricing["minimum_contract_months"]),
        2,
    )

    reasons: list[str] = []
    if bounded_discount > floor:
        reasons.append(
            f"Discount {bounded_discount:.2f} is above floor {floor:.2f}; founder approval required."
        )
    if pricing["gross_margin_target"] < margin_policy["minimum_gross_margin_target"]:
        reasons.append("Gross margin target is below minimum guardrail.")

    sellable = not reasons
    return Quote(
        service_id=pricing["service_id"],
        segment=resolved_segment,
        setup_fee_sar=pricing["setup_fee_sar"],
        monthly_retainer_sar=pricing["monthly_retainer_sar"],
        implementation_fee_sar=implementation_fee,
        annual_contract_value_sar=annual_contract,
        discount_applied=bounded_discount,
        gross_margin_target=pricing["gross_margin_target"],
        sellable=sellable,
        reasons=reasons,
    )


def package_for_segment(segment: str) -> list[dict[str, Any]]:
    rules = load_segment_rules()
    services = rules["package_recommendations"].get(segment, [])
    if not services:
        raise ValueError(f"No package recommendations for segment: {segment}")

    packaged: list[dict[str, Any]] = []
    for service_id in services:
        packaged.append(get_service_pricing(service_id, segment))
    return packaged
