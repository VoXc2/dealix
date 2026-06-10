"""Endgame Operating Doctrine — chain, governance product, agents, kill system."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import (
    AUTONOMY_LEVEL_MAX,
    MVP_AUTONOMY_CEILING,
    AgentControlCard,
    autonomy_allowed,
    normalize_agent_card_dict,
    validate_agent_card,
)
from auto_client_acquisition.endgame_os.business_units import (
    UNIT_REGISTRY,
    DealixBusinessUnit,
    UnitSystemProfile,
    get_unit_profile,
)
from auto_client_acquisition.endgame_os.capability_diagnostic import (
    CapabilityDiagnosticProfile,
    recommended_sprints,
)
from auto_client_acquisition.endgame_os.governance_product import (
    GOVERNANCE_RUNTIME_COMPONENTS,
    GovernanceDecision,
    governance_runtime_maturity_score,
)
from auto_client_acquisition.endgame_os.kill_system import (
    KillFeatureSignals,
    KillMarketSignals,
    KillServiceSignals,
    should_kill_feature,
    should_kill_market,
    should_kill_service,
)
from auto_client_acquisition.endgame_os.market_power import (
    MARKET_POWER_SIGNALS,
    market_power_activation_score,
)
from auto_client_acquisition.endgame_os.operating_chain import (
    CORE_OPERATING_CHAIN,
    can_enter_step,
    chain_complete_through,
    chain_index,
)
from auto_client_acquisition.endgame_os.proof_economy import (
    PROOF_PACK_SECTIONS,
    ProofKind,
    proof_to_retainer_hint,
    recurring_offer_for_proof,
)
from auto_client_acquisition.endgame_os.venture_factory import (
    VentureGateChecklist,
    venture_gate_passes,
)

__all__ = [
    "AUTONOMY_LEVEL_MAX",
    "CORE_OPERATING_CHAIN",
    "GOVERNANCE_RUNTIME_COMPONENTS",
    "MARKET_POWER_SIGNALS",
    "MVP_AUTONOMY_CEILING",
    "PROOF_PACK_SECTIONS",
    "UNIT_REGISTRY",
    "AgentControlCard",
    "CapabilityDiagnosticProfile",
    "DealixBusinessUnit",
    "GovernanceDecision",
    "KillFeatureSignals",
    "KillMarketSignals",
    "KillServiceSignals",
    "ProofKind",
    "UnitSystemProfile",
    "VentureGateChecklist",
    "autonomy_allowed",
    "can_enter_step",
    "chain_complete_through",
    "chain_index",
    "get_unit_profile",
    "governance_runtime_maturity_score",
    "market_power_activation_score",
    "normalize_agent_card_dict",
    "proof_to_retainer_hint",
    "recommended_sprints",
    "recurring_offer_for_proof",
    "should_kill_feature",
    "should_kill_market",
    "should_kill_service",
    "validate_agent_card",
    "venture_gate_passes",
]
