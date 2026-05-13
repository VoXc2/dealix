"""Dealix Global-Grade OS — enterprise-grade extensions on top of endgame_os.

The companion docs live under ``docs/global_grade/``. These modules add
the typed instruments that the global-grade layer relies on:

* ``CapabilityIndex`` — the DCI (7 axes, 0–5 maturity).
* ``TransformationGap`` — the DTG decision matrix.
* ``EnterpriseTrust`` — the Source Passport and trust posture.
* ``RuntimeGovernanceProduct`` — typed runtime evaluation records.
* ``AgentGovernance`` — enterprise constraints on agent operation.
* ``MarketPowerScore`` — composite score with sustained-quarter rule.

The modules are dependency-free and side-effect-free.
"""

from __future__ import annotations

from auto_client_acquisition.global_grade_os.agent_governance import (
    AgentOperationDecision,
    EnterpriseAgentConstraint,
    enterprise_allowed_levels,
)
from auto_client_acquisition.global_grade_os.capability_index import (
    DCI_AXES,
    DCI_MATURITY_LABELS,
    DCIAxis,
    DCIMaturity,
    DCIReading,
    DCIReport,
)
from auto_client_acquisition.global_grade_os.enterprise_trust import (
    AllowedUse,
    SensitivityLevel,
    SourcePassport,
    TrustPosture,
    default_trust_posture,
)
from auto_client_acquisition.global_grade_os.market_power_score import (
    MarketPowerScore,
    MarketPowerScoreReading,
    compute_market_power_score,
)
from auto_client_acquisition.global_grade_os.runtime_governance_product import (
    RuntimeEvaluation,
    RuntimeProductTier,
    runtime_tier_for_readiness,
)
from auto_client_acquisition.global_grade_os.transformation_gap import (
    DTGEntry,
    DTGRecommendation,
    Feasibility,
    recommend_for_gap,
)

__all__ = [
    "AgentOperationDecision",
    "EnterpriseAgentConstraint",
    "enterprise_allowed_levels",
    "DCI_AXES",
    "DCI_MATURITY_LABELS",
    "DCIAxis",
    "DCIMaturity",
    "DCIReading",
    "DCIReport",
    "AllowedUse",
    "SensitivityLevel",
    "SourcePassport",
    "TrustPosture",
    "default_trust_posture",
    "MarketPowerScore",
    "MarketPowerScoreReading",
    "compute_market_power_score",
    "RuntimeEvaluation",
    "RuntimeProductTier",
    "runtime_tier_for_readiness",
    "DTGEntry",
    "DTGRecommendation",
    "Feasibility",
    "recommend_for_gap",
]
