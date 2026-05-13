"""Dealix Evidence Control Plane OS."""

from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.evidence_coverage import (
    COVERAGE_THRESHOLDS,
    CoverageTier,
    EvidenceCoverageSnapshot,
    classify_evidence_coverage,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_gap_rules import (
    EvidenceGap,
    EvidenceGapDecision,
    evaluate_evidence_gap,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_maturity import (
    EVIDENCE_MATURITY_LEVELS,
    EvidenceMaturityLevel,
)

__all__ = [
    "COVERAGE_THRESHOLDS",
    "CoverageTier",
    "EvidenceCoverageSnapshot",
    "classify_evidence_coverage",
    "EvidenceGap",
    "EvidenceGapDecision",
    "evaluate_evidence_gap",
    "EVIDENCE_MATURITY_LEVELS",
    "EvidenceMaturityLevel",
]
