#!/usr/bin/env python3
"""Generate a read-only Universal Market Radar brief for existing Dealix runners.

The runner consumes normalized MarketSignalReceipt rows and the machine-readable
radar/playbook registries. It ranks internal research attention only. It cannot
create relationship, consent, opportunity, package, send, quote, payment, proof,
execution, production, spend, or scheduler authority.
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
RADAR_PATH = ROOT / "data/commercial/universal_market_radar_v1.json"
PLAYBOOK_PATH = ROOT / "data/commercial/universal_market_playbooks_v1.json"
SOURCE_ACCESS_PATH = ROOT / "data/commercial/market_radar_source_access_state_v1.json"
DEFAULT_OUT = ROOT / "data/founder_briefs/universal_market_radar_latest.json"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

FACTOR_NAMES = (
    "economic_pain",
    "measurable_outcome",
    "buyer_access",
    "data_availability",
    "repeatability",
    "readiness",
    "distribution_density",
    "regulatory_friction",
    "integration_complexity",
    "founder_minutes",
)

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


def load_source_access_state() -> dict[str, Any]:
    if not SOURCE_ACCESS_PATH.exists():
        return {
            "schema": "dealix.market-radar-source-access-state.v1",
            "observed_at": UNKNOWN,
            "source_states": {},
        }
    payload = load_json(SOURCE_ACCESS_PATH)
    if not isinstance(payload, dict):
        raise ValueError("source access state must be a JSON object")
    if payload.get("schema") != "dealix.market-radar-source-access-state.v1":
        raise ValueError("unexpected source access state schema")
    states = payload.get("source_states")
    if not isinstance(states, dict):
        raise ValueError("source access state source_states must be an object")
    return payload


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(UTC)


def validate_receipt(receipt: Any, required: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(receipt, dict):
        return ["receipt must be an object"]
    missing = sorted(required - set(receipt))
    if missing:
        errors.append(f"missing fields: {missing}")
    if not str(receipt.get("signal_id", "")).strip():
        errors.append("signal_id must be non-empty")
    if not str(receipt.get("source_id", "")).strip():
        errors.append("source_id must be non-empty")
    if not str(receipt.get("source_ref", "")).strip():
        errors.append("source_ref must be non-empty")
    if not str(receipt.get("provenance_ref", "")).strip():
        errors.append("provenance_ref must be non-empty")
    if parse_time(receipt.get("observed_at")) is None:
        errors.append("observed_at must be timezone-aware ISO time")
    if parse_time(receipt.get("ingested_at")) is None:
        errors.append("ingested_at must be timezone-aware ISO time")
    if parse_time(receipt.get("fresh_until")) is None:
        errors.append("fresh_until must be timezone-aware ISO time")
    if receipt.get("authority") != AUTHORITY:
        errors.append("receipt authority must exactly match all-false radar authority")
    for field in ("evidence_refs", "facts", "inferences", "unknowns", "next_evidence"):
        if not isinstance(receipt.get(field), list):
            errors.append(f"{field} must be a list")
    return errors


def numeric_factor(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        try:
            number = float(value.strip())
        except ValueError:
            return None
    else:
        return None
    if not 1.0 <= number <= 5.0:
        return None
    return number


def priority_score(receipt: dict[str, Any]) -> tuple[float | None, list[str]]:
    factors = receipt.get("priority_factors")
    if not isinstance(factors, dict):
        return None, list(FACTOR_NAMES)

    values: dict[str, float] = {}
    missing: list[str] = []
    for name in FACTOR_NAMES:
        value = numeric_factor(factors.get(name))
        if value is None:
            missing.append(name)
        else:
            values[name] = value
    if missing:
        return None, missing

    numerator_names = (
        "economic_pain",
        "measurable_outcome",
        "buyer_access",
        "data_availability",
        "repeatability",
        "readiness",
        "distribution_density",
    )
    denominator_names = (
        "regulatory_friction",
        "integration_complexity",
        "founder_minutes",
    )
    log_score = sum(math.log(values[name]) for name in numerator_names) - sum(
        math.log(values[name]) for name in denominator_names
    )
    return round(math.exp(log_score), 4), []


def build_sector_index(playbooks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("id")): row
        for row in playbooks.get("sector_families", [])
        if isinstance(row, dict) and row.get("id")
    }


def blocked_source_ids(access: dict[str, Any]) -> set[str]:
    blocked: set[str] = set()
    for source_id, state in access.get("source_states", {}).items():
        if isinstance(state, dict) and state.get("admit_new_receipts") is False:
            blocked.add(str(source_id))
    return blocked


def build_brief(signals: list[Any]) -> dict[str, Any]:
    radar = load_json(RADAR_PATH)
    playbooks = load_json(PLAYBOOK_PATH)
    source_access = load_source_access_state()
    required = set(radar.get("market_signal_receipt_contract", {}).get("required", []))
    source_ids = {
        str(row.get("source_id"))
        for row in radar.get("source_registry", [])
        if isinstance(row, dict) and row.get("source_id")
    }
    blocked_sources = blocked_source_ids(source_access)
    sector_index = build_sector_index(playbooks)
    now = datetime.now(UTC)

    valid_rows: list[dict[str, Any]] = []
    invalid_rows: list[dict[str, Any]] = []
    for raw in signals:
        errors = validate_receipt(raw, required)
        if isinstance(raw, dict):
            source_id = str(raw.get("source_id", "")).strip()
            if source_id not in source_ids:
                errors.append(f"source_id is not admitted by registry: {source_id}")
            elif source_id in blocked_sources:
                source_state = source_access["source_states"].get(source_id, {})
                state = source_state.get("state", "BLOCKED_CAPABILITY")
                reason = source_state.get("reason", UNKNOWN)
                errors.append(
                    f"source_id is blocked by current access state: {source_id}:{state}:{reason}"
                )
            sector_id = str(raw.get("sector_family", "")).strip()
            if sector_id not in sector_index:
                errors.append(f"sector_family is not in the 15-sector universe: {sector_id}")
        if errors:
            invalid_rows.append(
                {
                    "signal_id": raw.get("signal_id", UNKNOWN) if isinstance(raw, dict) else UNKNOWN,
                    "errors": errors,
                    "status": "INVALID_NOT_ADMITTED_TO_RADAR",
                }
            )
            continue

        receipt = dict(raw)
        score, missing_factors = priority_score(receipt)
        fresh_until = parse_time(receipt.get("fresh_until"))
        stale = fresh_until is None or fresh_until <= now
        sector = sector_index[str(receipt["sector_family"])]
        cluster = str(sector.get("cluster", UNKNOWN))
        cluster_playbook = playbooks.get("cluster_playbooks", {}).get(cluster, {})

        valid_rows.append(
            {
                "signal_id": receipt["signal_id"],
                "source_id": receipt["source_id"],
                "source_ref": receipt["source_ref"],
                "signal_family": receipt["signal_family"],
                "company_or_subject": receipt.get("company_or_subject", UNKNOWN),
                "market": receipt["market"],
                "sector_family": receipt["sector_family"],
                "operating_cluster": cluster,
                "sector_priority_tier": sector.get("priority", UNKNOWN),
                "business_archetype": receipt["business_archetype"],
                "priority_score": score if score is not None else UNKNOWN,
                "priority_score_missing_factors": missing_factors,
                "priority_score_semantics": "INTERNAL_RESEARCH_PRIORITY_ONLY_NOT_PURCHASE_PROBABILITY",
                "fresh_until": receipt["fresh_until"],
                "stale": stale,
                "facts": receipt["facts"],
                "inferences": receipt["inferences"],
                "unknowns": receipt["unknowns"],
                "evidence_refs": receipt["evidence_refs"],
                "next_evidence": receipt["next_evidence"],
                "playbook_hypotheses": {
                    "pain_taxonomy": cluster_playbook.get("pain_taxonomy", []),
                    "buyer_map": cluster_playbook.get("buyer_map", []),
                    "package_fit": cluster_playbook.get("package_fit", []),
                    "channel_hypotheses": cluster_playbook.get("channel_hypotheses", []),
                    "proof_methods": cluster_playbook.get("proof_methods", []),
                },
                "next_action": (
                    "REVERIFY_STALE_SIGNAL"
                    if stale
                    else "CONTINUE_RESEARCH_OR_HAND_TO_CANONICAL_PORTFOLIO_ROUTER_ONLY_AFTER_CANONICAL_INTERACTION_OR_EXPLICIT_INBOUND_EVIDENCE"
                ),
                "authority": dict(AUTHORITY),
                "status": "STALE_REVERIFY_REQUIRED" if stale else "RESEARCH_SIGNAL_ADMITTED",
            }
        )

    valid_rows.sort(
        key=lambda row: (
            row["stale"],
            -(row["priority_score"] if isinstance(row["priority_score"], (int, float)) else -1.0),
            str(row["signal_id"]),
        )
    )

    return {
        "schema": "dealix.universal-market-radar-brief.v1",
        "scope": "dealix_company",
        "generated_at": now.isoformat(),
        "objective": radar.get("objective"),
        "input_signal_count": len(signals),
        "admitted_signal_count": len(valid_rows),
        "invalid_signal_count": len(invalid_rows),
        "ranked_research_signals": valid_rows,
        "invalid_signals": invalid_rows,
        "source_access_state_observed_at": source_access.get("observed_at", UNKNOWN),
        "blocked_source_ids": sorted(blocked_sources),
        "blocked_source_semantics": "BLOCKED_CAPABILITY_IS_UNKNOWN_NOT_ZERO_DEMAND",
        "canonical_next_stage_owner": "dealix/commercial/portfolio_router.py",
        "new_scheduler": False,
        "new_permanent_agent": False,
        "external_send_or_spend": False,
        "authority": dict(AUTHORITY),
        "truth_notes": [
            "The radar ranks research attention only; score is never purchase probability.",
            "A radar signal cannot create relationship, consent, opportunity, package authority, quote, payment, proof, execution or production truth.",
            "Commercial package routing remains owned by the canonical portfolio router and requires its canonical interaction/inbound evidence semantics.",
            "Expired signals must be reverified before downstream use.",
            "A conceptually supported source with blocked current access cannot admit a new handoff; missing metrics stay UNKNOWN_NOT_EVIDENCE_BACKED rather than zero.",
        ],
    }


def read_signals(path: Path | None) -> list[Any]:
    if path is None:
        return []
    value = load_json(path)
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("signals"), list):
        return value["signals"]
    raise ValueError("signals input must be a JSON list or an object containing a signals list")


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temp = path.with_name(f".{path.name}.tmp")
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--signals", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    try:
        signals = read_signals(args.signals)
        brief = build_brief(signals)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"DEALIX_UNIVERSAL_MARKET_RADAR_RUNNER=FAIL: {exc}")
        return 1

    atomic_write(args.out, brief)
    print(f"UNIVERSAL_MARKET_RADAR_BRIEF={args.out}")
    print("DEALIX_UNIVERSAL_MARKET_RADAR_RUNNER=PASS")
    print("RADAR_AUTHORITY=RESEARCH_PRIORITY_ONLY")
    print("NEW_SCHEDULER=NO")
    print("OUTBOUND_SPEND=NO")
    if args.stdout:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
