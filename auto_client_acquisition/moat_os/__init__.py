"""Strategic Operating Moat — composite defensive system."""

from __future__ import annotations

from auto_client_acquisition.moat_os.anti_moat_risks import (
    AntiMoatHit,
    AntiMoatRisk,
    detect_anti_moat_risks,
)
from auto_client_acquisition.moat_os.governance_to_moat import (
    GOVERNANCE_TO_MOAT_STAGES,
    governance_moat_loop_complete,
    governance_to_moat_progress,
    risk_to_seed_artifacts,
)
from auto_client_acquisition.moat_os.market_language_score import (
    moat_market_language_adoption_score,
)
from auto_client_acquisition.moat_os.moat_score import (
    MoatScoreDimensions,
    MoatTier,
    moat_compound_index,
    moat_tier,
    weighted_moat_score,
)
from auto_client_acquisition.moat_os.partner_moat_score import (
    PartnerMoatSignals,
    partner_moat_score,
)
from auto_client_acquisition.moat_os.proof_to_moat import (
    PROOF_TO_MOAT_STAGES,
    proof_moat_loop_complete,
    proof_to_moat_progress,
)

__all__ = [
    "GOVERNANCE_TO_MOAT_STAGES",
    "PROOF_TO_MOAT_STAGES",
    "AntiMoatHit",
    "AntiMoatRisk",
    "MoatScoreDimensions",
    "MoatTier",
    "PartnerMoatSignals",
    "detect_anti_moat_risks",
    "governance_moat_loop_complete",
    "governance_to_moat_progress",
    "moat_compound_index",
    "moat_market_language_adoption_score",
    "moat_tier",
    "partner_moat_score",
    "proof_moat_loop_complete",
    "proof_to_moat_progress",
    "risk_to_seed_artifacts",
    "weighted_moat_score",
]
