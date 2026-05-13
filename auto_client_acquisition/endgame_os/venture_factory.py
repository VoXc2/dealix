"""Venture Factory — venture candidates and the venture gate.

See ``docs/endgame/VENTURE_FACTORY.md``. No venture launches without
proof; this module encodes the objective check.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VentureCandidate:
    code: str
    name: str
    originating_bu: str
    module: str


CANDIDATE_VENTURES: tuple[VentureCandidate, ...] = (
    VentureCandidate("REVENUE_OS", "Dealix Revenue OS", "REVENUE", "revenue_os"),
    VentureCandidate(
        "GOVERNANCE_CLOUD",
        "Dealix Governance Cloud",
        "GOVERNANCE",
        "governance_os",
    ),
    VentureCandidate(
        "COMPANY_BRAIN",
        "Dealix Company Brain",
        "BRAIN",
        "brain_os",
    ),
    VentureCandidate(
        "CLINICS_OS",
        "Dealix Clinics OS",
        "TBD",
        "operations_os/clinics",
    ),
    VentureCandidate(
        "LOGISTICS_OS",
        "Dealix Logistics OS",
        "TBD",
        "operations_os/logistics",
    ),
)


@dataclass(frozen=True)
class VentureGate:
    paid_clients: int
    active_retainers: int
    qa_pass_rate: float          # 0..1
    has_product_module: bool
    playbook_maturity: float     # 0..1
    named_owner_committed: bool
    healthy_margin: bool
    proof_library_size: int
    inherits_core_os: bool

    MIN_PAID_CLIENTS = 5
    MIN_ACTIVE_RETAINERS = 2
    MIN_QA_PASS_RATE = 0.80
    MIN_PLAYBOOK_MATURITY = 0.80
    MIN_PROOF_LIBRARY = 3


@dataclass(frozen=True)
class VentureGateEvaluation:
    passes: bool
    failed_checks: tuple[str, ...]


def evaluate_venture_gate(gate: VentureGate) -> VentureGateEvaluation:
    failures: list[str] = []
    if gate.paid_clients < gate.MIN_PAID_CLIENTS:
        failures.append("paid_clients_below_threshold")
    if gate.active_retainers < gate.MIN_ACTIVE_RETAINERS:
        failures.append("active_retainers_below_threshold")
    if gate.qa_pass_rate < gate.MIN_QA_PASS_RATE:
        failures.append("qa_pass_rate_below_threshold")
    if not gate.has_product_module:
        failures.append("missing_product_module")
    if gate.playbook_maturity < gate.MIN_PLAYBOOK_MATURITY:
        failures.append("playbook_maturity_below_threshold")
    if not gate.named_owner_committed:
        failures.append("missing_committed_owner")
    if not gate.healthy_margin:
        failures.append("unhealthy_margin")
    if gate.proof_library_size < gate.MIN_PROOF_LIBRARY:
        failures.append("proof_library_below_threshold")
    if not gate.inherits_core_os:
        # The doctrine forbids ventures that fork the Core OS.
        failures.append("must_inherit_core_os")
    return VentureGateEvaluation(passes=not failures, failed_checks=tuple(failures))
