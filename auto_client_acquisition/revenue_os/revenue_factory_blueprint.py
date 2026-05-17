"""Revenue Company Operating System blueprint for founder-led execution."""

from __future__ import annotations

from typing import Any


def _primary_offer() -> dict[str, Any]:
    return {
        "name": "7-Day Governed Revenue & AI Ops Diagnostic",
        "promise_ar": (
            "نكشف أين يضيع الإيراد، أين البيانات غير جاهزة، وأين الأتمتة أو AI "
            "غير محكومة، ثم نخرج 3 قرارات تشغيلية قابلة للتنفيذ بدليل."
        ),
        "deliverables": [
            "Revenue Workflow Map",
            "CRM / Source Quality Review",
            "AI Usage Risk Review",
            "Approval Boundaries",
            "Evidence Trail Gaps",
            "Top 3 Revenue Decisions",
            "Proof Pack",
            "Sprint / Retainer Recommendation",
        ],
        "tiers_sar": [
            {"tier": "starter", "price_sar": 4_999},
            {"tier": "standard", "price_sar": 9_999},
            {"tier": "executive", "price_sar": 15_000},
            {"tier": "enterprise_diagnostic", "price_sar": 25_000},
        ],
        "next_path": [
            "diagnostic",
            "revenue_intelligence_sprint",
            "governed_ops_retainer",
        ],
    }


def _operating_loop() -> list[dict[str, Any]]:
    return [
        {"stage": "audience", "output": "target_accounts"},
        {"stage": "signal", "output": "why_now_signals"},
        {"stage": "trust", "output": "founder_credibility"},
        {"stage": "proof", "output": "proof_assets"},
        {"stage": "qualification", "output": "scored_leads"},
        {"stage": "meeting", "output": "qualified_discovery"},
        {"stage": "scope", "output": "diagnostic_scope"},
        {"stage": "payment", "output": "invoice_paid"},
        {"stage": "delivery", "output": "diagnostic_delivery"},
        {"stage": "proof_pack", "output": "proof_pack_sent"},
        {"stage": "upsell", "output": "sprint_or_retainer_offer"},
        {"stage": "referral", "output": "partner_or_client_referral"},
        {"stage": "content", "output": "anonymized_market_learning"},
        {"stage": "more_audience", "output": "expanded_target_set"},
    ]


def _layers() -> list[dict[str, Any]]:
    return [
        {
            "layer": 1,
            "name": "Market Intelligence",
            "input": "icp hypotheses + buyer signals",
            "automation": "signal parsing + account clustering",
            "founder_decision": "which ICP to attack this week",
            "output": "ranked target accounts",
            "evidence_event": "market_signal_scored",
        },
        {
            "layer": 2,
            "name": "Demand Generation",
            "input": "ranked ICP + founder narrative",
            "automation": "content routing + outbound drafts + partner briefs",
            "founder_decision": "channel mix and weekly messaging angle",
            "output": "trust interactions and proof pack requests",
            "evidence_event": "trust_touch_logged",
        },
        {
            "layer": 3,
            "name": "Lead Capture",
            "input": "forms, DMs, referrals, warm intros",
            "automation": "CRM creation + source taxonomy + evidence log",
            "founder_decision": "accept/reject ambiguous leads",
            "output": "structured lead record",
            "evidence_event": "lead_captured",
        },
        {
            "layer": 4,
            "name": "Qualification",
            "input": "lead profile + urgency + budget + pain",
            "automation": "lead score + stage recommendation",
            "founder_decision": "A/B/C/D routing and partner path",
            "output": "qualified pipeline stage",
            "evidence_event": "lead_qualified",
        },
        {
            "layer": 5,
            "name": "Sales Conversion",
            "input": "qualified lead + meeting context",
            "automation": "call brief + scope draft + invoice draft",
            "founder_decision": "offer tier and commitment boundary",
            "output": "scope_sent or nurture_plan",
            "evidence_event": "scope_decision_logged",
        },
        {
            "layer": 6,
            "name": "Delivery & Proof",
            "input": "paid diagnostic + onboarding inputs",
            "automation": "workplan shell + proof pack draft assembly",
            "founder_decision": "final diagnostic conclusion",
            "output": "client proof pack + upsell recommendation",
            "evidence_event": "proof_pack_sent",
        },
        {
            "layer": 7,
            "name": "Expansion & Learning",
            "input": "delivery outcome + proof quality",
            "automation": "upsell recommendation + learning rollup",
            "founder_decision": "sprint/retainer/referral/content path",
            "output": "expansion motion + weekly playbook update",
            "evidence_event": "learning_cycle_closed",
        },
    ]


