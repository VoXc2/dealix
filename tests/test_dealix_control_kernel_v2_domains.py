from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "commercial" / "dealix_control_kernel_v2_domains.py"
KERNEL_PATH = ROOT / "config" / "company" / "dealix_control_kernel_v2.json"
SPEC = importlib.util.spec_from_file_location("dealix_control_kernel_v2_domains", MODULE_PATH)
assert SPEC and SPEC.loader
DOM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOM)
KERNEL = json.loads(KERNEL_PATH.read_text(encoding="utf-8"))


def test_workload_binding_requires_distinct_runtime_identity():
    binding = {
        "agent_id": "dealix-sales", "workload_id": "runtime-123", "environment": "test",
        "code_version": "sha", "policy_version": "2.0-control-kernel", "tool": "gmail-draft",
        "authority": "L2",
    }
    DOM.validate_workload_binding(binding)
    binding["workload_id"] = "dealix-sales"
    with pytest.raises(DOM.DomainContractError, match="AGENT_IDENTITY_MUST_DIFFER"):
        DOM.validate_workload_binding(binding)


def test_durable_task_requires_complete_contract_and_valid_state():
    task = {field: "x" for field in KERNEL["long_running_tasks"]["fields"]}
    task["state"] = "RUNNING"
    task["budget"] = {"TOOL_CALLS": 10}
    DOM.validate_durable_task(task)
    task["state"] = "IMMORTAL"
    with pytest.raises(DOM.DomainContractError, match="INVALID_TASK_STATE"):
        DOM.validate_durable_task(task)


def test_customer_memory_is_tenant_and_purpose_scoped():
    record = {
        "source": "first-party", "purpose": "delivery", "tenant": "customer-1",
        "sensitivity": "internal", "retention": "30d", "access_scope": "delivery-team",
        "last_validation": "2026-09-11",
    }
    DOM.validate_customer_memory(record)
    record["tenant"] = "GLOBAL"
    with pytest.raises(DOM.DomainContractError, match="GLOBAL_CUSTOMER_MEMORY_FORBIDDEN"):
        DOM.validate_customer_memory(record)


def test_relationship_promotion_requires_evidence():
    with pytest.raises(DOM.DomainContractError, match="RELATIONSHIP_PROMOTION_REQUIRES_EVIDENCE"):
        DOM.validate_relationship_change(from_state="PUBLIC_ONLY", to_state="PAST_INTERACTION", evidence=[])
    DOM.validate_relationship_change(
        from_state="PUBLIC_ONLY", to_state="PAST_INTERACTION", evidence=["message-receipt"]
    )


def test_model_change_requires_all_evidence_dimensions():
    evidence = {name: "pass" for name in KERNEL["model_change"]["evidence_dimensions"]}
    DOM.validate_model_change(from_state="DISCOVERED", to_state="EVALUATION", evidence=evidence)
    evidence.pop("ARABIC")
    with pytest.raises(DOM.DomainContractError, match="MODEL_CHANGE_EVIDENCE_MISSING:ARABIC"):
        DOM.validate_model_change(from_state="DISCOVERED", to_state="EVALUATION", evidence=evidence)


def test_canary_promotion_is_incremental_and_has_rollback():
    with pytest.raises(DOM.DomainContractError, match="CANARY_ROLLBACK_REQUIRED"):
        DOM.validate_canary_transition(from_state="SHADOW", to_state="CANARY", rollback_defined=False)
    with pytest.raises(DOM.DomainContractError, match="CANARY_PROMOTION_MUST_BE_INCREMENTAL"):
        DOM.validate_canary_transition(from_state="SHADOW", to_state="STANDARD", rollback_defined=True)
    DOM.validate_canary_transition(from_state="SHADOW", to_state="CANARY", rollback_defined=True)


def test_autonomy_degrades_on_known_failure_trigger():
    response = DOM.autonomy_degradation_response("NEW_FAILURE")
    assert response == ["REDUCE_AUTHORITY", "INCREASE_REVIEW", "RUN_EVALS", "RESTORE_ONLY_AFTER_PROOF"]


