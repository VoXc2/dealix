"""Canonical Evidence Control Plane — Wave 3 finish (14E).

Composes auditability_os + proof_ledger + value_os + capital_os +
friction_log into one typed graph + gap detector + compliance index.
"""
from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
    EvidenceObject,
    create_evidence,
    list_evidence,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import (
    EvidenceControlGraph,
    build_control_graph,
)
from auto_client_acquisition.evidence_control_plane_os.gap_detector import (
    EvidenceGap,
    find_gaps,
)
from auto_client_acquisition.evidence_control_plane_os.compliance_index import (
    ComplianceIndex,
    build_compliance_index,
)

__all__ = [
    "ComplianceIndex",
    "EvidenceControlGraph",
    "EvidenceGap",
    "EvidenceObject",
    "build_compliance_index",
    "build_control_graph",
    "create_evidence",
    "find_gaps",
    "list_evidence",
]
