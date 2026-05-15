"""Enterprise Evidence Control Plane — contracts for auditable AI operations."""

from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.accountability_map import (
    AccountabilityRecord,
    accountability_valid_for_execution,
    external_action_accountable,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_api import (
    EVIDENCE_API_ROUTES,
    evidence_route_registered,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_dashboard import (
    evidence_coverage_band,
    evidence_coverage_percent,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_gap_detector import (
    EvidencePresence,
    GapSeverity,
    detect_evidence_gaps,
    gap_severity,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import (
    MINI_CHAIN_KEYS,
    mini_evidence_chain_complete,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
    EvidenceObject,
    EvidenceType,
    evidence_object_valid,
    is_critical_evidence_type,
)
from auto_client_acquisition.evidence_control_plane_os.proof_linker import (
    PROOF_PACK_V3_SECTIONS,
    proof_pack_v3_sections_complete,
)

__all__ = (
    "EVIDENCE_API_ROUTES",
    "MINI_CHAIN_KEYS",
    "PROOF_PACK_V3_SECTIONS",
    "AccountabilityRecord",
    "EvidenceObject",
    "EvidencePresence",
    "EvidenceType",
    "GapSeverity",
    "accountability_valid_for_execution",
    "detect_evidence_gaps",
    "evidence_coverage_band",
    "evidence_coverage_percent",
    "evidence_object_valid",
    "evidence_route_registered",
    "external_action_accountable",
    "gap_severity",
    "is_critical_evidence_type",
    "mini_evidence_chain_complete",
    "proof_pack_v3_sections_complete",
)
