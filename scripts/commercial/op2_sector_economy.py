#!/usr/bin/env python3
"""OP2 sector economy — a multi-dimensional, evidence-bound research ranking.

This complements (does not replace) the canonical sector economic ranking in
``scripts/ops/sector_economic_ranking.py``. The canonical ranker scores sectors
from the Universal Market Radar brief; this OP2 ranker evaluates sector *cells*
across the full Dealix economic vector:

    SECTOR x BUYER x PROBLEM x OFFER x CHANNEL x MONETIZATION x DELIVERY
    x PROOF x AUTOMATION x TIME_TO_CASH

Inputs are the OP2 market-intelligence wave (fresh authoritative signals) plus
the governed sector blueprints. Output never leaves RESEARCHED_WITH_SIGNALS, and
never claims relationship, opportunity, pipeline, quote, payment, or revenue.

Prints: DEALIX_OP2_SECTOR_ECONOMY=OK plus TOP10/TOP3 machine lines.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

WAVE_PATH = REPO_ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"
OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_sector_economy_ranking_v1.json"

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
MAX_STATUS = "RESEARCHED_WITH_SIGNALS"

# Canonical 20 sectors are the denominator. Display names are pulled from the
# governed blueprints at runtime; we only map radar signal families here.
SECTOR_FAMILY_TO_CANONICAL: dict[str, tuple[str, str]] = {
    "AGRICULTURE_FOOD": ("agriculture_food_water", "direct"),
    "ENERGY": ("energy_utilities_oil_gas", "direct"),
    "HEALTHCARE_LIFE_SCIENCES": ("healthcare", "direct"),
    "ENVIRONMENTAL_SERVICES": ("industrial_manufacturing", "closest_canonical"),
    "MANUFACTURING": ("industrial_manufacturing", "direct"),
    "PHARMA_BIOTECH": ("healthcare", "closest_canonical"),
    "CHEMICALS": ("industrial_manufacturing", "closest_canonical"),
    "REAL_ESTATE": ("real_estate_proptech", "direct"),
    "FINANCIAL_SERVICES": ("finance_fintech_insurance", "direct"),
    "TRANSPORT_LOGISTICS": ("logistics_supply_chain", "direct"),
    "MINING_METALS": ("mining_metals", "direct"),
    "TOURISM_QUALITY_OF_LIFE": ("tourism_hospitality", "direct"),
    "ICT": ("technology_saas_si", "direct"),
    "HUMAN_CAPITAL_INNOVATION": ("education_training", "direct"),
    "AVIATION_DEFENSE": ("government_b2g", "closest_canonical"),
}

# Default economic vector per canonical sector (research hypotheses only).
# monetization values reference canonical MonetizationRail names.
DEFAULT_VECTOR: dict[str, dict[str, str]] = {
    "finance_fintech_insurance": {
        "offer": "GOVERNED_AI_COMPLIANCE_EVIDENCE",
        "channel": "direct_finance_ops",
        "monetization": "MANAGED_SERVICE",
        "delivery": "workspace_plus_week_review",
        "proof": "control_evidence_pack",
        "automation": "consent_and_report_pipeline",
        "time_to_cash": "medium_30_60d",
    },
    "technology_saas_si": {
        "offer": "AI_GOVERNANCE_AND_READINESS_ASSESSMENT",
        "channel": "direct_cto",
        "monetization": "PAID_SPRINT",
        "delivery": "assessment_then_build",
        "proof": "model_accountability_pack",
        "automation": "governance_evidence_trail",
        "time_to_cash": "fast_7_30d",
    },
    "healthcare": {
        "offer": "DIGITAL_HEALTH_EVIDENCE_READINESS",
        "channel": "partner_led",
        "monetization": "FIXED_SCOPE_IMPLEMENTATION",
        "delivery": "partner_joint_delivery",
        "proof": "regulatory_evidence_pack",
        "automation": "human_oversight_workflow",
        "time_to_cash": "slow_90d_plus",
    },
    "real_estate_proptech": {
        "offer": "PLATFORM_DATA_INTEGRITY_AUTOMATION",
        "channel": "direct_operator",
        "monetization": "FIXED_SCOPE_IMPLEMENTATION",
        "delivery": "platform_integration",
        "proof": "data_quality_pack",
        "automation": "integration_and_validation",
        "time_to_cash": "medium_30_60d",
    },
    "logistics_supply_chain": {
        "offer": "OPERATIONS_EXCEPTION_AUTOMATION",
        "channel": "direct_operations",
        "monetization": "MANAGED_SERVICE",
        "delivery": "ops_workspace",
        "proof": "exception_resolution_pack",
        "automation": "exception_detection",
        "time_to_cash": "medium_30_60d",
    },
    "industrial_manufacturing": {
        "offer": "QUALITY_AND_INVENTORY_AUTOMATION",
        "channel": "direct_operations",
        "monetization": "MANAGED_SERVICE",
        "delivery": "shopfloor_workspace",
        "proof": "quality_outcome_pack",
        "automation": "quality_signal_detection",
        "time_to_cash": "medium_30_60d",
    },
    "government_b2g": {
        "offer": "GOVERNED_EXECUTION_BACKEND",
        "channel": "partner_or_tender",
        "monetization": "WHITE_LABEL",
        "delivery": "partner_joint_delivery",
        "proof": "compliance_evidence_pack",
        "automation": "procurement_evidence_trail",
        "time_to_cash": "slow_90d_plus",
    },
    "education_training": {
        "offer": "ENROLLMENT_AND_REVENUE_LEAKAGE_AUTOMATION",
        "channel": "direct_ceo",
        "monetization": "PAID_SPRINT",
        "delivery": "lightweight_workspace",
        "proof": "leakage_reduction_pack",
        "automation": "lead_and_enrollment_pipeline",
        "time_to_cash": "fast_7_30d",
    },
    "retail_commerce_ecommerce": {
        "offer": "REVENUE_LEAKAGE_AND_ORDER_AUTOMATION",
        "channel": "direct_ceo",
        "monetization": "PAID_SPRINT",
        "delivery": "commerce_workspace",
        "proof": "conversion_and_leakage_pack",
        "automation": "order_and_support_automation",
        "time_to_cash": "fast_7_30d",
    },
    "construction_epc": {
        "offer": "PROJECT_CONTROL_AND_SUBMITTAL_AUTOMATION",
        "channel": "direct_project_controls",
        "monetization": "PAID_SPRINT",
        "delivery": "project_control_workspace",
        "proof": "cycle_time_and_exception_pack",
        "automation": "submittal_rfi_change_pipeline",
        "time_to_cash": "medium_30_60d",
    },
    "energy_utilities_oil_gas": {
        "offer": "ENERGY_OPERATIONS_AND_EVIDENCE_AUTOMATION",
        "channel": "partner_or_direct_operations",
        "monetization": "FIXED_SCOPE_IMPLEMENTATION",
        "delivery": "governed_operations_workspace",
        "proof": "energy_control_evidence_pack",
        "automation": "audit_measurement_exception_pipeline",
        "time_to_cash": "slow_90d_plus",
    },
    "mining_metals": {
        "offer": "MAINTENANCE_AND_PRODUCTION_INTELLIGENCE",
        "channel": "supplier_portal_plus_operations",
        "monetization": "PAID_SPRINT",
        "delivery": "maintenance_intelligence_workspace",
        "proof": "downtime_and_resolution_pack",
        "automation": "maintenance_exception_pipeline",
        "time_to_cash": "medium_30_60d",
    },
    "tourism_hospitality": {
        "offer": "GUEST_AND_REVENUE_OPERATIONS_AUTOMATION",
        "channel": "direct_general_manager",
        "monetization": "PAID_SPRINT",
        "delivery": "guest_operations_workspace",
        "proof": "booking_support_resolution_pack",
        "automation": "booking_guest_support_pipeline",
        "time_to_cash": "fast_7_30d",
    },
    "professional_services": {
        "offer": "LEAD_TO_CASH_AND_DELIVERY_AUTOMATION",
        "channel": "direct_managing_partner",
        "monetization": "PAID_SPRINT",
        "delivery": "professional_service_workspace",
        "proof": "proposal_cycle_and_utilization_pack",
        "automation": "lead_proposal_delivery_pipeline",
        "time_to_cash": "fast_7_30d",
    },
    "telecom_media_marketing": {
        "offer": "CUSTOMER_AND_CONTENT_OPERATIONS_AUTOMATION",
        "channel": "direct_growth_or_operations",
        "monetization": "MANAGED_SERVICE",
        "delivery": "growth_operations_workspace",
        "proof": "support_content_attribution_pack",
        "automation": "campaign_content_support_pipeline",
        "time_to_cash": "medium_30_60d",
    },
    "agriculture_food_water": {
        "offer": "TRACEABILITY_AND_RESOURCE_EFFICIENCY_DIAGNOSTIC",
        "channel": "partner_or_operations",
        "monetization": "PAID_SPRINT",
        "delivery": "traceability_workspace",
        "proof": "loss_quality_resource_pack",
        "automation": "traceability_quality_exception_pipeline",
        "time_to_cash": "medium_30_60d",
    },
    "mobility_automotive": {
        "offer": "FLEET_SERVICE_AND_PARTS_AUTOMATION",
        "channel": "direct_fleet_or_aftersales",
        "monetization": "PAID_SPRINT",
        "delivery": "fleet_service_workspace",
        "proof": "uptime_service_cycle_pack",
        "automation": "service_parts_exception_pipeline",
        "time_to_cash": "fast_7_30d",
    },
    "export_import_rhq": {
        "offer": "TRADE_DOCUMENT_AND_LANDED_COST_AUTOMATION",
        "channel": "partner_or_supply_chain",
        "monetization": "PAID_SPRINT",
        "delivery": "trade_operations_workspace",
        "proof": "document_cycle_and_exception_pack",
        "automation": "document_customs_exception_pipeline",
        "time_to_cash": "medium_30_60d",
    },
    "creative_sports_gaming": {
        "offer": "COMMERCIAL_AND_FAN_OPERATIONS_AUTOMATION",
        "channel": "direct_commercial_director",
        "monetization": "PAID_SPRINT",
        "delivery": "commercial_operations_workspace",
        "proof": "sponsorship_engagement_pack",
        "automation": "sponsorship_content_fan_pipeline",
        "time_to_cash": "fast_7_30d",
    },
    "associations_nonprofits": {
        "offer": "MEMBER_DONOR_AND_REPORTING_AUTOMATION",
        "channel": "partner_or_executive_director",
        "monetization": "FIXED_SCOPE_IMPLEMENTATION",
        "delivery": "mission_operations_workspace",
        "proof": "member_donor_reporting_pack",
        "automation": "member_donor_case_pipeline",
        "time_to_cash": "medium_30_60d",
    },
}

_DEFAULT = {
    "offer": "FREE_DIAGNOSTIC_THEN_QUOTE",
    "channel": "direct",
    "monetization": "FREE_DIAGNOSTIC",
    "delivery": "diagnostic_then_scope",
    "proof": "diagnostic_evidence_pack",
    "automation": UNKNOWN,
    "time_to_cash": UNKNOWN,
}


def load_wave(path: Path = WAVE_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_aggregates(wave: dict[str, Any]) -> dict[str, dict[str, Any]]:
    aggregates: dict[str, dict[str, Any]] = {}
    for signal in wave.get("signals", []) or []:
        family = str(signal.get("sector_family", UNKNOWN))
        canonical_override = str(signal.get("canonical_sector_id") or "").strip()
        if canonical_override:
            canonical = canonical_override
            mapping_note = f"{family}->{canonical}:explicit_canonical_sector_id"
        else:
            mapping = SECTOR_FAMILY_TO_CANONICAL.get(family)
            if mapping is None:
                continue
            canonical, mapping_note = mapping
        row = aggregates.setdefault(
            canonical,
            {
                "sector_id": canonical,
                "signal_count": 0,
                "priority_scores": [],
                "signal_ids": [],
                "evidence_refs": [],
                "authority_refs": [],
                "deadlines": [],
                "mapping_notes": [],
                "buyers": [],
                "problems": [],
            },
        )
        row["signal_count"] += 1
        factors = signal.get("priority_factors") or {}
        row["priority_scores"].append(priority_indicator(factors))
        row["signal_ids"].append(str(signal.get("signal_id")))
        refs = [str(ref) for ref in signal.get("evidence_refs", [])]
        if refs:
            row["evidence_refs"].append(refs[0])
        authority = str(signal.get("authority_ref") or "").strip()
        if authority and authority not in row["authority_refs"]:
            row["authority_refs"].append(authority)
        deadline = str(signal.get("deadline") or "")
        if deadline and deadline != UNKNOWN:
            row["deadlines"].append(deadline)
        buyer = str(signal.get("buyer") or "").strip()
        if buyer and buyer not in row["buyers"]:
            row["buyers"].append(buyer)
        problem = str(signal.get("problem") or "").strip()
        if problem and problem not in row["problems"]:
            row["problems"].append(problem)
        if mapping_note != "direct":
            row["mapping_notes"].append(f"{family}->{canonical}:{mapping_note}")
    return aggregates


def priority_indicator(factors: dict[str, Any]) -> float:
    """Apply the canonical radar priority formula to one receipt's factors."""
    def value(name: str) -> float:
        raw = factors.get(name)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            return 0.0
        return float(raw)

    numerator = (
        value("economic_pain")
        * value("measurable_outcome")
        * value("buyer_access")
        * value("data_availability")
        * value("repeatability")
        * value("readiness")
        * value("distribution_density")
    )
    denominator = max(value("regulatory_friction"), 0.5) * max(value("integration_complexity"), 0.5) * max(value("founder_minutes"), 0.5)
    if numerator <= 0 or denominator <= 0:
        return 0.0
    return round(numerator / denominator, 4)


