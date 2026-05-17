"""Dealix Agentic Revenue + AI Ops Factory blueprint.

This module converts the founder operating doctrine into deterministic,
machine-readable contracts that can be consumed by APIs, checklists,
and workflow runners.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AutomationLevel(StrEnum):
    FULLY_AUTOMATED = "fully_automated"
    AGENT_ASSISTED = "agent_assisted"
    FOUNDER_APPROVAL_REQUIRED = "founder_approval_required"


class ApprovalRiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentContract(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    agent_id: str
    mission_ar: str
    mission_en: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    forbidden_actions: list[str] = Field(default_factory=list)
    approval_required_for: list[str] = Field(default_factory=list)
    evidence_required: list[str] = Field(default_factory=list)
    quality_checks: list[str] = Field(default_factory=list)


class AutomationPlay(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    automation_id: int
    title: str
    category: str
    level: AutomationLevel


class ApprovalType(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    approval_type: str
    default_risk: ApprovalRiskLevel
    note: str


class OperatingLoop(BaseModel):
    model_config = ConfigDict(extra="forbid")

    loop_id: str
    name: str
    steps: list[str]


class ScheduleSlot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    when: str
    owner_agent: str
    output: str


class MetricGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")

    group: str
    metrics: list[str]


DOCTRINE_CHAIN: tuple[str, ...] = (
    "signal",
    "source",
    "approval",
    "action",
    "evidence",
    "decision",
    "value",
    "asset",
)


AGENT_CONTRACTS: tuple[AgentContract, ...] = (
    AgentContract(
        agent_id="MarketIntelligenceAgent",
        mission_ar="التقاط إشارات سوق يومية من مصادر مرخّصة لبناء قائمة فرص عالية الملاءمة.",
        mission_en="Capture daily licensed market signals and build high-fit account lists.",
        inputs=["linkedin_searches", "company_sites", "job_posts", "news", "crm_notes"],
        outputs=["target_account_list", "buying_signals", "recommended_angle", "confidence_score"],
        allowed_actions=["collect_signal", "rank_accounts", "draft_reachout_reason", "log_internal_signal"],
        forbidden_actions=["send_external_message", "scrape_unlicensed_data", "cold_whatsapp_live"],
        approval_required_for=["external_message_first_touch"],
        evidence_required=["source_link", "signal_timestamp"],
        quality_checks=["licensed_source_only", "no_sensitive_personal_data"],
    ),
    AgentContract(
        agent_id="IcpScoringAgent",
        mission_ar="تحديد أولوية العملاء حسب ICP وتصنيفهم إلى A/B/C/D.",
        mission_en="Score prospects against ICP and classify into A/B/C/D.",
        inputs=["lead_profile", "sector", "pain", "budget", "region"],
        outputs=["score", "stage", "reason", "next_action"],
        allowed_actions=["score_lead", "assign_stage", "flag_missing_data"],
        forbidden_actions=["force_stage_without_signal", "send_external_message"],
        approval_required_for=[],
        evidence_required=["lead_captured_event", "scoring_inputs_snapshot"],
        quality_checks=["deterministic_scoring", "no_invented_budget"],
    ),
    AgentContract(
        agent_id="PositioningAgent",
        mission_ar="توليد زاوية بيع دقيقة حسب القطاع والألم التشغيلي.",
        mission_en="Generate precise positioning angle by sector and workflow pain.",
        inputs=["industry", "company_size", "role", "pain", "budget", "crm_status"],
        outputs=["message_angle", "pain_hypothesis", "recommended_offer", "objection_prediction"],
        allowed_actions=["propose_angle", "recommend_demo_path", "suggest_offer"],
        forbidden_actions=["publish_claim_without_source", "send_external_message"],
        approval_required_for=["public_claim"],
        evidence_required=["strategy_source", "offer_catalog_reference"],
        quality_checks=["no_overclaim", "align_with_sector_defaults"],
    ),
    AgentContract(
        agent_id="ContentEngineAgent",
        mission_ar="تحويل الاعتراضات والتعلّمات إلى محتوى تسويقي موجّه.",
        mission_en="Turn objections and delivery learnings into focused content drafts.",
        inputs=["objections", "call_notes", "proof_insights", "market_signals"],
        outputs=["linkedin_post_draft", "email_snippet", "video_script", "partner_post"],
        allowed_actions=["draft_content", "map_objection_to_content", "queue_content_calendar"],
        forbidden_actions=["publish_directly", "reuse_client_data_without_approval", "send_external_message"],
        approval_required_for=["content_publish", "client_named_reference"],
        evidence_required=["objection_log", "proof_source_pointer"],
        quality_checks=["founder_voice", "no_client_data_leakage"],
    ),
    AgentContract(
        agent_id="OutreachPersonalizationAgent",
        mission_ar="تجهيز رسائل شخصية لكل حساب مع CTA واضح.",
        mission_en="Prepare personalized outreach drafts with explicit CTA.",
        inputs=["target_account", "buyer_role", "buying_signal", "recommended_angle"],
        outputs=["linkedin_dm_draft", "email_draft", "follow_up_draft", "booking_cta"],
        allowed_actions=["draft_message", "generate_follow_up_sequence", "suggest_next_action"],
        forbidden_actions=["send_external_message", "linkedin_automation", "cold_whatsapp_live"],
        approval_required_for=["external_send"],
        evidence_required=["signal_reference", "approved_angle"],
        quality_checks=["concise_founder_led_tone", "no_unsupported_claims"],
    ),
    AgentContract(
        agent_id="LeadCaptureAgent",
        mission_ar="تحويل كل تفاعل وارد إلى سجل CRM + حدث دليل.",
        mission_en="Convert every inbound interaction into CRM records and evidence events.",
        inputs=["form_submission", "reply_payload", "partner_intro", "manual_entry"],
        outputs=["contact_record", "company_record", "stage_assignment", "evidence_event"],
        allowed_actions=["create_contact", "create_company", "assign_source", "log_evidence_event"],
        forbidden_actions=["drop_unprocessed_lead", "send_external_message"],
        approval_required_for=[],
        evidence_required=["capture_source", "capture_timestamp", "owner_assignment"],
        quality_checks=["required_fields_present", "source_traceable"],
    ),
    AgentContract(
        agent_id="MeetingBriefAgent",
        mission_ar="إصدار brief قبل كل مكالمة مع أسئلة وديمو مسار وإغلاقات محتملة.",
        mission_en="Produce a pre-call brief with questions, demo path, and close options.",
        inputs=["lead_profile", "previous_replies", "scoring_result", "positioning_output"],
        outputs=["company_snapshot", "discovery_questions", "demo_path", "objection_map"],
        allowed_actions=["compose_brief", "suggest_discovery_questions", "rank_risks"],
        forbidden_actions=["edit_call_outcome_after_meeting", "send_external_message"],
        approval_required_for=[],
        evidence_required=["lead_score_event", "reply_context"],
        quality_checks=["demo_path_exists", "questions_match_pain"],
    ),
    AgentContract(
        agent_id="SalesCallCoachAgent",
        mission_ar="تحويل نتائج المكالمة إلى قرار: scope أو nurture أو partner route.",
        mission_en="Convert call outcomes to explicit decision paths: scope, nurture, or partner.",
        inputs=["meeting_notes", "pain_confirmation", "budget_range", "decision_maker_signal"],
        outputs=["outcome_classification", "next_action", "scope_trigger", "risk_flags"],
        allowed_actions=["classify_call_outcome", "request_scope_draft", "log_meeting_event"],
        forbidden_actions=["promote_l5_without_usage", "promote_l6_without_scope_or_request", "send_external_message"],
        approval_required_for=["meeting_outcome_override"],
        evidence_required=["meeting_done_event", "notes_reference"],
        quality_checks=["state_machine_respected", "no_revenue_without_payment"],
    ),
    AgentContract(
        agent_id="ScopeBuilderAgent",
        mission_ar="توليد scope تشخيص احترافي وفق ملاحظات اجتماع معتمدة.",
        mission_en="Generate a professional diagnostic scope from approved meeting notes.",
        inputs=["approved_meeting_notes", "pain", "workflow", "timeline", "tier", "price"],
        outputs=["scope_doc", "deliverables", "exclusions", "invoice_recommendation"],
        allowed_actions=["draft_scope", "draft_timeline", "draft_exclusions"],
        forbidden_actions=["send_scope_to_client", "security_claim_without_source"],
        approval_required_for=["scope_send", "invoice_send"],
        evidence_required=["meeting_done_event", "scope_requested_event"],
        quality_checks=["includes_exclusions", "price_within_approved_range"],
    ),
    AgentContract(
        agent_id="BillingAgent",
        mission_ar="تحويل scope المعتمد إلى invoice draft ومتابعة التحصيل.",
        mission_en="Turn approved scope into invoice draft and track collection.",
        inputs=["scope_approved", "pricing_tier", "payment_terms"],
        outputs=["invoice_draft", "payment_followups", "billing_status"],
        allowed_actions=["draft_invoice", "schedule_payment_reminder", "mark_payment_confirmed"],
        forbidden_actions=["send_invoice_without_scope", "start_delivery_without_payment", "send_external_message"],
        approval_required_for=["invoice_send", "refund_or_discount"],
        evidence_required=["scope_approved_event", "payment_proof"],
        quality_checks=["no_revenue_recognition_before_payment", "billing_terms_clear"],
    ),
    AgentContract(
        agent_id="DeliveryDiagnosticAgent",
        mission_ar="تنفيذ تشخيص منضبط بالبيانات والمصادر دون اختلاق.",
        mission_en="Execute governed diagnostic with strict source fidelity and no hallucination.",
        inputs=["onboarding_form", "crm_export", "workflow_docs", "call_notes", "screenshots"],
        outputs=["workflow_map", "source_quality_review", "approval_gap_map", "risk_register"],
        allowed_actions=["analyze_inputs", "flag_missing_data", "draft_findings"],
        forbidden_actions=["invent_data", "claim_nonexistent_fields", "send_external_message"],
        approval_required_for=["diagnostic_final"],
        evidence_required=["input_artifacts", "finding_source_links"],
        quality_checks=["every_claim_has_source", "estimates_marked_is_estimate"],
    ),
    AgentContract(
        agent_id="ProofPackAgent",
        mission_ar="تحويل التشخيص إلى Proof Pack قابل للبيع والتكرار.",
        mission_en="Convert diagnostics into reusable, sellable proof packs.",
        inputs=["diagnostic_notes", "findings", "decision_recommendations"],
        outputs=["proof_pack_draft", "learning_note", "anonymized_content_draft", "upsell_hint"],
        allowed_actions=["compose_proof_pack", "create_evidence_appendix", "propose_next_30_days_plan"],
        forbidden_actions=["send_to_client_without_approval", "use_non_approved_case_data", "send_external_message"],
        approval_required_for=["proof_pack_send", "case_study_publish"],
        evidence_required=["diagnostic_complete_event", "evidence_chain_links"],
        quality_checks=["decision_confidence_explicit", "missing_data_marked_missing"],
    ),
    AgentContract(
        agent_id="UpsellAgent",
        mission_ar="اقتراح العرض التالي الأنسب بعد التشخيص حسب الجاهزية.",
        mission_en="Recommend best next commercial offer based on post-diagnostic readiness.",
        inputs=["diagnostic_result", "budget_signal", "pain_level", "workflow_repeatability"],
        outputs=["recommended_offer", "upsell_reason", "nurture_alternative"],
        allowed_actions=["route_offer", "rank_candidates", "prepare_upsell_draft"],
        forbidden_actions=["force_upsell_without_proof", "send_external_message"],
        approval_required_for=["upsell_external_send", "price_override"],
        evidence_required=["proof_pack_event", "value_signal_reference"],
        quality_checks=["proof_before_upsell", "pricing_in_catalog_range"],
    ),
    AgentContract(
        agent_id="PartnerAgent",
        mission_ar="بناء قناة شركاء بترشيح وتقييم وتفعيل شراكات نوعية.",
        mission_en="Build partner channel via qualification, pitch drafting, and activation.",
        inputs=["partner_candidates", "fit_score", "referral_model", "joint_offer"],
        outputs=["partner_pitch_draft", "partner_priority_list", "referral_terms_draft"],
        allowed_actions=["score_partner_fit", "draft_partner_pitch", "queue_partner_followup"],
        forbidden_actions=["send_partner_terms_without_approval", "share_client_data_unapproved", "send_external_message"],
        approval_required_for=["partner_intro_send", "partner_terms_send"],
        evidence_required=["partner_signal", "fit_score_basis"],
        quality_checks=["partner_type_classified", "no_unapproved_data_sharing"],
    ),
    AgentContract(
        agent_id="GovernanceRiskAgent",
        mission_ar="حارس الثقة: يوقف المخاطر ويضمن أن كل فعل يمر عبر الموافقة والدليل.",
        mission_en="Trust guard: block risky actions and enforce approval + evidence gates.",
        inputs=["proposed_action", "risk_context", "source_context", "approval_state"],
        outputs=["risk_decision", "blocked_reason", "required_evidence", "policy_feedback"],
        allowed_actions=["classify_risk", "block_action", "request_approval", "log_governance_event"],
        forbidden_actions=["bypass_approval", "allow_unverified_security_claims", "send_external_message"],
        approval_required_for=[],
        evidence_required=["policy_match", "rule_hit", "audit_log_pointer"],
        quality_checks=["no_external_action_without_approval", "no_claim_without_source"],
    ),
)


APPROVAL_TYPES: tuple[ApprovalType, ...] = (
    ApprovalType(
        approval_type="external_message",
        default_risk=ApprovalRiskLevel.HIGH,
        note="First external send always needs founder approval.",
    ),
    ApprovalType(
        approval_type="invoice_send",
        default_risk=ApprovalRiskLevel.HIGH,
        note="No invoice send without approved scope.",
    ),
    ApprovalType(
        approval_type="scope_send",
        default_risk=ApprovalRiskLevel.HIGH,
        note="Scope is client-facing and must be approved.",
    ),
    ApprovalType(
        approval_type="diagnostic_final",
        default_risk=ApprovalRiskLevel.HIGH,
        note="Final diagnostic findings are founder-approved.",
    ),
    ApprovalType(
        approval_type="case_study",
        default_risk=ApprovalRiskLevel.CRITICAL,
        note="Requires explicit customer approval.",
    ),
    ApprovalType(
        approval_type="security_claim",
        default_risk=ApprovalRiskLevel.CRITICAL,
        note="Unsupported claims are blocked by governance.",
    ),
    ApprovalType(
        approval_type="agent_tool_action",
        default_risk=ApprovalRiskLevel.MEDIUM,
        note="Any external-impact tool call requires review.",
    ),
    ApprovalType(
        approval_type="refund_or_discount",
        default_risk=ApprovalRiskLevel.HIGH,
        note="Commercial exceptions need founder sign-off.",
    ),
    ApprovalType(
        approval_type="partner_terms",
        default_risk=ApprovalRiskLevel.MEDIUM,
        note="Partner terms must be reviewed before sharing.",
    ),
)


OPERATING_LOOPS: tuple[OperatingLoop, ...] = (
    OperatingLoop(
        loop_id="demand",
        name="Demand Loop",
        steps=[
            "market_signal",
            "content_angle",
            "publish_or_send_with_approval",
            "proof_pack_request",
            "lead_captured",
            "meeting",
            "learning_to_content",
        ],
    ),
    OperatingLoop(
        loop_id="sales",
        name="Sales Loop",
        steps=[
            "lead",
            "score",
            "message_draft",
            "founder_approval",
            "conversation",
            "meeting",
            "scope",
            "invoice",
            "payment",
        ],
    ),
    OperatingLoop(
        loop_id="delivery",
        name="Delivery Loop",
        steps=[
            "payment",
            "onboarding",
            "diagnostic",
            "proof_pack",
            "delivery_call",
            "value_confirmed",
            "upsell",
        ],
    ),
    OperatingLoop(
        loop_id="product_learning",
        name="Product Learning Loop",
        steps=[
            "manual_workflow_repeated_3x",
            "document_playbook",
            "automate_internal_step",
            "test",
            "reuse",
            "productize_if_multi_client",
        ],
    ),
    OperatingLoop(
        loop_id="partner",
        name="Partner Loop",
        steps=[
            "partner_signal",
            "partner_pitch",
            "call",
            "shared_diagnostic",
            "proof_pack",
            "implementation_handoff",
            "next_intro",
        ],
    ),
    OperatingLoop(
        loop_id="governance",
        name="Governance Loop",
        steps=[
            "proposed_action",
            "risk_classification",
            "approval_required_check",
            "approved_or_rejected",
            "action_logged",
            "evidence_stored",
            "policy_improved",
        ],
    ),
    OperatingLoop(
        loop_id="weekly_ceo",
        name="Weekly CEO Loop",
        steps=[
            "pipeline_review",
            "bottleneck_detected",
            "single_fix_selected",
            "no_build_warning_check",
            "next_week_focus",
            "measure",
        ],
    ),
)


DAILY_SCHEDULE: tuple[ScheduleSlot, ...] = (
    ScheduleSlot(when="06:00", owner_agent="MarketIntelligenceAgent", output="top_market_signals_and_targets"),
    ScheduleSlot(when="08:00", owner_agent="ExecutiveBriefAgent", output="founder_daily_priorities"),
    ScheduleSlot(when="10:00", owner_agent="OutreachPersonalizationAgent", output="prospect_and_partner_message_drafts"),
    ScheduleSlot(when="13:00", owner_agent="ContentEngineAgent", output="daily_content_draft_from_objections"),
    ScheduleSlot(when="16:00", owner_agent="IcpScoringAgent", output="stale_deals_and_next_actions"),
    ScheduleSlot(when="20:00", owner_agent="ProofPackAgent", output="learning_digest_and_tomorrow_focus"),
)


WEEKLY_OPERATING_SYSTEM: tuple[dict[str, str], ...] = (
    {"day": "Sunday", "theme": "Targeting", "focus": "refresh_icp_and_target_accounts_and_partners"},
    {"day": "Monday", "theme": "Trust", "focus": "publish_framework_and_send_personalized_messages"},
    {"day": "Tuesday", "theme": "Proof", "focus": "promote_proof_pack_and_follow_up_warm_leads"},
    {"day": "Wednesday", "theme": "Conversion", "focus": "meetings_scopes_invoices"},
    {"day": "Thursday", "theme": "Delivery", "focus": "diagnostics_proof_packs_upsell"},
    {"day": "Friday", "theme": "CEO Review", "focus": "review_metrics_and_build_no_build_decision"},
    {"day": "Saturday", "theme": "Asset Creation", "focus": "improve_templates_update_proof_pack_schedule_content"},
)


AUTOMATION_PLAYS: tuple[AutomationPlay, ...] = (
    AutomationPlay(automation_id=1, title="new_target_account_to_scored_record", category="growth", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=2, title="linkedin_reply_to_classified_next_action_draft", category="growth", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=3, title="proof_pack_form_to_lead_and_followup_task", category="growth", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=4, title="risk_score_to_offer_recommendation", category="growth", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=5, title="new_partner_candidate_to_pitch_draft", category="growth", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=6, title="score_a_to_meeting_invite_draft", category="sales", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=7, title="meeting_booked_to_pre_call_brief", category="sales", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=8, title="meeting_reminder_to_founder_prep_note", category="sales", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=9, title="meeting_done_to_outcome_classification", category="sales", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=10, title="scope_requested_to_scope_draft", category="sales", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=11, title="scope_approved_to_invoice_draft", category="sales", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=12, title="invoice_sent_to_payment_reminder_schedule", category="sales", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=13, title="invoice_paid_to_onboarding_sequence", category="sales", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=14, title="onboarding_submitted_to_delivery_checklist", category="delivery", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=15, title="crm_export_to_source_quality_review_draft", category="delivery", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=16, title="missing_data_to_info_request_draft", category="delivery", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=17, title="findings_complete_to_proof_pack_draft", category="delivery", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=18, title="approved_proof_pack_to_delivery_email_draft", category="delivery", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=19, title="delivery_done_to_upsell_recommendation", category="delivery", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=20, title="external_send_requested_to_approval_gate", category="governance", level=AutomationLevel.FOUNDER_APPROVAL_REQUIRED),
    AutomationPlay(automation_id=21, title="security_claim_detected_to_block_and_source_request", category="governance", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=22, title="case_study_generated_to_client_approval_gate", category="governance", level=AutomationLevel.FOUNDER_APPROVAL_REQUIRED),
    AutomationPlay(automation_id=23, title="revenue_marked_to_invoice_paid_validation", category="governance", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=24, title="l5_status_request_to_used_in_meeting_validation", category="governance", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=25, title="l6_status_request_to_scope_request_validation", category="governance", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=26, title="objection_logged_to_objection_library_update", category="learning", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=27, title="closed_lost_to_reason_classification", category="learning", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=28, title="proof_pack_delivered_to_anonymized_insight", category="learning", level=AutomationLevel.AGENT_ASSISTED),
    AutomationPlay(automation_id=29, title="workflow_repeated_3x_to_platform_signal", category="learning", level=AutomationLevel.FULLY_AUTOMATED),
    AutomationPlay(automation_id=30, title="weekly_review_to_build_or_sell_recommendation", category="learning", level=AutomationLevel.AGENT_ASSISTED),
)


METRICS: tuple[MetricGroup, ...] = (
    MetricGroup(
        group="acquisition",
        metrics=["target_accounts_added", "messages_approved", "messages_sent", "reply_rate", "proof_pack_requests", "risk_score_completions"],
    ),
    MetricGroup(
        group="conversion",
        metrics=["qualified_a", "meeting_booked", "meeting_done", "scope_requested", "scope_sent", "invoice_sent", "invoice_paid"],
    ),
    MetricGroup(
        group="delivery",
        metrics=["onboarding_complete", "diagnostic_complete", "proof_pack_sent", "client_value_confirmed"],
    ),
    MetricGroup(
        group="expansion",
        metrics=["sprint_candidates", "retainer_candidates", "referrals", "case_study_approvals"],
    ),
    MetricGroup(
        group="governance",
        metrics=["blocked_risky_actions", "missing_source_warnings", "unsupported_claims_caught", "approval_sla", "evidence_completeness"],
    ),
)


IMPLEMENTATION_ORDER: tuple[dict[str, Any], ...] = (
    {
        "sprint": 1,
        "name": "Revenue Control Base",
        "items": ["crm_stages", "lead_scoring", "approval_queue", "evidence_events", "proof_pack_form", "booking_link", "invoice_process"],
    },
    {
        "sprint": 2,
        "name": "Agent Drafting",
        "items": ["outreach_drafts", "meeting_briefs", "scope_drafts", "followup_drafts", "content_drafts"],
    },
    {
        "sprint": 3,
        "name": "Delivery Automation",
        "items": ["onboarding_checklist", "diagnostic_checklist", "proof_pack_generator", "missing_data_detector", "upsell_recommendation"],
    },
    {
        "sprint": 4,
        "name": "Governance Automation",
        "items": ["claim_checker", "approval_enforcement", "revenue_payment_validation", "case_study_gate", "client_data_policy"],
    },
    {
        "sprint": 5,
        "name": "Productization",
        "items": ["internal_module", "client_workspace", "partner_dashboard", "repeatable_playbooks"],
        "gate": "only_after_3_paid_diagnostics",
    },
)


def _validate_internal_contracts() -> None:
    # Every agent must explicitly forbid autonomous external sending.
    for contract in AGENT_CONTRACTS:
        assert any(
            action in contract.forbidden_actions
            for action in ("send_external_message", "cold_whatsapp_live", "send_scope_to_client")
        ), f"{contract.agent_id} must forbid autonomous client send actions"

    assert len(AGENT_CONTRACTS) == 15, "factory contract expects 15 core agents"
    assert len(AUTOMATION_PLAYS) == 30, "factory blueprint expects 30 automation plays"

    ids = [a.automation_id for a in AUTOMATION_PLAYS]
    assert ids == list(range(1, 31)), "automation ids must be 1..30"

    required_levels = {
        AutomationLevel.FULLY_AUTOMATED.value,
        AutomationLevel.AGENT_ASSISTED.value,
        AutomationLevel.FOUNDER_APPROVAL_REQUIRED.value,
    }
    assert required_levels == {p.level for p in AUTOMATION_PLAYS}


_validate_internal_contracts()


def build_revenue_factory_blueprint() -> dict[str, Any]:
    """Return the full machine-readable operating blueprint."""
    return {
        "model": "dealix_agentic_revenue_ai_ops_factory",
        "north_star": "governed_value_decisions_created",
        "doctrine_chain": list(DOCTRINE_CHAIN),
        "automation_levels": [level.value for level in AutomationLevel],
        "approval_risk_levels": [risk.value for risk in ApprovalRiskLevel],
        "agent_contracts": [contract.model_dump(mode="json") for contract in AGENT_CONTRACTS],
        "approval_types": [item.model_dump(mode="json") for item in APPROVAL_TYPES],
        "operating_loops": [loop.model_dump(mode="json") for loop in OPERATING_LOOPS],
        "daily_schedule": [slot.model_dump(mode="json") for slot in DAILY_SCHEDULE],
        "weekly_operating_system": list(WEEKLY_OPERATING_SYSTEM),
        "automation_plays": [play.model_dump(mode="json") for play in AUTOMATION_PLAYS],
        "metrics": [group.model_dump(mode="json") for group in METRICS],
        "implementation_order": list(IMPLEMENTATION_ORDER),
        "policies": {
            "no_autonomous_external_send": True,
            "approval_required_for_external_first_touch": True,
            "every_recommendation_requires_source": True,
            "every_number_requires_source_or_estimate_flag": True,
            "no_revenue_without_payment_proof": True,
            "build_vs_automate_rule": {
                "new_workflow": "manual_plus_checklist",
                "repeated_2x": "template",
                "repeated_3x": "automation",
                "repeated_with_2_clients": "internal_module",
                "repeated_with_3_clients_plus_retainer": "product_feature",
            },
        },
    }
