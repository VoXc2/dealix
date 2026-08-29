"""Governed Revenue Lab orchestration built on Dealix's existing contracts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.proof_ledger.schemas import ProofEvent, ProofEventType
from dealix.commercial.roi_calculator import ROIInput, estimate_roi
from dealix.commercial_universe import (
    CommercialAccount,
    DepartmentObjective,
    PermissionState,
    RelationshipType,
    create_approval_envelope,
    score_account,
)
from dealix.commercial_universe_approval import to_approval_request
from dealix.company_os.negotiation_engine import (
    NegotiationContext,
    build_negotiation_plan,
)

from .models import (
    CompanySignal,
    DeliveryPlan,
    LearningRecommendation,
    OpportunityNode,
    OutcomeEvent,
    ProposalDraft,
    RevenueLabBundle,
    SalesStrategy,
)

_CONTACTABLE = {"warm", "inbound", "referral", "opted_in", "approved"}
_RESTRICTED_COMMITMENTS = (
    "contract_signature",
    "delivery_date_without_capacity_check",
    "discount_approval",
    "final_price",
    "guaranteed_revenue",
    "guaranteed_roi",
    "legal_terms_acceptance",
    "payment_commitment",
    "production_change",
    "refund_commitment",
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _source_backed(signal: CompanySignal) -> bool:
    return (
        bool(signal.evidence)
        and not signal.demo
        and all(item.quality != "demo" for item in signal.evidence)
    )


def _evidence_status(signal: CompanySignal) -> str:
    if signal.demo or any(item.quality == "demo" for item in signal.evidence):
        return "demo_only"
    if not signal.evidence:
        return "blocked_no_source"
    return "source_backed"


def _roi(signal: CompanySignal) -> dict[str, Any]:
    required = {
        "manual_hours_per_week",
        "hourly_cost_sar",
        "lost_leads_per_month",
        "avg_deal_value_sar",
        "recovered_conversion_pct",
        "setup_cost_sar",
        "monthly_cost_sar",
    }
    if not required.issubset(signal.known_metrics):
        return {
            "status": "pending_client_baseline",
            "is_estimate": True,
            "missing_inputs": sorted(required - set(signal.known_metrics)),
            "disclaimer": "No ROI figure is produced until client-sourced baselines are recorded.",
        }
    estimate = estimate_roi(
        ROIInput(
            company_name=signal.company_name, **{key: signal.known_metrics[key] for key in required}
        )
    )
    return {
        "status": "scenario_estimate",
        "is_estimate": True,
        "gross_annual_value_sar_min": estimate.gross_annual_value_sar_min,
        "gross_annual_value_sar_max": estimate.gross_annual_value_sar_max,
        "net_annual_value_sar_min": estimate.net_annual_value_sar_min,
        "net_annual_value_sar_max": estimate.net_annual_value_sar_max,
        "disclaimer": estimate.disclaimer,
    }


def _learning_recommendation(event: OutcomeEvent) -> str:
    outcome = event.outcome.casefold()
    if outcome in {"rejected", "not_interested"}:
        return "Review ICP, pain hypothesis, and offer fit; propose one controlled wording or segment experiment."
    if outcome in {"no_reply", "stalled"}:
        return "Review permission, channel, timing, and first-line relevance before proposing a limited follow-up experiment."
    if outcome in {"meeting_booked", "proposal_requested", "payment_confirmed"}:
        return "Preserve the evidence-backed pattern as a candidate playbook; require repeated outcomes before changing weights."
    return "Classify the outcome with a human reviewer before proposing a model or scoring change."


class RevenueLabEngine:
    """Produce draft-only commercial bundles from traceable signals."""

    def run(
        self,
        signals: Iterable[CompanySignal],
        *,
        outcomes: Iterable[OutcomeEvent] = (),
    ) -> RevenueLabBundle:
        signal_list = list(signals)
        outcome_list = list(outcomes)
        stable_input = {
            "signals": [
                asdict(item)
                for item in sorted(signal_list, key=lambda signal: signal.account_id)
            ],
            "outcomes": [
                asdict(item)
                for item in sorted(
                    outcome_list,
                    key=lambda outcome: (outcome.account_id, outcome.outcome, outcome.source_ref),
                )
            ],
        }
        run_seed = json.dumps(stable_input, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        run_id = f"rlab_{hashlib.sha256(run_seed.encode()).hexdigest()[:12]}"

        opportunities: list[OpportunityNode] = []
        strategies: list[SalesStrategy] = []
        proposals: list[ProposalDraft] = []
        delivery_plans: list[DeliveryPlan] = []
        approvals: list[dict[str, Any]] = []
        proof_events: list[dict[str, Any]] = []
        blockers: list[str] = []

        for signal in signal_list:
            status = _evidence_status(signal)
            source_backed = _source_backed(signal)
            effective_permission = signal.permission if source_backed else "research_only"
            account = CommercialAccount(
                tenant_id=signal.tenant_id,
                account_id=signal.account_id,
                company_name=signal.company_name,
                department=DepartmentObjective(signal.department),
                relationship=RelationshipType(signal.relationship),
                permission=PermissionState(effective_permission),
                strategic_fit=signal.strategic_fit,
                urgency=signal.urgency,
                value_exchange=signal.value_exchange,
                source_ref=(
                    signal.evidence[0].source_ref
                    if signal.evidence
                    else f"missing:{signal.account_id}"
                ),
            )
            base_score = score_account(account)
            evidence_adjustment = 10 if source_backed else -25
            priority_score = max(0, min(100, base_score + evidence_adjustment))
            contactable = source_backed and signal.permission in _CONTACTABLE
            stage = "approval_queue" if contactable else "research"
            next_action = "prepare_diagnostic" if contactable else "validate_sources_and_permission"

            opportunities.append(
                OpportunityNode(
                    account_id=signal.account_id,
                    company_name=signal.company_name,
                    sector=signal.sector,
                    company_size=signal.company_size,
                    decision_maker_role=signal.decision_maker_role,
                    pain_hypotheses=signal.pain_hypotheses,
                    unknowns=signal.unknowns,
                    offer_match=signal.offer_match,
                    why_now=signal.why_now,
                    priority_score=priority_score,
                    evidence_status=status,
                    evidence_refs=tuple(item.source_ref for item in signal.evidence),
                    stage=stage,
                    next_action=next_action,
                )
            )

            objections = (
                "We already have a CRM or ERP.",
                "The problem may be process or people, not software.",
                "Show evidence before a larger commitment.",
                "How is company data protected?",
                "Why is this the right priority now?",
            )
            negotiation = build_negotiation_plan(
                NegotiationContext(
                    account_name=signal.company_name,
                    offer_id=signal.offer_match,
                    customer_problem=signal.pain_hypotheses[0],
                    known_objections=objections,
                    list_price_sar=signal.known_metrics.get("approved_list_price_sar"),
                    approved_floor_sar=signal.known_metrics.get("approved_floor_sar"),
                    evidence_refs=tuple(item.source_ref for item in signal.evidence),
                )
            )

            strategies.append(
                SalesStrategy(
                    account_id=signal.account_id,
                    objective=f"Validate the pain and earn permission for {signal.offer_match}.",
                    positioning=(
                        "AI Business Operating System that works above existing systems and produces "
                        "reviewable actions, approvals, and evidence."
                    ),
                    expected_objections=objections,
                    response_principles=(
                        "Separate sourced facts, hypotheses, and unknowns.",
                        "After qualified discovery, prepare a customer-specific 30-day pilot rather than a guarantee or fixed public offer.",
                        "Do not replace the customer's current system by default.",
                        "Escalate pricing, legal, privacy, and production commitments.",
                    ),
                    negotiation_give_get=tuple(
                        f"Give: {item['give']} | Get: {item['get']} | "
                        f"Approval: {item['approval_required']}"
                        for item in negotiation.concession_ladder
                    ),
                    negotiation_missing_inputs=negotiation.missing_inputs,
                    forbidden_commitments=_RESTRICTED_COMMITMENTS,
                )
            )

            proposals.append(
                ProposalDraft(
                    account_id=signal.account_id,
                    offer=signal.offer_match,
                    problem_statement=(f"Hypothesis for validation: {signal.pain_hypotheses[0]}"),
                    scope=(
                        "Confirm the baseline and decision owner.",
                        "Connect one bounded workflow without replacing the current system.",
                        "Run the workflow with human approvals and daily reporting.",
                        "Produce a before/after proof pack from client-sourced actuals.",
                    ),
                    timeline_days=30,
                    success_metrics=(
                        "baseline captured from an attributable source",
                        "approved actions completed",
                        "cycle time before versus after",
                        "exceptions and human overrides logged",
                        "client acceptance or rejection recorded",
                    ),
                    roi=_roi(signal),
                    assumptions=tuple(
                        [
                            "Pain points remain hypotheses until client validation.",
                            "Thirty days is an internal planning seed only; final scope, timeline, and price require qualified discovery plus customer-specific quote authority.",
                        ]
                        + [f"Unknown: {item}" for item in signal.unknowns]
                    ),
                )
            )

            delivery_plans.append(
                DeliveryPlan(
                    account_id=signal.account_id,
                    timeline_days=30,
                    phases=(
                        {
                            "days": "1-5",
                            "name": "baseline",
                            "exit_gate": "source-backed baseline approved",
                        },
                        {
                            "days": "6-10",
                            "name": "workflow design",
                            "exit_gate": "scope and acceptance criteria approved",
                        },
                        {
                            "days": "11-25",
                            "name": "governed run",
                            "exit_gate": "actions and exceptions logged",
                        },
                        {
                            "days": "26-30",
                            "name": "proof and decision",
                            "exit_gate": "proof pack reviewed",
                        },
                    ),
                    proof_requirements=(
                        "dated baseline",
                        "source references",
                        "approved action log",
                        "measured actuals",
                        "customer acceptance or rejection",
                    ),
                    upsell_gate="Only after verified delivery proof and an explicit customer need.",
                )
            )

            envelope = create_approval_envelope(
                account,
                action=next_action,
                channel="internal" if not contactable else "email_draft",
                proof_target="client-validated baseline or attributable response",
            )
            approvals.append(to_approval_request(account, envelope).model_dump(mode="json"))

            if source_backed:
                event = ProofEvent(
                    event_type=ProofEventType.LEAD_INTAKE,
                    customer_handle="Internal commercial account",
                    service_id="revenue_lab",
                    summary_ar="تم تقييم إشارة تجارية موثقة المصدر؛ لا تمثل نتيجة عميل.",
                    summary_en="A source-backed commercial signal was assessed; this is not a customer outcome.",
                    evidence_source=" | ".join(item.source_ref for item in signal.evidence),
                    confidence=1.0,
                    approval_status="internal_only",
                    risk_level="low",
                    payload={
                        "run_id": run_id,
                        "account_id": signal.account_id,
                        "proof_kind": "process_evidence",
                        "outcome_claimed": False,
                    },
                )
                proof_events.append(event.model_dump(mode="json"))
            else:
                blockers.append(f"{signal.account_id}: requires non-demo evidence before outreach")

        learning = tuple(
            LearningRecommendation(
                account_id=event.account_id,
                outcome=event.outcome,
                recommendation=_learning_recommendation(event),
                evidence_ref=event.source_ref or "demo-only",
            )
            for event in outcome_list
        )
        if not outcome_list:
            blockers.append(
                "No attributable outcomes supplied; conversion prediction remains uncalibrated"
            )

        mode = (
            "source_backed"
            if signal_list and all(_source_backed(item) for item in signal_list)
            else "mixed_or_demo"
        )
        summary = {
            "signals": len(signal_list),
            "source_backed_signals": sum(_source_backed(item) for item in signal_list),
            "opportunities": len(opportunities),
            "approval_requests": len(approvals),
            "proof_events": len(proof_events),
            "learning_recommendations": len(learning),
            "external_actions_executed": 0,
            "production_changes": 0,
            "verified_customer_outcomes": sum(
                item.is_customer_proof() for item in outcome_list
            ),
        }
        return RevenueLabBundle(
            run_id=run_id,
            generated_at=_now(),
            mode=mode,
            opportunities=tuple(opportunities),
            strategies=tuple(strategies),
            proposals=tuple(proposals),
            delivery_plans=tuple(delivery_plans),
            approval_requests=tuple(approvals),
            proof_events=tuple(proof_events),
            learning_recommendations=learning,
            blockers=tuple(dict.fromkeys(blockers)),
            summary=summary,
        )


def run_revenue_lab(
    signals: Iterable[CompanySignal], *, outcomes: Iterable[OutcomeEvent] = ()
) -> RevenueLabBundle:
    return RevenueLabEngine().run(signals, outcomes=outcomes)


__all__ = ["RevenueLabEngine", "run_revenue_lab"]
