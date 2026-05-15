"""Runtime governance product — re-exports endgame vocabulary for global-grade docs."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.governance_product import (
    GOVERNANCE_RUNTIME_COMPONENTS,
    GovernanceDecision,
    governance_runtime_maturity_score,
)

__all__ = [
    "GOVERNANCE_RUNTIME_COMPONENTS",
    "GovernanceDecision",
    "governance_runtime_maturity_score",
]