def test_external_a2a_requires_verified_card_and_policy():
    request = {str(name).lower(): "ok" for name in KERNEL["a2a_boundary"]["requirements"]}
    request["verified_agent_card"] = True
    request["policy_evaluation"] = "ALLOW"
    DOM.validate_external_a2a(request)
    request["verified_agent_card"] = False
    with pytest.raises(DOM.DomainContractError, match="EXTERNAL_AGENT_CARD_NOT_VERIFIED"):
        DOM.validate_external_a2a(request)


def test_regulatory_signal_requires_authoritative_source_and_fields():
    signal = {field: "x" for field in KERNEL["regulatory_radar"]["signal_fields"]}
    signal["classification"] = "WATCH"
    DOM.validate_regulatory_signal(signal, authoritative_source=True)
    with pytest.raises(DOM.DomainContractError, match="REGULATORY_SOURCE_NOT_AUTHORITATIVE"):
        DOM.validate_regulatory_signal(signal, authoritative_source=False)


def test_demand_radar_separates_hype_from_purchase_signal():
    assert DOM.classify_demand_evidence(["SOCIAL_BUZZ"]) == "MARKET_HYPE_OR_UNPROVEN_DEMAND"
    assert DOM.classify_demand_evidence(["BUDGET"]) == "PURCHASE_SIGNAL"


def test_company_twin_is_complete_and_not_second_brain():
    twin = {field: "x" for field in KERNEL["company_twin"]["fields"]}
    twin["source_system"] = "DERIVED_PROJECTION"
    DOM.validate_company_twin(twin)
    twin["source_system"] = "INDEPENDENT_COMPANY_BRAIN"
    with pytest.raises(DOM.DomainContractError, match="COMPANY_TWIN_CANNOT_BECOME_SECOND_BRAIN"):
        DOM.validate_company_twin(twin)


def test_proof_and_repeatability_dimensions_are_normalized():
    proof = {name: 0.5 for name in KERNEL["proof_compounding_index"]["dimensions"]}
    repeatability = {name: 0.5 for name in KERNEL["repeatability_index"]["dimensions"]}
    DOM.validate_proof_dimensions(proof)
    DOM.validate_repeatability_dimensions(repeatability)
    proof["CUSTOMER_VALIDATION"] = 1.1
    with pytest.raises(DOM.DomainContractError, match="CUSTOMER_VALIDATION_outside_0_1"):
        DOM.validate_proof_dimensions(proof)


def test_automation_roi_requires_inputs_without_invented_aggregation():
    cfg = KERNEL["automation_roi"]
    record = {name: 1 for name in cfg["record"]}
    record.update({name: 1 for name in cfg["required_components"]})
    DOM.validate_automation_roi_inputs(record)
    assert cfg["operator_relationship"] == "UNSPECIFIED_IN_FOUNDER_TEXT"
    assert cfg["aggregation_requires_explicit_policy"] is True


def test_agent_scorecard_cannot_reward_activity_metrics():
    scorecard = {name: 1 for name in KERNEL["agent_scorecard"]["metrics"]}
    scorecard["rewarded_metrics"] = ["economic_value", "customer_value"]
    DOM.validate_agent_scorecard(scorecard)
    scorecard["rewarded_metrics"] = ["token_usage"]
    with pytest.raises(DOM.DomainContractError, match="AGENT_ACTIVITY_METRIC_CANNOT_BE_REWARDED"):
        DOM.validate_agent_scorecard(scorecard)


def test_founder_surface_requires_bounded_decision_packet():
    packet = {field: "x" for field in KERNEL["minimum_founder_surface"]["request_packet_fields"]}
    packet["action"] = "APPROVE"
    DOM.validate_founder_request(packet)
    packet["action"] = "MANUAL_BUSYWORK"
    with pytest.raises(DOM.DomainContractError, match="FOUNDER_SURFACE_VIOLATION"):
        DOM.validate_founder_request(packet)


def test_self_healing_is_bounded():
    assert DOM.self_healing_decision("RETRY_SAFE_IDEMPOTENT_ACTION") == "ALLOW_BOUNDED"
    assert DOM.self_healing_decision("SECRET_REPLACEMENT") == "DENY"
    assert DOM.self_healing_decision("UNKNOWN_REPAIR") == "REQUIRE_POLICY_REVIEW"
