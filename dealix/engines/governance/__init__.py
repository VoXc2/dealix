"""Governance Engine (Engine 4) — production-depth governance for the platform."""

from __future__ import annotations

from dealix.engines.governance.engine import GOVERNANCE_ENGINE, GovernanceEngine
from dealix.engines.governance.explainability import Explanation
from dealix.engines.governance.models import ActionEvaluation, EvaluateResult
from dealix.engines.governance.risk import RiskSnapshot

__all__ = [
    "GOVERNANCE_ENGINE",
    "ActionEvaluation",
    "EvaluateResult",
    "Explanation",
    "GovernanceEngine",
    "RiskSnapshot",
]
