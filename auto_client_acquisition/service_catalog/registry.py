"""The 7 canonical Dealix offerings — Wave 13 Phase 2.

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


# Canonical 7-offering registry (order = catalog display order)
OFFERINGS: tuple[ServiceOffering, ...] = (
    _FREE_DIAGNOSTIC,
    _REVENUE_PROOF_SPRINT,
    _DATA_TO_REVENUE_PACK,
    _GROWTH_OPS_MONTHLY,
    _SUPPORT_OS_ADDON,
    _EXECUTIVE_COMMAND_CENTER,
    _AGENCY_PARTNER_OS,
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All 7 offerings in catalog display order."""
    return OFFERINGS


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one offering by id, or None if not found."""
    for o in OFFERINGS:
        if o.id == service_id:
            return o
    return None
