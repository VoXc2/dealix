"""Partner Gate — re-exports of partner covenant + scoring."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os.partner_score import (
    PartnerLadder,
    PartnerScoreComponents,
    classify_partner_ladder,
    compute_partner_score,
)
from auto_client_acquisition.operating_manual_os.partner_covenant import (
    CovenantClause,
    CovenantStatus,
    PartnerCovenant,
    evaluate_partner_covenant,
)

__all__ = [
    "PartnerLadder",
    "PartnerScoreComponents",
    "classify_partner_ladder",
    "compute_partner_score",
    "CovenantClause",
    "CovenantStatus",
    "PartnerCovenant",
    "evaluate_partner_covenant",
]
