#!/usr/bin/env python3
"""Evidence-backed 7/30-day benefit review for adopted software candidates."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from software_acquisition_factory import DEFAULT_REGISTRY, DEFAULT_STATE, load_json, write_json

REVIEW_SCHEMA = "dealix.software_benefit_review.v1"


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def review_candidate(candidate: dict[str, Any], *, window_days: int) -> dict[str, Any]:
    candidate_id = str(candidate.get("candidate_id") or "UNKNOWN")
    observations = candidate.get("benefit_observations")
    if not isinstance(observations, dict):
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "HOLD_UNKNOWN",
            "reason": "missing benefit_observations",
            "counts_as_verified_value": False,
        }

    security_incidents = _number(observations.get("security_incidents"))
    success_rate = _number(observations.get("job_success_rate"))
    founder_minutes_saved = _number(observations.get("founder_minutes_saved"))
    cash_saved = _number(observations.get("cash_saved"))
    cash_cost = _number(observations.get("cash_cost"))
    maintenance_minutes = _number(observations.get("maintenance_minutes"))
    evidence_refs = observations.get("evidence_refs")

    if not isinstance(evidence_refs, list) or not evidence_refs:
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "HOLD_UNKNOWN",
            "reason": "benefit observations lack evidence refs",
            "counts_as_verified_value": False,
        }

    vuln = str(candidate.get("vulnerability_status") or "UNKNOWN").upper()
    if vuln in {"CRITICAL", "KNOWN_CRITICAL", "BLOCKED_CRITICAL"} or (security_incidents is not None and security_incidents > 0):
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "QUARANTINE",
            "reason": "security regression or critical vulnerability evidence",
            "counts_as_verified_value": False,
            "evidence_refs": evidence_refs,
        }

    if success_rate is not None and success_rate < 0.70:
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "DEMOTE",
            "reason": "observed job success rate below 70%",
            "counts_as_verified_value": False,
            "evidence_refs": evidence_refs,
        }

    positive_value = (
        (founder_minutes_saved is not None and founder_minutes_saved > 0)
        or (cash_saved is not None and cash_saved > 0)
    )
    net_cash_positive = cash_saved is not None and cash_cost is not None and cash_saved > cash_cost
    low_maintenance = maintenance_minutes is None or maintenance_minutes <= max(60.0, (founder_minutes_saved or 0.0))

    if positive_value and (success_rate is None or success_rate >= 0.90) and low_maintenance:
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "PROMOTE" if window_days >= 30 else "KEEP_CANARY",
            "reason": "evidence-backed operational/economic benefit with acceptable reliability",
            "counts_as_verified_value": True,
            "net_cash_positive": net_cash_positive,
            "evidence_refs": evidence_refs,
        }

    if window_days >= 30 and cash_cost is not None and cash_cost > 0 and not positive_value:
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "KILL",
            "reason": "30-day evidence shows cost without verified benefit",
            "counts_as_verified_value": False,
            "evidence_refs": evidence_refs,
        }

    return {
        "candidate_id": candidate_id,
        "window_days": window_days,
        "decision": "HOLD_MEASURE",
        "reason": "insufficient evidence for promote/kill decision",
        "counts_as_verified_value": False,
        "evidence_refs": evidence_refs,
    }


def run_review(registry_path: Path, *, window_days: int) -> dict[str, Any]:
    payload = load_json(registry_path, {"candidates": []})
    candidates = payload if isinstance(payload, list) else payload.get("candidates", []) if isinstance(payload, dict) else []
    results = [review_candidate(item, window_days=window_days) for item in candidates if isinstance(item, dict)]
    return {
        "schema": REVIEW_SCHEMA,
        "generated_at": now_iso(),
        "window_days": window_days,
        "candidate_count": len(results),
        "results": results,
        "external_effects_executed": 0,
        "l5_executed": "NONE",
    }


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--window-days", type=int, choices=(7, 30), default=7)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    receipt = run_review(args.registry, window_days=args.window_days)
    output = args.state_dir / f"SOFTWARE_BENEFIT_REVIEW_{args.window_days}D.json"
    write_json(output, receipt)
    if args.stdout:
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
    print("DEALIX_SOFTWARE_BENEFIT_REVIEW=PASS")
    print(f"WINDOW_DAYS={args.window_days}")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
