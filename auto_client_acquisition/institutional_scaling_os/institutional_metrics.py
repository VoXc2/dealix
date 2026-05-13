"""Institutional Metrics — company / trust / market with scaling gate."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InstitutionalCompanyMetrics:
    mrr: float
    gross_margin: float
    proof_packs_delivered: int
    proof_to_retainer_conversion: float
    capital_assets_created: int
    governance_incidents: int
    ai_run_audit_coverage: float
    client_health: float
    business_unit_maturity: float


@dataclass(frozen=True)
class InstitutionalTrustMetrics:
    pct_sources_with_passport: float
    pct_outputs_with_governance: float
    pct_ai_runs_logged: float
    pct_external_actions_approved: float
    pii_flags_detected: int
    unsafe_actions_blocked: int


@dataclass(frozen=True)
class InstitutionalMarketMetrics:
    inbound_diagnostics: int
    partner_referrals: int
    proof_pack_requests: int
    capability_score_mentions: int
    benchmark_downloads: int
    academy_waitlist: int
    enterprise_trust_inquiries: int


def is_scaling_safe(
    *,
    trust: InstitutionalTrustMetrics,
    company: InstitutionalCompanyMetrics,
) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if trust.pct_ai_runs_logged < 1.0:
        reasons.append("ai_run_logging_below_100")
    if trust.pct_outputs_with_governance < 1.0:
        reasons.append("outputs_without_governance")
    if trust.pct_external_actions_approved < 1.0:
        reasons.append("external_actions_without_approval")
    if company.gross_margin < 0.5:
        reasons.append("margin_unhealthy")
    if company.capital_assets_created < company.proof_packs_delivered:
        reasons.append("less_capital_than_projects_agency_risk")
    return (not reasons, tuple(reasons))
