"""The canonical Dealix offerings — Revenue Autopilot offer model.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.

The Revenue Autopilot sells ONE primary offer — the 7-Day Governed Revenue
& AI Ops Diagnostic, at three price tiers — with two evidence-led follow-ons:
the Revenue Intelligence Sprint and the Governed Ops Retainer.

  Diagnostic (4,999 / 9,999 / 15,000) → Sprint (per scope) → Retainer (per scope)

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: KPI language is commitment ("نشتغل بدون مقابل لو لم يتحقق…"),
  not guarantee ("نضمن"). All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

Doctrine: docs/REVENUE_AUTOPILOT.md
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering

_FULL_HARD_GATES = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp",
    "no_linkedin_auto",
    "no_scraping",
    "no_fake_proof",
    "no_fake_revenue",
    "no_blast",
)

_DIAGNOSTIC_ACTION_MODES = (
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
)


_DIAGNOSTIC_STARTER = ServiceOffering(
    id="diagnostic_starter_4999",
    name_ar="تشخيص الإيراد والذكاء الاصطناعي المحكوم ٧ أيام — الباقة المبدئية",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Starter",
    price_sar=4999.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Revenue workflow map (1 workflow)",
        "Source & CRM data-quality review",
        "AI & automation governance risk scan",
        "Top 3 executable decisions with evidence",
        "Diagnostic Proof Pack",
    ),
    kpi_commitment_ar=(
        "نسلّم التشخيص خلال ٧ أيام عمل. إذا لم نطرح ٣ قرارات تشغيلية "
        "قابلة للتنفيذ بدليل، نواصل العمل بدون مقابل حتى نصل."
    ),
    kpi_commitment_en=(
        "Diagnostic delivered within 7 business days. If we don't surface "
        "3 evidence-backed executable decisions, we keep working at no "
        "charge until we do."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ٧ أيام إذا لم يُسلَّم التشخيص.",
    refund_policy_en="Full 100% refund within 7 days if the diagnostic is not delivered.",
    action_modes_used=_DIAGNOSTIC_ACTION_MODES,
    hard_gates=_FULL_HARD_GATES,
    customer_journey_stage="diagnostic",
)


_DIAGNOSTIC_STANDARD = ServiceOffering(
    id="diagnostic_standard_9999",
    name_ar="تشخيص الإيراد والذكاء الاصطناعي المحكوم ٧ أيام — الباقة القياسية",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Standard",
    price_sar=9999.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Revenue workflow map (up to 3 workflows)",
        "Source & CRM data-quality review",
        "AI & automation governance risk scan",
        "Approval-boundary gap analysis",
        "Top 5 executable decisions with evidence",
        "90-day governed action plan",
        "Diagnostic Proof Pack + executive readout",
    ),
    kpi_commitment_ar=(
        "نسلّم التشخيص خلال ٧ أيام عمل. إذا لم نطرح ٥ قرارات تشغيلية "
        "قابلة للتنفيذ بدليل، نواصل العمل بدون مقابل حتى نصل."
    ),
    kpi_commitment_en=(
        "Diagnostic delivered within 7 business days. If we don't surface "
        "5 evidence-backed executable decisions, we keep working at no "
        "charge until we do."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ٧ أيام إذا لم يُسلَّم التشخيص.",
    refund_policy_en="Full 100% refund within 7 days if the diagnostic is not delivered.",
    action_modes_used=_DIAGNOSTIC_ACTION_MODES,
    hard_gates=_FULL_HARD_GATES,
    customer_journey_stage="diagnostic",
)


_DIAGNOSTIC_EXECUTIVE = ServiceOffering(
    id="diagnostic_executive_15000",
    name_ar="تشخيص الإيراد والذكاء الاصطناعي المحكوم ٧ أيام — الباقة التنفيذية",
    name_en="7-Day Governed Revenue & AI Ops Diagnostic — Executive",
    price_sar=15000.0,
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Revenue workflow map (full funnel)",
        "Source, CRM & AI governance audit",
        "Approval & evidence-trail architecture review",
        "Top 7 executable decisions with evidence",
        "90-day governed action plan",
        "Diagnostic Proof Pack + executive readout + board memo",
        "Governed Ops Retainer scope draft",
    ),
    kpi_commitment_ar=(
        "نسلّم التشخيص خلال ٧ أيام عمل. إذا لم نطرح ٧ قرارات تشغيلية "
        "قابلة للتنفيذ بدليل، نواصل العمل بدون مقابل حتى نصل."
    ),
    kpi_commitment_en=(
        "Diagnostic delivered within 7 business days. If we don't surface "
        "7 evidence-backed executable decisions, we keep working at no "
        "charge until we do."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ٧ أيام إذا لم يُسلَّم التشخيص.",
    refund_policy_en="Full 100% refund within 7 days if the diagnostic is not delivered.",
    action_modes_used=_DIAGNOSTIC_ACTION_MODES,
    hard_gates=_FULL_HARD_GATES,
    customer_journey_stage="diagnostic",
)


_REVENUE_INTELLIGENCE_SPRINT = ServiceOffering(
    id="revenue_intelligence_sprint",
    name_ar="سبرنت ذكاء الإيراد",
    name_en="Revenue Intelligence Sprint",
    price_sar=0.0,  # custom — scoped from the diagnostic findings
    price_unit="custom",
    duration_days=14,
    deliverables=(
        "Prioritized revenue workflow rebuild",
        "Governed automation design",
        "Source & approval instrumentation",
        "Sprint Proof Pack",
        "Retainer transition plan",
    ),
    kpi_commitment_ar=(
        "نلتزم بتنفيذ نطاق السبرنت المتفق عليه خلال ١٤ يومًا مع Proof Pack. "
        "إن لم يكتمل النطاق، نواصل العمل بدون مقابل حتى يكتمل."
    ),
    kpi_commitment_en=(
        "Commit to delivering the agreed sprint scope within 14 days with a "
        "Proof Pack. If the scope is incomplete, we keep working at no "
        "charge until it is done."
    ),
    refund_policy_ar="استرداد تناسبي عن أي نطاق غير مُسلَّم خلال ٢١ يومًا.",
    refund_policy_en="Pro-rata refund for any scope not delivered within 21 days.",
    action_modes_used=_DIAGNOSTIC_ACTION_MODES,
    hard_gates=_FULL_HARD_GATES,
    customer_journey_stage="sprint",
)


_GOVERNED_OPS_RETAINER = ServiceOffering(
    id="governed_ops_retainer",
    name_ar="اشتراك العمليات المحكومة الشهري",
    name_en="Governed Ops Retainer",
    price_sar=0.0,  # custom — monthly price scoped per engagement
    price_unit="custom",
    duration_days=0,  # ongoing monthly
    deliverables=(
        "Monthly governed revenue ops run",
        "Approval queue operation (daily)",
        "Draft pack + follow-up plans",
        "Monthly Proof Pack",
        "Monthly executive summary + expansion recommendation",
    ),
    kpi_commitment_ar=(
        "نلتزم بتشغيل العمليات المحكومة شهريًا مع Proof Pack شهري. "
        "إن لم نلتزم بالمخرجات المتفق عليها، نعوّض الشهر التالي بدون مقابل."
    ),
    kpi_commitment_en=(
        "Commit to running governed ops monthly with a monthly Proof Pack. "
        "If we miss the agreed deliverables, the next month is at no charge."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة عند عدم الالتزام بالمخرجات.",
    refund_policy_en="Pro-rata refund of unused months if deliverables are unmet.",
    action_modes_used=_DIAGNOSTIC_ACTION_MODES,
    hard_gates=_FULL_HARD_GATES,
    customer_journey_stage="retainer",
)


# Canonical offering registry (order = catalog display order)
OFFERINGS: tuple[ServiceOffering, ...] = (
    _DIAGNOSTIC_STARTER,
    _DIAGNOSTIC_STANDARD,
    _DIAGNOSTIC_EXECUTIVE,
    _REVENUE_INTELLIGENCE_SPRINT,
    _GOVERNED_OPS_RETAINER,
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All offerings in catalog display order."""
    return OFFERINGS


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one offering by id, or None if not found."""
    for o in OFFERINGS:
        if o.id == service_id:
            return o
    return None
