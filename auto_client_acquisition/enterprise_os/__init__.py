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
    "KillMarketSignals",
    "KillServiceSignals",
    "MarketAuthorityInputs",
    "RedTeamVerdict",
    "SprintOpportunity",
    "VentureGateInputs",
    "capital_asset_band",
    "classify_sprint_opportunity",
    "compute_capital_asset_score",
    "compute_dci",
    "compute_dealix_capability_score",
    "compute_market_authority_score",
    "kill_feature_recommended",
    "kill_market_recommended",
    "kill_service_recommended",
    "meets_venture_gate",
    "red_team_verdict",
    "transformation_gap",
]
