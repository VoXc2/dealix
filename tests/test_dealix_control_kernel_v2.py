from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
KERNEL_PATH = ROOT / "config" / "company" / "dealix_control_kernel_v2.json"
VERIFY_PATH = ROOT / "scripts" / "commercial" / "verify_dealix_control_kernel_v2.py"
RUNTIME_PATH = ROOT / "scripts" / "commercial" / "dealix_control_kernel_v2.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VERIFY = _load(VERIFY_PATH, "dealix_control_kernel_verify")
RUNTIME = _load(RUNTIME_PATH, "dealix_control_kernel_runtime")


def valid_payload() -> dict:
    return copy.deepcopy(json.loads(KERNEL_PATH.read_text(encoding="utf-8")))


def test_canonical_kernel_passes():
    assert VERIFY.verify(valid_payload()) == []


def test_all_lxxi_to_cxx_sections_are_registered_exactly():
    payload = valid_payload()
    assert [row[0] for row in payload["section_registry"]] == VERIFY.EXPECTED_SECTIONS
    assert len(payload["section_registry"]) == 50


def test_prediction_cannot_be_promoted_to_fact_policy():
    payload = valid_payload()
    payload["decision_quality"]["prediction_is_not_fact"] = False
    assert "PREDICTION_NOT_FACT" in VERIFY.verify(payload)


def test_inference_cannot_be_customer_evidence_policy():
    payload = valid_payload()
    payload["decision_quality"]["inference_is_not_customer_evidence"] = False
    assert "INFERENCE_NOT_EVIDENCE" in VERIFY.verify(payload)


def test_value_weights_must_sum_to_one():
    payload = valid_payload()
    payload["economic_dispatcher"]["value_weights"]["CASH_IMPACT"] = 0.31
    assert "VALUE_WEIGHTS_SUM" in VERIFY.verify(payload)


def test_execution_drag_weights_must_sum_to_one():
    payload = valid_payload()
    payload["economic_dispatcher"]["execution_drag_weights"]["TIME_COST"] = 0.26
    assert "DRAG_WEIGHTS_SUM" in VERIFY.verify(payload)


def test_priority_formula_matches_constitution():
    values = {key: 1.0 for key in valid_payload()["economic_dispatcher"]["value_weights"]}
    drag = {key: 0.2 for key in valid_payload()["economic_dispatcher"]["execution_drag_weights"]}
    result = RUNTIME.calculate_priority(
        value_inputs=values,
        drag_inputs=drag,
        evidence_confidence=1.0,
        data_freshness=1.0,
        constraint_fit=1.0,
        urgency_factor=1.0,
    )
    assert result.value_vector == pytest.approx(1.0)
    assert result.execution_drag == pytest.approx(0.2)
    assert result.confidence_factor == pytest.approx(1.0)
    assert result.final_priority == pytest.approx(5.0)


def test_priority_rejects_non_normalized_input():
    values = {key: 0.5 for key in valid_payload()["economic_dispatcher"]["value_weights"]}
    drag = {key: 0.5 for key in valid_payload()["economic_dispatcher"]["execution_drag_weights"]}
    values["CASH_IMPACT"] = 1.1
    with pytest.raises(RUNTIME.ControlKernelError):
        RUNTIME.calculate_priority(
            value_inputs=values,
            drag_inputs=drag,
            evidence_confidence=1.0,
            data_freshness=1.0,
            constraint_fit=1.0,
            urgency_factor=1.0,
        )


def test_voi_research_first_when_information_is_more_valuable():
    voi = RUNTIME.value_of_information(expected_decision_loss_avoided=1000, information_cost=100)
    assert voi == pytest.approx(10.0)
    assert RUNTIME.choose_execution_vs_information(voi=voi, immediate_execution_advantage=2.0) == "RESEARCH_OR_TEST_FIRST"


def test_high_uncertainty_irreversible_action_defaults_hold():
    assert RUNTIME.reversibility_default(reversibility="R5", high_uncertainty=True) == "HOLD"


def test_high_confidence_read_only_defaults_execute():
    assert RUNTIME.reversibility_default(reversibility="R0", high_confidence=True) == "EXECUTE"


def test_conflicting_confidence_classification_fails_closed():
    with pytest.raises(RUNTIME.ControlKernelError, match="confidence_classification_conflict"):
        RUNTIME.reversibility_default(reversibility="R3", high_uncertainty=True, high_confidence=True)


def test_state_machine_allows_only_next_step():
    RUNTIME.validate_transition(machine="opportunity", from_state="KNOWN", to_state="INTERACTION")
    with pytest.raises(RUNTIME.InvalidStateTransition, match="INVALID_STATE_TRANSITION"):
        RUNTIME.validate_transition(machine="opportunity", from_state="KNOWN", to_state="PAID")


def test_transition_packet_requires_evidence_authority_side_effect_and_receipt():
    packet = {
        "from_state": "KNOWN",
        "to_state": "INTERACTION",
        "required_evidence": ["email-reply-1"],
        "authority": "permissioned-thread",
        "side_effect": "NONE",
        "receipt": "proof://interaction/1",
    }
    RUNTIME.validate_transition_packet(machine="opportunity", packet=packet)
    packet["required_evidence"] = []
    with pytest.raises(RUNTIME.InvalidStateTransition, match="TRANSITION_EVIDENCE_MISSING"):
        RUNTIME.validate_transition_packet(machine="opportunity", packet=packet)