def _automation_levels() -> dict[str, list[str]]:
    return {
        "autopilot": [
            "capture_lead",
            "create_crm_record",
            "score_lead",
            "assign_stage",
            "create_next_action",
            "log_evidence_event",
            "generate_meeting_brief",
            "generate_draft_assets",
            "schedule_followup_reminder",
        ],
        "copilot": [
            "recommend_best_message",
            "recommend_offer_tier",
            "recommend_price_tier",
            "prepare_meeting_questions",
            "prepare_scope_draft",
            "prepare_invoice_draft",
            "recommend_upsell_path",
        ],
        "founder_approval": [
            "send_external_message",
            "send_invoice",
            "publish_final_diagnostic",
            "publish_security_claim",
            "publish_case_study",
            "execute_agent_external_action",
            "publish_public_proof",
        ],
    }


def _automation_workflows() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "new_lead_intake",
            "trigger": "form_submitted",
            "chain": [
                "crm_contact_created",
                "company_record_created",
                "lead_scored",
                "stage_assigned",
                "first_draft_prepared",
            ],
            "evidence_event": "lead_captured",
        },
        {
            "id": 2,
            "name": "proof_pack_request",
            "trigger": "proof_pack_requested",
            "chain": ["consent_check", "sample_asset_ready", "followup_task_t_plus_2d"],
            "evidence_event": "proof_pack_requested",
        },
        {
            "id": 3,
            "name": "high_score_alert",
            "trigger": "lead_score_gte_15",
            "chain": ["booking_invite_approval_task", "meeting_brief_generated", "founder_notified"],
            "evidence_event": "lead_prioritized",
        },
        {
            "id": 4,
            "name": "partner_lead_sequence",
            "trigger": "partner_signal_detected",
            "chain": ["partner_sequence_opened", "referral_terms_draft", "partner_call_task"],
            "evidence_event": "partner_motion_started",
        },
        {
            "id": 5,
            "name": "meeting_booked",
            "trigger": "calendar_booking_confirmed",
            "chain": ["crm_meeting_booked", "precall_brief", "discovery_question_pack"],
            "evidence_event": "meeting_booked",
        },
        {
            "id": 6,
            "name": "meeting_reminder",
            "trigger": "meeting_t_minus_24h",
            "chain": ["prep_reminder_draft", "lead_context_snapshot", "opening_suggestion"],
            "evidence_event": "meeting_prep_ready",
        },
        {
            "id": 7,
            "name": "meeting_outcome_capture",
            "trigger": "founder_marks_meeting_done",
            "chain": ["capture_5_outcome_fields", "classify_outcome", "route_scope_or_nurture"],
            "evidence_event": "meeting_completed",
        },
        {
            "id": 8,
            "name": "scope_requested",
            "trigger": "scope_requested",
            "chain": ["scope_generated", "price_recommended", "invoice_draft_generated"],
            "evidence_event": "scope_requested",
        },
        {
            "id": 9,
            "name": "scope_sent",
            "trigger": "scope_approved",
            "chain": ["scope_sent", "followup_timer_started"],
            "evidence_event": "scope_sent",
        },
        {
            "id": 10,
            "name": "invoice_sent",
            "trigger": "invoice_approved",
            "chain": ["payment_link_sent"],
            "evidence_event": "invoice_sent",
        },
        {
            "id": 11,
            "name": "invoice_paid",
            "trigger": "payment_confirmed",
            "chain": ["delivery_folder_created", "onboarding_form_sent", "kickoff_checklist_ready"],
            "evidence_event": "invoice_paid",
        },
        {
            "id": 12,
            "name": "onboarding_submitted",
            "trigger": "inputs_received",
            "chain": ["missing_input_check", "diagnostic_workplan", "proof_pack_draft_shell"],
            "evidence_event": "onboarding_received",
        },
        {
            "id": 13,
            "name": "proof_pack_draft",
            "trigger": "analysis_completed",
            "chain": ["proof_pack_drafted", "founder_review_task", "client_delivery_task"],
            "evidence_event": "proof_pack_draft_ready",
        },
        {
            "id": 14,
            "name": "proof_pack_delivered",
            "trigger": "proof_pack_approved",
            "chain": ["proof_pack_sent", "upsell_recommendation_generated"],
            "evidence_event": "proof_pack_sent",
        },
        {
            "id": 15,
            "name": "upsell_candidate",
            "trigger": "value_confirmed",
            "chain": ["sprint_proposal_draft", "retainer_option_draft", "approval_task_created"],
            "evidence_event": "upsell_candidate_identified",
        },
        {
            "id": 16,
            "name": "testimonial_or_referral",
            "trigger": "positive_feedback_received",
            "chain": ["permission_check", "testimonial_request_draft", "referral_request_draft"],
            "evidence_event": "advocacy_prompt_ready",
        },
        {
            "id": 17,
            "name": "nurture_path",
            "trigger": "lead_not_ready",
            "chain": ["objection_segment_assigned", "education_asset_suggested", "reactivation_task"],
            "evidence_event": "nurture_started",
        },
        {
            "id": 18,
            "name": "weekly_ceo_review",
            "trigger": "friday_review_window",
            "chain": [
                "pipeline_report_generated",
                "blockers_highlighted",
                "conversion_rates_computed",
                "next_best_actions_suggested",
                "no_build_warning_if_needed",
            ],
            "evidence_event": "weekly_ceo_review_logged",
        },
    ]


