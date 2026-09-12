#!/usr/bin/env python3
"""Sector economic ranking — real research signals mapped onto canonical sectors.

Reads the canonical Universal Market Radar brief (research priority only) and the
governed sector blueprints, then produces a transparent research ranking. It never
promotes a sector beyond RESEARCHED_WITH_SIGNALS and never claims relationship,
pipeline, revenue, or customer facts.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

RADAR_BRIEF = REPO_ROOT / "data" / "founder_briefs" / "universal_market_radar_latest.json"
OUT_PATH = Path("/opt/dealix/company-os/founder-os/current/TOP_ECONOMIC_CELLS.json")

UNKNOWN = "UNKNOWN"
MAX_STATUS = "RESEARCHED_WITH_SIGNALS"

# 15 radar sector families -> canonical Dealix sector ids (IDs preserved).
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

TIER_WEIGHTS = {"A": 1.2, "B": 1.0, "C_GOVERNED": 0.85}


def load_radar_brief(path: Path = RADAR_BRIEF) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_sector_aggregates(brief: dict[str, Any]) -> dict[str, dict[str, Any]]:
    aggregates: dict[str, dict[str, Any]] = {}
    for row in brief.get("ranked_research_signals", []) or []:
        family = str(row.get("sector_family", UNKNOWN))
        mapping = SECTOR_FAMILY_TO_CANONICAL.get(family)
        if mapping is None:
            continue
        canonical, mapping_note = mapping
        aggregate = aggregates.setdefault(
            canonical,
            {
                "sector_id": canonical,
                "signal_families": [],
                "signal_count": 0,
                "priority_scores": [],
                "stale_count": 0,
                "signal_ids": [],
                "evidence_refs": [],
                "mapping_notes": [],
            },
        )
        aggregate["signal_count"] += 1
        score = row.get("priority_score")
        if isinstance(score, (int, float)):
            aggregate["priority_scores"].append(float(score))
        if row.get("stale") is True:
            aggregate["stale_count"] += 1
        aggregate["signal_ids"].append(str(row.get("signal_id")))
        aggregate["evidence_refs"].extend([str(ref) for ref in row.get("evidence_refs", [])][:2])
        if family not in aggregate["signal_families"]:
            aggregate["signal_families"].append(family)
        if mapping_note != "direct":
            aggregate["mapping_notes"].append(f"{family}->{canonical}:{mapping_note}")
    return aggregates


def tier_weight(tier: str) -> float:
    return TIER_WEIGHTS.get(str(tier), 1.0)


def composite_score(aggregate: dict[str, Any], tier: str, completeness_pct: int) -> tuple[float, dict[str, Any]]:
    scores = aggregate.get("priority_scores", [])
    if not scores:
        return 0.0, {"reason": "NO_SCORED_SIGNALS"}
    average = sum(scores) / len(scores)
    density = 1.0 + math.log(1.0 + aggregate.get("signal_count", 0))
    completeness_factor = max(0.5, min(1.5, completeness_pct / 100.0))
    value = round(average * density * tier_weight(tier) * completeness_factor, 4)
    return value, {
        "average_signal_priority": round(average, 4),
        "density_factor": round(density, 4),
        "tier_weight": tier_weight(tier),
        "completeness_factor": round(completeness_factor, 4),
        "semantics": "INTERNAL_RESEARCH_RANKING_ONLY_NOT_PURCHASE_PROBABILITY",
    }


def build_ranking(brief: dict[str, Any] | None = None) -> dict[str, Any]:
    from dealix.commercial.sector_company_blueprint import build_all_blueprints

    brief = brief if brief is not None else load_radar_brief()
    aggregates = build_sector_aggregates(brief)
    playbook_tiers = {
        str(row.get("id")): str(row.get("priority", UNKNOWN))
        for row in (load_playbooks().get("sector_families", []) or [])
        if isinstance(row, dict)
    }
    blueprints = {blueprint.sector_id: blueprint for blueprint in build_all_blueprints()}

    sectors: list[dict[str, Any]] = []
    for sector_id, blueprint in blueprints.items():
        aggregate = aggregates.get(sector_id, {"signal_count": 0, "priority_scores": [], "signal_ids": []})
        family_tiers = [
            playbook_tiers.get(family, UNKNOWN) for family in aggregates.get(sector_id, {}).get("signal_families", [])
        ]
        tier = "A" if "A" in family_tiers else ("B" if "B" in family_tiers else ("C_GOVERNED" if "C_GOVERNED" in family_tiers else UNKNOWN))
        score, breakdown = composite_score(aggregate, tier, blueprint.completeness_pct)
        status = MAX_STATUS if aggregate.get("signal_count", 0) > 0 else "INTERNAL_READY_NO_SIGNALS"
        top_buyer = blueprint.buyers[0].role if blueprint.buyers else UNKNOWN
        top_problem = blueprint.problem_cells[0].problem if blueprint.problem_cells else UNKNOWN
        sectors.append(
            {
                "sector_id": sector_id,
                "ar_name": blueprint.ar_name,
                "en_name": blueprint.en_name,
                "status": status,
                "research_rank_score": score,
                "score_breakdown": breakdown,
                "signal_count": aggregate.get("signal_count", 0),
                "stale_count": aggregate.get("stale_count", 0),
                "signal_ids": aggregate.get("signal_ids", []),
                "evidence_refs": aggregate.get("evidence_refs", []),
                "mapping_notes": aggregate.get("mapping_notes", []),
                "isic_sections": blueprint.isic_sections,
                "top_buyer_cell": {"buyer_role": top_buyer, "problem": top_problem, "truth_class": "PATTERN"},
                "blueprint_maturity": blueprint.maturity_status,
                "blueprint_completeness_pct": blueprint.completeness_pct,
            }
        )
    sectors.sort(key=lambda item: item["research_rank_score"], reverse=True)
    return {
        "schema": "dealix.top-economic-cells.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_brief": str(RADAR_BRIEF),
        "truth_class": "PATTERN_RESEARCH_RANKING",
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "status_ceiling": MAX_STATUS,
        "sectors": sectors,
        "top_cells": [
            {
                "sector_id": item["sector_id"],
                "buyer_role": item["top_buyer_cell"]["buyer_role"],
                "problem": item["top_buyer_cell"]["problem"],
                "research_rank_score": item["research_rank_score"],
                "signal_count": item["signal_count"],
                "evidence_refs": item["evidence_refs"],
                "truth_class": "PATTERN",
                "counts_as_pipeline": False,
            }
            for item in sectors[:10]
        ],
    }


_PLAYBOOKS_CACHE: dict[str, Any] | None = None


def load_playbooks() -> dict[str, Any]:
    global _PLAYBOOKS_CACHE
    if _PLAYBOOKS_CACHE is None:
        path = REPO_ROOT / "data" / "commercial" / "universal_market_playbooks_v1.json"
        try:
            _PLAYBOOKS_CACHE = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            _PLAYBOOKS_CACHE = {}
    return _PLAYBOOKS_CACHE


def render_summary(ranking: dict[str, Any], top: int = 10) -> str:
    lines = [
        "SECTOR_ECONOMIC_RANKING=OK",
        f"STATUS_CEILING={ranking['status_ceiling']}",
        f"COUNTS_AS_PIPELINE={ranking['counts_as_pipeline']}",
    ]
    for index, cell in enumerate(ranking["top_cells"][:top], start=1):
        lines.append(
            f"RANK{index} {cell['sector_id']} score={cell['research_rank_score']} "
            f"signals={cell['signal_count']} buyer={cell['buyer_role']} problem={cell['problem']}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank canonical sectors from real research signals")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    ranking = build_ranking()
    if args.json:
        print(json.dumps(ranking, indent=2, ensure_ascii=False))
    else:
        print(render_summary(ranking, args.top))
    if args.write:
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps(ranking, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
