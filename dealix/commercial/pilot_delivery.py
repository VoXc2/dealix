"""Governed customer-specific Revenue Command Pilot delivery plan.

This module prepares an internal, approval-gated plan only. It never sends a
customer message, creates a charge, infers a public price/duration, or treats
activity as customer value. The canonical path is qualified discovery ->
customer-specific quote/scope/duration -> governed delivery -> source-backed
Proof -> STOP / EXPAND / REDESIGN.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, date, datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field


class PilotStartRequest(BaseModel):
    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    contact_name: str = ""
    sector: str = "b2b_services"
    pain_points: list[str] = Field(default_factory=list)
    diagnostic_id: str = ""
    founder_name: str = "سامي"
    start_date: str = ""
    approved_duration_days: int | None = Field(default=None, ge=1)
    approved_duration_ref: str = ""
    approved_scope_ref: str = ""
    baseline_source_ref: str = ""
    approved_data_boundary_ref: str = ""
    approval_path_ref: str = ""
    acceptance_criteria_ref: str = ""
    customer_specific_quote_ref: str = ""
    customer_acceptance_ref: str = ""
    start_condition_ref: str = ""


class DayPlan(BaseModel):
    day: int
    date_str: str
    title_ar: str
    title_en: str
    tasks_ar: list[str]
    tasks_en: list[str]
    draft_messages_ar: list[str] = Field(default_factory=list)
    proof_event: str = ""
    approval_required: bool = True


class PilotPlan(BaseModel):
    pilot_id: str
    account_id: str
    company_name: str
    start_date: str
    end_date: str
    approved_duration_days: int | None = None
    approved_duration_ref: str = ""
    duration_authority: str = "customer_specific_approved_duration_only"
    legacy_fixed_duration_authority: bool = False
    day_plans: list[DayPlan]
    week1_report_template: str
    upsell_script: str
    proof_cadence: str = "weekly_and_final"
    decision_path: str = "STOP / EXPAND / REDESIGN"
    approval_status: str = "approval_required"
    governance_decision: str = "pending"
    missing_start_refs: list[str] = Field(default_factory=list)
    external_send_allowed: bool = False
    live_charge_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


_START_REFS = (
    "approved_duration_ref",
    "approved_scope_ref",
    "baseline_source_ref",
    "approved_data_boundary_ref",
    "approval_path_ref",
    "acceptance_criteria_ref",
    "customer_specific_quote_ref",
    "customer_acceptance_ref",
    "start_condition_ref",
)


class PilotDeliveryKit:
    """Prepare governed milestones across an approved customer-specific duration."""

    _MILESTONES = [
        ("تثبيت النطاق وخط الأساس", "Scope, baseline & governance lock", [
            "Verify the approved scope, accountable owner, data boundary and approval path",
            "Confirm the first-party baseline and acceptance criteria",
            "Confirm the customer-specific quote, duration and customer acceptance references",
        ], "pilot_start_gate_reviewed"),
        ("خريطة الإيراد والفجوات", "Revenue workflow & gap map", [
            "Map one bounded revenue workflow end to end",
            "Identify leakage, ownership gaps and missing evidence",
            "Record hypotheses without claiming outcomes",
        ], "workflow_baseline_mapped"),
        ("مراجعة الإثبات المبكر", "Early proof review", [
            "Review actions, approvals, blockers and evidence collected",
            "Separate activity, delivery, payment, revenue and customer value",
            "Prepare a Proof Pack for human review only",
        ], "early_proof_review"),
        ("مراجعة التشغيل", "Operating review", [
            "Compare current observations with the approved baseline",
            "Keep only interventions supported by evidence",
            "Record data gaps and customer decisions required",
        ], "operating_review"),
        ("تثبيت ما يتكرر", "Repeatability review", [
            "Identify repeatable governed workflows",
            "Measure operator effort, approval latency and evidence completeness",
            "Do not generalize a feature from one unverified observation",
        ], "repeatability_review"),
        ("تجهيز الإثبات النهائي", "Final proof preparation", [
            "Reconcile the final evidence ledger to source references",
            "Mark unsupported metrics as unverified rather than filled",
            "Prepare final outcome questions and remaining evidence gaps",
        ], "final_proof_prepared"),
        ("مراجعة النتيجة والقرار", "Final outcome review", [
            "Review measured outcomes against acceptance criteria",
            "Record customer feedback and actual delivery economics",
            "Choose STOP / EXPAND / REDESIGN; no automatic upsell or price inference",
        ], "final_outcome_reviewed"),
    ]

    @classmethod
    def _proportional_milestones(cls, duration_days: int) -> list[tuple[int, str, str, list[str], str]]:
        """Place all governance stages across the approved duration without minting a default duration."""
        by_day: dict[int, tuple[str, str, list[str], list[str]]] = {}
        last_index = len(cls._MILESTONES) - 1
        for index, (title_ar, title_en, tasks_en, proof_event) in enumerate(cls._MILESTONES):
            day = 1 if last_index == 0 else 1 + round((duration_days - 1) * index / last_index)
            current = by_day.get(day)
            if current is None:
                by_day[day] = (title_ar, title_en, list(tasks_en), [proof_event])
            else:
                old_ar, old_en, old_tasks, old_events = current
                by_day[day] = (
                    f"{old_ar} / {title_ar}",
                    f"{old_en} / {title_en}",
                    [*old_tasks, *tasks_en],
                    [*old_events, proof_event],
                )
        return [
            (day, title_ar, title_en, tasks_en, "+".join(events))
            for day, (title_ar, title_en, tasks_en, events) in sorted(by_day.items())
        ]

    def create_pilot_plan(self, req: PilotStartRequest) -> PilotPlan:
        pilot_id = hashlib.sha256(
            f"{req.account_id}:{req.company_name}:{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]
        start = date.fromisoformat(req.start_date) if req.start_date else date.today()
        missing = [name for name in _START_REFS if not getattr(req, name).strip()]
        if req.approved_duration_days is None:
            missing.append("approved_duration_days")

        duration_ready = bool(req.approved_duration_days and req.approved_duration_ref.strip())
        end = start + timedelta(days=req.approved_duration_days - 1) if duration_ready else None
        milestones = self._proportional_milestones(req.approved_duration_days) if duration_ready else []

        day_plans = [
            DayPlan(
                day=day,
                date_str=str(start + timedelta(days=day - 1)),
                title_ar=title_ar,
                title_en=title_en,
                tasks_ar=[
                    "تنفيذ داخلي محكوم ومراجعة الأدلة؛ لا إرسال أو دفع تلقائي.",
                    *tasks_en,
                ],
                tasks_en=tasks_en,
                proof_event=proof_event,
            )
            for day, title_ar, title_en, tasks_en, proof_event in milestones
        ]

        governance = "blocked_missing_start_refs" if missing else "ready_for_manual_approval"
        return PilotPlan(
            pilot_id=pilot_id,
            account_id=req.account_id,
            company_name=req.company_name,
            start_date=str(start),
            end_date=str(end) if end else "",
            approved_duration_days=req.approved_duration_days,
            approved_duration_ref=req.approved_duration_ref,
            day_plans=day_plans,
            week1_report_template=self._weekly_proof_template(req),
            upsell_script=self._final_outcome_review_template(req),
            proof_cadence="approved_duration_proportional_and_final",
            governance_decision=governance,
            missing_start_refs=missing,
        )

    def _weekly_proof_template(self, req: PilotStartRequest) -> str:
        return f"""# Weekly Proof Review — {req.company_name}

Status: INTERNAL / REVIEW REQUIRED / NOT CUSTOMER PROOF UNTIL VERIFIED

## Baseline and scope
- Approved scope ref: {{approved_scope_ref}}
- Baseline source ref: {{baseline_source_ref}}
- Approved data boundary ref: {{approved_data_boundary_ref}}

## This week's posture
- Actions completed: {{actions_completed}}
- Approvals: {{approvals}}
- Evidence candidates: {{evidence_candidates}}
- Evidence gaps: {{evidence_gaps}}
- Verified customer value: {{verified_customer_value_or_none}}

No external send or commercial claim is authorized by this template.
"""

    def _final_outcome_review_template(self, req: PilotStartRequest) -> str:
        return f"""# Final Outcome Review — {req.company_name}

1. What changed versus the approved baseline?
2. Which outcomes have source-backed evidence?
3. What did delivery actually cost in time/tools/support?
4. What remains unverified or customer-dependent?
5. Customer decision: **STOP / EXPAND / REDESIGN**.

Expansion, if chosen, requires a new customer-specific approved quote/contract.
There is no automatic upsell, live charge, or customer-facing auto-send.
"""