def _approval_matrix() -> list[dict[str, Any]]:
    return [
        {
            "action": "create_crm_contact",
            "automated": True,
            "needs_founder": False,
            "reason_ar": "إجراء داخلي",
        },
        {
            "action": "score_lead",
            "automated": True,
            "needs_founder": False,
            "reason_ar": "إجراء داخلي",
        },
        {
            "action": "draft_message",
            "automated": True,
            "needs_founder": False,
            "reason_ar": "مسودة فقط",
        },
        {
            "action": "send_cold_message",
            "automated": False,
            "needs_founder": True,
            "reason_ar": "فعل خارجي يحتاج موافقة",
        },
        {
            "action": "send_proof_pack_after_consent",
            "automated": True,
            "needs_founder": True,
            "reason_ar": "يتطلب مراجعة تأسيسية أولية",
        },
        {
            "action": "send_invoice",
            "automated": False,
            "needs_founder": True,
            "reason_ar": "التزام مالي",
        },
        {
            "action": "mark_revenue",
            "automated": False,
            "needs_founder": True,
            "reason_ar": "لا إيراد قبل إثبات الدفع",
        },
        {
            "action": "publish_case_study",
            "automated": False,
            "needs_founder": True,
            "reason_ar": "يتطلب موافقة العميل",
        },
        {
            "action": "make_security_claim",
            "automated": False,
            "needs_founder": True,
            "reason_ar": "ادعاء عالي المخاطر ويحتاج دليل",
        },
        {
            "action": "final_diagnostic_conclusion",
            "automated": False,
            "needs_founder": True,
            "reason_ar": "جودة وثقة نهائية",
        },
    ]


