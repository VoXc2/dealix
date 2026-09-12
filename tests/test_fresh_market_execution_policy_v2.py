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
    assert architecture["single_company_machine"] is True
    assert architecture["legacy_fixed_five_permanent_agents"] == "deprecated"
    assert architecture["logical_agents"] == "dynamic_hierarchical_registry"
    assert architecture["runtime_workers"] == "lazy_resource_governed"
    assert architecture["orphan_agents_allowed"] is False
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
    assert execution["routing_law"] == "cheapest_adequate_model_then_acceptance_gated_escalation"
    assert {"cpu_load", "available_ram", "provider_quota", "expected_economic_value", "task_risk", "worktree_availability"} <= governor


def test_material_external_actions_remain_exact_action_bound() -> None:
    authority = _policy()["authority"]

    assert authority["material_external_actions"] == "exact_action_bound_authority"
    assert authority["self_approval_forbidden"] is True
