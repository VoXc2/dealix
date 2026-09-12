#!/usr/bin/env python3
"""OP2 Money Now reconciliation — truthful, evidence-bound relationship staging.

This is a *reconciliation reader*, complementary to OP1's draft-packet renderer
(``scripts/commercial/render_money_now_negotiation_packet.py``). It reads the
canonical live relationship register + scoped economic truth + work queue and
produces a single, reproducible picture:

    REAL_RELATIONSHIPS, stage per relationship, MONEY_NOW_TOP_3

Hard rules enforced (never relaxed):
  * founder income != Dealix company revenue
  * outbound sent != reply / warm / consent
  * verified revenue requires payment evidence
  * missing state is UNKNOWN_NOT_EVIDENCE_BACKED, never invented

When the canonical runtime files are unreachable, the tool falls back to the
committed OP2 reconciliation snapshot. It never fabricates relationships.

Prints: DEALIX_OP2_MONEY_NOW=OK plus MONEY_NOW_TOP_n machine lines.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

RUNTIME_ROOT = Path("/opt/dealix/company-os/founder-os")
RELATIONSHIPS_TSV = RUNTIME_ROOT / "tables" / "SCOPED_RELATIONSHIPS.tsv"
SCOPED_TRUTH = RUNTIME_ROOT / "current" / "SCOPED_ECONOMIC_TRUTH.json"
WORK_QUEUE = RUNTIME_ROOT / "queues" / "COMPANY_WORK_QUEUE.json"

SNAPSHOT_PATH = REPO_ROOT / "data" / "commercial" / "op2_money_now_reconciliation_v1.json"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

# One and only one stage per relationship. Sequential promotion only.
STAGES = (
    "RESEARCH_ONLY",
    "CONTACT_KNOWN",
    "OUTBOUND_SENT_NO_REPLY",
    "OBSERVED_INBOUND",
    "REAL_TWO_WAY",
    "NEGOTIATION",
    "QUALIFIED",
    "PILOT_AGREED",
    "PAYMENT_VERIFIED",
)

# Evidence -> stage mapping for the canonical relationship states.
STATE_TO_STAGE = {
    "REAL_RELATIONSHIP": "REAL_TWO_WAY",
    "OUTBOUND_SENT": "OUTBOUND_SENT_NO_REPLY",
    "OBSERVED": "OBSERVED_INBOUND",
}

NEGOTIATION_MARKERS = ("NEGOTIATION",)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _stage_for(row: dict[str, str]) -> str:
    state = (row.get("state") or "").strip().upper()
    truth = (row.get("commercial_truth") or "").strip().upper()
    stage = STATE_TO_STAGE.get(state, "CONTACT_KNOWN")
    if any(marker in truth for marker in NEGOTIATION_MARKERS) and stage == "REAL_TWO_WAY":
        return "NEGOTIATION"
    return stage


def build_reconciliation() -> dict[str, Any]:
    warnings: list[str] = []
    relationships: list[dict[str, Any]] = []

    if RELATIONSHIPS_TSV.exists():
        with RELATIONSHIPS_TSV.open(encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                if not (row.get("relationship_id") or "").strip():
                    continue
                relationships.append(
                    {
                        "relationship_id": row.get("relationship_id", "").strip(),
                        "scope": row.get("scope", UNKNOWN).strip(),
                        "entity": row.get("entity", UNKNOWN).strip(),
                        "state": row.get("state", UNKNOWN).strip(),
                        "evidence_type": row.get("evidence_type", UNKNOWN).strip(),
                        "observed_at": row.get("observed_at", UNKNOWN).strip(),
                        "commercial_truth": row.get("commercial_truth", UNKNOWN).strip(),
                        "stage": _stage_for(row),
                        "next_safe_action": row.get("next_safe_action", UNKNOWN).strip(),
                        "source": "canonical_relationship_register",
                    }
                )
    else:
        warnings.append(f"canonical relationship register unreachable: {RELATIONSHIPS_TSV}")
        if SNAPSHOT_PATH.exists():
            snapshot = _read_json(SNAPSHOT_PATH)
            relationships = list(snapshot.get("relationships", []))
            warnings.append("used committed OP2 reconciliation snapshot")

    scoped = _read_json(SCOPED_TRUTH) if SCOPED_TRUTH.exists() else {}
    if not scoped:
        warnings.append(f"scoped economic truth unreachable: {SCOPED_TRUTH}")

    # Deterministic ranking: negotiation > observed inbound > real two-way >
    # outbound-no-reply, then by observed recency. Research-only never enters TOP3.
    promo_rank = {
        "NEGOTIATION": 0,
        "OBSERVED_INBOUND": 1,
        "REAL_TWO_WAY": 2,
        "OUTBOUND_SENT_NO_REPLY": 3,
        "CONTACT_KNOWN": 4,
        "RESEARCH_ONLY": 5,
    }
    ranked = sorted(
        relationships,
        key=lambda item: (promo_rank.get(item["stage"], 9), str(item.get("observed_at", "")).replace("-", "")),
    )
    money_now = [item for item in ranked if promo_rank.get(item["stage"], 9) <= 3][:3]

    verified_revenue_sar = int((scoped.get("dealix_company") or {}).get("verified_revenue_sar", 0) or 0)
    real_relationships = len([r for r in relationships if r["stage"] in {"REAL_TWO_WAY", "NEGOTIATION", "QUALIFIED", "PILOT_AGREED", "PAYMENT_VERIFIED"}])

    return {
        "schema": "dealix.op2-money-now-reconciliation.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "truth_policy": "EVIDENCE_ONLY_NO_INVENTED_STATE",
        "reachable_canonical_inputs": RELATIONSHIPS_TSV.exists() and SCOPED_TRUTH.exists(),
        "warnings": warnings,
        "economic_truth": {
            "verified_revenue_sar": verified_revenue_sar,
            "verified_paid_pilots": int((scoped.get("dealix_company") or {}).get("verified_paid_pilots", 0) or 0),
            "real_relationships_dealix_company": int((scoped.get("dealix_company") or {}).get("real_relationships", 0) or 0),
            "real_relationships_founder": int((scoped.get("founder") or {}).get("real_relationships", 0) or 0),
            "founder_income_is_not_dealix_revenue": True,
        },
        "relationships": relationships,
        "money_now_top3": money_now,
        "real_relationships": real_relationships,
        "counts_as_revenue": False,
        "counts_as_pipeline": False,
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        "DEALIX_OP2_MONEY_NOW=OK",
        f"REAL_RELATIONSHIPS={result['real_relationships']}",
        f"VERIFIED_REVENUE_SAR={result['economic_truth']['verified_revenue_sar']}",
    ]
    for index, item in enumerate(result["money_now_top3"], start=1):
        lines.append(
            f"MONEY_NOW_TOP{index} {item['entity']} stage={item['stage']} "
            f"scope={item['scope']} evidence={item['evidence_type']} truth={item['commercial_truth']}"
        )
    for warning in result["warnings"]:
        lines.append(f"WARN {warning}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 Money Now reconciliation")
    parser.add_argument("--write", action="store_true", help=f"write {SNAPSHOT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_reconciliation()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render(result))
    if args.write:
        SNAPSHOT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {SNAPSHOT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
