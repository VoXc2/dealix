"""Dealix Ecosystem OS — partners, certification, benchmarks, portals, venture gate."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os.academy_portal import (
    ACADEMY_PORTAL_SECTIONS,
    ACADEMY_TRACKS,
    AcademyPortalSection,
    AcademyTrack,
)
from auto_client_acquisition.ecosystem_os.benchmark_engine import (
    BenchmarkReport,
)
from auto_client_acquisition.ecosystem_os.certification import (
    CERTIFICATION_LEVELS,
    CertificationLevel,
)
from auto_client_acquisition.ecosystem_os.ecosystem_metrics import (
    AcademyMetrics,
    BenchmarkMetrics,
    EcosystemMetricsSnapshot,
    PartnerMetrics,
    PlatformMetrics,
)
from auto_client_acquisition.ecosystem_os.partner_portal import (
    PARTNER_PORTAL_SECTIONS,
    PartnerPortalSection,
)
from auto_client_acquisition.ecosystem_os.partner_score import (
    PARTNER_SCORE_WEIGHTS,
    PartnerLadder,
    PartnerScoreComponents,
    classify_partner_ladder,
    compute_partner_score,
)
from auto_client_acquisition.ecosystem_os.venture_gate import (
    VentureGateV2,
    evaluate_venture_gate_v2,
)

__all__ = [
    "ACADEMY_PORTAL_SECTIONS",
    "ACADEMY_TRACKS",
    "AcademyPortalSection",
    "AcademyTrack",
    "BenchmarkReport",
    "CERTIFICATION_LEVELS",
    "CertificationLevel",
    "AcademyMetrics",
    "BenchmarkMetrics",
    "EcosystemMetricsSnapshot",
    "PartnerMetrics",
    "PlatformMetrics",
    "PARTNER_PORTAL_SECTIONS",
    "PartnerPortalSection",
    "PARTNER_SCORE_WEIGHTS",
    "PartnerLadder",
    "PartnerScoreComponents",
    "classify_partner_ladder",
    "compute_partner_score",
    "VentureGateV2",
    "evaluate_venture_gate_v2",
]
