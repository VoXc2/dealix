"""Client maturity OS — transformation ladder, scoring, offers, playbooks."""

from __future__ import annotations

from auto_client_acquisition.client_maturity_os.maturity_dashboard import (
    PLATFORM_PULL_SIGNALS,
    MaturityDashboardView,
    build_maturity_dashboard,
    derive_readiness_blockers,
)
from auto_client_acquisition.client_maturity_os.maturity_engine import (
    ClientMaturityInputs,
    MaturityEngineResult,
    maturity_engine_result,
)
from auto_client_acquisition.client_maturity_os.maturity_score import (
    MATURITY_LADDER_STATES,
    ClientMaturityDimensions,
    client_maturity_band,
    client_maturity_score,
)
from auto_client_acquisition.client_maturity_os.offer_matrix import (
    BLOCKED_OFFERS_BY_LEVEL,
    PRIMARY_OFFER_BY_LEVEL,
    blocked_offers_for_level,
    level1_first_track,
    level7_entry_gates_met,
    primary_offer_for_level,
    retainer_eligibility_met,
)
from auto_client_acquisition.client_maturity_os.progression_playbooks import (
    PROGRESSION_DELIVERABLES,
    progression_deliverables,
    transition_key,
)

__all__ = (
    "BLOCKED_OFFERS_BY_LEVEL",
    "MATURITY_LADDER_STATES",
    "PLATFORM_PULL_SIGNALS",
    "PRIMARY_OFFER_BY_LEVEL",
    "PROGRESSION_DELIVERABLES",
    "ClientMaturityDimensions",
    "ClientMaturityInputs",
    "MaturityDashboardView",
    "MaturityEngineResult",
    "blocked_offers_for_level",
    "build_maturity_dashboard",
    "client_maturity_band",
    "client_maturity_score",
    "derive_readiness_blockers",
    "level1_first_track",
    "level7_entry_gates_met",
    "maturity_engine_result",
    "primary_offer_for_level",
    "progression_deliverables",
    "retainer_eligibility_met",
    "transition_key",
)
