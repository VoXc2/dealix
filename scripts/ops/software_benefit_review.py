#!/usr/bin/env python3
"""Evidence-backed 7/30-day benefit review for adopted software candidates."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

OPS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(OPS_DIR))

from software_acquisition_factory import DEFAULT_REGISTRY, DEFAULT_STATE, load_json, write_json

REVIEW_SCHEMA = "dealix.software_benefit_review.v2"


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _positive_refs(value: Any) -> bool:
    return isinstance(value, list) and any(str(item).strip() for item in value)


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
    policy_incidents = _number(observations.get("policy_incidents"))
    data_egress_incidents = _number(observations.get("unexpected_data_egress_incidents"))
    success_rate = _number(observations.get("job_success_rate"))
    founder_minutes_saved = _number(observations.get("founder_minutes_saved"))
    cash_saved = _number(observations.get("cash_saved"))
    cash_cost = _number(observations.get("cash_cost"))
    maintenance_minutes = _number(observations.get("maintenance_minutes"))
    evidence_refs = observations.get("evidence_refs")

    if not _positive_refs(evidence_refs):
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "HOLD_UNKNOWN",
            "reason": "benefit observations lack evidence refs",
            "counts_as_verified_value": False,
        }

    vuln = str(candidate.get("vulnerability_status") or "UNKNOWN").upper()
    if bool(candidate.get("cisa_kev_match")):
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "QUARANTINE",
            "reason": "candidate matches CISA Known Exploited Vulnerabilities evidence",
            "counts_as_verified_value": False,
            "evidence_refs": evidence_refs,
        }
    if vuln in {"CRITICAL", "HIGH", "KNOWN_CRITICAL", "KNOWN_HIGH", "BLOCKED_CRITICAL", "BLOCKED_HIGH"}:
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "QUARANTINE",
            "reason": "unresolved high/critical vulnerability evidence",
            "counts_as_verified_value": False,
            "evidence_refs": evidence_refs,
        }
    if any(
        value is not None and value > 0
        for value in (security_incidents, policy_incidents, data_egress_incidents)
    ):
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "QUARANTINE",
            "reason": "security, policy, or unexpected data-egress incident observed",
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
    low_maintenance = maintenance_minutes is None or maintenance_minutes <= max(60.0, founder_minutes_saved or 0.0)

    if window_days >= 30 and positive_value and (success_rate is None or success_rate >= 0.90) and low_maintenance:
        rollback_tested = bool(observations.get("rollback_tested"))
        rollback_refs = observations.get("rollback_evidence_refs")
        duplicate_stack_creep = bool(observations.get("duplicate_stack_creep"))
        keep_reason = str(observations.get("economic_reason_to_keep") or "").strip()
        if not rollback_tested or not _positive_refs(rollback_refs):
            return {
                "candidate_id": candidate_id,
                "window_days": window_days,
                "decision": "HOLD_MEASURE",
                "reason": "30-day promotion requires tested rollback with evidence",
                "counts_as_verified_value": False,
                "evidence_refs": evidence_refs,
            }
        if duplicate_stack_creep:
            return {
                "candidate_id": candidate_id,
                "window_days": window_days,
                "decision": "DEMOTE",
                "reason": "duplicate stack creep detected",
                "counts_as_verified_value": False,
                "evidence_refs": evidence_refs,
            }
        if not keep_reason:
            return {
                "candidate_id": candidate_id,
                "window_days": window_days,
                "decision": "HOLD_MEASURE",
                "reason": "30-day promotion requires explicit economic reason to keep",
                "counts_as_verified_value": False,
                "evidence_refs": evidence_refs,
            }
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "PROMOTE",
            "reason": "persistent verified benefit, reliability, rollback proof, and policy safety",
            "counts_as_verified_value": True,
            "net_cash_positive": net_cash_positive,
            "rollback_evidence_refs": rollback_refs,
            "economic_reason_to_keep": keep_reason,
            "evidence_refs": evidence_refs,
        }

    if window_days < 30 and positive_value and (success_rate is None or success_rate >= 0.90) and low_maintenance:
        return {
            "candidate_id": candidate_id,
            "window_days": window_days,
            "decision": "KEEP_CANARY",
            "reason": "7-day evidence-backed benefit with acceptable reliability; continue bounded canary",
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
