#!/usr/bin/env python3
"""Side-effect-free verifier for Dealix Growth Council + company delegation + Morning Command.

This verifier validates only the unique council/delegation/command layer.
Brand/public-surface, HubSpot mirror, Revenue Mesh, production, security and
other domain-specific checks remain owned by their existing canonical verifiers.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKLOADS = ROOT / "data/commercial/agent_council_growth_workloads.json"
MORNING = ROOT / "data/commercial/morning_revenue_command_contract.json"
DELEGATION = ROOT / "data/ops/agent_council_company_delegation.json"
DELEGATION_DOC = ROOT / "docs/ops/AGENT_COUNCIL_COMPANY_DELEGATION.md"
GENERATOR = ROOT / "scripts/generate_morning_revenue_command.py"
RUNNER = ROOT / "scripts/run_dealix_daily_ops.py"


def fail(message: str) -> None:
    print(f"DEALIX_GROWTH_COUNCIL_MORNING_COMMAND=FAIL reason={message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing:{path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid_json:{path.relative_to(ROOT)}:{exc}")
    require(isinstance(value, dict), f"not_object:{path.relative_to(ROOT)}")
    return value


def main() -> int:
    workloads = load(WORKLOADS)
    morning = load(MORNING)
    delegation = load(DELEGATION)
    require(DELEGATION_DOC.is_file(), "company_delegation_runbook_missing")
    require(GENERATOR.is_file(), "morning_generator_missing")
    require(RUNNER.is_file(), "daily_runner_missing")

    # Growth Council overlay contract.
    require(workloads.get("schema") == "dealix.agent-council-growth-workloads.v1", "workload_schema_drift")
    require(workloads.get("north_star") == "FIRST_VERIFIED_PAID_PILOT", "north_star_drift")

    shared = workloads.get("shared_state", {})
    for key in ("company_brain", "opportunity_graph", "proof_ledger", "approval_center"):
        require(shared.get(key) == "single", f"parallel_truth_system:{key}")
    require(shared.get("scheduler") == "existing_canonical_owner_only", "scheduler_owner_drift")

    expected_roles = {
        "president",
        "market_intelligence",
        "revenue",
        "content_strategist",
        "creative_director",
        "distribution_manager",
        "lifecycle_agent",
        "experiment_analyst",
        "proof_agent",
        "governance_agent",
    }
    roles = workloads.get("roles", {})
    require(set(roles) == expected_roles, "growth_role_set_drift")
    for role, row in roles.items():
        require(bool(row.get("maps_to")), f"role_mapping_missing:{role}")
        require(bool(row.get("mission")), f"role_mission_missing:{role}")

    cadence = workloads.get("workload_cadence", {})
    require(cadence.get("new_timer_created") is False, "duplicate_timer_created")
    require(cadence.get("new_permanent_agent_created") is False, "permanent_agent_created")

    truth = workloads.get("economic_truth", {})
    for key in (
        "research_is_relationship",
        "crm_contact_is_relationship",
        "provider_acceptance_is_delivery",
        "proposal_is_revenue",
        "invoice_is_payment",
        "analytics_event_is_payment",
    ):
        require(truth.get(key) is False, f"truth_firewall_drift:{key}")
    require(truth.get("verified_revenue_requires_payment_evidence") is True, "payment_evidence_gate_missing")
    require(truth.get("customer_proof_requires_customer_evidence_and_permission") is True, "customer_proof_gate_missing")

    gates = set(workloads.get("automation_policy", {}).get("specific_gate_required", []))
    for gate in (
        "named_price_or_quote",
        "contract_or_legal_commitment",
        "tender_submission",
        "payment_charge_refund_or_spend",
        "dns_production_or_destructive_database_mutation",
        "customer_proof_or_testimonial_publication_without_recorded_permission",
        "any_action_without_required_recipient_or_platform_consent",
    ):
        require(gate in gates, f"material_gate_missing:{gate}")

    # Company-wide delegation constitution.
    require(delegation.get("schema") == "dealix.agent-council-company-delegation.v1", "delegation_schema_drift")
    require(delegation.get("north_star") == "FIRST_VERIFIED_PAID_PILOT", "delegation_north_star_drift")
    require(delegation.get("operating_mode") == "REVENUE_FIRST", "delegation_operating_mode_drift")

    law = delegation.get("delegation_law", {})
    for key in (
        "deterministic_before_llm",
        "one_accountable_owner_per_outcome",
        "one_shared_company_brain",
        "one_shared_opportunity_graph",
        "one_shared_approval_center",
        "one_shared_proof_ledger",
        "one_canonical_scheduler_owner",
        "verified_revenue_requires_payment_evidence",
        "customer_proof_requires_evidence_and_permission",
    ):
        require(law.get(key) is True, f"delegation_law_missing:{key}")
    for key in (
        "research_is_relationship",
        "proposal_is_revenue",
        "invoice_is_payment",
        "provider_acceptance_is_delivery",
        "synthetic_is_customer_proof",
    ):
        require(law.get(key) is False, f"delegation_truth_drift:{key}")
    require(law.get("new_permanent_agents") == 0, "delegation_added_permanent_agents")
    require(law.get("new_timers_or_cron") == 0, "delegation_added_scheduler")

    expected_runtime_agents = {
        "company_brain",
        "sprint_orchestrator",
        "governance",
        "market_intel",
        "lead_intelligence",
        "revenue_intelligence",
        "sales_intelligence",
        "customer_acquisition",
        "diagnostic_agent",
        "data_architect",
        "managed_ops",
    }
    require(set(delegation.get("existing_runtime_agents", [])) == expected_runtime_agents, "runtime_agent_reuse_drift")

    expected_specialists = {
        "founder-president",
        "sovereign-security",
        "engineering-verifier",
        "production-sre",
        "revenue-copilot",
        "market-partner-scout",
        "sales-negotiation",
        "delivery-success",
        "proof-data",
        "governance-finance",
        "capability-research",
        "self-improvement",
    }
    require(set(delegation.get("existing_specialist_profiles", [])) == expected_specialists, "specialist_profile_reuse_drift")
    require(set(delegation.get("growth_workload_overlays", [])) == expected_roles, "delegation_growth_overlay_drift")

    expected_domains = {
        "executive_portfolio_command",
        "production_trust_security",
        "product_engineering_capability",
        "market_competitor_partner_intelligence",
        "revenue_sales_negotiation",
        "brand_content_distribution",
        "lifecycle_inbound_relationships",
        "customer_delivery_success",
        "data_proof_analytics_experiments",
        "governance_finance_compliance",
        "partner_market_access_ecosystem",
        "self_improvement_cost_friction",
    }
    domains = delegation.get("delegated_domains", {})
    require(set(domains) == expected_domains, "delegated_domain_set_drift")
    for domain, row in domains.items():
        require(bool(row.get("accountable")), f"delegated_owner_missing:{domain}")
        require(bool(row.get("mission")), f"delegated_mission_missing:{domain}")
        require(bool(row.get("automatic")), f"delegated_automatic_scope_missing:{domain}")

    delegation_l5 = set(delegation.get("autonomy", {}).get("specific_l5", []))
    for required in (
        "merge_to_main",
        "production_deploy_or_mutation",
        "dns_mutation",
        "destructive_or_material_production_database_mutation",
        "sensitive_secret_write_or_rotation",
        "payment_charge_refund_or_paid_spend",
        "contract_or_legal_commitment",
        "tender_submission",
        "destructive_deletion",
    ):
        require(required in delegation_l5, f"delegation_l5_gate_missing:{required}")

    handoff = delegation.get("handoff_contract", {})
    required_handoff_fields = {
        "work_id",
        "timestamp",
        "source_owner",
        "target_owner",
        "objective",
        "truth_class",
        "evidence_refs",
        "current_state",
        "required_output",
        "autonomy_level",
        "approval_class",
        "deadline_or_staleness",
        "stop_condition",
    }
    require(set(handoff.get("required_fields", [])) == required_handoff_fields, "handoff_contract_drift")
    require(bool(handoff.get("forbidden_handoff")), "handoff_fail_closed_rules_missing")

    queue = delegation.get("queue_policy", {})
    require(queue.get("global_primary_wip") == 1, "global_wip_drift")
    require(bool(queue.get("default_priority_order")), "priority_order_missing")
    require(bool(queue.get("stale_work_rule")), "stale_work_stop_rule_missing")

    override = delegation.get("timeboxed_portfolio_override", {})
    capacity = override.get("capacity_percent", {})
    require(sum(v for v in capacity.values() if isinstance(v, int)) == 100, "event_capacity_not_100")
    require(str(override.get("active_until", "")).startswith("2026-09-03"), "event_window_drift")
    require(bool(override.get("event_rule")), "event_rule_missing")

    delegated_cadence = delegation.get("cadence", {})
    require(delegated_cadence.get("new_scheduler_created") is False, "delegation_duplicate_scheduler")
    require(delegated_cadence.get("new_agent_created") is False, "delegation_duplicate_agent")

    founder_contract = delegation.get("founder_command_contract", {})
    require(bool(founder_contract.get("default_output")), "founder_command_output_missing")
    vanity = set(founder_contract.get("never_report_vanity_as_success", []))
    for metric in ("token_count", "lead_universe_size", "draft_count", "provider_accepted_count"):
        require(metric in vanity, f"vanity_guard_missing:{metric}")

    # Morning Revenue Command contract.
    require(morning.get("schema") == "dealix.morning-revenue-command.v1", "morning_schema_drift")
    require(morning.get("north_star") == "FIRST_VERIFIED_PAID_PILOT", "morning_north_star_drift")
    expected_sections = [
        "money", "pipeline", "marketing", "content", "market", "experiments", "agents", "approvals", "next_best_action"
    ]
    actual_sections = [row.get("id") for row in morning.get("sections", []) if isinstance(row, dict)]
    require(actual_sections == expected_sections, "morning_section_order_drift")
    automation = morning.get("automation", {})
    require(automation.get("new_timer_created") is False, "morning_duplicate_timer")
    require(automation.get("new_permanent_agent_created") is False, "morning_permanent_agent")

    generator = GENERATOR.read_text(encoding="utf-8")
    require("UNKNOWN_NOT_EVIDENCE_BACKED" in generator, "unknown_truth_semantics_missing")
    require("DEALIX_COMPANY_OS_CURRENT" in generator, "company_os_current_input_missing")
    require("atomic_write" in generator, "atomic_output_missing")

    # Labels such as HubSpot/PostHog are allowed in the founder brief. What is forbidden
    # here is direct external execution from the generator itself. The Morning Command
    # must consume Company OS evidence, never reach out to SaaS providers or use their
    # credentials directly.
    forbidden_external_execution = (
        "requests.post",
        "requests.put",
        "requests.patch",
        "requests.delete",
        "urlopen(",
        "httpx.post",
        "httpx.put",
        "httpx.patch",
        "httpx.delete",
        "HUBSPOT_ACCESS_TOKEN",
        "HUBSPOT_API_KEY",
        "POSTHOG_API_KEY",
        "CLAY_API_KEY",
        "CANVA_ACCESS_TOKEN",
    )
    for forbidden in forbidden_external_execution:
        require(forbidden not in generator, f"unexpected_external_dependency:{forbidden}")

    runner = RUNNER.read_text(encoding="utf-8")
    require("step_growth_council_verify" in runner, "daily_runner_growth_verify_missing")
    require("step_morning_revenue_command" in runner, "daily_runner_morning_command_missing")

    print("DEALIX_GROWTH_COUNCIL_MORNING_COMMAND=PASS")
    print("COMPANY_WIDE_DELEGATION=PASS")
    print("DELEGATED_DOMAINS=12")
    print("RUNTIME_AGENTS_REUSED=11")
    print("SPECIALIST_PROFILES_REUSED=12")
    print("GROWTH_WORKLOADS=10")
    print("PERMANENT_AGENT_COUNT_DELTA=0")
    print("SCHEDULER_COUNT_DELTA=0")
    print("ECONOMIC_TRUTH=EVIDENCE_FIRST")
    print("MORNING_COMMAND=EXISTING_DAILY_RUNNER")
    print("NORTH_STAR=FIRST_VERIFIED_PAID_PILOT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
