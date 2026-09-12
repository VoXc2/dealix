from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config/company/agentic_holding_canonical_contract.json"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_contract_is_canonical_and_one_company() -> None:
    contract = _contract()
    law = contract["one_company_law"]

    assert contract["schema"] == "dealix.agentic_holding_canonical_contract.v1"
    assert contract["status"] == "CANONICAL"
    assert contract["architecture"] == "agentic_holding_sector_company_mesh"
    assert law["single_company_machine"] is True
    assert law["single_company_brain"] is True
    assert law["single_economic_truth"] is True
    assert law["single_approval_path"] is True
    assert law["single_proof_path"] is True
    assert law["single_scheduler"] is True
    assert law["single_model_routing_policy"] is True
    assert law["parallel_sector_businesses_forbidden"] is True


def test_dynamic_hierarchy_has_no_orphan_or_process_per_agent_design() -> None:
    model = _contract()["agent_model"]

    assert model["logical_agents"] == "dynamic_hierarchical_registry"
    assert model["runtime_workers"] == "lazy_resource_governed"
    assert model["process_per_logical_agent_forbidden"] is True
    assert model["orphan_agents_allowed"] is False
    assert {"agent_id", "parent_id", "authority_scope", "capabilities", "lifecycle_state"} <= set(model["required_identity_fields"])
    assert {"holding", "group", "sector_company", "arm_pod", "bounded_specialist"} == set(model["layers"])


def test_handoffs_are_scoped_filtered_and_do_not_transfer_authority_implicitly() -> None:
    coordination = _contract()["coordination"]
    required = set(coordination["handoff_packet_required"])

    assert coordination["default_pattern"] == "manager_for_bounded_specialists_handoff_for_ownership_transfer"
    assert coordination["manager_pattern"]["manager_retains_final_ownership"] is True
    assert coordination["handoff_pattern"]["authorization_before_side_effects"] is True
    assert coordination["handoff_pattern"]["receiving_agent_context_is_filtered"] is True
    assert {"trace_id", "source_agent", "target_agent", "scope", "facts", "inferences", "evidence_refs", "authority_scope", "context_filter", "acceptance_criteria"} <= required
    assert coordination["implicit_authority_transfer_forbidden"] is True
    assert coordination["implicit_relationship_transfer_forbidden"] is True
    assert coordination["implicit_consent_transfer_forbidden"] is True


def test_tool_guardrails_block_material_side_effects_before_execution() -> None:
    guardrails = _contract()["guardrails"]

    assert guardrails["blocking_before_side_effects"] is True
    assert guardrails["pre_execution_fail_closed"] is True
    assert guardrails["self_approval_forbidden"] is True
    assert guardrails["model_output_is_authority"] is False
    assert {"external_send", "public_publish", "payment_or_spend", "production_mutation", "dns_db_secret_mutation"} <= set(guardrails["tool_input_guardrails_required_for"])
    assert {"read_only", "reversible_internal", "material_external", "destructive"} == set(guardrails["side_effect_classes"])


def test_tracing_covers_handoffs_tools_guardrails_and_acceptance() -> None:
    tracing = _contract()["tracing_and_receipts"]
    events = set(tracing["trace_events"])
    correlation = set(tracing["required_correlation_fields"])

    assert tracing["end_to_end_trace_required"] is True
    assert {"model_call", "tool_call", "handoff", "guardrail", "approval_check", "acceptance_check", "receipt", "rollback"} <= events
    assert {"trace_id", "work_id", "agent_id", "parent_agent_id", "authority_level", "model_route", "cost_class", "evidence_refs"} <= correlation
    assert tracing["acceptance_receipt_required"] is True
    assert tracing["historical_pass_is_current_pass"] is False


def test_context_is_least_privilege_and_provenance_aware() -> None:
    context = _contract()["context_and_memory"]

    assert context["least_context_handoff"] is True
    assert context["filtered_history_preferred"] is True
    assert context["secret_propagation_forbidden"] is True
    assert context["customer_data_cross_sector_leakage_forbidden"] is True
    assert context["facts_inferences_and_unknowns_separated"] is True
    assert context["provenance_required_for_market_claims"] is True


def test_mcp_connector_security_is_identity_and_resource_bound() -> None:
    security = _contract()["mcp_and_connector_security"]

    assert security["oauth_or_equivalent_for_protected_remote_tools"] is True
    assert security["issuer_validation_required"] is True
    assert security["credentials_issuer_bound"] is True
    assert security["resource_bound_tokens_required"] is True
    assert security["token_passthrough_forbidden"] is True
    assert security["agent_identity_and_delegated_scope_must_be_explicit"] is True
    assert security["credentials_never_enter_prompt_context"] is True
    assert security["ssrf_protection_for_remote_metadata_fetch"] is True
    assert {"https_only", "internal_network_block", "timeout", "size_limit", "strict_schema_validation"} == set(security["remote_metadata_fetch_limits"])


def test_verifier_is_independent_and_truth_firewall_is_preserved() -> None:
    contract = _contract()
    evaluation = contract["evaluation"]
    firewall = set(contract["truth_firewall"])

    assert evaluation["verifier_role_required_for_material_outputs"] is True
    assert evaluation["verifier_must_not_self_approve_originating_work"] is True
    assert evaluation["acceptance_criteria_before_execution"] is True
    assert evaluation["synthetic_proof_is_customer_proof"] is False
    assert evaluation["delivery_is_customer_value"] is False
    assert evaluation["merged_pr_is_deployed_release"] is False
    assert {"research != relationship", "public_contact != consent", "draft != sent", "quote != invoice", "invoice != payment", "model_output != authority"} <= firewall


def test_resource_cost_and_lifecycle_remain_governed() -> None:
    contract = _contract()
    resource = contract["resource_and_cost"]
    lifecycle = contract["lifecycle"]

    assert resource["deterministic_first"] is True
    assert resource["cheapest_adequate_model"] is True
    assert resource["acceptance_gated_escalation"] is True
    assert resource["paid_spill_default"] is False
    assert resource["resource_aware_concurrency"] is True
    assert resource["parallel_repo_writers_require_isolated_worktrees"] is True
    assert resource["logical_agent_count_is_runtime_worker_count"] is False
    assert lifecycle["self_grant_external_authority_forbidden"] is True
    assert {"PROMOTE", "KEEP", "SPECIALIZE", "IMPROVE", "DEMOTE", "SUSPEND", "KILL"} == set(lifecycle["allowed_decisions"])
    assert {"versioned_change", "tests", "reviewability", "rollback", "receipt"} == set(lifecycle["self_improvement_requires"])


def test_research_basis_is_explicit_not_silent() -> None:
    basis = _contract()["research_basis"]
    urls = {row["url"] for row in basis}

    assert "https://openai.github.io/openai-agents-python/" in urls
    assert "https://openai.github.io/openai-agents-python/multi_agent/" in urls
    assert "https://openai.github.io/openai-agents-python/guardrails/" in urls
    assert "https://openai.github.io/openai-agents-python/tracing/" in urls
    assert "https://blog.modelcontextprotocol.io/posts/2026-07-28/" in urls
    assert "https://blog.modelcontextprotocol.io/posts/mcp-roadmap/" in urls
