"""Dealix Self-Growth OS — safe, evidence-based growth primitives.

This package is intentionally small. Each module wraps EXISTING
infrastructure rather than inventing new logic:

  - ``schemas``               — typed records used across the package
  - ``service_activation_matrix`` — wraps docs/registry/SERVICE_READINESS_MATRIX.yaml
  - ``seo_technical_auditor`` — wraps scripts/seo_audit.py
  - ``safe_publishing_gate``  — wraps the forbidden-claims regex
  - ``tool_registry``         — introspects which optional packages are available
  - ``evidence_collector``    — small structured-event recorder

Modules referenced in earlier prompts but **not implemented yet**
(search_radar, content_brief_generator, content_draft_engine,
distribution_planner, partner_distribution_radar, daily_growth_loop,
weekly_growth_scorecard, self_improvement_loop, geo_aio_radar,
landing_page_opportunity_engine, internal_linking_planner,
community_signal_radar, social_draft_engine, proof_snippet_engine)
are deferred per ``docs/SELF_GROWTH_OS_PACKAGE.md`` until they have
real callers, real input data, and real tests. No stubs.

Hard guarantees of every module here:

  - draft-only by default; no external send / charge / scrape
  - approval_required for any external-action recommendation
  - Arabic-primary, English-secondary text where applicable
  - never claim guaranteed revenue / ranking / proof
"""
from __future__ import annotations

from auto_client_acquisition.self_growth_os.schemas import (
    ApprovalStatus,
    EvidenceRecord,
    Language,
    PublishingDecision,
    RiskLevel,
    SafePublishingResult,
    ServiceActivationCheck,
    ServiceBundle,
    ToolCapability,
)

__all__ = [
    "ApprovalStatus",
    "EvidenceRecord",
    "Language",
    "PublishingDecision",
    "RiskLevel",
    "SafePublishingResult",
    "ServiceActivationCheck",
    "ServiceBundle",
    "ToolCapability",
]
