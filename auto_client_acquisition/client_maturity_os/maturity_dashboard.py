"""Maturity dashboard snapshot — single client view."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.client_maturity_os.maturity_engine import (
    ClientMaturityInputs,
    maturity_engine_result,
)

PLATFORM_PULL_SIGNALS: tuple[str, ...] = (
    "multiple_users_need_access",
    "approvals_repeat",
    "proof_reports_repeat",
    "executive_dashboard_request",
    "audit_requested",
)


def derive_readiness_blockers(inp: ClientMaturityInputs) -> tuple[str, ...]:
    """Heuristic blockers from dimension scores + ownership + shadow AI."""
    d = inp.dimensions
    threshold = 55
    out: list[str] = []
    checks: tuple[tuple[str, int], ...] = (
        ("leadership_alignment_low", d.leadership_alignment),
        ("data_readiness_low", d.data_readiness),
        ("workflow_ownership_low", d.workflow_ownership),
        ("governance_coverage_low", d.governance_coverage),
        ("proof_discipline_low", d.proof_discipline),
        ("adoption_low", d.adoption),
        ("operating_cadence_low", d.operating_cadence),
    )
    for slug, val in checks:
        if val < threshold:
            out.append(slug)
    if inp.shadow_ai_uncontrolled:
        out.append("shadow_ai_uncontrolled")
    if not inp.workflow_owner_exists:
        out.append("workflow_owner_missing")
    return tuple(out)


@dataclass(frozen=True, slots=True)
class MaturityDashboardView:
    client_id: str
    current_level: int
    target_level: int
    maturity_score: int
    maturity_band: str
    proof_score: int
    adoption_score: int
    governance_score: int
    readiness_blockers: tuple[str, ...]
    recommended_next_offer: str
    blocked_offers: tuple[str, ...]
    reason: str
    platform_pull_signals: tuple[str, ...]


def build_maturity_dashboard(
    client_id: str,
    inputs: ClientMaturityInputs,
    *,
    target_level: int | None = None,
    platform_pull_signals: tuple[str, ...] = (),
) -> MaturityDashboardView:
    result = maturity_engine_result(client_id, inputs)
    tgt = target_level if target_level is not None else min(7, result.maturity_level + 1)
    if tgt < result.maturity_level:
        tgt = result.maturity_level
    if tgt > 7:
        tgt = 7
    return MaturityDashboardView(
        client_id=result.client_id,
        current_level=result.maturity_level,
        target_level=tgt,
        maturity_score=result.maturity_score,
        maturity_band=result.maturity_band,
        proof_score=inputs.proof_score,
        adoption_score=inputs.adoption_score,
        governance_score=inputs.dimensions.governance_coverage,
        readiness_blockers=derive_readiness_blockers(inputs),
        recommended_next_offer=result.recommended_next_offer,
        blocked_offers=result.blocked_offers,
        reason=result.reason,
        platform_pull_signals=platform_pull_signals,
    )