def test_production_cannot_jump_from_build_to_green():
    with pytest.raises(RUNTIME.InvalidStateTransition):
        RUNTIME.validate_transition(machine="production", from_state="BUILD_ACCEPTED", to_state="PRODUCTION_GREEN")


def test_production_green_can_explicitly_degrade_or_enter_rollback():
    RUNTIME.validate_transition(machine="production", from_state="PRODUCTION_GREEN", to_state="DEGRADED")
    RUNTIME.validate_transition(machine="production", from_state="PRODUCTION_GREEN", to_state="ROLLBACK_ACTIVE")


def test_financial_quote_cannot_jump_to_payment_verified():
    with pytest.raises(RUNTIME.InvalidStateTransition):
        RUNTIME.validate_transition(machine="financial", from_state="QUOTE", to_state="PAYMENT_VERIFIED")


def test_close_priority_candidates_use_constitutional_tie_break_order():
    first = {
        "id": "A",
        "final_priority": 1.00,
        "reversibility": "R2",
        "feedback_speed": 0.8,
        "customer_learning": 0.8,
        "founder_attention": 0.2,
        "proof_potential": 0.8,
    }
    second = {
        "id": "B",
        "final_priority": 1.05,
        "reversibility": "R1",
        "feedback_speed": 0.6,
        "customer_learning": 0.6,
        "founder_attention": 0.3,
        "proof_potential": 0.6,
    }
    assert RUNTIME.choose_close_candidate(first=first, second=second) == "B"


def test_non_close_priority_candidates_choose_higher_score():
    first = {
        "id": "A",
        "final_priority": 1.00,
        "reversibility": "R0",
        "feedback_speed": 1.0,
        "customer_learning": 1.0,
        "founder_attention": 0.0,
        "proof_potential": 1.0,
    }
    second = {
        "id": "B",
        "final_priority": 1.50,
        "reversibility": "R5",
        "feedback_speed": 0.0,
        "customer_learning": 0.0,
        "founder_attention": 1.0,
        "proof_potential": 0.0,
    }
    assert RUNTIME.choose_close_candidate(first=first, second=second) == "B"


def test_budget_exhaustion_is_fail_closed():
    with pytest.raises(RUNTIME.BudgetBlocked, match="BUDGET_BLOCKED"):
        RUNTIME.check_budget(used=10, limit=10)


def test_marginal_value_stops_negative_increment():
    assert RUNTIME.should_continue_increment(marginal_value=4, marginal_cost=5) is False
    assert RUNTIME.should_continue_increment(marginal_value=5, marginal_cost=5) is True


def test_policy_receipt_is_structured_and_observable():
    receipt = RUNTIME.policy_decision_receipt(
        policy_decision_id="pd-1",
        agent_id="dealix-sales",
        workload_id="runtime-123",
        resource="gmail-draft",
        requested_action="CREATE_DRAFT",
        risk="R1",
        policy_version="2.0-control-kernel",
        decision="ALLOW",
        reason="draft-only bounded action",
        authority_source="company-policy",
        timestamp="2026-09-11T00:00:00+00:00",
    )
    assert receipt["decision"] == "ALLOW"
    assert receipt["workload_id"] == "runtime-123"
    assert receipt["timestamp"] == "2026-09-11T00:00:00+00:00"


def test_agent_name_alone_can_never_authorize_material_action():
    payload = valid_payload()
    payload["identity"]["never_authorize_by_agent_name_only"] = False
    assert "NO_AGENT_NAME_AUTHORITY" in VERIFY.verify(payload)


def test_universal_l5_autonomy_is_forbidden():
    payload = valid_payload()
    payload["autonomy_promotion"]["universal_l5_autonomy_forbidden"] = False
    assert "NO_UNIVERSAL_L5" in VERIFY.verify(payload)


def test_model_change_cannot_be_silent():
    payload = valid_payload()
    payload["model_change"]["silent_model_replacement_forbidden"] = False
    assert "NO_SILENT_MODEL_CHANGE" in VERIFY.verify(payload)


def test_shadow_execution_must_have_no_material_effect():
    payload = valid_payload()
    payload["shadow_execution"]["material_effect"] = True
    assert "SHADOW_NO_EFFECT" in VERIFY.verify(payload)


def test_customer_memory_cannot_be_global_uncontrolled_store():
    payload = valid_payload()
    payload["customer_memory"]["global_uncontrolled_customer_sensitive_memory_forbidden"] = False
    assert "NO_GLOBAL_CUSTOMER_MEMORY" in VERIFY.verify(payload)


def test_self_healing_cannot_cross_material_boundaries():
    payload = valid_payload()
    payload["self_healing"]["forbidden"].remove("SECRET_REPLACEMENT")
    assert "SELF_HEALING_BOUNDARY" in VERIFY.verify(payload)


def test_prompt_injection_privilege_escalation_control_test_is_mandatory():
    payload = valid_payload()
    payload["control_tests"].remove("PROMPT_INJECTION_DOES_NOT_ESCALATE_PRIVILEGE")
    assert "PROMPT_INJECTION_CONTROL_TEST" in VERIFY.verify(payload)