def _ceo_dashboard() -> dict[str, list[str]]:
    return {
        "today": [
            "new_leads",
            "qualified_a",
            "meetings_today",
            "scopes_pending",
            "invoices_pending",
            "blocked_approvals",
            "next_best_action",
        ],
        "funnel": [
            "targets",
            "connections",
            "replies",
            "proof_pack_requests",
            "forms",
            "qualified_a",
            "meetings",
            "scopes",
            "invoices",
            "paid_diagnostics",
        ],
        "quality": [
            "icp_fit",
            "pain_clarity",
            "budget_clarity",
            "urgency",
            "source_quality",
            "evidence_level",
        ],
        "revenue": [
            "pipeline_value",
            "invoice_sent_value",
            "paid_value",
            "sprint_candidates",
            "retainer_candidates",
        ],
        "learning": [
            "top_objections",
            "best_performing_message",
            "best_icp",
            "best_channel",
            "repeatable_workflow_signals",
        ],
    }


def _execution_targets() -> dict[str, Any]:
    return {
        "day_30_targets": {
            "paid_diagnostics": 1,
            "meetings": 3,
            "scopes": 2,
            "proof_packs_delivered": 1,
            "requires": [
                "clear_best_icp",
                "clear_best_message",
                "documented_objections",
                "first_partner_channel",
            ],
        },
        "day_90_targets": {
            "diagnostics_range": [3, 5],
            "revenue_sprints": 1,
            "retainers": 1,
            "requires": [
                "repeatable_workflow",
                "proof_moat",
                "partner_adoption",
            ],
            "scale_gate_before_platform": [
                "min_3_paid_diagnostics",
                "min_1_sprint",
                "min_1_retainer",
                "proof_packs_documented",
                "kpis_documented",
                "unit_economics_clear",
            ],
        },
    }


def _weekly_operating_rhythm() -> dict[str, Any]:
    return {
        "daily_90_minute_system": [
            {
                "block_minutes": 30,
                "name": "revenue_control",
                "actions": [
                    "review_leads",
                    "approve_drafts",
                    "move_stages",
                    "review_invoices",
                    "unblock_approvals",
                ],
            },
            {
                "block_minutes": 30,
                "name": "trust_building",
                "actions": [
                    "comment_on_5_target_accounts",
                    "send_5_connections",
                    "send_3_partner_messages",
                    "publish_proof_snippet_or_framework",
                ],
            },
            {
                "block_minutes": 30,
                "name": "conversion",
                "actions": [
                    "follow_interested_leads",
                    "push_scopes",
                    "review_meeting_briefs",
                    "send_requested_proof_packs",
                ],
            },
        ],
        "friday_ceo_review_questions_ar": [
            "كم lead؟",
            "كم meeting؟",
            "كم scope؟",
            "كم invoice؟",
            "كم paid؟",
            "ما أفضل ICP؟",
            "ما أسوأ channel؟",
            "ما الاعتراض المتكرر؟",
            "ما الذي يجب قتله؟",
            "ما الذي يجب مضاعفته؟",
        ],
    }


def revenue_factory_blueprint() -> dict[str, Any]:
    """Return the canonical Revenue Company Operating System blueprint."""
    return {
        "positioning_statement_ar": (
            "Dealix شركة تحوّل AI والإيراد إلى تشغيل محكوم، قابل للقياس، "
            "مثبت بالأدلة، وقابل للتكرار."
        ),
        "operating_formula": [
            "Founder-led trust",
            "Proof-led funnel",
            "Automated revenue ops",
            "Disciplined approval system",
            "Partner leverage",
            "Delivery-to-content loop",
            "Evidence-based scaling",
        ],
        "primary_offer": _primary_offer(),
        "closed_loop": _operating_loop(),
        "layers": _layers(),
        "automation_levels": _automation_levels(),
        "automation_workflows": _automation_workflows(),
        "approval_matrix": _approval_matrix(),
        "ceo_dashboard": _ceo_dashboard(),
        "weekly_operating_rhythm": _weekly_operating_rhythm(),
        "execution_targets": _execution_targets(),
        "non_negotiables": [
            "no_external_send_without_founder_approval",
            "no_scraping",
            "no_autonomous_linkedin_or_whatsapp_sending",
            "no_revenue_mark_before_payment_proof",
            "no_public_case_study_without_client_approval",
            "no_security_claim_without_evidence",
            "no_build_without_repeatability_or_customer_pull",
        ],
    }


__all__ = ["revenue_factory_blueprint"]
