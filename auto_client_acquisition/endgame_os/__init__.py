"""Dealix Endgame OS — operating doctrine encoded as runnable Python.

The companion docs live under ``docs/endgame/``. This package is the typed
interface to the Endgame doctrine: stages of the operating chain, the
governance decision vocabulary, agent control, capability diagnostic,
proof economy, business unit and venture gates, market power signals,
and the kill system.

Every module is dependency-free and side-effect-free so it can be imported
from anywhere in the Core OS without risk.
"""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import (
    AgentCard,
    AgentRegistry,
    AutonomyLevel,
)
from auto_client_acquisition.endgame_os.business_units import (
    BUSINESS_UNITS,
    BusinessUnit,
    BusinessUnitPromotionGate,
    PromotionEvaluation,
)
from auto_client_acquisition.endgame_os.capability_diagnostic import (
    CapabilityAxis,
    CapabilityDiagnosticReport,
    CapabilityScore,
)
from auto_client_acquisition.endgame_os.governance_product import (
    GovernanceDecision,
    GovernanceProductForm,
    GovernanceRuntimeDecision,
)
from auto_client_acquisition.endgame_os.kill_system import (
    KillCriteria,
    KillDecision,
    KillTarget,
    evaluate_kill,
)
from auto_client_acquisition.endgame_os.market_power import (
    MARKET_POWER_INDICATORS,
    MarketPowerIndicator,
    MarketPowerReading,
    should_escalate_market_spend,
)
from auto_client_acquisition.endgame_os.operating_chain import (
    OPERATING_CHAIN,
    ChainStage,
    ChainViolation,
    validate_transition,
)
from auto_client_acquisition.endgame_os.proof_economy import (
    ProofPack,
    ProofToRetainerMotion,
    ProofType,
    recommended_retainer,
)
from auto_client_acquisition.endgame_os.venture_factory import (
    VentureCandidate,
    VentureGate,
    VentureGateEvaluation,
)

__all__ = [
    "AgentCard",
    "AgentRegistry",
    "AutonomyLevel",
    "BUSINESS_UNITS",
    "BusinessUnit",
    "BusinessUnitPromotionGate",
    "PromotionEvaluation",
    "CapabilityAxis",
    "CapabilityDiagnosticReport",
    "CapabilityScore",
    "GovernanceDecision",
    "GovernanceProductForm",
    "GovernanceRuntimeDecision",
    "KillCriteria",
    "KillDecision",
    "KillTarget",
    "evaluate_kill",
    "MARKET_POWER_INDICATORS",
    "MarketPowerIndicator",
    "MarketPowerReading",
    "should_escalate_market_spend",
    "OPERATING_CHAIN",
    "ChainStage",
    "ChainViolation",
    "validate_transition",
    "ProofPack",
    "ProofToRetainerMotion",
    "ProofType",
    "recommended_retainer",
    "VentureCandidate",
    "VentureGate",
    "VentureGateEvaluation",
]
