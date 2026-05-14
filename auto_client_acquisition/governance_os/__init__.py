"""Canonical Governance OS — single decision authority for every Dealix output.

Composes existing channel_policy_gateway, safe_send_gateway, safety_v10,
compliance_os_v12 into one `decide()` entry point that returns a
GovernanceDecision enum.
"""
from auto_client_acquisition.governance_os.runtime_decision import (
    DecisionResult,
    GovernanceDecision,
    decide,
)
from auto_client_acquisition.governance_os.channel_policy import (
    FORBIDDEN_CHANNEL_MODES,
    is_forbidden,
)
from auto_client_acquisition.governance_os.claim_safety import (
    FORBIDDEN_CLAIM_PATTERNS,
    contains_unsafe_claim,
)

__all__ = [
    "DecisionResult",
    "FORBIDDEN_CHANNEL_MODES",
    "FORBIDDEN_CLAIM_PATTERNS",
    "GovernanceDecision",
    "contains_unsafe_claim",
    "decide",
    "is_forbidden",
]
