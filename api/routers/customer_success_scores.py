"""Wave 13 Phase 8 — Customer Success Intelligence (5 scores aggregator).

- GET /api/v1/customer-success/{handle}/all-scores  → 5-score response
- GET /api/v1/customer-success/status              → layer health

The 5 scores:
  1. Health Score              (existing customer_success/health_score.py)
  2. Comfort Score             (existing customer_readiness/scores.py)
  3. Expansion Readiness Score (existing customer_readiness/scores.py)
  4. Churn Risk Score          (NEW Wave 13 customer_success/churn_risk.py)
  5. Proof Maturity Score      (NEW Wave 13 customer_success/proof_maturity.py)

Hard rules (Article 8): every score `is_estimate=True`; aggregator
returns the union with all 5 estimate flags surfaced.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from auto_client_acquisition.customer_success.churn_risk import compute_churn_risk
from auto_client_acquisition.customer_success.proof_maturity import (
    compute_proof_maturity,
)

router = APIRouter(prefix="/api/v1/customer-success", tags=["Customer Success"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "every_score_is_estimate": True,
}


@router.get("/status")
async def customer_success_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "wave": "wave13_phase_8_customer_success_intelligence",
        "scores_available": [
            "health_score",
            "comfort_score",
            "expansion_readiness",
            "churn_risk",
            "proof_maturity",
        ],
        "hard_gates": _HARD_GATES,
    }


@router.get("/{handle}/all-scores")
async def all_scores(
    handle: str,
    # Health Score inputs (optional — defaults produce neutral scores)
    logins_last_30d: int = Query(0, ge=0),
    drafts_approved_last_30d: int = Query(0, ge=0),
    replies_acted_on_last_30d: int = Query(0, ge=0),
    demos_booked_last_30d: int = Query(0, ge=0),
    deals_stage_progressed_last_30d: int = Query(0, ge=0),
    paid_customers_last_30d: int = Query(0, ge=0),
    pipeline_value_sar: float = Query(0.0, ge=0.0),
    # Comfort + Expansion (existing)
    has_status_timeline: bool = False,
    has_next_action: bool = False,
    pending_approvals: int = Query(0, ge=0),
    open_support_tickets: int = Query(0, ge=0),
    proof_events_count: int = Query(0, ge=0),
    max_proof_level: int = Query(0, ge=0, le=5),
    payment_ok: bool = False,
    delivery_sessions_active: int = Query(0, ge=0),
    avg_response_hours: float = Query(48.0, ge=0.0),
    # Churn Risk
    engagement_drop_pct: float = Query(0.0, ge=0.0, le=100.0),
    support_escalations_last_30d: int = Query(0, ge=0),
    payment_late_count: int = Query(0, ge=0),
    nps_below_7: bool = False,
    decision_maker_left: bool = False,
    # Proof Maturity
    publishable_count: int = Query(0, ge=0),
    consent_signed_count: int = Query(0, ge=0),
) -> dict[str, Any]:
    """Aggregate all 5 customer-success scores for one customer.

    Article 8: every score returns `is_estimate=True`. Inputs are
    query params (so callers can pass aggregates from their CRM).
    """
    # ── Health (defer import to avoid api/security pyo3 cascade in tests) ──
    from auto_client_acquisition.customer_success.health_score import (
        compute_health_score,
    )
    health = compute_health_score(
        customer_id=handle,
        logins_last_30d=logins_last_30d,
        drafts_approved_last_30d=drafts_approved_last_30d,
        replies_acted_on_last_30d=replies_acted_on_last_30d,
        demos_booked_last_30d=demos_booked_last_30d,
        deals_stage_progressed_last_30d=deals_stage_progressed_last_30d,
        paid_customers_last_30d=paid_customers_last_30d,
        pipeline_value_sar=pipeline_value_sar,
    )

    # ── Comfort + Expansion ────────────────────────────────────────────
    from auto_client_acquisition.customer_readiness.scores import (
        compute_comfort_and_expansion,
    )
    comfort_expansion = compute_comfort_and_expansion(
        has_status_timeline=has_status_timeline,
        has_next_action=has_next_action,
        pending_approvals=pending_approvals,
        open_support_tickets=open_support_tickets,
        proof_events_count=proof_events_count,
        max_proof_level=max_proof_level,
        payment_ok=payment_ok,
        delivery_sessions_active=delivery_sessions_active,
        avg_response_hours=avg_response_hours,
    )

    # ── Churn Risk (Wave 13) ───────────────────────────────────────────
    churn = compute_churn_risk(
        customer_id=handle,
        engagement_drop_pct=engagement_drop_pct,
        support_escalations_last_30d=support_escalations_last_30d,
        payment_late_count=payment_late_count,
        nps_below_7=nps_below_7,
        decision_maker_left=decision_maker_left,
    )

    # ── Proof Maturity (Wave 13) ───────────────────────────────────────
    proof = compute_proof_maturity(
        customer_id=handle,
        proof_event_count=proof_events_count,
        max_evidence_level=max_proof_level,
        publishable_count=publishable_count,
        consent_signed_count=consent_signed_count,
    )

    return {
        "customer_handle": handle,
        "scores": {
            "health_score": health.to_dict(),
            "comfort_score": comfort_expansion.get("comfort_score"),
            "expansion_readiness": comfort_expansion.get("expansion_readiness"),
            "churn_risk": churn.to_dict(),
            "proof_maturity": proof.to_dict(),
        },
        "all_is_estimate": True,
        "hard_gates": _HARD_GATES,
    }


# ── Wave 2: Adoption Score endpoint ──────────────────────────────────


@router.get("/{handle}/adoption-score")
async def adoption_score(
    handle: str,
    channels_enabled: int = Query(0, ge=0),
    integrations_connected: int = Query(0, ge=0),
    sectors_targeted: int = Query(0, ge=0),
    total_drafts_lifetime: int = Query(0, ge=0),
    logins_last_30d: int = Query(0, ge=0),
    drafts_approved_last_30d: int = Query(0, ge=0),
    replies_acted_on_last_30d: int = Query(0, ge=0),
    previous_score: float | None = Query(None),
    proof_score: float = Query(0.0, ge=0.0, le=100.0),
    workflow_owner_present: bool = Query(False),
    governance_risk_controlled: bool = Query(True),
) -> dict[str, Any]:
    """Wave 2 Adoption Score endpoint — wraps adoption_os.compute() and
    pairs it with a RetainerReadiness gate. Estimate per Article 8."""
    from auto_client_acquisition.adoption_os.adoption_score import compute as compute_adoption
    from auto_client_acquisition.adoption_os.retainer_readiness import evaluate as evaluate_retainer

    score = compute_adoption(
        customer_id=handle,
        channels_enabled=channels_enabled,
        integrations_connected=integrations_connected,
        sectors_targeted=sectors_targeted,
        total_drafts_lifetime=total_drafts_lifetime,
        logins_last_30d=logins_last_30d,
        drafts_approved_last_30d=drafts_approved_last_30d,
        replies_acted_on_last_30d=replies_acted_on_last_30d,
        previous_score=previous_score,
    )
    retainer = evaluate_retainer(
        customer_id=handle,
        adoption_score=score.score,
        proof_score=proof_score,
        workflow_owner_present=workflow_owner_present,
        governance_risk_controlled=governance_risk_controlled,
    )
    return {
        "customer_handle": handle,
        "adoption_score": score.to_dict(),
        "retainer_readiness": retainer.to_dict(),
        "is_estimate": True,
        "governance_decision": score.governance_decision,
    }
