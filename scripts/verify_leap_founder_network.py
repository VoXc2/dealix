#!/usr/bin/env python3
"""Deterministic verifier for the Dealix LEAP Founder Network contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "commercial" / "leap_founder_network_contract.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(data.get("schema") == "dealix.leap-founder-network.v1", "schema")
    require(data.get("north_star") == "FIRST_VERIFIED_PAID_PILOT", "north star")
    require(data.get("default_new_record_state") == "RESEARCH_ONLY", "new records must be research-only")

    event = data.get("event", {})
    require(
        event.get("dates") == ["2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03"],
        "LEAP dates",
    )
    metrics = event.get("official_surface_metrics", {})
    require(metrics.get("rocket_fuel_pitches") == 100, "Rocket Fuel 100 cohort")
    require(metrics.get("rocket_fuel_prize_usd") == 1_000_000, "Rocket Fuel prize")

    lanes = {item["id"]: item for item in data.get("lanes", [])}
    require("F0_INBOUND" in lanes, "inbound-first lane")
    require("F1_ROCKET_FUEL_100" in lanes, "Rocket Fuel lane")
    require(lanes["F0_INBOUND"]["priority"] > lanes["F1_ROCKET_FUEL_100"]["priority"], "inbound outranks research")

    policy = data.get("channel_policy", {})
    require(policy.get("linkedin_personal", {}).get("mode") == "MANUAL_NATIVE", "LinkedIn personal must be manual-native")
    linkedin_blocked = set(policy.get("linkedin_personal", {}).get("blocked", []))
    require({"scraping", "auto_connect", "auto_message"}.issubset(linkedin_blocked), "LinkedIn automation block")

    whatsapp = policy.get("whatsapp", {})
    require(whatsapp.get("mode") == "CONSENT_OR_REAL_RELATIONSHIP_ONLY", "WhatsApp relationship/consent gate")
    require({"cold", "bulk"}.issubset(set(whatsapp.get("blocked", []))), "cold/bulk WhatsApp block")

    email = policy.get("email", {})
    require(email.get("public_endpoint_alone_is_permission") is False, "public email cannot equal permission")

    rules = set(data.get("hard_truth_rules", []))
    required_rules = {
        "directory_listing != lead",
        "LEAP_profile != verified_relationship",
        "research_score != relationship_state",
        "proposal != revenue",
        "payment_evidence_required_for_revenue",
    }
    require(required_rules.issubset(rules), "truth firewall rules")

    score = data.get("founder_attention_score", {})
    require(sum(score.values()) == 100, "founder attention score must total 100")

    capacity = data.get("daily_capacity", {})
    require(capacity.get("top_targets") == 20, "daily target cap")
    require(
        capacity.get("must_meet", 0)
        + capacity.get("partner_candidates", 0)
        + capacity.get("customer_fit_candidates", 0)
        + capacity.get("ecosystem_referral_candidates", 0)
        == capacity.get("top_targets"),
        "daily cohort allocation",
    )

    outcomes = set(data.get("outcomes", []))
    require("VERIFIED_RELATIONSHIP" in outcomes and "PAID_PILOT" in outcomes, "economic outcomes")

    blocked = set(data.get("blocked_outcomes", []))
    require("DIRECTORY_COUNT_AS_PIPELINE" in blocked, "directory-count vanity blocked")
    require("MASS_CONNECTION_COUNT_AS_SUCCESS" in blocked, "connection-count vanity blocked")

    print("DEALIX_LEAP_FOUNDER_NETWORK=PASS")
    print(f"LANES={len(lanes)}")
    print(f"FOUNDER_SCORE_TOTAL={sum(score.values())}")
    print(f"OFFICIAL_SOURCES={len(event.get('official_sources', []))}")
    print(f"ROCKET_FUEL_PITCHES={metrics.get('rocket_fuel_pitches')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
