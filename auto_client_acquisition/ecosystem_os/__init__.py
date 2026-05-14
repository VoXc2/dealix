"""Ecosystem & platform expansion — partners, academy, benchmarks, ventures."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os.academy_portal import (
    ACADEMY_PORTAL_SIGNALS,
    academy_portal_coverage_score,
)
from auto_client_acquisition.ecosystem_os.benchmark_engine import (
    BENCHMARK_ARTIFACT_SLUGS,
    BENCHMARK_PORTAL_SIGNALS,
    BENCHMARK_SAFE_SOURCE_KINDS,
    benchmark_methodology_ok,
    benchmark_portal_coverage_score,
)
from auto_client_acquisition.ecosystem_os.certification import (
    CERTIFICATION_LEVELS,
    certification_level_valid,
    certification_slug_for_level,
)
from auto_client_acquisition.ecosystem_os.ecosystem_metrics import (
    ECOSYSTEM_LAUNCH_STEPS,
    ECOSYSTEM_METRICS_SIGNALS,
    ecosystem_launch_step_index,
    ecosystem_metrics_coverage_score,
)
from auto_client_acquisition.ecosystem_os.partner_portal import (
    PARTNER_PORTAL_SIGNALS,
    partner_portal_coverage_score,
)
from auto_client_acquisition.ecosystem_os.partner_score import (
    PARTNER_GATE_CRITERIA,
    PartnerQualityDimensions,
    partner_gate_passes,
    partner_quality_band,
    partner_quality_score,
)
from auto_client_acquisition.ecosystem_os.venture_gate import (
    VentureGateInput,
    venture_gate_passes,
)

__all__ = (
    "ACADEMY_PORTAL_SIGNALS",
    "BENCHMARK_ARTIFACT_SLUGS",
    "BENCHMARK_PORTAL_SIGNALS",
    "BENCHMARK_SAFE_SOURCE_KINDS",
    "CERTIFICATION_LEVELS",
    "ECOSYSTEM_LAUNCH_STEPS",
    "ECOSYSTEM_METRICS_SIGNALS",
    "PARTNER_GATE_CRITERIA",
    "PARTNER_PORTAL_SIGNALS",
    "PartnerQualityDimensions",
    "VentureGateInput",
    "academy_portal_coverage_score",
    "benchmark_methodology_ok",
    "benchmark_portal_coverage_score",
    "certification_level_valid",
    "certification_slug_for_level",
    "ecosystem_launch_step_index",
    "ecosystem_metrics_coverage_score",
    "partner_gate_passes",
    "partner_portal_coverage_score",
    "partner_quality_band",
    "partner_quality_score",
    "venture_gate_passes",
)
