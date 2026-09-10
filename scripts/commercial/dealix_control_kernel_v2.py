#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
KERNEL_PATH = ROOT / "config" / "company" / "dealix_control_kernel_v2.json"


class ControlKernelError(ValueError):
    pass


class InvalidStateTransition(ControlKernelError):
    pass


class BudgetBlocked(ControlKernelError):
    pass


@dataclass(frozen=True)
class PriorityResult:
    value_vector: float
    execution_drag: float
    confidence_factor: float
    final_priority: float


def load_kernel(path: Path = KERNEL_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ControlKernelError("kernel_root_not_object")
    return data


def _bounded01(name: str, value: float) -> float:
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise ControlKernelError(f"{name}_outside_0_1")
    return number


def calculate_priority(
    *,
    value_inputs: dict[str, float],
    drag_inputs: dict[str, float],
    evidence_confidence: float,
    data_freshness: float,
    constraint_fit: float,
    urgency_factor: float,
    kernel: dict[str, Any] | None = None,
) -> PriorityResult:
    kernel = kernel or load_kernel()
    dispatcher = kernel["economic_dispatcher"]
    value_weights = dispatcher["value_weights"]
    drag_weights = dispatcher["execution_drag_weights"]

    missing_value = set(value_weights) - set(value_inputs)
    missing_drag = set(drag_weights) - set(drag_inputs)
    if missing_value:
        raise ControlKernelError("missing_value_inputs:" + ",".join(sorted(missing_value)))
    if missing_drag:
        raise ControlKernelError("missing_drag_inputs:" + ",".join(sorted(missing_drag)))

    normalized_value = {key: _bounded01(key, value_inputs[key]) for key in value_weights}
    normalized_drag = {key: _bounded01(key, drag_inputs[key]) for key in drag_weights}
    evidence_confidence = _bounded01("evidence_confidence", evidence_confidence)
    data_freshness = _bounded01("data_freshness", data_freshness)
    constraint_fit = _bounded01("constraint_fit", constraint_fit)
    urgency_factor = _bounded01("urgency_factor", urgency_factor)

    value_vector = sum(float(value_weights[k]) * normalized_value[k] for k in value_weights)
    execution_drag = sum(float(drag_weights[k]) * normalized_drag[k] for k in drag_weights)
    confidence_factor = evidence_confidence * data_freshness
    final_priority = value_vector * confidence_factor * constraint_fit * urgency_factor / max(0.20, execution_drag)
    return PriorityResult(value_vector, execution_drag, confidence_factor, final_priority)


def value_of_information(*, expected_decision_loss_avoided: float, information_cost: float) -> float:
    if information_cost <= 0:
        raise ControlKernelError("information_cost_must_be_positive")
    if expected_decision_loss_avoided < 0:
        raise ControlKernelError("expected_decision_loss_avoided_must_be_nonnegative")
    return float(expected_decision_loss_avoided) / float(information_cost)


def choose_execution_vs_information(*, voi: float, immediate_execution_advantage: float) -> str:
    if voi < 0 or immediate_execution_advantage < 0:
        raise ControlKernelError("voi_and_advantage_must_be_nonnegative")
    return "RESEARCH_OR_TEST_FIRST" if voi > immediate_execution_advantage else "EXECUTE_BOUNDED_ACTION"


def reversibility_default(*, reversibility: str, confidence: float) -> str:
    confidence = _bounded01("confidence", confidence)
    if reversibility not in {"R0", "R1", "R2", "R3", "R4", "R5"}:
        raise ControlKernelError("unknown_reversibility")
    if reversibility in {"R4", "R5"} and confidence < 0.80:
        return "HOLD"
    if reversibility in {"R0", "R1"} and confidence >= 0.80:
        return "EXECUTE"
    return "REVIEW"


def _machine(kernel: dict[str, Any], machine: str) -> list[str]:
    states = kernel["state_machines"].get(machine)
    if not isinstance(states, list) or not states:
        raise ControlKernelError(f"unknown_state_machine:{machine}")
    return [str(x) for x in states]


def validate_transition(*, machine: str, from_state: str, to_state: str, kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    states = _machine(kernel, machine)
    if from_state not in states or to_state not in states:
        raise InvalidStateTransition("INVALID_STATE_TRANSITION")
    if states.index(to_state) != states.index(from_state) + 1:
        raise InvalidStateTransition("INVALID_STATE_TRANSITION")


def check_budget(*, used: float, limit: float) -> None:
    if limit < 0 or used < 0:
        raise ControlKernelError("budget_values_must_be_nonnegative")
    if used >= limit:
        raise BudgetBlocked("BUDGET_BLOCKED")


def should_continue_increment(*, marginal_value: float, marginal_cost: float) -> bool:
    if marginal_value < 0 or marginal_cost < 0:
        raise ControlKernelError("marginal_values_must_be_nonnegative")
    return marginal_value >= marginal_cost


def policy_decision_receipt(
    *,
    policy_decision_id: str,
    agent_id: str,
    workload_id: str,
    resource: str,
    requested_action: str,
    risk: str,
    policy_version: str,
    decision: str,
    reason: str,
    authority_source: str,
    timestamp: str | None = None,
    kernel: dict[str, Any] | None = None,
) -> dict[str, str]:
    kernel = kernel or load_kernel()
    allowed = set(kernel["policy_decision_receipt"]["outcomes"])
    if decision not in allowed:
        raise ControlKernelError("invalid_policy_decision")
    receipt = {
        "policy_decision_id": policy_decision_id,
        "agent_id": agent_id,
        "workload_id": workload_id,
        "resource": resource,
        "requested_action": requested_action,
        "risk": risk,
        "policy_version": policy_version,
        "decision": decision,
        "reason": reason,
        "authority_source": authority_source,
    }
    if any(not str(value).strip() for value in receipt.values()):
        raise ControlKernelError("policy_receipt_required_field_missing")
    receipt["timestamp"] = timestamp or datetime.now(timezone.utc).isoformat()
    return receipt


def tie_break_order(kernel: dict[str, Any] | None = None) -> list[str]:
    kernel = kernel or load_kernel()
    return list(kernel["economic_dispatcher"]["tie_breakers"])
