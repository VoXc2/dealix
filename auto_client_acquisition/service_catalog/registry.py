"""The 12 canonical Dealix offerings — Wave 13 Phase 2 + Enterprise tier.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: KPI language is commitment ("نشتغل بدون مقابل لو لم يتحقق…"),
  not guarantee ("نضمن"). All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

Pricing ladder (must be ascending for paid services):
  Free Diagnostic (0) → Sprint (499) → Data-to-Revenue (1500)
  → Growth Ops (2999/mo) → Support Add-on (1500/mo) → ECC (7500/mo)
  → Agency Partner OS (custom)

Enterprise tier (custom-priced, customer_journey_stage="enterprise"). These
unlock only after >=3 documented proof packs from the lower ladder; until the
DEALIX_READINESS gates pass they are tracked as Planned in
dealix/registers/no_overclaim.yaml and listed under "Do Not Sell Yet":
  Enterprise AI Operating System · AI Revenue Transformation
  · Company Brain & Knowledge OS · AI Governance & Trust Program
  · Executive Intelligence & Command Center

Strategic mapping (roles → offerings): docs/strategic/DEALIX_ROLE_SERVICE_LADDER_AR.md
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering

_FREE_DIAGNOSTIC = ServiceOffering(
    id="free_mini_diagnostic",
    name_ar="التشخيص المجاني المختصر",
    name_en="Free Mini Diagnostic",
    price_sar=0.0,
    price_unit="one_time",
    duration_days=1,
    deliverables=(
        "1-page sector-fit analysis",
        "3 ranked opportunities",
        "1 Arabic message draft",
        "1 best channel recommendation",
        "1 risk to avoid",
        "1 next-step decision passport",
    ),
    kpi_commitment_ar="نسلّم خلال 24 ساعة من تعبئة النموذج.",
    kpi_commitment_en="Delivered within 24 hours of form submission.",
    refund_policy_ar="مجاني — لا يوجد دفع.",
    refund_policy_en="Free — no payment.",
    action_modes_used=("suggest_only", "draft_only"),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_scraping",
        "no_fake_proof",
    ),
    customer_journey_stage="discovery",
)


_REVENUE_PROOF_SPRINT = ServiceOffering(
    id="revenue_proof_sprint_499",
    name_ar="سبرنت إثبات الإيرادات (٤٩٩ ر.س)",
    name_en="499 SAR Revenue Proof Sprint",
    price_sar=499.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Company Brain v1",
        "Top 10 Opportunities (ranked)",
        "Decision Passports for top 3",
        "Arabic Draft Pack (5 messages)",
        "Follow-up Plan (7-day timeline)",
        "Risk + Objection Map",
        "Executive Pack",
        "Proof Pack",
        "Next Best Offer recommendation",
    ),
    kpi_commitment_ar=(
        "نسلّم ٧ مخرجات في ٧ أيام. إذا لم يصل عدد الفرص ≥١٠، "
        "نشتغل بدون مقابل حتى نوصل."
    ),
    kpi_commitment_en=(
        "7 deliverables in 7 days. If we don't surface ≥10 opportunities, "
        "we work for free until we do."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا، بدون أسئلة.",
    refund_policy_en="Full 100% refund within 14 days, no questions asked.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
    ),
    customer_journey_stage="first_paid",
)


_DATA_TO_REVENUE_PACK = ServiceOffering(
    id="data_to_revenue_pack_1500",
    name_ar="حزمة من البيانات إلى الإيراد (١٥٠٠ ر.س)",
    name_en="Data-to-Revenue Pack",
    price_sar=1500.0,
    price_unit="one_time",
    duration_days=14,
    deliverables=(
        "Clean Lead Board (deduplicated)",
        "Duplicate Report",
        "Source Validation Report",
        "Risk Report",
        "Top 20 Opportunities (scored)",
        "10 Arabic Drafts",
        "Follow-up Plan",
        "Decision Passports for top 5",
    ),
    kpi_commitment_ar=(
        "تنظيف ٤٠٠+ سطر في ١٤ يومًا. إذا لم نصل لـ٢٠ فرصة معتمدة، "
        "نواصل العمل حتى نوصل."
    ),
    kpi_commitment_en=(
        "Clean 400+ rows in 14 days. If we don't surface 20 approved "
        "opportunities, we work until we do."
    ),
    refund_policy_ar="استرداد ٧٥٪ إذا لم يتحقق التزام KPI خلال ٢١ يومًا.",
    refund_policy_en="75% refund if KPI commitment unmet within 21 days.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
    ),
    customer_journey_stage="expansion",
)


_GROWTH_OPS_MONTHLY = ServiceOffering(
    id="growth_ops_monthly_2999",
    name_ar="عمليات النمو الشهرية (٢٩٩٩ ر.س / شهر)",
    name_en="Growth Ops Monthly",
    price_sar=2999.0,
    price_unit="per_month",
    duration_days=120,  # 4-month minimum commitment
    deliverables=(
        "4 Weekly Pipeline Audits",
        "Weekly Lead Board",
        "Approval Queue (daily)",
        "Draft Pack (≥20 messages/month)",
        "Support Insights",
        "Proof Events (ongoing)",
        "Monthly Proof Pack",
        "Monthly Executive Summary",
        "Expansion Recommendation",
    ),
    kpi_commitment_ar=(
        "نلتزم بزيادة معدل الردود +٢٠٪ خلال ٤ أشهر. "
        "إن لم يتحقق، نشتغل بدون مقابل حتى يتحقق."
    ),
    kpi_commitment_en=(
        "Commit to +20% reply-rate lift in 4 months. "
        "If not reached, we work for free until reached."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق KPI.",
    refund_policy_en="Pro-rata refund of unused months if KPI commitment unmet.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
        "no_blast",
    ),
    customer_journey_stage="monthly",
)


_SUPPORT_OS_ADDON = ServiceOffering(
    id="support_os_addon_1500",
    name_ar="دعم Support OS (١٥٠٠ ر.س / شهر)",
    name_en="Support OS Add-on",
    price_sar=1500.0,
    price_unit="per_month",
    duration_days=30,
    deliverables=(
        "Ticket Classification (12 categories)",
        "Suggested Replies (draft_only)",
        "Escalation List (weekly)",
        "Root Cause Map",
        "Customer Health Score updates",
        "Support Proof Events",
        "SLA breach alerts",
    ),
    kpi_commitment_ar=(
        "نقلّل وقت الرد الأول إلى ≤٣٠ دقيقة في ساعات العمل. "
        "إن لم يتحقق، اشتراكان مجانيان."
    ),
    kpi_commitment_en=(
        "Reduce first-response time to ≤30 min business hours. "
        "If unmet, 2 free months."
    ),
    refund_policy_ar="استرداد ١٠٠٪ في الشهر الأول إذا لم يلتزم KPI.",
    refund_policy_en="100% refund in month 1 if KPI commitment unmet.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_scraping",
        "no_fake_proof",
    ),
    customer_journey_stage="support_addon",
)


_EXECUTIVE_COMMAND_CENTER = ServiceOffering(
    id="executive_command_center_7500",
    name_ar="غرفة قيادة الإدارة (٧٥٠٠ ر.س / شهر)",
    name_en="Executive Command Center",
    price_sar=7500.0,
    price_unit="per_month",
    duration_days=120,
    deliverables=(
        "Daily founder brief (WhatsApp)",
        "Weekly Pipeline Audit",
        "Monthly board pack",
        "Revenue Radar (live)",
        "Sales Pipeline view",
        "Growth Signals dashboard",
        "Support Health overview",
        "Delivery Progress tracker",
        "Payment State view",
        "Proof Ledger access",
        "Approval Queue (daily)",
        "Risk register (weekly)",
        "Next 7 days plan",
    ),
    kpi_commitment_ar=(
        "نوفر للإدارة ٤٠٪+ من وقت اتخاذ القرار خلال ٤ أشهر. "
        "إن لم يتحقق، شهر مجاني."
    ),
    kpi_commitment_en=(
        "Save executive 40%+ of decision time in 4 months. "
        "If unmet, 1 free month."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة.",
    refund_policy_en="Pro-rata refund of unused months.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
        "no_blast",
    ),
    customer_journey_stage="executive",
)


_AGENCY_PARTNER_OS = ServiceOffering(
    id="agency_partner_os",
    name_ar="نظام الشريك الوكالة",
    name_en="Agency Partner OS",
    price_sar=0.0,  # custom — actual price set per partnership
    price_unit="custom",
    duration_days=0,  # ongoing
    deliverables=(
        "Partner Intake doc",
        "Co-branded Diagnostic",
        "Client Proof Sprint (per client)",
        "Proof Pack (per client)",
        "Renewal / Upsell Pack",
        "Partner Revenue Tracking",
        "30% commission tracking",
    ),
    kpi_commitment_ar=(
        "نلتزم بـ٣٠٪ عمولة لأول سنة من كل عميل محوّل. "
        "ولا نشر proof بدون موافقة موقّعة."
    ),
    kpi_commitment_en=(
        "30% commission for first paid year per referred customer. "
        "Never publish proof without signed consent."
    ),
    refund_policy_ar="عقد رسمي بشروط الإلغاء — يتم بمراجعة قانونية.",
    refund_policy_en="Formal contract with cancellation terms — lawyer-reviewed.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
        "no_blast",
    ),
    customer_journey_stage="channel",
)


# ═══════════════════════════════════════════════════════════════════
# Enterprise tier — custom-priced six-figure engagements.
# Status: Planned (see dealix/registers/no_overclaim.yaml). Not sellable
# until the DEALIX_READINESS gates pass; listed under "Do Not Sell Yet".
# ═══════════════════════════════════════════════════════════════════

_ENTERPRISE_AI_OPERATING_SYSTEM = ServiceOffering(
    id="enterprise_ai_operating_system",
    name_ar="نظام التشغيل المؤسسي بالذكاء الاصطناعي",
    name_en="Enterprise AI Operating System",
    price_sar=0.0,
    price_unit="custom",
    duration_days=90,
    price_sar_min=75_000.0,
    price_sar_max=250_000.0,
    monthly_fee_sar_min=15_000.0,
    monthly_fee_sar_max=60_000.0,
    deliverables=(
        "AI Opportunity Map + 30/60/90 roadmap",
        "Company Brain v1 (knowledge base + citations)",
        "Sales / Support / Operations AI agents (draft-first)",
        "Executive Command Center dashboard",
        "Approval workflows + append-only audit trail",
        "CRM / WhatsApp / Email / Drive integration contracts",
        "ROI dashboard wired to the value ledger",
        "Governance policy pack + risk register",
        "Monthly Proof Pack + optimization cycle",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم برنامج التحول في ٩٠ يومًا عبر ٥ مراحل ببوابات تحقق. "
        "إن لم تُجتَز بوابة مرحلة، نواصل العمل على تلك المرحلة بدون مقابل."
    ),
    kpi_commitment_en=(
        "We commit to a 90-day transformation across 5 gated phases. "
        "If a phase gate is not met, we keep working that phase at no charge."
    ),
    refund_policy_ar="عقد مرحلي؛ كل مرحلة تُدفع عند اجتياز بوابتها — مراجعة قانونية.",
    refund_policy_en="Phased contract; each phase invoiced on gate pass — lawyer-reviewed.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
        "no_blast",
    ),
    customer_journey_stage="enterprise",
)


_AI_REVENUE_TRANSFORMATION = ServiceOffering(
    id="ai_revenue_transformation",
    name_ar="تحويل الإيرادات بالذكاء الاصطناعي",
    name_en="AI Revenue Transformation",
    price_sar=0.0,
    price_unit="custom",
    duration_days=60,
    price_sar_min=35_000.0,
    price_sar_max=100_000.0,
    monthly_fee_sar_min=10_000.0,
    monthly_fee_sar_max=40_000.0,
    deliverables=(
        "ICP analysis + lead-machine design",
        "Lead scoring + enrichment model",
        "Outbound strategy + Arabic sales messaging",
        "WhatsApp / Email follow-up workflows (draft-first)",
        "CRM pipeline build + AI follow-up",
        "Executive revenue dashboard",
        "Proof Pack + monthly ROI report",
    ),
    kpi_commitment_ar=(
        "نلتزم ببناء نظام مبيعات يكشف ويؤهل ويتابع الفرص بمؤشرات قابلة للقياس. "
        "إن لم تتحسن مؤشرات الـ pipeline المتفق عليها، نواصل بدون مقابل."
    ),
    kpi_commitment_en=(
        "We commit to a revenue system that surfaces, qualifies and follows up "
        "leads with measurable KPIs. If the agreed pipeline KPIs do not improve, "
        "we keep working at no charge."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق التزام KPI.",
    refund_policy_en="Pro-rata refund of unused months if the KPI commitment is unmet.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
        "no_blast",
    ),
    customer_journey_stage="enterprise",
)


_COMPANY_BRAIN_KNOWLEDGE_OS = ServiceOffering(
    id="company_brain_knowledge_os",
    name_ar="عقل الشركة ونظام المعرفة",
    name_en="Company Brain & Knowledge OS",
    price_sar=0.0,
    price_unit="custom",
    duration_days=60,
    price_sar_min=40_000.0,
    price_sar_max=150_000.0,
    monthly_fee_sar_min=8_000.0,
    monthly_fee_sar_max=35_000.0,
    deliverables=(
        "Document ingestion + knowledge base build",
        "Retrieval with citations + confidence scores",
        "Role-based access controls",
        "Internal employee / sales / support assistants",
        "Board + executive summaries with source tracking",
        "No-source-no-answer enforcement",
        "Eval report + usage dashboard",
    ),
    kpi_commitment_ar=(
        "نلتزم بأن كل إجابة تأتي بمصدر ودرجة ثقة وصلاحية وسجل تدقيق، "
        "ومنع الإجابة عند غياب الدليل. إن لم يتحقق معيار الجودة، نواصل بدون مقابل."
    ),
    kpi_commitment_en=(
        "We commit that every answer carries a source, confidence, permission "
        "and audit record, and is withheld when no evidence exists. If the "
        "quality bar is not met, we keep working at no charge."
    ),
    refund_policy_ar="استرداد ٧٥٪ إذا لم يتحقق التزام جودة الاسترجاع خلال ٣٠ يومًا.",
    refund_policy_en="75% refund if the retrieval-quality commitment is unmet within 30 days.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_scraping",
        "no_fake_proof",
        "no_sourceless_answer",
    ),
    customer_journey_stage="enterprise",
)


_AI_GOVERNANCE_TRUST_PROGRAM = ServiceOffering(
    id="ai_governance_trust_program",
    name_ar="برنامج حوكمة وثقة الذكاء الاصطناعي",
    name_en="AI Governance & Trust Program",
    price_sar=0.0,
    price_unit="custom",
    duration_days=45,
    price_sar_min=50_000.0,
    price_sar_max=180_000.0,
    deliverables=(
        "Company AI policy + AI risk matrix",
        "Approval classes + data-handling rules",
        "Employee AI usage rules",
        "Audit logging + human-approval workflows",
        "PDPL readiness assessment",
        "Vendor / model risk review",
        "Executive governance dashboard",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم إطار حوكمة قابل للتدقيق ومتوافق مع نظام حماية البيانات. "
        "إن لم يجتز مراجعة الجاهزية المتفق عليها، نواصل بدون مقابل."
    ),
    kpi_commitment_en=(
        "We commit to an auditable, PDPL-aligned governance framework. "
        "If it does not pass the agreed readiness review, we keep working "
        "at no charge."
    ),
    refund_policy_ar="عقد مرحلي بمراجعة جاهزية؛ مراجعة قانونية لشروط الإلغاء.",
    refund_policy_en="Phased contract with a readiness review; cancellation terms lawyer-reviewed.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_scraping",
        "no_fake_proof",
    ),
    customer_journey_stage="enterprise",
)


_EXECUTIVE_INTELLIGENCE_CENTER = ServiceOffering(
    id="executive_intelligence_center",
    name_ar="مركز الذكاء والقيادة التنفيذي",
    name_en="Executive Intelligence & Command Center",
    price_sar=0.0,
    price_unit="custom",
    duration_days=0,  # ongoing, retainer-led
    price_sar_min=80_000.0,
    price_sar_max=250_000.0,
    monthly_fee_sar_min=20_000.0,
    monthly_fee_sar_max=70_000.0,
    deliverables=(
        "Revenue + customer-health + operational-risk signals",
        "Strategic / partnership / expansion opportunity radar",
        "AI recommendations + decision memos",
        "Approval queue",
        "Weekly executive brief",
        "Quarterly growth strategy",
        "Proof Ledger access",
    ),
    kpi_commitment_ar=(
        "نلتزم بتوفير وقت اتخاذ القرار للإدارة عبر مؤشرات وقرارات مرتبطة بالنتائج. "
        "إن لم يتحقق التزام التوفير المتفق عليه، نواصل بدون مقابل."
    ),
    kpi_commitment_en=(
        "We commit to saving executive decision time via signals and "
        "outcome-linked decisions. If the agreed time-saving commitment is "
        "unmet, we keep working at no charge."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة.",
    refund_policy_en="Pro-rata refund of unused months.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(
        "no_live_send",
        "no_live_charge",
        "no_cold_whatsapp",
        "no_linkedin_auto",
        "no_scraping",
        "no_fake_proof",
        "no_fake_revenue",
        "no_blast",
    ),
    customer_journey_stage="enterprise",
)


# Canonical 12-offering registry (order = catalog display order)
OFFERINGS: tuple[ServiceOffering, ...] = (
    _FREE_DIAGNOSTIC,
    _REVENUE_PROOF_SPRINT,
    _DATA_TO_REVENUE_PACK,
    _GROWTH_OPS_MONTHLY,
    _SUPPORT_OS_ADDON,
    _EXECUTIVE_COMMAND_CENTER,
    _AGENCY_PARTNER_OS,
    _ENTERPRISE_AI_OPERATING_SYSTEM,
    _AI_REVENUE_TRANSFORMATION,
    _COMPANY_BRAIN_KNOWLEDGE_OS,
    _AI_GOVERNANCE_TRUST_PROGRAM,
    _EXECUTIVE_INTELLIGENCE_CENTER,
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)

# Enterprise-tier service ids (customer_journey_stage == "enterprise").
ENTERPRISE_SERVICE_IDS: frozenset[str] = frozenset(
    o.id for o in OFFERINGS if o.customer_journey_stage == "enterprise"
)


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All 12 offerings in catalog display order."""
    return OFFERINGS


def list_enterprise_offerings() -> tuple[ServiceOffering, ...]:
    """The enterprise-tier offerings only, in catalog display order."""
    return tuple(o for o in OFFERINGS if o.customer_journey_stage == "enterprise")


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one offering by id, or None if not found."""
    for o in OFFERINGS:
        if o.id == service_id:
            return o
    return None
