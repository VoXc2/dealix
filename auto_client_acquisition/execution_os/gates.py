"""Execution gates — no stage advance without explicit checks."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import IntEnum


class ExecutionGate(IntEnum):
    MARKET_PAIN = 1
    OFFER = 2
    DELIVERY = 3
    GOVERNANCE = 4
    PROOF = 5
    PRODUCTIZATION = 6
    RETAINER = 7
    VENTURE = 8


_GATE_REQUIRED: dict[int, frozenset[str]] = {
    ExecutionGate.MARKET_PAIN: frozenset(
        {
            "client_describes_pain_without_long_training",
            "pain_repeats_across_clients",
            "pain_near_money_time_or_risk",
        },
    ),
    ExecutionGate.OFFER: frozenset(
        {
            "buyer",
            "pain",
            "promise",
            "scope",
            "exclusions",
            "price",
            "qa",
            "governance",
            "proof",
            "next_offer",
        },
    ),
    ExecutionGate.DELIVERY: frozenset(
        {
            "client_inputs_clear",
            "owner_clear",
            "success_metric_clear",
            "approval_path_clear",
        },
    ),
    ExecutionGate.GOVERNANCE: frozenset(
        {
            "source_status",
            "pii_status",
            "allowed_use",
            "risk_level",
            "approval_decision",
            "audit_event",
        },
    ),
    ExecutionGate.PROOF: frozenset(
        {
            "proof_pack",
            "value_metric",
            "limitations",
            "next_recommendation",
            "capital_asset",
        },
    ),
    ExecutionGate.PRODUCTIZATION: frozenset(
        {
            "manual_repeat_3plus",
            "time_cost_meaningful",
            "revenue_linked",
            "risk_reducing",
            "testable",
            "reusable",
        },
    ),
    ExecutionGate.RETAINER: frozenset(
        {
            "proof_score_strong",
            "client_health_good",
            "workflow_recurring",
            "monthly_value_clear",
        },
    ),
    ExecutionGate.VENTURE: frozenset(
        {
            "paid_clients_5plus",
            "retainers_2plus",
            "repeatable_delivery",
            "product_module_used",
            "playbook_maturity_80plus",
            "owner_exists",
            "healthy_margin",
        },
    ),
}


@dataclass(frozen=True, slots=True)
class GateResult:
    gate: ExecutionGate
    passed: bool
    missing_keys: tuple[str, ...]


def evaluate_gate(gate: ExecutionGate, checklist: Mapping[str, bool]) -> GateResult:
    """All required checklist keys must be present and True."""
    required = _GATE_REQUIRED[gate]
    missing = sorted(k for k in required if not checklist.get(k))
    return GateResult(gate=gate, passed=not missing, missing_keys=tuple(missing))


def all_gates_pass(
    checklists: Mapping[int, Mapping[str, bool]],
    *,
    gates: Iterable[ExecutionGate] | None = None,
) -> bool:
    """checklists maps ExecutionGate int value -> field dict."""
    to_check = tuple(gates) if gates is not None else tuple(ExecutionGate)
    return all(evaluate_gate(g, checklists.get(int(g), {})).passed for g in to_check)
