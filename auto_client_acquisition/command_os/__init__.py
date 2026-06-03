"""Sovereign Command System — pure scoring, classification, and policy helpers (no I/O)."""

from auto_client_acquisition.command_os.board_memo import BOARD_MEMO_SECTION_TITLES
from auto_client_acquisition.command_os.capability_score import (
    OperatingCapabilityBand,
    OperatingCapabilityInputs,
    compute_operating_capability_score,
    operating_capability_band,
)
from auto_client_acquisition.command_os.capital_allocation import (
    WorldClassAllocationBand,
    WorldClassAllocationInputs,
    compute_world_class_allocation_score,
    world_class_allocation_band,
)
from auto_client_acquisition.command_os.capital_creation_score import (
    meets_minimum_capital_creation,
)
from auto_client_acquisition.command_os.decision_rights import (
    DECISION_RIGHTS_ROWS,
    DecisionRightRow,
    decision_right_for_key,
)
from auto_client_acquisition.command_os.governance_risk_index import (
    GovernanceRiskBand,
    GovernanceRiskInputs,
    compute_governance_risk_index,
    governance_risk_band,
)
from auto_client_acquisition.command_os.kill_criteria import (
    KillMarketSignals,
    KillServiceSignals,
    kill_feature_recommended,
    kill_market_recommended,
    kill_service_recommended,
)
from auto_client_acquisition.command_os.kill_protocol import kill_partner_recommended
from auto_client_acquisition.command_os.market_authority_score import (
    MarketAuthorityInputs,
    compute_market_authority_score,
)
from auto_client_acquisition.command_os.metrics_tree import (
    NORTH_STAR_METRIC,
    SUPPORTING_METRICS,
)
from auto_client_acquisition.command_os.proof_strength_score import (
    ProofPackUseTier,
    ProofStrengthInputs,
    compute_proof_strength_score,
    proof_pack_use_tier,
)
from auto_client_acquisition.command_os.red_team import (
    RedTeamVerdict,
    red_team_verdict,
)
from auto_client_acquisition.command_os.red_team_protocol import (
    ExpansionRedTeamVerdict,
    expansion_red_team_verdict,
)
from auto_client_acquisition.command_os.unit_maturity_score import (
    BusinessUnitMaturityBand,
    BusinessUnitMaturityInputs,
    business_unit_maturity_band,
    compute_business_unit_maturity_score,
)

__all__ = [
    "BOARD_MEMO_SECTION_TITLES",
    "DECISION_RIGHTS_ROWS",
    "NORTH_STAR_METRIC",
    "SUPPORTING_METRICS",
    "BusinessUnitMaturityBand",
    "BusinessUnitMaturityInputs",
    "DecisionRightRow",
    "ExpansionRedTeamVerdict",
    "GovernanceRiskBand",
    "GovernanceRiskInputs",
    "KillMarketSignals",
    "KillServiceSignals",
    "MarketAuthorityInputs",
    "OperatingCapabilityBand",
    "OperatingCapabilityInputs",
    "ProofPackUseTier",
    "ProofStrengthInputs",
    "RedTeamVerdict",
    "WorldClassAllocationBand",
    "WorldClassAllocationInputs",
    "business_unit_maturity_band",
    "compute_business_unit_maturity_score",
    "compute_governance_risk_index",
    "compute_market_authority_score",
    "compute_operating_capability_score",
    "compute_proof_strength_score",
    "compute_world_class_allocation_score",
    "decision_right_for_key",
    "expansion_red_team_verdict",
    "governance_risk_band",
    "kill_feature_recommended",
    "kill_market_recommended",
    "kill_partner_recommended",
    "kill_service_recommended",
    "meets_minimum_capital_creation",
    "operating_capability_band",
    "proof_pack_use_tier",
    "red_team_verdict",
    "world_class_allocation_band",
]
