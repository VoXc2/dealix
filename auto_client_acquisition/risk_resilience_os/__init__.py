"""Dealix Risk & Resilience OS.

Companion doc: ``docs/risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md``.
"""

from __future__ import annotations

from auto_client_acquisition.risk_resilience_os.client_risk_score import (
    CLIENT_RISK_DIMENSIONS,
    ClientRiskSignals,
    ClientRiskTier,
    classify_client_risk,
)
from auto_client_acquisition.risk_resilience_os.resilience_score import (
    RESILIENCE_WEIGHTS,
    ResilienceComponents,
    ResilienceTier,
    classify_resilience,
    compute_resilience_score,
)
from auto_client_acquisition.risk_resilience_os.risk_taxonomy import (
    RISK_CATEGORIES,
    RiskCategory,
)

__all__ = [
    "CLIENT_RISK_DIMENSIONS",
    "ClientRiskSignals",
    "ClientRiskTier",
    "classify_client_risk",
    "RESILIENCE_WEIGHTS",
    "ResilienceComponents",
    "ResilienceTier",
    "classify_resilience",
    "compute_resilience_score",
    "RISK_CATEGORIES",
    "RiskCategory",
]
