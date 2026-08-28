#!/usr/bin/env python3
"""Deterministically verify the Dealix Marketing & Distribution OS contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "commercial" / "marketing_distribution_contract.json"
EXPERIMENTS = ROOT / "data" / "commercial" / "marketing_experiment_portfolio.json"
DOC = ROOT / "docs" / "commercial" / "MARKETING_DISTRIBUTION_OS.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"MARKETING_DISTRIBUTION_VERIFY=FAIL reason={message}")


def load_json(path: Path) -> dict:
    require(path.is_file(), f"missing:{path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"not_object:{path.relative_to(ROOT)}")
    return value


def main() -> None:
    contract = load_json(CONTRACT)
    portfolio = load_json(EXPERIMENTS)
    require(DOC.is_file(), "missing:docs/commercial/MARKETING_DISTRIBUTION_OS.md")

    require(contract.get("schema") == "dealix.marketing-distribution.v1", "schema")
    require(contract.get("north_star") == "FIRST_VERIFIED_PAID_DEALIX_PILOT", "north_star")
    require(contract.get("scheduler_policy") == "REUSE_EXISTING_CANONICAL_OWNERS_ONLY", "scheduler_policy")

    channels = contract.get("channels", {})
    require(channels.get("linkedin", {}).get("mode") == "MANUAL_NATIVE", "linkedin_mode")
    require(channels.get("linkedin", {}).get("scraping") is False, "linkedin_scraping")
    require(channels.get("linkedin", {}).get("automated_messages") is False, "linkedin_automation")
    require(channels.get("whatsapp", {}).get("cold_bulk") is False, "whatsapp_cold_bulk")
    require(channels.get("whatsapp", {}).get("opt_out_suppression") is True, "whatsapp_suppression")
    require(channels.get("email", {}).get("endpoint_alone_is_permission") is False, "email_permission")
    require(channels.get("events", {}).get("directory_record_is_relationship") is False, "event_truth")

    invariants = set(contract.get("truth_invariants", []))
    required_invariants = {
        "RESEARCH_NE_RELATIONSHIP",
        "PROVIDER_ACCEPTED_NE_DELIVERED",
        "PROPOSAL_NE_REVENUE",
        "INVOICE_NE_PAYMENT",
        "SYNTHETIC_NE_CUSTOMER_PROOF",
        "NO_LEGACY_PUBLIC_PRICING_OR_GUARANTEES",
    }
    require(required_invariants <= invariants, "truth_invariants")

    paid = contract.get("paid_media", {})
    require(paid.get("spend_authorized") is False, "paid_media_spend")
    require(paid.get("requires_separate_budget_approval") is True, "paid_media_approval")

    forbidden = set(contract.get("forbidden_new_parallel_systems", []))
    require({"CRM", "OPPORTUNITY_GRAPH", "APPROVAL_CENTER", "PROOF_LEDGER", "REVENUE_ENGINE", "SCHEDULER"} <= forbidden, "parallel_system_guard")

    experiments = portfolio.get("experiments")
    require(isinstance(experiments, list) and len(experiments) >= 7, "experiment_count")
    ids = [item.get("id") for item in experiments if isinstance(item, dict)]
    require(len(ids) == len(set(ids)), "duplicate_experiment_id")
    for item in experiments:
        require(isinstance(item, dict), "experiment_shape")
        for key in ("id", "hypothesis", "audience", "channel", "offer", "success_event", "stop_rule", "authority"):
            require(bool(item.get(key)), f"experiment_missing:{item.get('id')}:{key}")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "FIRST VERIFIED PAID DEALIX PILOT",
        "research is not a relationship",
        "No automated LinkedIn messaging",
        "Actual spend is a separate founder decision",
        "Big 5 Construct Saudi",
        "LEAP + DeepFest",
    ):
        require(phrase in doc, f"doc_guard:{phrase}")

    print("DEALIX_MARKETING_DISTRIBUTION_OS=PASS")
    print(f"EXPERIMENTS={len(experiments)}")
    print(f"ATTRIBUTION_EVENTS={len(contract.get('attribution_events', []))}")
    print(f"TOPIC_CLUSTERS={len(contract.get('seo_ai_search', {}).get('topic_clusters', []))}")


if __name__ == "__main__":
    main()
