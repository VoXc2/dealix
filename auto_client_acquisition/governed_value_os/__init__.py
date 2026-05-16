"""Governed Value OS — North Star metric, proof state machine, gate map.

Encodes Dealix's "Governed Revenue & AI Operations" doctrine into the operating
backbone: the canonical chain Signal → Source → Approval → Action → Evidence →
Decision → Value → Asset. Code only — never sends, never charges.
"""

from auto_client_acquisition.governed_value_os.decisions_ledger import (
    GovernedValueDecision,
    count_decisions,
    list_decisions,
    record_decision,
)
from auto_client_acquisition.governed_value_os.gate_map import (
    GATES,
    Gate,
    evaluate_gates,
)
from auto_client_acquisition.governed_value_os.state_machine import (
    ALLOWED_TRANSITIONS,
    PROOF_LEVEL_LABEL,
    ProofState,
    ProofTransitionError,
    level_label,
    revenue_recognized,
    validate_transition,
)

__all__ = [
    "ALLOWED_TRANSITIONS",
    "GATES",
    "PROOF_LEVEL_LABEL",
    "Gate",
    "GovernedValueDecision",
    "ProofState",
    "ProofTransitionError",
    "count_decisions",
    "evaluate_gates",
    "level_label",
    "list_decisions",
    "record_decision",
    "revenue_recognized",
    "validate_transition",
]
