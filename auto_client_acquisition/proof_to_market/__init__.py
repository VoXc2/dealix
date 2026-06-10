"""V12.5 Proof-to-Market — convert real proof events into approval-required marketing content.

NEVER fabricates. NEVER publishes externally without signed customer
permission. NEVER attaches customer name/logo without explicit
``signed_publish_permission`` field.
"""
from auto_client_acquisition.proof_to_market.engine import (
    approval_gate_check,
    case_study_candidate,
    proof_to_snippet,
    sector_learning_summary,
    select_publishable_proofs,
)

__all__ = [
    "approval_gate_check",
    "case_study_candidate",
    "proof_to_snippet",
    "sector_learning_summary",
    "select_publishable_proofs",
]
