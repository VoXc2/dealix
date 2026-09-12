#!/usr/bin/env python3
"""OP2 B2G / Etimad + partner-economy research artifact.

Bridges the OP2 market wave into two research surfaces the founder actually
acts on:

  * B2G radar  — tender/procurement signals, each with a strict bid/no-bid
    posture defaulting to PARTNER_OR_NO_BID until eligibility, credentials,
    economics and bid authority are proven.
  * Partner economy — leverages the canonical ``PartnerEconomy`` scorer to rank
    partner motions (SI, ERP, accounting/Fatoora, cyber, cloud, consultancy)
    against the OP2 priority sectors.

A tender is not a relationship. Research is not consent. This tool never
submits, contacts, or commits. Default bid posture is PARTNER_OR_NO_BID.

Prints: DEALIX_OP2_B2G_PARTNER=OK plus machine lines.
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
ECONOMY_PATH = REPO_ROOT / "data" / "commercial" / "op2_sector_economy_ranking_v1.json"
OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_b2g_partner_research_v1.json"

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

# Partner motion hypotheses per OP2 priority sector. Scores are internal
# research priors (1-5), never claims about a named partner.
PARTNER_HYPOTHESES: list[dict[str, Any]] = [
    {
        "partner_id": "op2-si-gov",
        "type": "system_integrator",
        "motion": "white_label",
        "sector_fit": ["government_b2g", "technology_saas_si"],
        "access_score": 4,
        "capability_score": 4,
        "trust_score": 4,
        "margin_share_pct": 0.2,
        "win_rate": 0.3,
        "proof_reuse": 3,
        "rationale": "Governed AI execution backend behind an SI with existing Etimad credentials.",
    },
    {
        "partner_id": "op2-erp-fatoora",
        "type": "erp_vendor",
        "motion": "co_sell",
        "sector_fit": ["finance_fintech_insurance", "retail_commerce_ecommerce"],
        "access_score": 4,
        "capability_score": 3,
        "trust_score": 4,
        "margin_share_pct": 0.15,
        "win_rate": 0.35,
        "proof_reuse": 3,
        "rationale": "E-invoicing/ERP implementers already inside ZATCA Wave 25 scoped clients.",
    },
    {
        "partner_id": "op2-accounting",
        "type": "accounting",
        "motion": "referral",
        "sector_fit": ["finance_fintech_insurance"],
        "access_score": 5,
        "capability_score": 3,
        "trust_score": 4,
        "margin_share_pct": 0.12,
        "win_rate": 0.4,
        "proof_reuse": 4,
        "rationale": "Fatoora/accounting firms hold the exact Wave 25 client relationships.",
    },
    {
        "partner_id": "op2-cyber",
        "type": "cyber_firm",
        "motion": "co_sell",
        "sector_fit": ["technology_saas_si", "government_b2g"],
        "access_score": 3,
        "capability_score": 4,
        "trust_score": 4,
        "margin_share_pct": 0.18,
        "win_rate": 0.3,
        "proof_reuse": 3,
        "rationale": "NCA ECC-2/PDPL evidence work pairs with cybersecurity delivery partners.",
    },
    {
        "partner_id": "op2-cloud",
        "type": "cloud_provider",
        "motion": "integration",
        "sector_fit": ["technology_saas_si", "healthcare"],
        "access_score": 4,
        "capability_score": 5,
        "trust_score": 4,
        "margin_share_pct": 0.15,
        "win_rate": 0.3,
        "proof_reuse": 3,
        "rationale": "Sovereign/cloud residency work sits alongside cloud partners.",
    },
]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_b2g(wave: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for signal in wave.get("signals", []) or []:
        family = str(signal.get("signal_family"))
        sector = str(signal.get("sector_family"))
        if family != "TENDER_OR_PROCUREMENT" and sector not in {"AVIATION_DEFENSE", "HEALTHCARE_LIFE_SCIENCES"}:
            if sector != "AVIATION_DEFENSE":
                continue
        if family != "TENDER_OR_PROCUREMENT":
            continue
        items.append(
            {
                "signal_id": signal.get("signal_id"),
                "agency_or_channel": signal.get("authority_ref", UNKNOWN),
                "deadline": signal.get("deadline", UNKNOWN),
                "scope": signal.get("problem", UNKNOWN),
                "eligibility": UNKNOWN,
                "fit": signal.get("sector_family"),
                "partner_requirement": "EXPECTED_LOCAL_CONTENT_OR_PRIME",
                "delivery_burden": "HIGH_LICENSES_STAFFING_GUARANTEES",
                "economic_potential": "UNKNOWN_NOT_INVENTED",
                "risk": "HIGH_IF_DIRECT_BID_WITHOUT_CREDENTIALS",
                "bid_posture": "PARTNER_OR_NO_BID",
                "source_ref": signal.get("source_ref"),
                "evidence_refs": signal.get("evidence_refs") or [],
                "truth_class": "RESEARCH_ONLY_NOT_SUBMISSION",
                "counts_as_relationship": False,
            }
        )
    return items


def rank_partners() -> list[dict[str, Any]]:
    from dealix.commercial.partner_economy import (
        PartnerCandidate,
        PartnerEconomy,
        PartnerMotion,
        PartnerType,
    )

    economy = PartnerEconomy()
    for item in PARTNER_HYPOTHESES:
        economy.add(
            PartnerCandidate(
                partner_id=item["partner_id"],
                name=item["partner_id"],
                type=PartnerType(item["type"]),
                motion=PartnerMotion(item["motion"]),
                sector_fit=item["sector_fit"],
                access_score=item["access_score"],
                capability_score=item["capability_score"],
                trust_score=item["trust_score"],
                margin_share_pct=item["margin_share_pct"],
                win_rate=item["win_rate"],
                proof_reuse=item["proof_reuse"],
            )
        )
    ranked = economy.rank()
    rationale = {item["partner_id"]: item["rationale"] for item in PARTNER_HYPOTHESES}
    return [
        {
            "partner_id": partner.partner_id,
            "type": str(partner.type),
            "motion": str(partner.motion),
            "sector_fit": partner.sector_fit,
            "economic_score": partner.economic_score(),
            "rationale": rationale.get(partner.partner_id, UNKNOWN),
            "relationship_state": "RESEARCH_ONLY",
            "counts_as_relationship": False,
        }
        for partner in ranked
    ]


def build() -> dict[str, Any]:
    wave = _read_json(WAVE_PATH)
    economy = _read_json(ECONOMY_PATH)
    warnings: list[str] = []
    if not wave:
        warnings.append(f"market wave unreachable: {WAVE_PATH}")
    if not economy:
        warnings.append(f"sector economy ranking unreachable: {ECONOMY_PATH}")

    b2g = build_b2g(wave)
    partners = rank_partners()
    return {
        "schema": "dealix.op2-b2g-partner-research.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "truth_policy": "RESEARCH_ONLY_NO_RELATIONSHIP_NO_SUBMISSION_NO_CONSENT",
        "authority": {
            "relationship": False,
            "consent": False,
            "tender_submission": False,
            "external_send": False,
            "contract": False,
            "payment": False,
        },
        "default_bid_posture": "PARTNER_OR_NO_BID",
        "warnings": warnings,
        "b2g_items": b2g,
        "top_priority_sectors": [cell["sector_id"] for cell in (economy.get("cells") or [])[:3]],
        "partner_candidates": partners,
        "counts_as_relationship": False,
        "counts_as_pipeline": False,
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        "DEALIX_OP2_B2G_PARTNER=OK",
        f"B2G_ITEMS={len(result['b2g_items'])}",
        f"PARTNER_CANDIDATES={len(result['partner_candidates'])}",
        f"DEFAULT_BID_POSTURE={result['default_bid_posture']}",
    ]
    for index, item in enumerate(result["b2g_items"], start=1):
        lines.append(f"B2G_{index} {item['signal_id']} posture={item['bid_posture']} deadline={item['deadline']}")
    for index, partner in enumerate(result["partner_candidates"], start=1):
        lines.append(f"PARTNER_{index} {partner['partner_id']} motion={partner['motion']} score={partner['economic_score']}")
    for warning in result["warnings"]:
        lines.append(f"WARN {warning}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 B2G / partner research")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build()
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
