"""The canonical Dealix service catalog — one five-rung ladder + one channel.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: KPI language is commitment ("نشتغل بدون مقابل لو لم يتحقق…"),
  not guarantee ("نضمن"). All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

Canonical five-rung ladder (ascending — each rung unlocks after the prior):
  1. Free Diagnostic (0)         — discovery
  2. Sprint (2,500)              — first paid proof
  3. Pilot (9,500)               — operational validation
  4. Retainer / Managed Ops      — 6,000–18,000 / month — continuity
  5. Enterprise / Custom AI      — 45,000–120,000 — scale

Plus one distribution channel (NOT a ladder rung):
  - Agency Partner OS (custom)

Strategic mapping (roles → offerings): docs/strategic/DEALIX_ROLE_SERVICE_LADDER_AR.md
Human-readable mirror: docs/company/SERVICE_CATALOG.md
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering

# Hard gates declared on every offering (Article 4 — immutable prohibitions).
_HARD_GATES: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp",
    "no_linkedin_auto",
    "no_scraping",
    "no_fake_proof",
    "no_fake_revenue",
    "no_blast",
)


# ── Rung 1 — Free Diagnostic ─────────────────────────────────────────
_FREE_DIAGNOSTIC = ServiceOffering(
    id="free_diagnostic",
    name_ar="التشخيص المجاني للذكاء الاصطناعي",
    name_en="Free AI Diagnostic",
    price_sar=0.0,
    price_display_ar="مجاني",
    price_display_en="Free",
    price_unit="one_time",
    duration_days=2,
    deliverables=(
        "1-page bilingual sector-fit diagnostic",
        "3 ranked revenue opportunities",
        "1 Arabic message draft",
        "1 best-channel recommendation",
        "1 risk to avoid",
        "1 next-step decision passport",
    ),
    kpi_commitment_ar="نسلّم التشخيص خلال ٤٨ ساعة من تعبئة النموذج.",
    kpi_commitment_en="Diagnostic delivered within 48 hours of form submission.",
    refund_policy_ar="مجاني — لا يوجد دفع.",
    refund_policy_en="Free — no payment.",
    action_modes_used=("suggest_only", "draft_only"),
    hard_gates=_HARD_GATES,
    customer_journey_stage="discovery",
    is_rung=True,
)


# ── Rung 2 — Sprint ──────────────────────────────────────────────────
_SPRINT = ServiceOffering(
    id="sprint",
    name_ar="سبرنت إثبات القيمة",
    name_en="Value Proof Sprint",
    price_sar=2500.0,
    price_display_ar="2,500 ر.س",
    price_display_en="2,500 SAR",
    price_unit="one_time",
    duration_days=10,
    deliverables=(
        "Company Brain v1",
        "Cleaned + deduplicated lead board",
        "Source + data-quality report",
        "Top 20 ranked opportunities",
        "Decision Passports for the top 5",
        "Arabic Draft Pack (10 messages)",
        "7-day follow-up plan",
        "Risk + objection map",
        "Executive Pack",
        "Proof Pack",
        "Next-best-offer recommendation",
    ),
    kpi_commitment_ar=(
        "نسلّم المخرجات خلال ١٠ أيام عمل. إذا لم نُبرز ٢٠ فرصة معتمدة، "
        "نواصل العمل بدون مقابل إضافي حتى نصل."
    ),
    kpi_commitment_en=(
        "Deliverables shipped within 10 working days. If we do not surface "
        "20 approved opportunities, we keep working at no extra cost until we do."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا، بدون أسئلة.",
    refund_policy_en="Full 100% refund within 14 days, no questions asked.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="first_paid",
    is_rung=True,
)


# ── Rung 3 — Pilot ───────────────────────────────────────────────────
_PILOT = ServiceOffering(
    id="pilot",
    name_ar="بايلوت التشغيل",
    name_en="Operating Pilot",
    price_sar=9500.0,
    price_display_ar="9,500 ر.س",
    price_display_en="9,500 SAR",
    price_unit="one_time",
    duration_days=30,
    deliverables=(
        "4 weekly pipeline operating cycles",
        "Weekly lead board + scoring refresh",
        "Weekly Arabic Draft Pack",
        "Opportunity + meeting tracker",
        "Weekly executive report",
        "Support + operations insights",
        "Closing Proof Pack",
        "Next-best-offer recommendation",
    ),
    kpi_commitment_ar=(
        "تشغيل أسبوعي للـ pipeline على مدى ٣٠ يومًا. إذا تأخّرت دورة أسبوعية، "
        "نمدّد العمل بدون مقابل إضافي حتى تكتمل."
    ),
    kpi_commitment_en=(
        "A weekly pipeline operating cycle across 30 days. If a weekly cycle "
        "slips, we extend the work at no extra cost until it completes."
    ),
    refund_policy_ar="استرداد ٧٥٪ إذا لم يتحقق التزام KPI خلال ٤٥ يومًا.",
    refund_policy_en="75% refund if the KPI commitment is unmet within 45 days.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="pilot",
    is_rung=True,
)


# ── Rung 4 — Retainer / Managed Operations (banded) ──────────────────
_RETAINER = ServiceOffering(
    id="retainer_managed_ops",
    name_ar="التشغيل المُدار الشهري",
    name_en="Managed Operations Retainer",
    price_sar=6000.0,
    price_sar_min=6000.0,
    price_sar_max=18000.0,
    price_display_ar="6,000–18,000 ر.س / شهر",
    price_display_en="6,000–18,000 SAR / month",
    price_unit="per_month",
    duration_days=120,  # 4-month minimum commitment
    deliverables=(
        "Monthly operating cadence (revenue + support + ops + delivery + proof)",
        "Weekly pipeline audits",
        "Daily approval queue",
        "Arabic Draft Pack (≥20 messages / month)",
        "Support insights (included)",
        "Monthly Proof Pack",
        "Monthly executive summary + board pack (upper band)",
        "Expansion recommendation",
    ),
    kpi_commitment_ar=(
        "نلتزم برفع معدل الردود +٢٠٪ خلال ٤ أشهر. إن لم يتحقق، "
        "نواصل العمل بدون مقابل إضافي حتى يتحقق."
    ),
    kpi_commitment_en=(
        "We commit to a +20% reply-rate lift within 4 months. If it is not "
        "reached, we keep working at no extra cost until it is."
    ),
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق التزام KPI.",
    refund_policy_en="Pro-rata refund of unused months if the KPI commitment is unmet.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="retainer",
    is_rung=True,
)


# ── Rung 5 — Enterprise / Custom AI (banded) ─────────────────────────
_ENTERPRISE = ServiceOffering(
    id="enterprise_custom_ai",
    name_ar="المؤسسات والذكاء الاصطناعي المخصّص",
    name_en="Enterprise & Custom AI",
    price_sar=45000.0,
    price_sar_min=45000.0,
    price_sar_max=120000.0,
    price_display_ar="45,000–120,000 ر.س",
    price_display_en="45,000–120,000 SAR",
    price_unit="one_time",
    duration_days=120,
    deliverables=(
        "Discovery + AI readiness review",
        "Custom workflow + agent design",
        "Integrations scope + data governance",
        "PDPL-aware data review",
        "Build + iteration cycles",
        "Team training + handover",
        "AI governance program + audit pack",
        "SLA definition",
    ),
    kpi_commitment_ar=(
        "نثبّت النطاق والمراحل ومعايير القبول في SOW مكتوب قبل بدء العمل، "
        "ونلتزم بمراحل الـ SOW."
    ),
    kpi_commitment_en=(
        "Scope, milestones, and acceptance criteria are fixed in a written "
        "SOW before work begins, and we commit to the SOW milestones."
    ),
    refund_policy_ar="وفق عقد SOW موقّع بشروط إلغاء — يُراجَع قانونيًا.",
    refund_policy_en="Per a signed SOW with cancellation terms — lawyer-reviewed.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="enterprise",
    is_rung=True,
)


# ── Channel — Agency Partner OS (NOT a ladder rung) ──────────────────
_AGENCY_PARTNER = ServiceOffering(
    id="agency_partner_os",
    name_ar="نظام شريك الوكالة",
    name_en="Agency Partner OS",
    price_sar=0.0,  # custom — actual price set per partnership
    price_display_ar="بالاتفاق",
    price_display_en="Custom",
    price_unit="custom",
    duration_days=0,  # ongoing
    deliverables=(
        "Partner intake doc",
        "Co-branded diagnostic for the partner's clients",
        "Client Proof Sprint (per client)",
        "Proof Pack (per client)",
        "Renewal / upsell pack",
        "Partner revenue tracking",
        "30% commission tracking",
    ),
    kpi_commitment_ar=(
        "نلتزم بـ٣٠٪ عمولة لأول سنة من كل عميل محوّل، "
        "ولا نشر proof بدون موافقة موقّعة."
    ),
    kpi_commitment_en=(
        "30% commission for the first paid year per referred customer. "
        "Never publish proof without signed consent."
    ),
    refund_policy_ar="عقد رسمي بشروط الإلغاء — يُراجَع قانونيًا.",
    refund_policy_en="Formal contract with cancellation terms — lawyer-reviewed.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="channel",
    is_rung=False,
)


# Canonical registry — 5 ascending ladder rungs + 1 distribution channel.
# Order = catalog display order.
OFFERINGS: tuple[ServiceOffering, ...] = (
    _FREE_DIAGNOSTIC,
    _SPRINT,
    _PILOT,
    _RETAINER,
    _ENTERPRISE,
    _AGENCY_PARTNER,
)

# The 5 customer-facing ladder rungs (excludes the partner channel).
RUNGS: tuple[ServiceOffering, ...] = tuple(o for o in OFFERINGS if o.is_rung)

# The distribution channel offering(s) (not part of the customer ladder).
CHANNEL_OFFERINGS: tuple[ServiceOffering, ...] = tuple(
    o for o in OFFERINGS if not o.is_rung
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All offerings (5 rungs + partner channel) in catalog display order."""
    return OFFERINGS


def list_rungs() -> tuple[ServiceOffering, ...]:
    """The 5 customer-facing ladder rungs, ascending by price."""
    return RUNGS


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one offering by id, or None if not found."""
    for o in OFFERINGS:
        if o.id == service_id:
            return o
    return None
