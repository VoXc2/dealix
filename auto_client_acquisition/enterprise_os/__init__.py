"""Dealix Enterprise OS — holding/group façade over Intelligence + Command scoring."""

from __future__ import annotations

from auto_client_acquisition.enterprise_os.ai_control_plane import (
    CONTROL_PLANE_ENTERPRISE_MODULES,
    CONTROL_PLANE_PRODUCT_PHASES,
)
from auto_client_acquisition.enterprise_os.capability_score import (
    CapabilityScores,
    compute_dci,
    compute_dealix_capability_score,
)
from auto_client_acquisition.enterprise_os.capital_asset_score import (
    CapitalAssetBand,
    CapitalAssetScoreInputs,
    capital_asset_band,
    compute_capital_asset_score,
)
from auto_client_acquisition.enterprise_os.enterprise_program import (
    EnterpriseProgram,
    ProgramPhase,
    get_program,
    list_phases,
    phase_by_key,
)
from auto_client_acquisition.enterprise_os.enterprise_readiness import (
    ReadinessBand,
    ReadinessReport,
    ReadinessScores,
    compute_readiness_score,
    get_readiness,
    is_sellable,
    list_readiness,
    score_band,
)
from auto_client_acquisition.enterprise_os.governance_runtime_product import (
    GOVERNANCE_RUNTIME_DECISIONS,
    GOVERNANCE_RUNTIME_PRODUCT_COMPONENTS,
)
from auto_client_acquisition.enterprise_os.kill_system import (
    KillMarketSignals,
    KillServiceSignals,
    kill_feature_recommended,
    kill_market_recommended,
    kill_service_recommended,
)
from auto_client_acquisition.enterprise_os.market_authority_score import (
    MarketAuthorityInputs,
    compute_market_authority_score,
)
from auto_client_acquisition.enterprise_os.red_team import RedTeamVerdict, red_team_verdict
from auto_client_acquisition.enterprise_os.transformation_gap import (
    SprintOpportunity,
    classify_sprint_opportunity,
    transformation_gap,
)
from auto_client_acquisition.enterprise_os.trust_pack import TRUST_PRODUCT_COMPONENTS
from auto_client_acquisition.enterprise_os.venture_factory import (
    VentureGateInputs,
    meets_venture_gate,
)

__all__ = [
    "CONTROL_PLANE_ENTERPRISE_MODULES",
    "CONTROL_PLANE_PRODUCT_PHASES",
    "GOVERNANCE_RUNTIME_DECISIONS",
    "GOVERNANCE_RUNTIME_PRODUCT_COMPONENTS",
    "TRUST_PRODUCT_COMPONENTS",
    "CapabilityScores",
    "CapitalAssetBand",
    "CapitalAssetScoreInputs",
    "EnterpriseProgram",
    "KillMarketSignals",
    "KillServiceSignals",
    "MarketAuthorityInputs",
    "ProgramPhase",
    "ReadinessBand",
    "ReadinessReport",
    "ReadinessScores",
    "RedTeamVerdict",
    "SprintOpportunity",
    "VentureGateInputs",
    "capital_asset_band",
    "classify_sprint_opportunity",
    "compute_capital_asset_score",
    "compute_dci",
    "compute_dealix_capability_score",
    "compute_market_authority_score",
    "compute_readiness_score",
    "get_program",
    "get_readiness",
    "is_sellable",
    "kill_feature_recommended",
    "kill_market_recommended",
    "kill_service_recommended",
    "list_phases",
    "list_readiness",
    "meets_venture_gate",
    "phase_by_key",
    "red_team_verdict",
    "score_band",
    "transformation_gap",
]
