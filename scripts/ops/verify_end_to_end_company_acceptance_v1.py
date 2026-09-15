#!/usr/bin/env python3
"""Verify the Dealix end-to-end company acceptance composition contract."""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "data/ops/end_to_end_company_acceptance_v1.json"

EXPECTED_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
# Historical five names are legacy compatibility aliases only. Canonical
# logical-agent authority is the Agentic Holding current registry; runtime
# capacity belongs to ResourceGovernor + Session Factory.
LEGACY_EXECUTOR_ALIASES = set(EXPECTED_AGENTS)
LEGACY_ALIAS_SEMANTICS = "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_ARCHITECTURE_AUTHORITY"
LOGICAL_AGENT_AUTHORITY = "dealix.agentic_holding.runtime.build_current_registry"
RUNTIME_CAPACITY_AUTHORITY = "ResourceGovernor+Session Factory"
EXPECTED_SYSTEMS = {
    "command_os",
    "revenue_os",
    "proof_os",
    "client_os",
    "delivery_os",
    "support_os",
    "finance_os",
    "data_os",
    "governance_os",
    "academy_os",
    "partner_os",
    "venture_os",
}
EXPECTED_STAGES = [
    "MARKET_SIGNAL",
    "ACCOUNT_RESEARCH",
    "ELIGIBILITY_IDENTITY_AND_CONSENT",
    "CONTENT_AND_DEMAND",
    "REAL_INTERACTION",
    "QUALIFIED_PROBLEM",
    "FREE_MINI_DIAGNOSTIC",
    "QUALIFIED_DISCOVERY",
    "CUSTOMER_SPECIFIC_QUOTE",
    "NEGOTIATION_AND_DECISION",
    "PAYMENT_VERIFICATION",
    "ONBOARDING",
    "DELIVERY_PLANNING",
    "DELIVERY_EXECUTION",
    "SUPPORT_AND_CUSTOMER_SUCCESS",
    "PROOF_ACCEPTANCE_AND_HANDOVER",
    "RENEWAL_EXPANSION_PARTNER_AND_REFERRAL",
    "LEARNING_AND_PRODUCTIZATION",
]
EXPECTED_COMMERCIAL_CHAIN = [
    "real_interaction",
    "verified_relationship",
    "qualified_problem",
    "free_mini_diagnostic",
    "qualified_discovery",
    "customer_specific_quote",
    "pilot_decision",
    "pilot_payment_verified",
    "pilot_delivery",
    "proof_review",
    "expansion_or_stop",
]
REQUIRED_FORBIDDEN_ACQUISITION = {
    "scraping",
    "cold_whatsapp",
    "mass_linkedin_automation",
    "identity_deception",
    "consent_inference_from_public_data",
}
REQUIRED_CONNECTORS = {
    "github",
    "vps",
    "railway",
    "n8n",
    "gmail",
    "whatsapp_business",
    "linkedin",
    "telegram_openclaw",
    "airtable_hubspot",
    "posthog_sentry_otel_langfuse",
    "canva_gamma_drive",
    "apollo_clay_ahrefs",
    "official_signal_sources",
}
REQUIRED_ACCEPTANCE_LEVELS = {
    "A0_SOURCE_CONSISTENCY",
    "A1_EXACT_HEAD_INTERNAL_MACHINE",
    "A2_CHANNEL_AND_FOUNDER_CONTROL",
    "A3_PRODUCTION_AND_PUBLIC_TRUTH",
    "A4_CONTROLLED_LIFECYCLE_CANARY",
    "A5_REAL_COMMERCIAL_PROOF",
    "A6_REPEATABILITY",
}
FORBIDDEN_ACTIVE_AI_WORKFORCE_MOTION = {
    "499 SAR Pilot invoice draft prepared",
    "مسوّدة فاتورة 499 ريال",
    'tier_id="growth_starter_pilot"',
    'return "growth_starter"',
    'recommended_service: str = "growth_starter"',
    "7-Day Revenue Command Room Sprint",
    "7-Day Operating Diagnostic",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _error(errors: list[str], condition: bool, code: str) -> None:
    if not condition:
        errors.append(code)


def verify() -> list[str]:
    errors: list[str] = []
    _error(errors, CONTRACT_PATH.is_file(), "missing_contract")
    if errors:
        return errors

    contract = _load(CONTRACT_PATH)
    _error(errors, contract.get("schema") == "dealix.end-to-end-company-acceptance.v1", "schema")
    _error(errors, contract.get("version") == "1.0.0", "version")
    _error(errors, contract.get("status") == "DRAFT_EXACT_HEAD_ACCEPTANCE_REQUIRED", "status")
    source_sha = str(contract.get("source_main_sha", ""))
    _error(errors, bool(re.fullmatch(r"[0-9a-f]{40}", source_sha)), "source_main_sha")

    agents = set(contract.get("canonical_agents") or [])
    systems = set(contract.get("canonical_systems") or [])
    _error(errors, agents == EXPECTED_AGENTS, "canonical_agents")
    _error(errors, contract.get("canonical_agents_field_semantics") == LEGACY_ALIAS_SEMANTICS, "canonical_agents_semantics")
    _error(errors, set(contract.get("legacy_executor_aliases") or []) == LEGACY_EXECUTOR_ALIASES, "legacy_executor_aliases")
    _error(errors, contract.get("logical_agent_authority") == LOGICAL_AGENT_AUTHORITY, "logical_agent_authority")
    _error(errors, contract.get("fixed_five_authority") is False, "fixed_five_authority")
    _error(errors, contract.get("runtime_capacity_authority") == RUNTIME_CAPACITY_AUTHORITY, "runtime_capacity_authority")
    _error(errors, contract.get("agent_owner_field_semantics") == LEGACY_ALIAS_SEMANTICS, "agent_owner_semantics")
    _error(errors, systems == EXPECTED_SYSTEMS, "canonical_systems")

    composition = contract.get("composition_only") or {}
    _error(errors, bool(composition), "composition_only_missing")
    for key, value in composition.items():
        _error(errors, value is False, f"parallel_or_new_owner_enabled:{key}")

    founder = contract.get("founder_attention_model") or {}
    _error(errors, founder.get("automatic_levels") == ["L0", "L1", "L2", "L3", "L4"], "automatic_levels")
    _error(errors, founder.get("external_level") == "L5_ACTION_BOUND", "external_level")
    _error(errors, founder.get("may_self_grant_external_authority") is False, "self_grant_external_authority")

    voice = contract.get("founder_voice_policy") or {}
    _error(errors, voice.get("drafting_from_approved_style_profile") is True, "voice_drafting")
    for key in (
        "may_claim_human_founder_identity",
        "may_fabricate_personal_experience",
        "may_fabricate_relationship_or_memory",
        "may_hide_material_automation",
    ):
        _error(errors, voice.get(key) is False, f"voice_policy:{key}")
    _error(
        errors,
        voice.get("external_identity") == "AUTHORIZED_DEALIX_AI_OR_TEAM_REPRESENTATIVE_DISCLOSURE_REQUIRED",
        "external_identity",
    )

    acquisition = contract.get("lead_acquisition_policy") or {}
    forbidden = set(acquisition.get("forbidden") or [])
    _error(errors, REQUIRED_FORBIDDEN_ACQUISITION <= forbidden, "lead_acquisition_forbidden_set")
    _error(errors, bool(acquisition.get("promotion_requirements")), "lead_promotion_requirements")

    connectors = contract.get("connector_control_plane") or []
    connector_ids = [row.get("id") for row in connectors]
    _error(errors, len(connector_ids) == len(set(connector_ids)), "duplicate_connector")
    _error(errors, REQUIRED_CONNECTORS <= set(connector_ids), "required_connectors")
    _error(errors, "slack_telegram" not in set(connector_ids), "legacy_founder_connector_reintroduced")
    for row in connectors:
        cid = row.get("id", "unknown")
        _error(errors, row.get("owner") in EXPECTED_AGENTS, f"connector_owner:{cid}")
        _error(errors, bool(row.get("role")), f"connector_role:{cid}")
        _error(errors, bool(row.get("write_ceiling")), f"connector_write_ceiling:{cid}")

    founder_connector = next((row for row in connectors if row.get("id") == "telegram_openclaw"), {})
    _error(errors, founder_connector.get("owner") == "dealix-pm", "founder_connector_owner")
    _error(
        errors,
        founder_connector.get("role") == "canonical_founder_command_approvals_and_receipts",
        "founder_connector_role",
    )
    _error(errors, founder_connector.get("truth_owner") is False, "founder_connector_truth_owner")
    _error(errors, founder_connector.get("write_ceiling") == "INTERNAL_ONLY", "founder_connector_write_ceiling")

    lifecycle = contract.get("client_lifecycle") or []
    stage_names = [row.get("stage") for row in lifecycle]
    orders = [row.get("order") for row in lifecycle]
    _error(errors, stage_names == EXPECTED_STAGES, "lifecycle_stage_order")
    _error(errors, orders == list(range(1, len(EXPECTED_STAGES) + 1)), "lifecycle_order")
    covered_systems: set[str] = set()
    covered_owners: set[str] = set()
    for row in lifecycle:
        stage = row.get("stage", "unknown")
        owner = row.get("owner")
        stage_systems = set(row.get("systems") or [])
        covered_owners.add(owner)
        covered_systems.update(stage_systems)
        _error(errors, owner in EXPECTED_AGENTS, f"lifecycle_owner:{stage}")
        _error(errors, stage_systems <= EXPECTED_SYSTEMS, f"lifecycle_system:{stage}")
        _error(errors, bool(row.get("required_evidence")), f"lifecycle_evidence:{stage}")
        _error(errors, bool(row.get("outputs")), f"lifecycle_outputs:{stage}")
        _error(errors, bool(row.get("automation_default")), f"lifecycle_automation:{stage}")
        _error(errors, bool(row.get("external_effect_class")), f"lifecycle_effect:{stage}")
    _error(errors, covered_systems == EXPECTED_SYSTEMS, "system_coverage")
    _error(errors, covered_owners == EXPECTED_AGENTS, "agent_owner_coverage")

    receipts = set(contract.get("universal_work_receipt_required") or [])
    for field in {
        "workload_id",
        "system_id",
        "agent_owner",
        "tenant_or_company_scope",
        "source_sha",
        "input_evidence_refs",
        "authority_class",
        "result",
        "output_evidence_refs",
        "idempotency_key",
        "rollback_or_safe_failure",
        "founder_minutes",
        "agent_minutes",
        "ai_cost",
        "tool_cost",
        "risk",
        "economic_delta",
        "learning_signal",
    }:
        _error(errors, field in receipts, f"receipt_field:{field}")

    acceptance = contract.get("acceptance_levels") or []
    acceptance_ids = [row.get("id") for row in acceptance]
    _error(errors, len(acceptance_ids) == len(set(acceptance_ids)), "duplicate_acceptance_level")
    _error(errors, set(acceptance_ids) == REQUIRED_ACCEPTANCE_LEVELS, "acceptance_levels")
    for row in acceptance:
        aid = row.get("id", "unknown")
        _error(errors, bool(row.get("result_required")), f"acceptance_result:{aid}")
        _error(errors, bool(row.get("evidence")), f"acceptance_evidence:{aid}")

    a2 = next((row for row in acceptance if row.get("id") == "A2_CHANNEL_AND_FOUNDER_CONTROL"), {})
    a2_evidence = set(a2.get("evidence") or [])
    _error(errors, "telegram_openclaw_e2e_receipt" in a2_evidence, "a2_telegram_openclaw_receipt")
    _error(errors, "slack_or_telegram_e2e_receipt" not in a2_evidence, "a2_legacy_slack_or_telegram_receipt")

    contract_paths = contract.get("canonical_contracts") or {}
    for name, rel in contract_paths.items():
        _error(errors, (ROOT / rel).is_file(), f"canonical_contract_missing:{name}:{rel}")

    machine = _load(ROOT / contract_paths["company_machine"])
    _error(errors, set(machine.get("agent_roster") or {}) == EXPECTED_AGENTS, "machine_agents")
    _error(errors, {row.get("id") for row in machine.get("systems") or []} == EXPECTED_SYSTEMS, "machine_systems")
    machine_effects = machine.get("external_effect_defaults") or {}
    _error(errors, all(value is False for value in machine_effects.values()), "machine_external_effect_defaults")

    continuous = _load(ROOT / contract_paths["continuous_operations"])
    _error(errors, set(continuous.get("canonical_workers") or []) == EXPECTED_AGENTS, "continuous_workers")
    _error(errors, continuous.get("canonical_workers_field_semantics") == LEGACY_ALIAS_SEMANTICS, "continuous_workers_semantics")
    _error(errors, set(continuous.get("legacy_executor_aliases") or []) == LEGACY_EXECUTOR_ALIASES, "continuous_legacy_aliases")
    _error(errors, continuous.get("logical_agent_authority") == LOGICAL_AGENT_AUTHORITY, "continuous_logical_authority")
    _error(errors, continuous.get("fixed_five_authority") is False, "continuous_fixed_five_authority")
    _error(errors, continuous.get("runtime_capacity_authority") == RUNTIME_CAPACITY_AUTHORITY, "continuous_runtime_capacity")
    _error(
        errors,
        (continuous.get("founder_interface") or {}).get("maximum_active_growth_bets_semantics")
        == "ECONOMIC_FOCUS_HEURISTIC_ONLY_NOT_RUNTIME_CAPACITY",
        "continuous_growth_bet_semantics",
    )
    runtime_ownership = continuous.get("runtime_ownership") or {}
    for key in (
        "new_scheduler_allowed",
        "new_timer_allowed",
        "new_permanent_agent_allowed",
        "new_company_os_allowed",
        "new_truth_store_allowed",
    ):
        _error(errors, runtime_ownership.get(key) is False, f"continuous_runtime:{key}")

    channel = _load(ROOT / contract_paths["channel_runtime"])
    service_model = channel.get("service_model") or {}
    _error(errors, set(service_model.get("canonical_agents") or []) == EXPECTED_AGENTS, "channel_agents")
    channel_effects = channel.get("global_external_effects_default") or {}
    _error(errors, all(value is False for value in channel_effects.values()), "channel_external_effect_defaults")
    _error(errors, (channel.get("slack_founder_bridge") or {}).get("arbitrary_shell") is False, "legacy_slack_arbitrary_shell_guard")

    sys.path.insert(0, str(ROOT))
    operating = importlib.import_module("auto_client_acquisition.orchestrator.operating_company_contract")
    _error(errors, list(operating.CANONICAL_COMMERCIAL_CHAIN) == EXPECTED_COMMERCIAL_CHAIN, "operating_commercial_chain")
    built = operating.build_operating_company_contract()
    summary = built.to_summary()
    _error(errors, summary.get("agents_total", 0) >= 5, "operating_specialist_roles_present")
    _error(errors, summary.get("loops_total", 0) >= 7, "operating_loops")

    delegation = importlib.import_module("auto_client_acquisition.ai_workforce.canonical_delegation")
    registry_module = importlib.import_module("auto_client_acquisition.ai_workforce.agent_registry")
    factory_module = importlib.import_module("auto_client_acquisition.ai_workforce.canonical_revenue_factory")
    runtime_mapping = dict(delegation.RUNTIME_SPECIALIST_DELEGATION)
    revenue_mapping = dict(delegation.REVENUE_SPECIALIST_DELEGATION)
    canonical_agents = set(delegation.CANONICAL_AGENTS)
    _error(errors, canonical_agents == EXPECTED_AGENTS, "ai_workforce_canonical_agents")
    # Delegated specialist roles are bounded workloads under legacy executor
    # aliases, never a second permanent fleet or runtime-capacity authority.
    _error(errors, getattr(delegation, "SPECIALIST_ROLE_SEMANTICS", "") == "BOUNDED_WORKLOAD_NOT_PERMANENT_AGENT", "specialist_role_semantics")
    _error(errors, set(registry_module.AGENT_REGISTRY) == set(runtime_mapping), "runtime_specialist_role_set")
    _error(errors, set(runtime_mapping.values()) <= EXPECTED_AGENTS, "runtime_specialist_owner_set")
    _error(errors, set(revenue_mapping.values()) <= EXPECTED_AGENTS, "revenue_specialist_owner_set")
    _error(
        errors,
        set(runtime_mapping.values()) | set(revenue_mapping.values()) == EXPECTED_AGENTS,
        "specialist_workloads_cover_five_agents",
    )

    blueprint = factory_module.build_canonical_revenue_factory_blueprint()
    _error(errors, blueprint.get("canonical_agents_total") == 5, "revenue_factory_canonical_agents_total")
    _error(errors, set(blueprint.get("canonical_agents") or []) == EXPECTED_AGENTS, "revenue_factory_canonical_agents")
    _error(errors, blueprint.get("specialist_roles_total") == 15, "revenue_factory_specialist_roles_total")
    _error(errors, len(blueprint.get("automation_plays") or []) == 30, "revenue_factory_automation_plays")
    _error(
        errors,
        {row.get("agent_id") for row in blueprint.get("agent_contracts") or []} == set(revenue_mapping),
        "revenue_factory_specialist_role_set",
    )
    _error(
        errors,
        all(row.get("canonical_owner") in EXPECTED_AGENTS for row in blueprint.get("agent_contracts") or []),
        "revenue_factory_contract_ownership",
    )
    _error(
        errors,
        all(row.get("canonical_owner") in EXPECTED_AGENTS for row in blueprint.get("daily_schedule") or []),
        "revenue_factory_schedule_ownership",
    )

    active_ai_sources = "\n".join(
        (ROOT / rel).read_text(encoding="utf-8")
        for rel in (
            "auto_client_acquisition/ai_workforce/agent_contracts.py",
            "auto_client_acquisition/ai_workforce/orchestrator.py",
            "auto_client_acquisition/ai_workforce/schemas.py",
        )
    )
    for retired in FORBIDDEN_ACTIVE_AI_WORKFORCE_MOTION:
        _error(errors, retired not in active_ai_sources, f"retired_ai_workforce_motion:{retired}")
    for required in (
        "free_mini_diagnostic",
        "revenue_command_pilot_30d",
        "customer_specific_quote",
        "verified_payment",
        "customer_validated_proof",
        "canonical_owner",
    ):
        _error(errors, required in active_ai_sources, f"missing_ai_workforce_truth:{required}")

    activation = contract.get("activation_state") or {}
    _error(
        errors,
        activation.get("external_customer_autonomy") == "PREPARED_NOT_GLOBALLY_ACTIVATED",
        "external_customer_autonomy_state",
    )
    _error(
        errors,
        activation.get("full_commercial_proof") == "BLOCKED_UNTIL_A5_REAL_COMMERCIAL_PROOF",
        "full_commercial_proof_state",
    )
    return errors


def main() -> int:
    errors = verify()
    if errors:
        print("DEALIX_END_TO_END_COMPANY_ACCEPTANCE_V1=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("DEALIX_END_TO_END_COMPANY_ACCEPTANCE_V1=PASS")
    print("legacy_executor_aliases=5")
    print("fixed_five_authority=FALSE")
    print("logical_agent_authority=AGENTIC_HOLDING_REGISTRY")
    print("runtime_capacity=RESOURCE_GOVERNOR_PLUS_SESSION_FACTORY")
    print("runtime_specialist_roles=12")
    print("revenue_factory_specialist_roles=15")
    print("automation_plays=30")
    print("systems=12")
    print("lifecycle_stages=18")
    print("internal_autonomy=L0-L4")
    print("external_authority=L5_ACTION_BOUND")
    print("founder_control=TELEGRAM_OPENCLAW")
    print("founder_voice=AUTHORIZED_REPRESENTATIVE_NO_IMPERSONATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
