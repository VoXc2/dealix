"""Governed 30-day Revenue Command Pilot delivery plan.

This module prepares an internal, approval-gated plan only. It never sends a
customer message, creates a charge, infers a public price, or treats activity as
customer value. The canonical path is qualified discovery -> customer-specific
quote -> approved 30-day Pilot -> weekly/final Proof -> STOP / EXPAND / REDESIGN.
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
    """Prepare seven governed milestones across a 30-day Pilot."""

    def create_pilot_plan(self, req: PilotStartRequest) -> PilotPlan:
        pilot_id = hashlib.sha256(
            f"{req.account_id}:{req.company_name}:{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]
        start = date.fromisoformat(req.start_date) if req.start_date else date.today()
        end = start + timedelta(days=29)
        missing = [name for name in _START_REFS if not getattr(req, name).strip()]

        milestones = [
            (1, "تثبيت النطاق وخط الأساس", "Scope, baseline & governance lock", [
                "Verify the approved scope, accountable owner, data boundary and approval path",
                "Confirm the first-party baseline and acceptance criteria",
                "Confirm the customer-specific quote and customer acceptance references",
            ], "pilot_start_gate_reviewed"),
            (3, "خريطة الإيراد والفجوات", "Revenue workflow & gap map", [
                "Map one bounded revenue workflow end to end",
                "Identify leakage, ownership gaps and missing evidence",
                "Record hypotheses without claiming outcomes",
            ], "workflow_baseline_mapped"),
            (7, "الإثبات الأسبوعي الأول", "Week-1 proof review", [
                "Review actions, approvals, blockers and evidence collected",
                "Separate activity, delivery, payment, revenue and customer value",
                "Prepare the weekly Proof Pack for human review only",
            ], "weekly_proof_review_1"),
            (14, "مراجعة منتصف التجربة", "Mid-pilot operating review", [
                "Compare current observations with the approved baseline",
                "Keep only interventions supported by evidence",
                "Record data gaps and customer decisions required",
            ], "mid_pilot_review"),
            (21, "تثبيت ما يتكرر", "Repeatability review", [
                "Identify repeatable governed workflows",
                "Measure operator effort, approval latency and evidence completeness",
                "Do not generalize a feature from one unverified observation",
            ], "repeatability_review"),
            (28, "تجهيز الإثبات النهائي", "Final proof preparation", [
                "Reconcile the final evidence ledger to source references",
                "Mark unsupported metrics as unverified rather than filled",
                "Prepare final outcome questions and remaining evidence gaps",
            ], "final_proof_prepared"),
            (30, "مراجعة النتيجة والقرار", "Final outcome review", [
                "Review measured outcomes against acceptance criteria",
                "Record customer feedback and actual delivery economics",
                "Choose STOP / EXPAND / REDESIGN; no automatic upsell or price inference",
            ], "final_outcome_reviewed"),
        ]

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
            end_date=str(end),
            day_plans=day_plans,
            week1_report_template=self._weekly_proof_template(req),
            upsell_script=self._final_outcome_review_template(req),
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
        return f"""# Day-30 Outcome Review — {req.company_name}

1. What changed versus the approved baseline?
2. Which outcomes have source-backed evidence?
3. What did delivery actually cost in time/tools/support?
4. What remains unverified or customer-dependent?
5. Customer decision: **STOP / EXPAND / REDESIGN**.

Expansion, if chosen, requires a new customer-specific approved quote/contract.
There is no automatic upsell, live charge, or customer-facing auto-send.
"""
