"""Dealix Category Standard & Certification — D-GAOS registry."""

from __future__ import annotations

from auto_client_acquisition.standards_os.agent_control_standard import (
    MVP_AUTONOMY_LEVEL_MAX,
    agent_autonomy_allowed_in_mvp,
    agent_autonomy_level_valid,
    ai_output_qa_band,
)
from auto_client_acquisition.standards_os.capability_standard import (
    CAPABILITY_DOMAINS,
    CAPABILITY_LEVEL_MAX,
    capability_level_valid,
)
from auto_client_acquisition.standards_os.certification import (
    CERTIFICATION_EXAM_COMPONENTS,
    CERTIFICATION_LEVELS,
    capital_minimum_bundle_ok,
    certification_exam_components_complete,
    certification_level_valid,
    certification_slug_for_level,
)
from auto_client_acquisition.standards_os.data_readiness_standard import (
    data_readiness_score_band,
)
from auto_client_acquisition.standards_os.governance_standard import (
    RuntimeGovernanceDecision,
    runtime_governance_decision_valid,
)
from auto_client_acquisition.standards_os.partner_gate import (
    PARTNER_COVENANT_RULES,
    partner_certification_gate,
)
from auto_client_acquisition.standards_os.proof_pack_standard import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.standards_os.source_passport_standard import (
    SOURCE_PASSPORT_REQUIRED_KEYS,
    source_passport_keys_present,
)

D_GAOS_STANDARD_IDS: tuple[str, ...] = (
    "capability_diagnostic",
    "data_readiness",
    "source_passport",
    "runtime_governance",
    "ai_agent_control",
    "ai_output_qa",
    "proof_pack",
    "operating_cadence",
    "capital_creation",
)

__all__ = (
    "CAPABILITY_DOMAINS",
    "CAPABILITY_LEVEL_MAX",
    "CERTIFICATION_EXAM_COMPONENTS",
    "CERTIFICATION_LEVELS",
    "D_GAOS_STANDARD_IDS",
    "MVP_AUTONOMY_LEVEL_MAX",
    "PARTNER_COVENANT_RULES",
    "PROOF_PACK_V2_SECTIONS",
    "RuntimeGovernanceDecision",
    "SOURCE_PASSPORT_REQUIRED_KEYS",
    "agent_autonomy_allowed_in_mvp",
    "agent_autonomy_level_valid",
    "ai_output_qa_band",
    "capital_minimum_bundle_ok",
    "capability_level_valid",
    "certification_exam_components_complete",
    "certification_level_valid",
    "certification_slug_for_level",
    "data_readiness_score_band",
    "partner_certification_gate",
    "proof_pack_v2_sections_complete",
    "runtime_governance_decision_valid",
    "source_passport_keys_present",
)
