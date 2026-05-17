"""The 10 canonical Dealix offerings — Governed Revenue & AI Ops ladder.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: KPI language is commitment ("نلتزم"/"we commit"),
  not guarantee ("نضمن"/"guarantee"). All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

Governed Revenue & AI Ops offer ladder (catalog display order):
  Rung 0  Free Risk Score (0)
  Rung 1  7-Day Diagnostic — Starter (4,999) / Standard (9,999)
          / Executive (15,000) / Enterprise (25,000)
  Rung 2  Revenue Intelligence Sprint (25,000 floor)
  Rung 3  Governed Ops Retainer (4,999/mo floor of a 4,999-35,000 band)
  Adjacent Board Decision Memo (9,999) / Trust Pack Lite (9,999)
           / CRM & Data Readiness for AI (9,999)

Strategic mapping (roles -> offerings): docs/strategic/.
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering


_GOVERNED_REVENUE_RISK_SCORE = ServiceOffering(
    id="governed_revenue_risk_score",
    name_ar="درجة مخاطر الإيراد المحوكم وعمليات الذكاء الاصطناعي (مجاني)",
    name_en="Governed Revenue & AI Ops Risk Score (Free)",
    price_sar=0.0,
    price_unit="one_time",
    duration_days=1,
    deliverables=(
        "Governed Revenue & AI Ops risk score",
        "Sample proof pack",
        "Top-3 ranked workflow risks",
        "Recommended next rung on the ladder",
    ),
    kpi_commitment_ar="نلتزم بالتسليم خلال 24 ساعة من تعبئة النموذج.",
    kpi_commitment_en="We commit to delivery within 24 hours of form submission.",
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


_DIAGNOSTIC_STARTER = ServiceOffering(
    id="diagnostic_starter",
    name_ar="تشخيص الإيراد المحوكم وعمليات الذكاء الاصطناعي ٧ أيام — المبتدئ",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Starter",
    price_sar=4999.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Workflow map (core revenue path)",
        "Source and data-quality review",
        "Approval-boundary map",
        "Top-3 governed decisions",
        "Proof pack",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم التشخيص خلال ٧ أيام. إن لم نسلّم، نواصل العمل بدون "
        "مقابل حتى يكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the diagnostic within 7 days. If we miss it, "
        "we keep working at no charge until it is complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    ),
    customer_journey_stage="diagnostic",
)


_DIAGNOSTIC_STANDARD = ServiceOffering(
    id="diagnostic_standard",
    name_ar="تشخيص الإيراد المحوكم وعمليات الذكاء الاصطناعي ٧ أيام — القياسي",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Standard",
    price_sar=9999.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Workflow map (core + adjacent revenue paths)",
        "Source and data-quality review",
        "Approval-boundary map",
        "Evidence gaps assessment",
        "Top-3 governed decisions",
        "Proof pack",
        "Sprint recommendation",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم التشخيص خلال ٧ أيام. إن لم نسلّم، نواصل العمل بدون "
        "مقابل حتى يكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the diagnostic within 7 days. If we miss it, "
        "we keep working at no charge until it is complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    ),
    customer_journey_stage="diagnostic",
)


_DIAGNOSTIC_EXECUTIVE = ServiceOffering(
    id="diagnostic_executive",
    name_ar="تشخيص الإيراد المحوكم وعمليات الذكاء الاصطناعي ٧ أيام — التنفيذي",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Executive",
    price_sar=15000.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Workflow map across all revenue paths",
        "Source and data-quality review",
        "Approval-boundary map",
        "Evidence gaps assessment",
        "Top-3 governed decisions with owners",
        "Proof pack",
        "Sprint recommendation",
        "Executive readout session",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم التشخيص خلال ٧ أيام مع جلسة عرض تنفيذية. إن لم نسلّم، "
        "نواصل العمل بدون مقابل حتى يكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the diagnostic within 7 days with an executive "
        "readout. If we miss it, we keep working at no charge until complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    customer_journey_stage="diagnostic",
)


_DIAGNOSTIC_ENTERPRISE = ServiceOffering(
    id="diagnostic_enterprise",
    name_ar="تشخيص الإيراد المحوكم وعمليات الذكاء الاصطناعي ٧ أيام — المؤسسي",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Enterprise",
    price_sar=25000.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Workflow map across all revenue and AI ops paths",
        "Source and data-quality review (multi-system)",
        "Approval-boundary map with role matrix",
        "Evidence gaps assessment",
        "Top-3 governed decisions with owners and timelines",
        "Proof pack",
        "Sprint recommendation with phased plan",
        "Executive readout session",
        "Board-ready summary",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم التشخيص المؤسسي خلال ٧ أيام مع ملخص جاهز للمجلس. إن لم "
        "نسلّم، نواصل العمل بدون مقابل حتى يكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the enterprise diagnostic within 7 days with a "
        "board-ready summary. If we miss it, we keep working at no charge until "
        "complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    customer_journey_stage="diagnostic",
)


_REVENUE_INTELLIGENCE_SPRINT = ServiceOffering(
    id="revenue_intelligence_sprint",
    name_ar="سبرنت ذكاء الإيراد",
    name_en="Revenue Intelligence Sprint",
    price_sar=25000.0,  # floor / starting price — actual scope priced per engagement
    price_unit="one_time",
    duration_days=42,  # multi-week engagement
    deliverables=(
        "Governed revenue workflow build",
        "Source-of-truth and data-quality remediation",
        "Approval-boundary instrumentation",
        "Decision passports for the top governed workflows",
        "Proof pack with evidence trail",
        "Retainer readiness recommendation",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم سبرنت ذكاء الإيراد على مراحل متفق عليها. إن لم نلتزم "
        "بمرحلة، نواصل العمل بدون مقابل حتى تكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the Revenue Intelligence Sprint in agreed "
        "milestones. If we miss a milestone, we keep working at no charge "
        "until it is complete."
    ),
    refund_policy_ar="استرداد تناسبي للمراحل غير المسلّمة إن لم يلتزم KPI.",
    refund_policy_en="Pro-rata refund for undelivered milestones if the KPI commitment is unmet.",
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
    customer_journey_stage="sprint",
)


_GOVERNED_OPS_RETAINER = ServiceOffering(
    id="governed_ops_retainer",
    name_ar="اشتراك العمليات المحوكمة",
    name_en="Governed Ops Retainer",
    price_sar=4999.0,  # floor of a 4,999-35,000 SAR/month band — scope-priced
    price_unit="per_month",
    duration_days=120,  # 4-month minimum commitment
    deliverables=(
        "Weekly governed revenue brief",
        "Monthly value report (estimated / observed / verified)",
        "Approval queue operation",
        "Ongoing proof events",
        "Adoption score and retainer readiness review",
        "Monthly executive summary",
    ),
    kpi_commitment_ar=(
        "نلتزم بتشغيل العمليات المحوكمة وتسليم تقرير قيمة شهري. إن لم نلتزم، "
        "نواصل العمل بدون مقابل حتى نلتزم."
    ),
    kpi_commitment_en=(
        "We commit to running governed ops and delivering a monthly value "
        "report. If we miss it, we keep working at no charge until we meet it."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق KPI.",
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
    customer_journey_stage="retainer",
)


_BOARD_DECISION_MEMO = ServiceOffering(
    id="board_decision_memo",
    name_ar="مذكرة قرار المجلس",
    name_en="Board Decision Memo",
    price_sar=9999.0,  # estimate — scoped per memo
    price_unit="one_time",
    duration_days=14,
    deliverables=(
        "Board-ready decision memo",
        "Governed evidence appendix",
        "Risk and approval-boundary summary",
        "Recommended decision options with trade-offs",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم مذكرة قرار جاهزة للمجلس خلال ١٤ يومًا. إن لم نسلّم، "
        "نواصل العمل بدون مقابل حتى تكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering a board-ready decision memo within 14 days. "
        "If we miss it, we keep working at no charge until it is complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    customer_journey_stage="board",
)


_TRUST_PACK_LITE = ServiceOffering(
    id="trust_pack_lite",
    name_ar="حزمة الثقة وحوكمة الذكاء الاصطناعي — المختصرة",
    name_en="AI Governance / Trust Pack Lite",
    price_sar=9999.0,  # estimate — scoped per engagement
    price_unit="one_time",
    duration_days=14,
    deliverables=(
        "AI governance baseline assessment",
        "Trust pack document (bilingual)",
        "Approval-boundary and audit-trail review",
        "Evidence gaps and remediation list",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم حزمة الثقة خلال ١٤ يومًا. إن لم نسلّم، نواصل العمل بدون "
        "مقابل حتى تكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the Trust Pack within 14 days. If we miss it, "
        "we keep working at no charge until it is complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    customer_journey_stage="governance",
)


_CRM_DATA_READINESS = ServiceOffering(
    id="crm_data_readiness",
    name_ar="جاهزية إدارة علاقات العملاء والبيانات للذكاء الاصطناعي",
    name_en="CRM / Data Readiness for AI",
    price_sar=9999.0,  # estimate — scoped per engagement
    price_unit="one_time",
    duration_days=21,
    deliverables=(
        "CRM and data source inventory",
        "Data-quality score and cleanup plan",
        "AI-readiness gap assessment",
        "Approval-boundary and access review",
        "Proof pack with data-quality evidence",
    ),
    kpi_commitment_ar=(
        "نلتزم بتسليم تقييم جاهزية البيانات خلال ٢١ يومًا. إن لم نسلّم، نواصل "
        "العمل بدون مقابل حتى يكتمل."
    ),
    kpi_commitment_en=(
        "We commit to delivering the data-readiness assessment within 21 days. "
        "If we miss it, we keep working at no charge until it is complete."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إن لم يلتزم KPI.",
    refund_policy_en="Full 100% refund within 14 days if the KPI commitment is unmet.",
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
    customer_journey_stage="data_readiness",
)


# Canonical 10-offering registry (order = catalog display order).
OFFERINGS: tuple[ServiceOffering, ...] = (
    _GOVERNED_REVENUE_RISK_SCORE,
    _DIAGNOSTIC_STARTER,
    _DIAGNOSTIC_STANDARD,
    _DIAGNOSTIC_EXECUTIVE,
    _DIAGNOSTIC_ENTERPRISE,
    _REVENUE_INTELLIGENCE_SPRINT,
    _GOVERNED_OPS_RETAINER,
    _BOARD_DECISION_MEMO,
    _TRUST_PACK_LITE,
    _CRM_DATA_READINESS,
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All 10 offerings in catalog display order."""
    return OFFERINGS


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one offering by id, or None if not found."""
    for o in OFFERINGS:
        if o.id == service_id:
            return o
    return None
