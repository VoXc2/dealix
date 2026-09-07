#!/usr/bin/env python3
"""Build a bounded Daily Market Advantage execution brief from Universal Market Radar output.

This layer ranks internal execution attention only. It does not create relationship,
consent, opportunity, quote, bid, send, payment, customer-proof, production, or legal
authority. D3 requires an explicit confirmed-problem evidence map supplied separately;
it is never inferred from the mere existence of an inbound/reply signal.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "data/commercial/daily_market_advantage_v1.json"
DEFAULT_RADAR = ROOT / "data/founder_briefs/universal_market_radar_latest.json"
DEFAULT_OUT = ROOT / "data/founder_briefs/daily_market_advantage_latest.json"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

AUTHORITY = {
    "relationship": False,
    "consent": False,
    "offer": False,
    "price": False,
    "quote": False,
    "contract": False,
    "external_send": False,
    "payment": False,
    "customer_proof": False,
    "execution": False,
    "production": False,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def confirmed_problem_ids(path: Path | None) -> set[str]:
    if path is None:
        return set()
    payload = load_json(path)
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict) and isinstance(payload.get("confirmed_problems"), list):
        rows = payload["confirmed_problems"]
    else:
        raise ValueError("confirmed problems must be a list or object with confirmed_problems list")

    confirmed: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        signal_id = str(row.get("signal_id", "")).strip()
        evidence_ref = str(row.get("evidence_ref", "")).strip()
        confirmed_problem = row.get("confirmed_problem") is True
        if signal_id and evidence_ref and confirmed_problem:
            confirmed.add(signal_id)
    return confirmed


def grade_signal(signal: dict[str, Any], config: dict[str, Any], confirmed: set[str]) -> str:
    family = str(signal.get("signal_family", "")).strip()
    signal_id = str(signal.get("signal_id", "")).strip()
    grades = config["demand_grades"]

    if family in grades["D4"]["signal_families"]:
        return "D4"
    if family in grades["D3"]["signal_families"] and signal_id in confirmed:
        return "D3"
    if family in grades["D2"]["signal_families"]:
        return "D2"
    return "D1"


def research_score(value: Any, cap: float) -> float:
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)) and value >= 0:
        return min(cap, round(12.0 * math.log1p(float(value)), 2))
    return 0.0


def execution_priority(signal: dict[str, Any], grade: str, config: dict[str, Any]) -> float:
    score_cfg = config["score"]
    score = research_score(signal.get("priority_score"), float(score_cfg["research_score_cap"]))
    score += float(score_cfg["demand_grade_bonus"].get(grade, 0))
    if signal.get("stale") is True:
        score -= float(score_cfg["stale_penalty"])
    if signal.get("priority_score") == UNKNOWN:
        score -= float(score_cfg["missing_priority_penalty"])
    return round(max(0.0, min(100.0, score)), 2)


def safe_next_action(grade: str, stale: bool, config: dict[str, Any]) -> str:
    if stale:
        return "REVERIFY_STALE_SIGNAL"
    return str(config["execution_route_by_grade"].get(grade, "KEEP_RESEARCH_ONLY"))


def build_brief(radar: dict[str, Any], config: dict[str, Any], confirmed: set[str]) -> dict[str, Any]:
    if radar.get("schema") != config.get("input_contract"):
        raise ValueError("unexpected radar schema")
    if radar.get("authority") != AUTHORITY:
        raise ValueError("radar authority must remain exactly all-false")

    rows = radar.get("ranked_research_signals")
    if not isinstance(rows, list):
        raise ValueError("radar ranked_research_signals must be a list")

    lane_map = config.get("signal_lane_map", {})
    grades = config.get("demand_grades", {})
    candidates: list[dict[str, Any]] = []

    for raw in rows:
        if not isinstance(raw, dict):
            continue
        if raw.get("authority") != AUTHORITY:
            continue

        grade = grade_signal(raw, config, confirmed)
        stale = raw.get("stale") is True
        family = str(raw.get("signal_family", "")).strip()
        candidate = {
            "signal_id": raw.get("signal_id", UNKNOWN),
            "company_or_subject": raw.get("company_or_subject", UNKNOWN),
            "source_id": raw.get("source_id", UNKNOWN),
            "source_ref": raw.get("source_ref", UNKNOWN),
            "signal_family": family or UNKNOWN,
            "lane": lane_map.get(family, "UNMAPPED_RESEARCH"),
            "market": raw.get("market", UNKNOWN),
            "sector_family": raw.get("sector_family", UNKNOWN),
            "demand_grade": grade,
            "demand_grade_label": grades.get(grade, {}).get("label", UNKNOWN),
            "deep_qualification_allowed": bool(grades.get(grade, {}).get("deep_qualification_allowed", False)),
            "confirmed_problem_evidence_required": grade == "D3",
            "execution_priority": execution_priority(raw, grade, config),
            "execution_priority_semantics": config["score"]["semantics"],
            "research_priority_score": raw.get("priority_score", UNKNOWN),
            "stale": stale,
            "facts": raw.get("facts", []),
            "inferences": raw.get("inferences", []),
            "unknowns": raw.get("unknowns", []),
            "evidence_refs": raw.get("evidence_refs", []),
            "next_evidence": raw.get("next_evidence", []),
            "safe_next_action": safe_next_action(grade, stale, config),
            "authority": dict(AUTHORITY),
        }
        candidates.append(candidate)

    candidates.sort(key=lambda row: (-float(row["execution_priority"]), str(row["signal_id"])))
    top_n = int(config.get("wip", {}).get("top_actions_per_cycle", 3))
    top_actions = candidates[:top_n]

    return {
        "schema": "dealix.daily-market-advantage-brief.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "objective": config.get("objective"),
        "source_radar_generated_at": radar.get("generated_at", UNKNOWN),
        "input_signal_count": radar.get("input_signal_count", len(rows)),
        "candidate_count": len(candidates),
        "top_actions": top_actions,
        "ranked_candidates": candidates,
        "wip": config.get("wip", {}),
        "truth_firewall": config.get("truth_firewall", []),
        "new_scheduler": False,
        "new_permanent_agent": False,
        "external_send_or_spend": False,
        "authority": dict(AUTHORITY),
        "truth_notes": [
            "D4 means an explicit procurement signal, not Dealix eligibility, win probability, award, revenue, or cash.",
            "D3 is never inferred from an inbound/reply signal alone; a separate confirmed-problem evidence map is required.",
            "D2 and D1 remain research-only until canonical downstream evidence promotes them.",
            "Execution priority is an internal WIP ordering score only.",
            "This layer cannot submit bids, create relationship/consent, send externally, bind quotes/contracts, or mutate production.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radar", type=Path, default=DEFAULT_RADAR)
    parser.add_argument("--confirmed-problems", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    try:
        config = load_json(args.config)
        if config.get("schema") != "dealix.daily-market-advantage.v1":
            raise ValueError("unexpected market advantage config schema")
        if config.get("authority") != AUTHORITY:
            raise ValueError("market advantage config authority must remain exactly all-false")
        radar = load_json(args.radar)
        confirmed = confirmed_problem_ids(args.confirmed_problems)
        brief = build_brief(radar, config, confirmed)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"DEALIX_DAILY_MARKET_ADVANTAGE=FAIL: {exc}")
        return 1

    atomic_write(args.out, brief)
    print(f"DAILY_MARKET_ADVANTAGE_BRIEF={args.out}")
    print("DEALIX_DAILY_MARKET_ADVANTAGE=PASS")
    print("AUTHORITY=INTERNAL_PRIORITY_ONLY")
    print("NEW_SCHEDULER=NO")
    print("NEW_PERMANENT_AGENT=NO")
    print("OUTBOUND_SPEND=NO")
    if args.stdout:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
