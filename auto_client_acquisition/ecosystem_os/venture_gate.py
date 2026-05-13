"""Venture Gate v2 — extends the endgame gate with proof-library requirements."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VentureGateV2:
    paid_clients: int
    active_retainers: int
    proof_pack_count: int
    average_proof_score: float
    qa_pass_rate: float
    has_product_module: bool
    playbook_maturity: float
    named_owner_committed: bool
    healthy_margin: bool
    inherits_core_os: bool


@dataclass(frozen=True)
class VentureGateV2Result:
    passes: bool
    failed_checks: tuple[str, ...]


def evaluate_venture_gate_v2(g: VentureGateV2) -> VentureGateV2Result:
    failures: list[str] = []
    if g.paid_clients < 5:
        failures.append("paid_clients_below_5")
    if g.active_retainers < 2:
        failures.append("active_retainers_below_2")
    if g.proof_pack_count < 10:
        failures.append("proof_pack_count_below_10")
    if g.average_proof_score < 80:
        failures.append("average_proof_score_below_80")
    if g.qa_pass_rate < 0.80:
        failures.append("qa_pass_rate_below_80_pct")
    if not g.has_product_module:
        failures.append("missing_product_module")
    if g.playbook_maturity < 0.80:
        failures.append("playbook_maturity_below_80_pct")
    if not g.named_owner_committed:
        failures.append("missing_committed_owner")
    if not g.healthy_margin:
        failures.append("unhealthy_margin")
    if not g.inherits_core_os:
        failures.append("must_inherit_core_os")
    return VentureGateV2Result(passes=not failures, failed_checks=tuple(failures))
