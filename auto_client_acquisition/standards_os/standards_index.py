"""D-GAOS — the nine sub-standards index."""

from __future__ import annotations

from enum import Enum


class SubStandard(str, Enum):
    CAPABILITY_DIAGNOSTIC = "capability_diagnostic_standard"
    DATA_READINESS = "data_readiness_standard"
    SOURCE_PASSPORT = "source_passport_standard"
    RUNTIME_GOVERNANCE = "runtime_governance_standard"
    AGENT_CONTROL = "ai_agent_control_standard"
    OUTPUT_QA = "ai_output_qa_standard"
    PROOF_PACK = "proof_pack_standard"
    OPERATING_CADENCE = "operating_cadence_standard"
    CAPITAL_CREATION = "capital_creation_standard"


DEALIX_SUB_STANDARDS: tuple[SubStandard, ...] = tuple(SubStandard)
