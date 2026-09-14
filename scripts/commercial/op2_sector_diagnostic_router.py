#!/usr/bin/env python3
"""OP2 evidence-bound sector diagnostic router.

The OP2 market wave and sector-economy ranking are research artifacts. This
router makes them actionable for the genuinely-free diagnostic funnel without
touching the canonical diagnostic engine (``universal_diagnostic_factory``) or
the canonical public API route. Given a sector surface and a qualified problem
signal, it produces a bridge record that maps:

    SECTOR SURFACE -> diagnostic families -> free diagnostic entry
    -> Omega V3 Agentic Holding handoff -> discovery-prep fields

Historical five executor names are preserved only as legacy compatibility
aliases. They are not architecture authority. Current execution authority is:
Dealix Holding -> Sector Companies -> Arm Pods -> Specialist Logical Agents ->
ResourceGovernor-bounded runtime workers.

It never claims a relationship, consent, offer, price, quote, or revenue, and
it never fabricates ROI. All output is ``INTERNAL_RESEARCH_ONLY`` and
promotion remains owned by the canonical downstream state owners.

Prints: DEALIX_OP2_DIAGNOSTIC_ROUTER=OK plus ROUTE_n machine lines.
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

from dealix.agentic_holding.runtime import build_current_registry
from dealix.commercial.sector_company_blueprint import build_all_blueprints

WAVE_PATH = REPO_ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"
ECONOMY_PATH = REPO_ROOT / "data" / "commercial" / "op2_sector_economy_ranking_v1.json"
OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_sector_diagnostic_routes_v1.json"

# Backward-compatible aliases only. Omega V3 architecture is registry-derived.
LEGACY_EXECUTOR_ALIASES = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
FREE_DEPTHS = ("D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL")

SECTOR_FAMILY_TO_CANONICAL: dict[str, str] = {
    "AGRICULTURE_FOOD": "agriculture_food_water",
    "ENERGY": "energy_utilities_oil_gas",
    "HEALTHCARE_LIFE_SCIENCES": "healthcare",
    "ENVIRONMENTAL_SERVICES": "industrial_manufacturing",
    "MANUFACTURING": "industrial_manufacturing",
    "PHARMA_BIOTECH": "healthcare",
    "CHEMICALS": "industrial_manufacturing",
    "REAL_ESTATE": "real_estate_proptech",
    "FINANCIAL_SERVICES": "finance_fintech_insurance",
    "TRANSPORT_LOGISTICS": "logistics_supply_chain",
    "MINING_METALS": "mining_metals",
    "TOURISM_QUALITY_OF_LIFE": "tourism_hospitality",
    "ICT": "technology_saas_si",
    "HUMAN_CAPITAL_INNOVATION": "education_training",
    "AVIATION_DEFENSE": "government_b2g",
}

# Priority diagnostic families by canonical sector, chosen from the A01..A50
# catalog. Used only to order the free diagnostic entry; not a claim of need.
SECTOR_PRIORITY_FAMILIES: dict[str, list[str]] = {
    "government_b2g": ["A28", "A36", "A13", "A15"],
    "construction_epc": ["A10", "A28", "A29", "A15"],
    "industrial_manufacturing": ["A10", "A11", "A27", "A05"],
    "logistics_supply_chain": ["A27", "A28", "A10", "A05"],
    "energy_utilities_oil_gas": ["A11", "A13", "A18", "A43"],
    "mining_metals": ["A10", "A11", "A27", "A28"],
    "real_estate_proptech": ["A05", "A28", "A46", "A29"],
    "healthcare": ["A44", "A08", "A18", "A13", "A45"],
    "finance_fintech_insurance": ["A03", "A04", "A14", "A15", "A13"],
    "retail_commerce_ecommerce": ["A05", "A08", "A09", "A27"],
    "tourism_hospitality": ["A01", "A08", "A09", "A27"],
    "professional_services": ["A01", "A02", "A03", "A15"],
    "technology_saas_si": ["A05", "A11", "A12", "A13", "A43"],
    "telecom_media_marketing": ["A05", "A08", "A09", "A12"],
    "education_training": ["A05", "A08", "A06", "A12"],
    "agriculture_food_water": ["A10", "A27", "A28", "A45"],
    "mobility_automotive": ["A10", "A27", "A28", "A05"],
    "export_import_rhq": ["A03", "A04", "A15", "A28"],
    "creative_sports_gaming": ["A01", "A05", "A08", "A09"],
    "associations_nonprofits": ["A01", "A06", "A08", "A15"],
}


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_routes() -> dict[str, Any]:
    wave = _read_json(WAVE_PATH)
    economy = _read_json(ECONOMY_PATH)
    warnings: list[str] = []
    if not wave:
        warnings.append(f"market wave unreachable: {WAVE_PATH}")
    if not economy:
        warnings.append(f"sector economy ranking unreachable: {ECONOMY_PATH}")

    holding_receipt = build_current_registry().receipt()
    if holding_receipt.get("orphan_failures"):
        warnings.extend(f"agentic holding: {item}" for item in holding_receipt["orphan_failures"])

    economy_by_sector = {cell["sector_id"]: cell for cell in economy.get("cells", []) or []}
    blueprints = {item.sector_id: item for item in build_all_blueprints()}

    # Group wave signals by canonical sector, preserving evidence refs.
    per_sector: dict[str, list[dict[str, Any]]] = {}
    for signal in wave.get("signals", []) or []:
        canonical = str(signal.get("canonical_sector_id") or "").strip()
        if not canonical:
            canonical = SECTOR_FAMILY_TO_CANONICAL.get(str(signal.get("sector_family"))) or ""
        if canonical in blueprints:
            per_sector.setdefault(canonical, []).append(signal)

    routes: list[dict[str, Any]] = []
    for sector_id, blueprint in blueprints.items():
        cell = economy_by_sector.get(sector_id)
        signals = per_sector.get(sector_id, [])
        evidence_backed = bool(cell and signals)
        first_problem = blueprint.top_problems[0] if blueprint.top_problems else UNKNOWN
        first_buyer = blueprint.buyers[0].role if blueprint.buyers else UNKNOWN
        priority_families = SECTOR_PRIORITY_FAMILIES.get(sector_id)
        if not priority_families and blueprint.problem_cells:
            priority_families = blueprint.problem_cells[0].diagnostic_families[:5]
        if not priority_families:
            priority_families = ["A01"]
        routes.append(
            {
                "sector_id": sector_id,
                "ar_name": cell.get("ar_name", blueprint.ar_name) if cell else blueprint.ar_name,
                "en_name": cell.get("en_name", blueprint.en_name) if cell else blueprint.en_name,
                "buyer": cell.get("buyer", first_buyer) if cell else first_buyer,
                "problem": cell.get("problem", first_problem) if cell else first_problem,
                "research_rank_score": cell.get("research_rank_score", 0.0) if cell else 0.0,
                "market_evidence_status": "EVIDENCE_BACKED" if evidence_backed else "PATTERN_ONLY_NEEDS_FRESH_SIGNAL",
                "market_evidence_scope": (
                    "PUBLIC_MARKET_SIGNAL_ONLY_NOT_BUYER_DEMAND"
                    if evidence_backed
                    else "PATTERN_ONLY_NO_FRESH_PUBLIC_SIGNAL"
                ),
                "buyer_demand_status": "UNKNOWN_NOT_EVIDENCE_BACKED",
                "maturity_status": blueprint.maturity_status,
                "diagnostic_entry": {
                    "factory": "dealix.commercial.universal_diagnostic_factory",
                    "free_depths": list(FREE_DEPTHS),
                    "priority_families": priority_families,
                    "route": "/book",
                    "api": "POST /api/v1/public/execution-diagnostic",
                    "card_required": False,
                    "roi_promised": False,
                },
                "commercial_pattern": {
                    "offer_ladder": list(blueprint.dealix_offers.offer_ladder),
                    "procurement_paths": list(blueprint.procurement.procurement_paths),
                    "compliance_constraints": list(blueprint.signals.compliance_constraints),
                    "distribution_channels": list(blueprint.next_best_actions.distribution_channels),
                    "acceptance_criteria": list(blueprint.delivery_proof.acceptance_criteria),
                    "proof_requirements": list(blueprint.delivery_proof.proof_requirements),
                },
                "crm_handoff": {
                    "architecture": holding_receipt["architecture"],
                    "registry_source": "dealix.agentic_holding.runtime.build_current_registry",
                    "logical_agents": holding_receipt["logical_agents"],
                    "sector_companies": holding_receipt["sector_companies"],
                    "arm_pods": holding_receipt["arm_pods"],
                    "fixed_five_authority": False,
                    # Preserve the old field only so stored/schema consumers do not break.
                    "canonical_agents": list(LEGACY_EXECUTOR_ALIASES),
                    "canonical_agents_field_semantics": "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_ARCHITECTURE_AUTHORITY",
                    "legacy_executor_aliases": list(LEGACY_EXECUTOR_ALIASES),
                    "routing_authority": "Company Operator -> Agentic Holding registry -> Session Factory",
                    "mirror_target": "revenue_ops_autopilot",
                    "hubspot_is_mirror_not_truth": True,
                },
                "discovery_prep": {
                    "evidence_gaps": (["fresh official market signal"] if not evidence_backed else [])
                    + ["platform/brief/scope", "acceptance criteria", "decision owner"],
                    "problem_state": "HYPOTHESIS_WITH_BASELINE_PENDING_VALIDATION",
                    "signal_ids": [str(s.get("signal_id")) for s in signals],
                    "deadlines": [str(s.get("deadline")) for s in signals if s.get("deadline") not in (None, UNKNOWN)],
                    "evidence_refs": [ref for s in signals for ref in (s.get("evidence_refs") or [])][:4],
                },
                "truth_class": "PATTERN_RESEARCH_ROUTING",
                "allowed_use": ["INTERNAL_RESEARCH_ONLY"],
                "counts_as_pipeline": False,
                "counts_as_revenue": False,
            }
        )
    routes.sort(
        key=lambda item: (
            item["market_evidence_status"] == "EVIDENCE_BACKED",
            item["research_rank_score"],
            item["sector_id"],
        ),
        reverse=True,
    )

    return {
        "schema": "dealix.op2-sector-diagnostic-routes.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "truth_policy": "RESEARCH_ONLY_NO_RELATIONSHIP_NO_CONSENT_NO_PIPELINE",
        "agentic_holding": {
            **holding_receipt,
            "registry_source": "dealix.agentic_holding.runtime.build_current_registry",
            "fixed_five_authority": False,
            "legacy_executor_aliases": list(LEGACY_EXECUTOR_ALIASES),
        },
        "authority": {
            "relationship": False,
            "consent": False,
            "offer": False,
            "price": False,
            "quote": False,
            "external_send": False,
            "payment": False,
            "execution": False,
        },
        "warnings": warnings,
        "route_count": len(routes),
        "evidence_backed_count": sum(
            1 for route in routes if route["market_evidence_status"] == "EVIDENCE_BACKED"
        ),
        "pattern_only_count": sum(
            1 for route in routes if route["market_evidence_status"] != "EVIDENCE_BACKED"
        ),
        "routes": routes,
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
    }


def render(result: dict[str, Any]) -> str:
    lines = ["DEALIX_OP2_DIAGNOSTIC_ROUTER=OK", f"ROUTES={result['route_count']}"]
    for index, route in enumerate(result["routes"], start=1):
        entry = route["diagnostic_entry"]
        lines.append(
            f"ROUTE_{index} {route['sector_id']} families={','.join(entry['priority_families'])} "
            f"route={entry['route']} buyer={route['buyer']}"
        )
    for warning in result["warnings"]:
        lines.append(f"WARN {warning}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 sector diagnostic router")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_routes()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render(result))
    if args.write:
        OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
