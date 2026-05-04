"""
Service Contract — single source of truth for every productized service.

Every bundle in the public Service Tower (api/routers/services.py CATALOG)
must have a matching contract here. The contract is the **Definition of Done**:

  - target_customer       (who buys this)
  - pain                  (what we solve)
  - promise               (specific, no guaranteed claims)
  - forbidden_claims      (audit-enforced)
  - required_inputs       (intake-questions are derived from this)
  - workflow_steps        (delivery factory consumes this)
  - agents_used           (registered AI agents)
  - human_approvals       (which steps need approval)
  - safe_tool_policy      (allowed channels)
  - deliverables          (what the customer gets)
  - proof_metrics         (revenue work units we will emit)
  - sla_hours             (hard delivery deadline)
  - pricing_sar           (or "custom")
  - risks                 (what we will NOT do)
  - upgrade_path          (next bundle when this Proof Pack lands)
  - frontend_page         (where the customer reads about it)

The contract is checked by `excellence_score.compute_excellence(contract)`.
A score >= 80 is sellable, 70-79 beta-only, <70 internal-only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ServiceContract:
    service_id: str
    arabic_name: str
    english_name: str
    bundle_tier: str                          # diagnostic | starter | data_to_revenue | growth_os | partnership | control_tower
    target_customer: str
    pain: str
    promise: str                              # never include "نضمن" / "guaranteed"
    forbidden_claims: tuple[str, ...]
    required_inputs: tuple[str, ...]
    workflow_steps: tuple[str, ...]
    agents_used: tuple[str, ...]
    human_approvals: tuple[str, ...]
    safe_tool_policy: tuple[str, ...]
    deliverables: tuple[str, ...]
    proof_metrics: tuple[str, ...]
    sla_hours: int
    pricing_sar: float | None                  # None = custom
    pricing_label: str
    risks: tuple[str, ...]
    upgrade_path: str | None                   # next service_id
    frontend_page: str
    tests_required: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""


# ── The 6 contracts (Free Diagnostic + 5 paid bundles) ───────────


_FORBIDDEN = (
    "نضمن", "guaranteed", "ضمان نتائج",
    "auto-dm", "cold whatsapp", "scrape", "scraping",
)


CONTRACTS: tuple[ServiceContract, ...] = (
    ServiceContract(
        service_id="free_diagnostic",
        arabic_name="Free Diagnostic",
        english_name="Free Growth Diagnostic",
        bundle_tier="diagnostic",
        target_customer="مؤسس / مدير نمو يستكشف Dealix قبل الالتزام",
        pain="لا يعرف من أين يبدأ + لا يستطيع تقييم الباقة المناسبة",
        promise="خلال 24 ساعة: تشخيص قنواتك + 3 فرص تحسين فورية + توصية الباقة المناسبة",
        forbidden_claims=_FORBIDDEN,
        required_inputs=("company_name", "sector", "main_offer"),
        workflow_steps=(
            "intake_capture",
            "channel_audit",
            "icp_clarify",
            "improvement_areas_extract",
            "bundle_recommend",
        ),
        agents_used=("intake_agent", "channel_audit_agent", "bundle_recommender"),
        human_approvals=("recommend_bundle",),
        safe_tool_policy=("internal_only", "no_outbound"),
        deliverables=(
            "diagnostic_report_pdf",
            "3_improvement_areas",
            "recommended_bundle_card",
        ),
        proof_metrics=("diagnostic_completed", "improvement_areas_extracted", "bundle_recommended"),
        sla_hours=24,
        pricing_sar=0.0,
        pricing_label="مجاني",
        risks=("لا تواصل خارجي", "لا scraping", "approval-first"),
        upgrade_path="growth_starter",
        frontend_page="private-beta.html",
        tests_required=("test_diagnostic_intake", "test_diagnostic_recommends_bundle"),
    ),
    ServiceContract(
        service_id="growth_starter",
        arabic_name="Growth Starter",
        english_name="Growth Starter Pilot",
        bundle_tier="starter",
        target_customer="شركة أو وكالة تريد أول Proof سريع قبل الاشتراك",
        pain="لا يوجد proof من Dealix يقنع الفريق/المجلس بالاستثمار في الاشتراك",
        promise="خلال 7 أيام: 10 فرص + رسائل عربية + قناة موصى بها + Proof Pack مختصر — كل draft يمر بموافقتك",
        forbidden_claims=_FORBIDDEN,
        required_inputs=("company_name", "sector", "ideal_customer", "current_channels"),
        workflow_steps=(
            "intake_capture",
            "icp_define",
            "target_research",
            "target_rank",
            "draft_messages",
            "channel_recommend",
            "approval_collect",
            "followup_plan",
            "proof_pack_build",
        ),
        agents_used=(
            "intake_agent", "icp_agent", "research_agent", "ranking_agent",
            "personalization_agent", "channel_policy_agent", "proof_pack_agent",
        ),
        human_approvals=("approve_drafts", "approve_channel", "approve_proof_pack"),
        safe_tool_policy=("email_via_resend_with_approval", "linkedin_manual_only", "no_cold_whatsapp"),
        deliverables=(
            "10_opportunities",
            "10_arabic_drafts",
            "channel_recommendation",
            "risk_notes",
            "7day_followup_plan",
            "proof_pack_pdf",
        ),
        proof_metrics=(
            "opportunity_created", "draft_created", "approval_collected",
            "risk_blocked", "proof_generated",
        ),
        sla_hours=168,  # 7 days
        pricing_sar=499.0,
        pricing_label="499 ريال / 7 أيام",
        risks=("لا cold WhatsApp", "لا scraping", "لا live charge", "approval per draft"),
        upgrade_path="executive_growth_os",
        frontend_page="private-beta.html",
        tests_required=("test_growth_starter_session", "test_growth_starter_proof_pack"),
    ),
    ServiceContract(
        service_id="data_to_revenue",
        arabic_name="Data to Revenue",
        english_name="Data to Revenue",
        bundle_tier="data_to_revenue",
        target_customer="عميل عنده قائمة (CSV/CRM/Sheet) ويحتاج تنظيف + تحويل",
        pain="القائمة موجودة لكن لا تعمل — لا contactability، لا why-now، لا drafts عربية",
        promise="خلال 10 أيام: تنظيف القائمة + Top 50 targets + drafts عربية + قائمة محظورين PDPL",
        forbidden_claims=_FORBIDDEN,
        required_inputs=("data_source", "row_count", "consent_status", "ideal_customer"),
        workflow_steps=(
            "data_intake",
            "permission_classify",
            "normalize",
            "deduplicate",
            "enrich",
            "contactability_score",
            "rank_top_50",
            "draft_messages",
            "build_suppression_list",
            "proof_pack_build",
        ),
        agents_used=(
            "data_intake_agent", "compliance_agent", "enrichment_agent",
            "ranking_agent", "personalization_agent", "proof_pack_agent",
        ),
        human_approvals=("approve_consent_classification", "approve_drafts"),
        safe_tool_policy=("customer_uploaded_only", "licensed_enrichment_only", "pdpl_consent_check"),
        deliverables=(
            "cleaned_dataset",
            "top_50_targets",
            "arabic_drafts_per_target",
            "suppression_list",
            "consent_audit_log",
            "proof_pack_pdf",
        ),
        proof_metrics=(
            "records_normalized", "dedup_rate", "contactable_rate",
            "target_ranked", "draft_created", "proof_generated",
        ),
        sla_hours=240,  # 10 days
        pricing_sar=1500.0,
        pricing_label="1,500 ريال",
        risks=("PDPL consent enforced", "no licensed-data sharing", "opt-out respected"),
        upgrade_path="executive_growth_os",
        frontend_page="services.html",
        tests_required=("test_data_to_revenue_session",),
    ),
    ServiceContract(
        service_id="executive_growth_os",
        arabic_name="Executive Growth OS",
        english_name="Executive Growth OS",
        bundle_tier="growth_os",
        target_customer="مدير تنفيذي يريد تشغيل يومي + Proof أسبوعي",
        pain="لا يوجد رؤية يومية على القرارات + الفريق يعمل بدون أولويات واضحة",
        promise="يومياً: 3 قرارات للـ CEO + sales/growth/service cards + approval queue. أسبوعياً: Proof Pack",
        forbidden_claims=_FORBIDDEN,
        required_inputs=("company_name", "team_size", "ceo_email"),
        workflow_steps=(
            "daily_signals_scan",
            "card_generation_per_role",
            "approval_queue_compile",
            "weekly_proof_pack",
            "quarterly_review",
        ),
        agents_used=(
            "ceo_brief_agent", "sales_card_agent", "growth_card_agent",
            "service_card_agent", "approval_agent", "proof_pack_agent",
        ),
        human_approvals=("approve_outbound_drafts", "approve_pricing_changes", "approve_meeting_briefs"),
        safe_tool_policy=("approval_first_everywhere", "live_actions_disabled_by_default"),
        deliverables=(
            "daily_ceo_brief",
            "role_cards_feed",
            "approval_queue",
            "weekly_proof_pack",
            "quarterly_business_review",
        ),
        proof_metrics=(
            "daily_decisions_recorded", "approvals_processed",
            "weekly_proof_packs", "qbr_generated",
        ),
        sla_hours=24,  # daily cadence
        pricing_sar=2999.0,
        pricing_label="2,999 ريال / شهر",
        risks=("live actions remain off", "every outbound passes approval", "no auto-charge"),
        upgrade_path="full_growth_control_tower",
        frontend_page="growth-os.html",
        tests_required=("test_growth_os_daily_brief",),
    ),
    ServiceContract(
        service_id="partnership_growth",
        arabic_name="Partnership Growth",
        english_name="Partnership Growth Sprint",
        bundle_tier="partnership",
        target_customer="شركة تريد بناء قناة شراكات / وكالات",
        pain="لا يعرف الشركاء المناسبين + لا يوجد material احترافي للمحادثة معهم",
        promise="partner shortlist + co-branded Proof Pack + meeting briefs + revenue share tracker",
        forbidden_claims=_FORBIDDEN,
        required_inputs=("partner_kind", "value_prop_to_partner"),
        workflow_steps=(
            "partner_intake",
            "shortlist_research",
            "scorecard_build",
            "meeting_brief_per_partner",
            "co_branded_proof",
            "referral_tracker_setup",
        ),
        agents_used=(
            "partner_research_agent", "scorecard_agent",
            "meeting_brief_agent", "proof_pack_agent",
        ),
        human_approvals=("approve_partner_outreach", "approve_revenue_share_terms"),
        safe_tool_policy=("manual_outreach_only", "no_revenue_share_without_signed_agreement"),
        deliverables=(
            "partner_shortlist",
            "partner_scorecards",
            "meeting_briefs_per_partner",
            "co_branded_proof_pack",
            "referral_tracker",
        ),
        proof_metrics=(
            "partners_shortlisted", "scorecards_generated",
            "meeting_briefs_drafted", "co_branded_proof_packs",
        ),
        sla_hours=720,  # 30 days
        pricing_sar=3000.0,
        pricing_label="3,000–7,500 ريال",
        risks=("no white-label until 3 paid pilots", "no exclusivity early", "referral attribution required"),
        upgrade_path="full_growth_control_tower",
        frontend_page="agency-partner.html",
    ),
    ServiceContract(
        service_id="full_growth_control_tower",
        arabic_name="Full Growth Control Tower",
        english_name="Full Growth Control Tower",
        bundle_tier="control_tower",
        target_customer="شركات تحتاج تشغيل كامل + tenant + roles + integrations",
        pain="حجم العمليات يتطلب multi-role command center + audit logs + Saudi data residency",
        promise="onboarding 3-4 أسابيع + dedicated CSM + multi-role Command Center + custom integrations",
        forbidden_claims=_FORBIDDEN,
        required_inputs=("annual_revenue_sar", "team_size", "data_residency_required"),
        workflow_steps=(
            "scoping_call",
            "tenant_provision",
            "role_setup",
            "integrations_implement",
            "training",
            "go_live",
            "ongoing_qbrs",
        ),
        agents_used=("integration_agent", "role_factory", "ceo_brief_agent", "proof_pack_agent"),
        human_approvals=("approve_scoping_doc", "approve_go_live", "approve_data_residency_setup"),
        safe_tool_policy=("saudi_data_residency", "pdpl_audit_logs", "tenant_isolation"),
        deliverables=(
            "tenant_environment",
            "role_setup",
            "integration_implementations",
            "trained_team",
            "ongoing_qbrs",
        ),
        proof_metrics=(
            "tenant_provisioned", "roles_configured",
            "integrations_live", "qbrs_delivered",
        ),
        sla_hours=720,  # 30 days for go-live
        pricing_sar=None,
        pricing_label="Custom",
        risks=("PDPL audit logs required", "tenant isolation enforced"),
        upgrade_path=None,
        frontend_page="services.html",
    ),
)


# ── Lookups ──────────────────────────────────────────────────────


def all_contracts() -> tuple[ServiceContract, ...]:
    return CONTRACTS


def get_contract(service_id: str) -> ServiceContract | None:
    for c in CONTRACTS:
        if c.service_id == service_id:
            return c
    return None


def contract_to_dict(c: ServiceContract) -> dict[str, Any]:
    return {
        "service_id": c.service_id,
        "arabic_name": c.arabic_name,
        "english_name": c.english_name,
        "bundle_tier": c.bundle_tier,
        "target_customer": c.target_customer,
        "pain": c.pain,
        "promise": c.promise,
        "forbidden_claims": list(c.forbidden_claims),
        "required_inputs": list(c.required_inputs),
        "workflow_steps": list(c.workflow_steps),
        "agents_used": list(c.agents_used),
        "human_approvals": list(c.human_approvals),
        "safe_tool_policy": list(c.safe_tool_policy),
        "deliverables": list(c.deliverables),
        "proof_metrics": list(c.proof_metrics),
        "sla_hours": c.sla_hours,
        "pricing_sar": c.pricing_sar,
        "pricing_label": c.pricing_label,
        "risks": list(c.risks),
        "upgrade_path": c.upgrade_path,
        "frontend_page": c.frontend_page,
        "tests_required": list(c.tests_required),
        "notes": c.notes,
    }
