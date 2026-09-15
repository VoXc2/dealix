"""The 17 canonical Dealix offerings — Wave 13 Phase 2 + Transformation OS.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: KPI language covers controllable delivery and measurement only.
  Customer outcomes require a first-party baseline; no open-ended free-work promise.
  All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

First-launch motion:
  Free Diagnostic → Revenue Command Pilot (customer-specific duration, quote-only after discovery).
  Every other price remains an internal experiment or future catalogue entry
  until a separate approval changes ``commercial_status``.

Enterprise Transformation OS (customer_journey_stage="transformation"): 10
higher-value systems sold to enterprises that need measurable transformation
across sales, operations, brand, customer experience, automation, reporting,
governance, and bespoke builds. These are NOT a linear funnel — they are a
menu. Their pricing is a *range* (price_sar = setup floor / billable anchor,
price_sar_max = setup ceiling) plus a recurring monthly range
(price_monthly_sar_min/max). Every figure is an estimate. "Growth Engine OS"
is modeled draft-only/approval-gated — never cold outreach or automation.
Positioning: docs/transformation/DEALIX_TRANSFORMATION_OS_MASTER_AR.md

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
    commercial_status="free_entry",
)


_REVENUE_COMMAND_PILOT = ServiceOffering(
    id="revenue_command_pilot_30d",
    name_ar="تجربة مركز قيادة الإيرادات — مدة مخصصة للحالة",
    name_en="Revenue Command Pilot — customer-specific duration",
    price_sar=0.0,
    price_unit="custom",
    duration_days=None,
    duration_policy="customer_specific_after_qualified_discovery",
    deliverables=(
        "Company Brain v1",
        "One ICP",
        "One revenue workflow",
        "One approval queue",
        "One operational baseline",
        "Weekly proof pack",
        "End-of-pilot stop, extend, or redesign decision",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم النطاق المكتوب بعد جلسة الاكتشاف وقياس خط أساس تشغيلي؛ "
        "الإيراد وعدد المبيعات خارج نطاق الالتزام."
    ),
    kpi_commitment_en=(
        "We deliver the written post-discovery scope and an operational baseline; "
        "revenue and sales counts are outside the commitment."
    ),
    refund_policy_ar="السعر والنطاق وشروط المعالجة تحدد في عرض موثق بعد الاكتشاف.",
    refund_policy_en=(
        "Price, scope, and remedy terms are documented in a quote after discovery."
    ),
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
    commercial_status="quote_only",
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
        "نلتزم بتنظيف البيانات المتفق عليها وتوثيق التكرار والمصدر والجودة، "
        "ولا نعد بعدد فرص دون اعتماد العميل."
    ),
    kpi_commitment_en=(
        "We clean the agreed dataset and document duplicates, provenance, and "
        "quality; no opportunity count is promised without customer validation."
    ),
    refund_policy_ar="تُحدد معالجة عدم تسليم النطاق في أمر العمل المعتمد، ولا ترتبط بنتيجة تجارية غير مضمونة.",
    refund_policy_en=(
        "Remedies for undelivered scope are defined in the approved order form "
        "and are separate from business outcomes."
    ),
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
        "نلتزم بإيقاع تشغيلي أسبوعي، ومسودات خاضعة للموافقة، وقياس خط أساس "
        "ونتيجة؛ أي تحسن في الردود فرضية تُقاس ولا تُضمن."
    ),
    kpi_commitment_en=(
        "We deliver a weekly operating cadence, approval-gated drafts, and "
        "baseline/after measurement; reply-rate lift is a measured hypothesis."
    ),
    refund_policy_ar="تُحدد الإلغاء والاسترداد ورصيد الخدمة في العقد المعتمد وفق النطاق المسلّم.",
    refund_policy_en="Cancellation, refund, and service-credit terms are defined in the approved contract against delivered scope.",
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
        "نلتزم بتصنيف التذاكر ومسودات الرد والتنبيهات وقياس زمن الاستجابة؛ "
        "أي هدف زمني يعتمد في أمر العمل بعد baseline."
    ),
    kpi_commitment_en=(
        "We deliver ticket classification, reply drafts, alerts, and response-time "
        "measurement; any time target is approved after baseline."
    ),
    refund_policy_ar="تُحدد معالجة إخفاق التسليم في أمر العمل؛ أهداف الخدمة تحتاج baseline واعتمادًا صريحًا.",
    refund_policy_en="Remedies for delivery failure are defined in the order form; service targets require a baseline and explicit approval.",
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
        "نلتزم بقراءة تنفيذية وسجل قرار ومخاطر وإجراء تالٍ؛ وفر الوقت يُقاس "
        "من baseline العميل ولا يُضمن."
    ),
    kpi_commitment_en=(
        "We deliver an executive readout, decision/risk log, and next-action "
        "cadence; time savings are measured from the customer baseline."
    ),
    refund_policy_ar="تُحدد الإلغاء والاسترداد ورصيد الخدمة في العقد المعتمد وفق النطاق المسلّم.",
    refund_policy_en="Cancellation, refund, and service-credit terms follow the approved contract and delivered scope.",
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


# ═══════════════════════════════════════════════════════════════════════
# Enterprise Transformation OS — 10 systems (customer_journey_stage =
# "transformation"). Setup is a range (price_sar = floor, price_sar_max =
# ceiling); monthly is a range (price_monthly_sar_min/max). All estimates.
# ═══════════════════════════════════════════════════════════════════════

# Shared gate baseline — also satisfies the commercial-map contract
# (every offer must enforce no_cold_whatsapp + no_scraping + no_fake_proof)
# and the catalog contract (no_live_send + no_live_charge + no_fake_proof).
_TX_GATES_BASE: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp",
    "no_scraping",
    "no_fake_proof",
    "no_fake_revenue",
)


_AI_COMMAND_CENTER_OS = ServiceOffering(
    id="ai_command_center_os",
    name_ar="مركز القيادة الذكي للأعمال",
    name_en="AI Business Command Center",
    price_sar=35000.0,
    price_sar_max=120000.0,
    price_monthly_sar_min=8000.0,
    price_monthly_sar_max=35000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=60,
    deliverables=(
        "Executive command dashboard (Arabic-first)",
        "Daily action board across sales / follow-up / reviews / proposals",
        "Weekly executive report",
        "KPI definitions + semantic metric layer",
        "Team operating cadence",
        "Approval queue wired to governance",
    ),
    kpi_commitment_ar=(
        "نلتزم بإطلاق رؤية يومية موحّدة للإدارة خلال مدة الإعداد. "
        "الأسعار نطاقات تقديرية تُحدَّد بعد جلسة تشخيص مدفوعة."
    ),
    kpi_commitment_en=(
        "We commit to a unified daily executive view live within the setup window. "
        "Prices are estimate ranges, finalized after a paid diagnostic."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(*_TX_GATES_BASE, "no_blast"),
    customer_journey_stage="transformation",
)


_WHATSAPP_REVENUE_OS = ServiceOffering(
    id="whatsapp_revenue_os",
    name_ar="نظام إيرادات واتساب",
    name_en="WhatsApp Revenue OS",
    price_sar=12000.0,
    price_sar_max=45000.0,
    price_monthly_sar_min=3000.0,
    price_monthly_sar_max=15000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=30,
    deliverables=(
        "Lead intake model + pipeline stages",
        "Follow-up task system (approval-gated drafts)",
        "Approved message templates (draft_only)",
        "Booking + reporting flow",
        "Lost-reason analysis",
        "Weekly pipeline report",
    ),
    kpi_commitment_ar=(
        "نلتزم بتحويل واتساب إلى pipeline قابل للقياس خلال مدة الإعداد. "
        "كل رسالة خارجية مسودة تتطلب موافقة — لا إرسال بارد ولا أتمتة."
    ),
    kpi_commitment_en=(
        "We commit to turning WhatsApp into a measurable pipeline within the setup "
        "window. Every external message is an approval-gated draft — no cold send, no automation."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(*_TX_GATES_BASE, "no_linkedin_auto", "no_blast"),
    customer_journey_stage="transformation",
)


_BRAND_INTELLIGENCE_OS = ServiceOffering(
    id="brand_intelligence_os",
    name_ar="نظام ذكاء العلامة التجارية",
    name_en="Brand Intelligence OS",
    price_sar=15000.0,
    price_sar_max=60000.0,
    price_monthly_sar_min=4000.0,
    price_monthly_sar_max=18000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=45,
    deliverables=(
        "Brand strategy + positioning map",
        "Visual identity direction",
        "Tone-of-voice system (AR + EN)",
        "Offer messaging bank",
        "Content pillars + social / landing templates",
        "Brand-safe AI prompt library",
        "Content approval workflow",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم نظام هوية موحّد قابل لإعادة الاستخدام خلال مدة الإعداد. "
        "الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to a reusable, unified brand operating system within the setup "
        "window. Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=_TX_GATES_BASE,
    customer_journey_stage="transformation",
)


_AI_AGENT_WORKFORCE_OS = ServiceOffering(
    id="ai_agent_workforce_os",
    name_ar="نظام قوى العمل من وكلاء الذكاء الاصطناعي",
    name_en="AI Agent Workforce OS",
    price_sar=40000.0,
    price_sar_max=180000.0,
    price_monthly_sar_min=12000.0,
    price_monthly_sar_max=60000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=90,
    deliverables=(
        "Agent role map + task boundaries",
        "Human approval gates for high-risk actions",
        "Agent prompts + allowed tools registry",
        "Audit log structure",
        "Weekly agent performance review",
        "Cost + usage monitoring model",
    ),
    kpi_commitment_ar=(
        "نلتزم بنشر وكلاء بأدوار وحدود وصلاحيات واضحة ومراجعة بشرية للإجراءات "
        "الحساسة. لا تنفيذ خارجي تلقائي. الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to role-scoped agents with clear boundaries, permissions, and "
        "human approval on sensitive actions. No autonomous external execution. "
        "Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(*_TX_GATES_BASE, "no_blast"),
    customer_journey_stage="transformation",
)


_CLIENT_EXPERIENCE_OS = ServiceOffering(
    id="client_experience_os",
    name_ar="نظام تجربة العميل",
    name_en="Client Experience OS",
    price_sar=20000.0,
    price_sar_max=80000.0,
    price_monthly_sar_min=6000.0,
    price_monthly_sar_max=25000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=60,
    deliverables=(
        "Customer journey map (first contact → repeat purchase)",
        "Onboarding workflow",
        "Support workflow",
        "Feedback / review capture loop",
        "Retention dashboard",
        "Escalation system",
    ),
    kpi_commitment_ar=(
        "نلتزم بتوحيد رحلة العميل من أول تواصل إلى إعادة الشراء خلال مدة الإعداد. "
        "الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to a unified customer journey from first contact to repeat "
        "purchase within the setup window. Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_TX_GATES_BASE,
    customer_journey_stage="transformation",
)


_OPERATIONS_AUTOMATION_OS = ServiceOffering(
    id="operations_automation_os",
    name_ar="نظام أتمتة العمليات",
    name_en="Operations Automation OS",
    price_sar=25000.0,
    price_sar_max=120000.0,
    price_monthly_sar_min=7000.0,
    price_monthly_sar_max=35000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=75,
    deliverables=(
        "Workflow map + automation blueprint",
        "Approval matrix",
        "Alerts + reminders",
        "Operations dashboard",
        "SOP library",
        "Handoff + escalation flows",
    ),
    kpi_commitment_ar=(
        "نلتزم بأتمتة العمليات المتكررة بحوكمة وتنبيهات ولوحات خلال مدة الإعداد. "
        "نُخرِّط أولاً ثم نؤتمت — لا نؤتمت الفوضى. الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to automating repeatable operations with governance, alerts, and "
        "dashboards within the setup window. Map first, then automate — never automate "
        "chaos. Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_TX_GATES_BASE,
    customer_journey_stage="transformation",
)


_EXECUTIVE_REPORTING_OS = ServiceOffering(
    id="executive_reporting_os",
    name_ar="نظام التقارير التنفيذية",
    name_en="Executive Reporting OS",
    price_sar=18000.0,
    price_sar_max=75000.0,
    price_monthly_sar_min=5000.0,
    price_monthly_sar_max=20000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=45,
    deliverables=(
        "KPI model + data source map",
        "Weekly report template",
        "Monthly executive pack",
        "Insights + recommendations layer",
        "Decision tracker",
    ),
    kpi_commitment_ar=(
        "نلتزم بتحويل بيانات التشغيل إلى تقارير تنفيذية أسبوعية وشهرية تربط بالقرار "
        "خلال مدة الإعداد. الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to converting operational data into weekly + monthly executive "
        "reports tied to decisions within the setup window. Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=_TX_GATES_BASE,
    customer_journey_stage="transformation",
)


_TRUST_GOVERNANCE_OS = ServiceOffering(
    id="trust_governance_os",
    name_ar="نظام الثقة وحوكمة الذكاء الاصطناعي",
    name_en="Trust & AI Governance OS",
    price_sar=30000.0,
    price_sar_max=150000.0,
    price_monthly_sar_min=10000.0,
    price_monthly_sar_max=50000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=60,
    deliverables=(
        "AI usage policy",
        "Data handling map",
        "Agent risk register",
        "Approval matrix",
        "Monitoring checklist",
        "Incident response runbook",
        "Vendor / tool register",
    ),
    kpi_commitment_ar=(
        "نلتزم ببناء حوكمة عملية للذكاء الاصطناعي والبيانات متوائمة مع PDPL "
        "وإدارة المخاطر، قابلة للتطبيق التشغيلي. الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to practical AI + data governance aligned with PDPL and risk "
        "management, enforceable operationally. Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(*_TX_GATES_BASE, "no_blast"),
    customer_journey_stage="transformation",
)


_GROWTH_ENGINE_OS = ServiceOffering(
    id="growth_engine_os",
    name_ar="نظام محرك النمو",
    name_en="Growth Engine OS",
    price_sar=25000.0,
    price_sar_max=100000.0,
    price_monthly_sar_min=8000.0,
    price_monthly_sar_max=30000.0,
    price_unit="one_time",
    setup_is_range=True,
    duration_days=60,
    deliverables=(
        "ICP map + prospecting workflow",
        "Approved-draft outreach packs (draft_only, approval-gated)",
        "Offer ladder + demo script",
        "Proposal templates",
        "Warm-intro drafts (approval-gated)",
        "Pipeline report",
    ),
    kpi_commitment_ar=(
        "نلتزم ببناء آلة نمو قابلة للتكرار عبر مسودات معتمدة فقط. "
        "لا واتساب بارد ولا أتمتة LinkedIn ولا إرسال جماعي ولا scraping. "
        "الأسعار نطاقات تقديرية."
    ),
    kpi_commitment_en=(
        "We commit to a repeatable growth machine built on approved drafts only. "
        "No cold WhatsApp, no LinkedIn automation, no blast, no scraping. "
        "Prices are estimate ranges."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلَّمة وفق بنود العقد.",
    refund_policy_en="Pro-rata refund for undelivered milestones per the contract.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=(*_TX_GATES_BASE, "no_linkedin_auto", "no_blast"),
    customer_journey_stage="transformation",
)


_CUSTOM_ENTERPRISE_SYSTEM = ServiceOffering(
    id="custom_enterprise_system",
    name_ar="نظام مؤسسي مخصص",
    name_en="Custom Enterprise System",
    price_sar=0.0,  # custom — setup range 100,000–500,000+ SAR set per scope
    price_sar_max=None,
    price_monthly_sar_min=25000.0,
    price_monthly_sar_max=None,
    price_unit="custom",
    setup_is_range=False,
    duration_days=0,  # scoped per engagement
    deliverables=(
        "Paid discovery sprint",
        "Solution architecture",
        "UX / workflow prototype",
        "Backend / API blueprint",
        "Dashboards + automations",
        "Integrations",
        "Training + SLA",
    ),
    kpi_commitment_ar=(
        "نلتزم ببناء نظام تشغيل مخصص حول عمليات الشركة وبياناتها وفريقها، "
        "يبدأ بجلسة تشخيص مدفوعة. النطاق ٠٠٠ر١٠٠–٠٠٠ر٥٠٠+ تقديري يُحدَّد بالعقد."
    ),
    kpi_commitment_en=(
        "We commit to a bespoke operating system built around the company's "
        "workflows, data, and team — starting with a paid discovery sprint. "
        "Scope 100,000–500,000+ SAR is an estimate, set in the contract."
    ),
    refund_policy_ar="عقد رسمي بشروط دفع على مراحل ومراجعة قانونية.",
    refund_policy_en="Formal milestone-based contract, lawyer-reviewed.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=(*_TX_GATES_BASE, "no_blast"),
    customer_journey_stage="transformation",
)


# Canonical 17-offering registry (order = catalog display order).
# Core funnel (7) first, then Enterprise Transformation OS (10).
OFFERINGS: tuple[ServiceOffering, ...] = (
    _FREE_DIAGNOSTIC,
    _REVENUE_COMMAND_PILOT,
    _DATA_TO_REVENUE_PACK,
    _GROWTH_OPS_MONTHLY,
    _SUPPORT_OS_ADDON,
    _EXECUTIVE_COMMAND_CENTER,
    _AGENCY_PARTNER_OS,
    # ── Enterprise Transformation OS ──
    _AI_COMMAND_CENTER_OS,
    _WHATSAPP_REVENUE_OS,
    _BRAND_INTELLIGENCE_OS,
    _AI_AGENT_WORKFORCE_OS,
    _CLIENT_EXPERIENCE_OS,
    _OPERATIONS_AUTOMATION_OS,
    _EXECUTIVE_REPORTING_OS,
    _TRUST_GOVERNANCE_OS,
    _GROWTH_ENGINE_OS,
    _CUSTOM_ENTERPRISE_SYSTEM,
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All 17 offerings in catalog display order (7 core funnel + 10 transformation)."""
    return OFFERINGS


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one offering by id, or None if not found."""
    for o in OFFERINGS:
        if o.id == service_id:
            return o
    return None
