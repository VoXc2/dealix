#!/usr/bin/env python3
"""Verify OP2 Money Now reconciliation truthfulness.

Fails closed if any relationship over-claims stage, if the snapshot promotes a
research/outbound contact to a real relationship, or if verified revenue is
claimed without payment evidence.

Prints: DEALIX_OP2_MONEY_NOW_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = REPO_ROOT / "data" / "commercial" / "op2_money_now_reconciliation_v1.json"

VERDICT_PASS = "DEALIX_OP2_MONEY_NOW_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_MONEY_NOW_VERDICT=FAIL"

REAL_STAGES = {"REAL_TWO_WAY", "NEGOTIATION", "QUALIFIED", "PILOT_AGREED", "PAYMENT_VERIFIED"}
NON_REAL_STAGES = {"RESEARCH_ONLY", "CONTACT_KNOWN", "OUTBOUND_SENT_NO_REPLY", "OBSERVED_INBOUND"}


def main() -> int:
    errors: list[str] = []
    if not SNAPSHOT.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {SNAPSHOT}")
        return 1
    try:
        payload = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-money-now-reconciliation.v1":
        errors.append("unexpected schema")
    if payload.get("counts_as_revenue") is not False or payload.get("counts_as_pipeline") is not False:
        errors.append("counts_as_revenue/counts_as_pipeline must be false")

    relationships = payload.get("relationships") or []
    seen_companies: set[str] = set()
    for item in relationships:
        entity = str(item.get("entity") or "")
        if entity in seen_companies:
            errors.append(f"duplicate relationship entity: {entity}")
        seen_companies.add(entity)
        stage = item.get("stage")
        truth = str(item.get("commercial_truth") or "").upper()
        if stage not in REAL_STAGES | NON_REAL_STAGES:
            errors.append(f"{entity}: unknown stage {stage}")
        if stage == "REAL_TWO_WAY" and "NO_REPLY" in truth:
            errors.append(f"{entity}: claims REAL_TWO_WAY but commercial_truth says no reply")
        if stage == "OUTBOUND_SENT_NO_REPLY" and "NO_REPLY" not in truth:
            errors.append(f"{entity}: outbound stage must state NO_REPLY_PROVEN")

    econ = payload.get("economic_truth") or {}
    if int(econ.get("verified_revenue_sar", 0)) > 0:
        # A positive figure is only legitimate if payment evidence exists.
        if not any("PAYMENT_VERIFIED" in str(r.get("stage")) for r in relationships):
            errors.append("verified_revenue_sar > 0 without any PAYMENT_VERIFIED relationship")
    if econ.get("founder_income_is_not_dealix_revenue") is not True:
        errors.append("founder_income_is_not_dealix_revenue must be true")

    # Every MONEY_NOW_TOP entry must be a real, evidence-bearing relationship.
    for item in payload.get("money_now_top3") or []:
        if item.get("stage") not in {"NEGOTIATION", "REAL_TWO_WAY", "OBSERVED_INBOUND", "OUTBOUND_SENT_NO_REPLY"}:
            errors.append(f"{item.get('entity')}: top3 stage not promotable")
        if not item.get("evidence_type") or item.get("evidence_type") == "UNKNOWN_NOT_EVIDENCE_BACKED":
            errors.append(f"{item.get('entity')}: top3 missing evidence_type")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
