"""Proof-to-retainer paths and venture factory gate v2."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RetainerPath(StrEnum):
    CONTINUE = "continue"
    EXPAND = "expand"
    PAUSE = "pause"


@dataclass(frozen=True, slots=True)
class RetainerGateInput:
    proof_score: int
    client_health: int
    workflow_recurring: bool
    owner_exists: bool
    monthly_value_clear: bool
    governance_risk_controlled: bool


def retainer_gate_passes(gate: RetainerGateInput) -> tuple[bool, tuple[str, ...]]:
    errs: list[str] = []
    if gate.proof_score < 80:
        errs.append("proof_score_below_retainer_threshold")
    if gate.client_health < 70:
        errs.append("client_health_below_threshold")
    if not gate.workflow_recurring:
        errs.append("workflow_not_recurring")
    if not gate.owner_exists:
        errs.append("owner_missing")
    if not gate.monthly_value_clear:
        errs.append("monthly_value_unclear")
    if not gate.governance_risk_controlled:
        errs.append("governance_risk_not_controlled")
    return not errs, tuple(errs)


def retainer_path_recommendation(
    *,
    retainer_gate_ok: bool,
    adjacent_capability_ready: bool,
) -> RetainerPath:
    if not retainer_gate_ok:
        return RetainerPath.PAUSE
    if adjacent_capability_ready:
        return RetainerPath.EXPAND
    return RetainerPath.CONTINUE


@dataclass(frozen=True, slots=True)
class VentureFactoryGateV2Input:
    paid_clients: int
    retainers: int
    proof_packs_count: int
    avg_proof_score: float
    repeatable_delivery: bool
    product_module_used: bool
    playbook_maturity: float
    owner_exists: bool
    healthy_margin: bool
    core_os_dependency_documented: bool


def venture_factory_gate_v2_passes(
    v: VentureFactoryGateV2Input,
) -> tuple[bool, tuple[str, ...]]:
    errs: list[str] = []
    if v.paid_clients < 5:
        errs.append("paid_clients_below_5")
    if v.retainers < 2:
        errs.append("retainers_below_2")
    if v.proof_packs_count < 10:
        errs.append("proof_library_below_10")
    if v.avg_proof_score < 80.0:
        errs.append("avg_proof_score_below_80")
    if not v.repeatable_delivery:
        errs.append("delivery_not_repeatable")
    if not v.product_module_used:
        errs.append("product_module_not_used")
    if v.playbook_maturity < 80.0:
        errs.append("playbook_maturity_below_80")
    if not v.owner_exists:
        errs.append("venture_owner_missing")
    if not v.healthy_margin:
        errs.append("margin_not_healthy")
    if not v.core_os_dependency_documented:
        errs.append("core_os_dependency_not_documented")
    return not errs, tuple(errs)