def economic_vector(sector_id: str) -> dict[str, str]:
    return {**_DEFAULT, **DEFAULT_VECTOR.get(sector_id, {})}


def build_ranking(wave: dict[str, Any] | None = None) -> dict[str, Any]:
    from dealix.commercial.sector_company_blueprint import build_all_blueprints

    wave = wave if wave is not None else load_wave()
    aggregates = build_aggregates(wave)
    blueprints = {blueprint.sector_id: blueprint for blueprint in build_all_blueprints()}

    cells: list[dict[str, Any]] = []
    for sector_id, blueprint in blueprints.items():
        aggregate = aggregates.get(sector_id)
        if not aggregate or aggregate["signal_count"] == 0:
            continue
        scores = aggregate["priority_scores"]
        score = round(sum(scores) / len(scores) * (1 + 0.3 * (len(scores) - 1)), 4)
        top_buyer = (aggregate["buyers"] or [blueprint.buyers[0].role if blueprint.buyers else UNKNOWN])[0]
        top_problem = (aggregate["problems"] or [blueprint.problem_cells[0].problem if blueprint.problem_cells else UNKNOWN])[0]
        cells.append(
            {
                "sector_id": sector_id,
                "ar_name": blueprint.ar_name,
                "en_name": blueprint.en_name,
                "status": MAX_STATUS,
                "research_rank_score": score,
                "signal_count": aggregate["signal_count"],
                "signal_ids": aggregate["signal_ids"],
                "evidence_refs": aggregate["evidence_refs"],
                "authority_refs": aggregate["authority_refs"],
                "deadlines": aggregate["deadlines"],
                "mapping_notes": aggregate["mapping_notes"],
                "buyer": top_buyer,
                "problem": top_problem,
                "vector": economic_vector(sector_id),
                "truth_class": "PATTERN_RESEARCH_RANKING",
                "counts_as_pipeline": False,
                "counts_as_revenue": False,
            }
        )
    cells.sort(key=lambda item: item["research_rank_score"], reverse=True)

    top3 = cells[:3]
    return {
        "schema": "dealix.op2-sector-economy.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_wave": str(WAVE_PATH),
        "truth_class": "PATTERN_RESEARCH_RANKING",
        "authority": "RESEARCH_ONLY_NO_RELATIONSHIP_NO_OPPORTUNITY_NO_PIPELINE",
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "status_ceiling": MAX_STATUS,
        "cells": cells,
        "top_cells": cells[:10],
        "deep_wip_top3": [
            {
                "sector_id": cell["sector_id"],
                "buyer": cell["buyer"],
                "problem": cell["problem"],
                "research_rank_score": cell["research_rank_score"],
                "vector": cell["vector"],
                "evidence_refs": cell["evidence_refs"],
                "truth_class": "PATTERN",
                "counts_as_pipeline": False,
            }
            for cell in top3
        ],
    }


def render(ranking: dict[str, Any]) -> str:
    lines = [
        "DEALIX_OP2_SECTOR_ECONOMY=OK",
        f"STATUS_CEILING={ranking['status_ceiling']}",
        f"CELLS_WITH_SIGNALS={len(ranking['cells'])}",
    ]
    for index, cell in enumerate(ranking["top_cells"], start=1):
        lines.append(
            f"TOP{index} {cell['sector_id']} score={cell['research_rank_score']} "
            f"signals={cell['signal_count']} buyer={cell['buyer']} problem={cell['problem']}"
        )
    for index, cell in enumerate(ranking["deep_wip_top3"], start=1):
        lines.append(f"DEEP_WIP_{index} {cell['sector_id']} {cell['buyer']} / {cell['problem']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 sector economy research ranking")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ranking = build_ranking()
    if args.json:
        print(json.dumps(ranking, indent=2, ensure_ascii=False))
    else:
        print(render(ranking))
    if args.write:
        OUT_PATH.write_text(json.dumps(ranking, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
