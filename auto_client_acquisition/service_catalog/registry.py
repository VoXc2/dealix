"""The 3 canonical Dealix offerings — 2026-Q2 commercial reframe.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: KPI language is commitment ("نشتغل بدون مقابل لو لم يتحقق…"),
  not guarantee ("نضمن"). All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

Pricing ladder (ascending floor):
  Strategic Diagnostic (0) → Governed Ops Retainer (4,999/mo)
  → Revenue Intelligence Sprint (25,000 one-time)

Beachhead: Saudi B2B services. PDPL/NDMO/SAMA exposed mid-market
(50–500 employees) is the wedge. Banking, energy, healthcare, gov
are handled inside Custom AI engagements after the Sprint produces
a Capital Asset.

The 2026-Q2 reframe collapsed the 2025 7-offer ladder down to 3:
- Free Mini Diagnostic → upgraded to Strategic Diagnostic (PDPL/NDMO posture audit anchor).
- 499 SAR Sprint → archived (priced below founder conviction).
- 1,500 SAR Data-to-Revenue Pack → archived (folded into Sprint).
- 2,999 SAR/mo Growth Ops → promoted to 4,999 SAR/mo Governed Ops Retainer.
- 1,500 SAR/mo Support OS Add-on → archived (folded into Retainer).
- 7,500 SAR/mo Executive Command Center → reshaped as 25,000 SAR Sprint outcome.
- Agency Partner OS → moved out of the customer-facing ladder; remains a
  partner-channel contract via partnership_os only.

The archived offerings are preserved at the bottom of this file
(`_LEGACY_2025_OFFERINGS`) for audit trail (Article 11) — they are NOT
exported in `OFFERINGS` and NOT served by the public commercial map.

`_LEGACY_ID_ALIASES` lets older e2e tests and historical engagement
records resolve via `get_offering()` to the closest 2026 successor.

Strategic mapping (roles → offerings): docs/sales-kit/PRICING_REFRAME_2026Q2.md
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering


# ─────────────────────────────────────────────────────────────────────
# Active 2026-Q2 ladder — three offerings.
# ─────────────────────────────────────────────────────────────────────

_STRATEGIC_DIAGNOSTIC = ServiceOffering(
    id="strategic_diagnostic",
    name_ar="التشخيص الاستراتيجي المجاني",
    name_en="Strategic Diagnostic",
    price_sar=0.0,
    price_unit="one_time",
    duration_days=1,
    deliverables=(
        "PDPL + NDMO posture audit (sector-specific)",
        "Revenue intelligence gap report",
        "Source-of-truth inventory (top 5 systems)",
        "1-page 90-day action plan",
        "Top 3 ranked opportunities with effort/value scoring",
        "1 Arabic message draft for the highest-value opportunity",
        "Decision passport for the founder's next step",
    ),
    kpi_commitment_ar=(
        "نسلّم خلال يوم عمل واحد من تعبئة النموذج. إذا لم نوصل ٣ فرص "
        "قابلة للتنفيذ، نواصل العمل بدون مقابل حتى نوصل."
    ),
    kpi_commitment_en=(
        "Delivered within 1 working day of form submission. If we don't "
        "surface 3 actionable opportunities, we keep working until we do."
    ),
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


_GOVERNED_OPS_RETAINER = ServiceOffering(
    id="governed_ops_retainer_4999",
    name_ar="ريتينر العمليات المحوكمة (٤٬٩٩٩ ر.س / شهر)",
    name_en="Governed Ops Retainer",
    price_sar=4999.0,
    price_unit="per_month",
    duration_days=90,  # 3-month minimum commitment
    deliverables=(
        "Weekly Pipeline Audit + Lead Board",
        "Source Passport curation (every data source documented)",
        "Daily Approval Queue (draft_only — founder approves every send)",
        "Monthly Value Report (revenue impact, governance posture, friction trends)",
        "Monthly Proof Pack (signed, audit-ready)",
        "Friction Log review + remediation plan",
        "Decision Passports for every material decision",
        "Adoption Score + retainer-readiness gate",
        "Dedicated WhatsApp draft channel for founder approval",
    ),
    kpi_commitment_ar=(
        "نلتزم بتوصيل تقرير قيمة شهري قابل للتدقيق + رفع جودة بيانات "
        "خط الإيرادات بنسبة ≥٢٠٪ خلال ٣ أشهر. إن لم يتحقق، نواصل بدون "
        "مقابل حتى يتحقق."
    ),
    kpi_commitment_en=(
        "We commit to: an audit-ready monthly Value Report + a ≥20% lift "
        "in revenue-pipeline data quality within 3 months. If not achieved, "
        "we keep working at no cost until it is."
    ),
    refund_policy_ar=(
        "استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق KPI. "
        "الحد الأدنى للالتزام: ٣ أشهر."
    ),
    refund_policy_en=(
        "Pro-rata refund of unused months if KPI commitment unmet. "
        "Minimum commitment: 3 months."
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
        "no_blast",
    ),
    customer_journey_stage="monthly",
)


_REVENUE_INTELLIGENCE_SPRINT = ServiceOffering(
    id="revenue_intelligence_sprint_25k",
    name_ar="سبرنت ذكاء الإيرادات الرئيسي (٢٥٬٠٠٠ ر.س / ٣٠ يومًا)",
    name_en="Revenue Intelligence Sprint",
    price_sar=25000.0,
    price_unit="one_time",
    duration_days=30,
    deliverables=(
        "Three sources of truth merged (CRM + finance + ops)",
        "Revenue forecast model (rolling 90-day, accuracy target ≥85%)",
        "Audit-ready governance pack (PDPL Article 5/13/14/18/21 mapped)",
        "Decision Passports for the top 20 opportunities",
        "Arabic + English Draft Pack (15 messages, founder-approved)",
        "Risk + Objection Map (sector-specific)",
        "Executive board pack (monthly cadence template)",
        "Capital Asset registered: proprietary forecast + clean data spine",
        "Full Proof Pack (signed, exportable as PDF)",
        "Retainer-readiness gate + Next Best Offer recommendation",
    ),
    kpi_commitment_ar=(
        "نسلّم ١٠ مخرجات في ٣٠ يومًا، مع دمج ٣ مصادر بيانات + بناء نموذج "
        "تنبؤ بدقة هدف ≥٨٥٪ + حزمة حوكمة قابلة للتدقيق. إن لم تتحقق "
        "بوابة جاهزية الريتينر، نواصل بدون مقابل حتى تتحقق."
    ),
    kpi_commitment_en=(
        "10 deliverables in 30 days: 3 sources merged, target forecast "
        "accuracy ≥85%, audit-ready governance pack. If the retainer-"
        "readiness gate is not met, we keep working at no cost until it is."
    ),
    refund_policy_ar=(
        "استرداد ٥٠٪ خلال ٦٠ يومًا إذا لم تتحقق بوابة جاهزية الريتينر. "
        "٥٠٪ على القبول، ٥٠٪ على تسليم Proof Pack."
    ),
    refund_policy_en=(
        "50% refund within 60 days if the retainer-readiness gate is not "
        "met. 50% on acceptance, 50% on Proof Pack delivery."
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
        "no_blast",
    ),
    customer_journey_stage="flagship",
)


# Canonical 2026-Q2 registry (order = catalog display order)
OFFERINGS: tuple[ServiceOffering, ...] = (
    _STRATEGIC_DIAGNOSTIC,
    _GOVERNED_OPS_RETAINER,
    _REVENUE_INTELLIGENCE_SPRINT,
)

SERVICE_IDS: frozenset[str] = frozenset(o.id for o in OFFERINGS)


# Legacy ID aliases — let pre-2026-Q2 e2e tests and historical
# engagement records resolve to the closest current successor via
# get_offering(). NEW code MUST use canonical 2026 IDs.
_LEGACY_ID_ALIASES: dict[str, str] = {
    "free_mini_diagnostic": "strategic_diagnostic",
    "revenue_proof_sprint_499": "revenue_intelligence_sprint_25k",
    "data_to_revenue_pack_1500": "revenue_intelligence_sprint_25k",
    "growth_ops_monthly_2999": "governed_ops_retainer_4999",
    "support_os_addon_1500": "governed_ops_retainer_4999",
    "executive_command_center_7500": "governed_ops_retainer_4999",
}


def list_offerings() -> tuple[ServiceOffering, ...]:
    """All 3 active offerings in catalog display order."""
    return OFFERINGS


def get_offering(service_id: str) -> ServiceOffering | None:
    """Return one active offering by id. Legacy IDs resolve to their
    2026 successor; unknown ids return None.
    """
    canonical = _LEGACY_ID_ALIASES.get(service_id, service_id)
    for o in OFFERINGS:
        if o.id == canonical:
            return o
    return None
