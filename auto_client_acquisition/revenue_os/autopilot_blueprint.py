"""Dealix Revenue Autopilot blueprint.

Single source for the founder-led trust + proof-led funnel operating model.
Pure deterministic constants/functions, no side effects.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any


class ExecutionLane(StrEnum):
    AUTOPILOT = "autopilot"
    COPILOT = "copilot"
    FOUNDER_APPROVAL = "founder_approval"


class LeadBucket(StrEnum):
    QUALIFIED_A = "qualified_A"
    QUALIFIED_B = "qualified_B"
    NURTURE = "nurture"
    CLOSED_LOST = "closed_lost"


LEAD_SCORE_RULES: tuple[dict[str, Any], ...] = (
    {"signal": "decision_maker", "points": 3},
    {"signal": "b2b_company", "points": 3},
    {"signal": "has_crm_or_revenue_workflow", "points": 3},
    {"signal": "uses_or_plans_ai", "points": 3},
    {"signal": "saudi_or_gcc", "points": 2},
    {"signal": "urgency_within_30_days", "points": 2},
    {"signal": "budget_5k_plus_sar", "points": 2},
    {"signal": "no_company", "points": -3},
    {"signal": "student_or_job_seeker", "points": -3},
    {"signal": "vague_curiosity", "points": -2},
)

PIPELINE_STAGES: tuple[str, ...] = (
    "new_lead",
    "qualified_A",
    "qualified_B",
    "nurture",
    "partner_candidate",
    "meeting_booked",
    "meeting_done",
    "scope_requested",
    "scope_sent",
    "invoice_sent",
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "sprint_candidate",
    "retainer_candidate",
    "closed_lost",
)


def classify_lead_bucket(score: int) -> LeadBucket:
    if score >= 12:
        return LeadBucket.QUALIFIED_A
    if score >= 8:
        return LeadBucket.QUALIFIED_B
    if score >= 5:
        return LeadBucket.NURTURE
    return LeadBucket.CLOSED_LOST


def build_revenue_autopilot_blueprint() -> dict[str, Any]:
    return {
        "operating_formula": {
            "slug": "founder-led-trust-proof-led-funnel-automated-ops-disciplined-approval",
            "summary_ar": "الثقة من المؤسس، الإثبات من الأصول، التشغيل من الأتمتة، والحوكمة من الموافقات.",
            "summary_en": "Founder-led trust + proof-led funnel + automated revenue ops + disciplined approval system.",
        },
        "positioning": {
            "type": "Governed Revenue & AI Operations Company",
            "not": ["AI agency", "chatbot company", "early generic SaaS"],
        },
        "core_offer": {
            "name": "7-Day Governed Revenue & AI Ops Diagnostic",
            "outcome_ar": "تحديد فاقد الإيراد، جاهزية CRM/البيانات، ومخاطر AI/automation مع أول 3 قرارات تشغيلية بدليل.",
            "pricing_sar": [
                {"tier": "starter", "amount": 4999},
                {"tier": "standard", "amount": 9999},
                {"tier": "executive", "amount": 15000},
            ],
            "after_diagnostic_path": [
                "Revenue Intelligence Sprint",
                "Governed Ops Retainer",
            ],
        },
        "funnel_flow": [
            "content_or_outbound_or_partner",
            "lead_magnet",
            "lead_capture",
            "lead_score",
            "proof_pack",
            "booking",
            "meeting_brief",
            "diagnostic_scope",
            "invoice_or_payment_link",
            "onboarding",
            "delivery",
            "proof_pack_final",
            "sprint_or_retainer_upsell",
            "referral_or_case_study",
        ],
        "execution_lanes": {
            ExecutionLane.AUTOPILOT.value: [
                "collect",
                "classify",
                "log",
                "prepare",
                "remind",
                "generate_drafts",
            ],
            ExecutionLane.COPILOT.value: [
                "recommend_decision",
                "write_reply_draft",
                "prepare_scope",
                "prepare_invoice",
            ],
            ExecutionLane.FOUNDER_APPROVAL.value: [
                "external_send",
                "final_invoice_send",
                "claims_security_or_compliance",
                "publish_case_study",
                "final_diagnostic_conclusion",
                "high_impact_agent_action",
            ],
        },
        "proof_funnel_assets": [
            "sample_proof_pack_pdf",
            "ai_revenue_ops_risk_score_form",
            "diagnostic_deck",
            "one_page_offer_pdf",
            "case_style_demo_no_fake_client_claim",
        ],
        "landing_page": {
            "path": "/dealix-diagnostic",
            "cta_primary": "Get Sample Proof Pack",
            "cta_secondary": "Book Diagnostic Review",
            "sections": [
                "the_problem",
                "who_this_is_for",
                "what_you_get",
                "sample_outputs",
                "what_we_do_not_do",
                "pricing_range",
                "book_review",
            ],
            "what_we_do_not_do": [
                "no_autonomous_ai_messages",
                "no_revenue_claim_without_evidence",
                "no_crm_replacement_promise",
                "no_case_study_publish_without_approval",
                "no_generic_chatbot_automation_pitch",
            ],
        },
        "pipeline_stages": list(PIPELINE_STAGES),
        "lead_scoring": {
            "rules": list(LEAD_SCORE_RULES),
            "bucket_thresholds": {
                LeadBucket.QUALIFIED_A.value: "score >= 12",
                LeadBucket.QUALIFIED_B.value: "score 8-11",
                LeadBucket.NURTURE.value: "score 5-7",
                LeadBucket.CLOSED_LOST.value: "score < 5",
            },
        },
        "automation_playbooks": [
            {"id": 1, "name": "lead_capture"},
            {"id": 2, "name": "qualified_lead"},
            {"id": 3, "name": "proof_pack_request"},
            {"id": 4, "name": "meeting_booked"},
            {"id": 5, "name": "meeting_done"},
            {"id": 6, "name": "scope_requested"},
            {"id": 7, "name": "invoice_paid"},
            {"id": 8, "name": "delivery"},
            {"id": 9, "name": "proof_pack_sent"},
            {"id": 10, "name": "retainer_or_sprint_upsell"},
        ],
        "hard_gates": {
            "invoice_sent_requires_scope_sent": True,
            "delivery_started_requires_invoice_paid": True,
            "revenue_recognition_requires_invoice_paid": True,
            "all_external_actions_are_draft_or_approval_first": True,
        },
        "daily_operating_rhythm_minutes": {
            "morning_approval_review": 30,
            "midday_founder_outreach": 30,
            "day_end_classification_and_ledger": 30,
            "total": 90,
        },
        "north_star": {
            "now": "paid_diagnostics",
            "next": [
                "proof_packs_delivered",
                "sprint_candidates",
                "retainer_candidates",
            ],
            "future": "governed_value_decisions_created",
        },
        "fourteen_day_targets": {
            "target_accounts": 50,
            "connection_requests": 20,
            "conversations": 10,
            "proof_pack_requests": 5,
            "meetings": 3,
            "scopes": 2,
            "paid_diagnostics": 1,
        },
        "operating_order": [
            "dealix_diagnostic_page",
            "sample_proof_pack_gated_form",
            "crm_lifecycle_stages",
            "lead_score_automation",
            "meeting_brief_automation",
            "scope_invoice_draft_automation",
            "payment_link_process",
            "delivery_proof_pack_checklist",
            "founder_led_linkedin_content",
            "50_target_accounts",
            "20_partner_targets",
            "daily_approval_queue",
        ],
    }
