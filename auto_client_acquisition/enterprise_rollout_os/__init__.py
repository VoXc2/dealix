"""Dealix Enterprise Rollout OS — adoption gates + rollout stages."""

from __future__ import annotations

from auto_client_acquisition.enterprise_rollout_os.adoption_gates import (
    ADOPTION_GATES,
    AdoptionGate,
    AdoptionGateChecks,
    evaluate_adoption_gates,
)
from auto_client_acquisition.enterprise_rollout_os.rollout_stage import (
    ROLLOUT_STAGES,
    RolloutStage,
)

__all__ = [
    "ADOPTION_GATES",
    "AdoptionGate",
    "AdoptionGateChecks",
    "evaluate_adoption_gates",
    "ROLLOUT_STAGES",
    "RolloutStage",
]
