"""Enterprise maturity OS — measures Dealix's own platform capability maturity.

Answers the doctrine question: not "how many features?" but "can Dealix
reliably and measurably operate an enterprise via AI-first workflows?"

Three pillars: 5 maturity stages, 10 enterprise-readiness gates,
5 verification systems. Read-only assessment — no live sends/charges/agents.
"""

from __future__ import annotations

from auto_client_acquisition.enterprise_maturity_os.maturity_assessment import (
    MaturityAssessment,
    assess_current_platform,
    assess_platform_maturity,
)
from auto_client_acquisition.enterprise_maturity_os.readiness_gates import (
    GATE_CRITERIA,
    GATE_IDS,
    GateScore,
    gate_criteria,
    readiness_band,
    score_gate,
)
from auto_client_acquisition.enterprise_maturity_os.stages import (
    MAX_LEVEL,
    MIN_LEVEL,
    STAGES,
    MaturityStage,
    next_stage,
    stage_by_id,
    stage_for_level,
)
from auto_client_acquisition.enterprise_maturity_os.verification_systems import (
    VERIFICATION_SYSTEM_IDS,
    VERIFICATION_SYSTEMS,
    VerificationSystem,
    verification_coverage,
    verification_system,
)

__all__ = [
    "GATE_CRITERIA",
    "GATE_IDS",
    "MAX_LEVEL",
    "MIN_LEVEL",
    "STAGES",
    "VERIFICATION_SYSTEMS",
    "VERIFICATION_SYSTEM_IDS",
    "GateScore",
    "MaturityAssessment",
    "MaturityStage",
    "VerificationSystem",
    "assess_current_platform",
    "assess_platform_maturity",
    "gate_criteria",
    "next_stage",
    "readiness_band",
    "score_gate",
    "stage_by_id",
    "stage_for_level",
    "verification_coverage",
    "verification_system",
]
