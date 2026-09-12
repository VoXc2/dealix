from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config/company/fresh_market_execution_policy.json"


def _policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def test_fresh_market_policy_uses_agentic_holding_not_fixed_five() -> None:
    policy = _policy()
    architecture = policy["architecture"]
    execution = policy["execution"]

    assert policy["schema"] == "dealix.fresh_market_execution_policy.v2"
    assert architecture["model"] == "agentic_holding_sector_company_mesh"
    assert architecture["status"] == "CANONICAL"
    assert architecture["canonical_source"] == "docs/architecture/DEALIX_AGENTIC_HOLDING_CANONICAL_2026_09_12.md"
    assert architecture["canonical_contract"] == "config/company/agentic_holding_canonical_contract.json"
    assert architecture["single_company_machine"] is True
    assert architecture["legacy_fixed_five_permanent_agents"] == "deprecated"
    assert architecture["logical_agents"] == "dynamic_hierarchical_registry"
    assert architecture["runtime_workers"] == "lazy_resource_governed"
    assert architecture["orphan_agents_allowed"] is False
    assert architecture["process_per_logical_agent_forbidden"] is True
    assert execution["resource_aware_concurrency_governor"] is True
    assert execution["legacy_global_deep_wip_max_3"] == "deprecated"
    assert "agents" not in policy
    assert "deep_wip_max" not in execution


def test_fresh_market_policy_is_free_diagnostic_and_quote_only() -> None:
    truth = _policy()["commercial_truth"]

    assert truth["public_fixed_prices"] is False
    assert truth["free_diagnostic"] is True
    assert truth["diagnostic_payment_required"] is False
    assert truth["quote_policy"] == "customer_specific_after_qualified_discovery"
    assert truth["invented_roi_forbidden"] is True
    assert truth["invented_revenue_forbidden"] is True
    assert truth["research_is_relationship"] is False
    assert truth["public_contact_is_consent"] is False
    assert truth["quote_is_invoice"] is False
    assert truth["invoice_is_payment"] is False
    assert truth["payment_is_revenue"] is False
    assert truth["delivery_is_customer_value"] is False
    assert truth["customer_value_is_public_proof"] is False


def test_fresh_market_policy_routes_work_by_cost_risk_and_acceptance() -> None:
    policy = _policy()
    execution = policy["execution"]
    governor = set(policy["resource_governor_inputs"])

    assert execution["orchestrator"] == "Hermes"
    assert execution["executor"] == "scripts/ops/session_factory.py"
    assert execution["paid_spill_default"] is False
    assert execution["acceptance_receipt_required"] is True
    assert execution["verifier_required_for_material_outputs"] is True
    assert execution["routing_law"] == "cheapest_adequate_model_then_acceptance_gated_escalation"
    assert execution["coordination_default"] == "manager_for_bounded_specialists_handoff_for_ownership_transfer"
    assert execution["handoff_contract_required"] is True
    assert execution["filtered_handoff_context"] is True
    assert execution["trace_handoffs_tools_guardrails"] is True
    assert execution["blocking_guardrails_before_material_side_effects"] is True
    assert {"cpu_load", "available_ram", "provider_quota", "expected_economic_value", "task_risk", "worktree_availability"} <= governor


def test_connector_security_is_fail_closed() -> None:
    security = _policy()["connector_security"]

    assert security["protected_remote_tools_require_authorization"] is True
    assert security["issuer_validation_required"] is True
    assert security["issuer_bound_credentials"] is True
    assert security["resource_bound_tokens"] is True
    assert security["token_passthrough_forbidden"] is True
    assert security["agent_identity_and_delegated_scope_explicit"] is True
    assert security["credentials_in_prompt_context_forbidden"] is True
    assert security["remote_metadata_ssrf_protection_required"] is True


def test_observability_covers_agentic_boundaries() -> None:
    observability = _policy()["observability"]
    events = set(observability["trace_events"])

    assert observability["end_to_end_trace_required"] is True
    assert {"model_call", "tool_call", "handoff", "guardrail", "approval_check", "acceptance_check", "receipt"} <= events
    assert observability["facts_inferences_unknowns_separated"] is True
    assert observability["market_claim_provenance_required"] is True


def test_material_external_actions_remain_exact_action_bound() -> None:
    authority = _policy()["authority"]

    assert authority["material_external_actions"] == "exact_action_bound_authority"
    assert authority["delegated_authority_must_be_explicit"] is True
    assert authority["implicit_authority_transfer_forbidden"] is True
    assert authority["self_approval_forbidden"] is True
