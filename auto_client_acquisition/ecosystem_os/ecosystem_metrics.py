"""Ecosystem headline metrics — partner, academy, benchmark, platform, venture."""

from __future__ import annotations

ECOSYSTEM_METRICS_SIGNALS: tuple[str, ...] = (
    "partner_leads",
    "partner_win_rate",
    "partner_qa_score",
    "partner_compliance_incidents",
    "partner_revenue",
    "academy_registrations",
    "academy_completion_rate",
    "academy_assessment_pass_rate",
    "certified_partners_from_academy",
    "course_to_lead_conversion",
    "benchmark_downloads",
    "benchmark_inbound_diagnostics",
    "benchmark_media_mentions",
    "benchmark_partner_usage",
    "benchmark_enterprise_inquiries",
    "workspace_active_clients",
    "proof_timeline_views",
    "approval_completion_rate",
    "monthly_active_stakeholders",
    "audit_export_requests",
    "venture_unit_revenue",
    "venture_retainers",
    "venture_proof_library_size",
    "venture_module_usage",
    "venture_owner_readiness",
    "venture_margin",
)

ECOSYSTEM_LAUNCH_STEPS: tuple[str, ...] = (
    "productized_services",
    "proof_pack_standard",
    "client_workspace_mvp",
    "partner_referral_program",
    "dealix_method_public_page",
    "first_benchmark_report",
    "academy_pilot_workshop",
    "certified_partner_track",
    "partner_portal",
    "enterprise_ai_control_plane",
    "venture_candidates",
)


def ecosystem_metrics_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not ECOSYSTEM_METRICS_SIGNALS:
        return 0
    n = sum(1 for s in ECOSYSTEM_METRICS_SIGNALS if s in signals_tracked)
    return (n * 100) // len(ECOSYSTEM_METRICS_SIGNALS)


def ecosystem_launch_step_index(step: str) -> int | None:
    try:
        return ECOSYSTEM_LAUNCH_STEPS.index(step)
    except ValueError:
        return None
