#!/usr/bin/env python3
"""Read-only probability/expected-value selector for Dealix commercial targets.

This runner does not discover synthetic targets, send, publish, charge, merge,
deploy or mutate production. It reads the canonical Company OS target inputs and
emits a ranked internal report. Unknown probabilities remain unknown.
"""
from __future__ import annotations

import argparse
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "config" / "commercial" / "probability_revenue_engine_v1.json"
TARGETS_PATH = ROOT / "data" / "self_operating_company_os" / "targets.json"
REPORT_ROOT = ROOT / "reports" / "probability_revenue_engine"

PROBABILITY_KEYS = (
    "p_real_problem",
    "p_reach_decision_maker",
    "p_response_given_eligible_channel",
    "p_qualified_discovery",
    "p_close",
)
VALUE_KEYS = (
    "expected_margin",
    "proof_value",
    "partner_leverage",
    "repeatability_value",
)
COST_RISK_KEYS = (
    "founder_minutes",
    "delivery_risk",
    "compliance_risk",
    "cash_collection_risk",
)
SUPPRESSED = {"SUPPRESSED", "OPTED_OUT", "WITHDRAWN"}


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def date_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def bounded_probability(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not 0.0 <= number <= 1.0:
        return None
    return number


def finite_nonnegative(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def truth_flags(target: dict[str, Any]) -> dict[str, Any]:
    source = str(target.get("source", "")).strip()
    refs = target.get("evidence_refs")
    evidence_refs = [str(item).strip() for item in refs if str(item).strip()] if isinstance(refs, list) else []
    suppression = str(target.get("suppression_state", "CLEAR")).upper()
    relationship = str(target.get("relationship_state", "RESEARCH")).upper()
    consent = str(target.get("consent_state", "NONE")).upper()
    return {
        "source_present": bool(source),
        "evidence_ref_count": len(evidence_refs),
        "suppression_state": suppression,
        "relationship_state": relationship,
        "consent_state": consent,
        "hard_stop": suppression in SUPPRESSED,
    }


def evidence_ready_for_deep_wip(target: dict[str, Any], flags: dict[str, Any]) -> bool:
    """Require attributable evidence before consuming scarce deep commercial WIP."""
    if not flags["source_present"]:
        return False
    evidence_score = finite_nonnegative(target.get("evidence_score"))
    return flags["evidence_ref_count"] > 0 or (evidence_score is not None and evidence_score >= 50.0)


def probability_ev(target: dict[str, Any]) -> tuple[float | None, dict[str, Any]]:
    probabilities = {key: bounded_probability(target.get(key)) for key in PROBABILITY_KEYS}
    missing = [key for key, value in probabilities.items() if value is None]
    if missing:
        return None, {"probabilities": probabilities, "missing_probability_fields": missing}

    values = {key: finite_nonnegative(target.get(key)) for key in VALUE_KEYS}
    costs = {key: finite_nonnegative(target.get(key)) for key in COST_RISK_KEYS}
    missing_value = [key for key, value in values.items() if value is None]
    missing_cost = [key for key, value in costs.items() if value is None]
    if missing_value or missing_cost:
        return None, {
            "probabilities": probabilities,
            "values": values,
            "cost_risks": costs,
            "missing_value_fields": missing_value,
            "missing_cost_risk_fields": missing_cost,
        }

    p = math.prod(value for value in probabilities.values() if value is not None)
    value_total = sum(value for value in values.values() if value is not None)
    cost_total = max(1.0, sum(value for value in costs.values() if value is not None))
    return p * value_total / cost_total, {
        "probabilities": probabilities,
        "values": values,
        "cost_risks": costs,
    }


def evidence_priority(target: dict[str, Any], flags: dict[str, Any]) -> float:
    def score(name: str, fallback: float) -> float:
        value = finite_nonnegative(target.get(name))
        return min(100.0, value if value is not None else fallback)

    fit = score("fit_score", 50)
    urgency = score("urgency_score", 50)
    evidence = score("evidence_score", 25 if flags["source_present"] else 0)
    access = score("access_score", 10)
    risk = score("risk_score", 50)
    completeness_bonus = min(10.0, flags["evidence_ref_count"] * 2.0) + (5.0 if flags["source_present"] else 0.0)
    raw = fit * 0.30 + urgency * 0.25 + evidence * 0.25 + access * 0.20 - risk * 0.15 + completeness_bonus
    return round(max(0.0, min(100.0, raw)), 3)


def rank_targets(targets: list[dict[str, Any]], deep_wip: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, target in enumerate(targets, start=1):
        flags = truth_flags(target)
        ev, details = probability_ev(target)
        evidence_score = evidence_priority(target, flags)
        deep_wip_evidence_ready = evidence_ready_for_deep_wip(target, flags)
        if flags["hard_stop"]:
            disposition = "STOP_SUPPRESSED"
            rank_key = (-1.0, -1.0)
        elif ev is not None and deep_wip_evidence_ready:
            disposition = "EV_EVIDENCE_READY"
            rank_key = (2.0, ev)
        elif ev is not None:
            disposition = "EV_BLOCKED_EVIDENCE_GAP"
            rank_key = (1.0, evidence_score)
        else:
            disposition = "PROBABILITY_UNKNOWN_RESEARCH_ONLY"
            rank_key = (1.0, evidence_score)

        rows.append(
            {
                "source_index": index,
                "company_name": str(target.get("company_name", "Unknown company")),
                "segment": str(target.get("segment", "unknown")),
                "commercial_stage": str(target.get("commercial_stage", "RESEARCH")).upper(),
                "disposition": disposition,
                "expected_value": round(ev, 8) if ev is not None else None,
                "evidence_priority": evidence_score,
                "deep_wip_evidence_ready": deep_wip_evidence_ready,
                "truth": flags,
                "ev_detail": details,
                "next_action": str(target.get("next_action", "")).strip(),
                "_rank_key": rank_key,
            }
        )

    rows.sort(key=lambda item: item["_rank_key"], reverse=True)
    active = 0
    for position, row in enumerate(rows, start=1):
        row["rank"] = position
        if (
            row["disposition"] != "STOP_SUPPRESSED"
            and row["deep_wip_evidence_ready"] is True
            and active < deep_wip
        ):
            row["deep_wip_candidate"] = True
            active += 1
        else:
            row["deep_wip_candidate"] = False
        row.pop("_rank_key", None)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1500)
    args = parser.parse_args()

    contract = load_json(CONTRACT_PATH, {})
    if not contract:
        print("PROBABILITY_REVENUE_ENGINE=BLOCKED_CONTRACT_MISSING_OR_INVALID")
        return 2
    if contract.get("authority", {}).get("external_send") is not False:
        print("PROBABILITY_REVENUE_ENGINE=BLOCKED_EXTERNAL_SEND_AUTHORITY")
        return 2

    raw_signal_ceiling = int(contract["capacity_ceiling_per_operating_day"]["raw_signal_refresh"])
    requested_limit = max(0, args.limit)
    effective_limit = min(requested_limit, raw_signal_ceiling)

    raw_targets = load_json(TARGETS_PATH, [])
    targets = [item for item in raw_targets if isinstance(item, dict)][:effective_limit] if isinstance(raw_targets, list) else []
    deep_wip = int(contract["capacity_ceiling_per_operating_day"]["deep_commercial_wip"])
    ranked = rank_targets(targets, deep_wip)

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at": utc_stamp(),
        "mode": "draft-only",
        "requested_limit": requested_limit,
        "effective_limit": effective_limit,
        "raw_signal_ceiling": raw_signal_ceiling,
        "target_count": len(targets),
        "deep_wip_limit": deep_wip,
        "unknown_probability_policy": contract["unknown_probability_policy"],
        "external_send_authority": False,
        "ranked_targets": ranked,
    }
    path = REPORT_ROOT / f"{date_stamp()}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"PROBABILITY_REVENUE_REPORT={path.relative_to(ROOT)}")
    print("PROBABILITY_REVENUE_ENGINE=PASS_DRAFT_ONLY")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())