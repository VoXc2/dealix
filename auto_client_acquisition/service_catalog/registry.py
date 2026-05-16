"""The 7 canonical Dealix offerings — Governed Revenue & AI Operations.

Truth registry. Backend + portal + WhatsApp + landing pages all read from here.
Canonical spec: docs/COMPANY_SERVICE_LADDER.md.

Pricing is expressed as `range` or `recommended_draft`, never a fabricated
single number. A `recommended_draft` service does not get a fixed price until
>= 3 paid pilots of that service have been delivered.

Constitution:
- Article 4: action_modes never include 'live_send' or 'live_charge'.
- Article 8: language is commitment, never guarantee. All `is_estimate=True`.
- Article 11: pricing changes are 1-line edits to this file (no engine code).

`customer_journey_stage` reuses the existing journey-stage Literal so that
downstream consumers of the service catalog remain unchanged.
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering

_HARD_GATES = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp",
    "no_linkedin_auto",
    "no_scraping",
    "no_fake_proof",
    "no_fake_revenue",
)


# ── 1 — Governed Revenue Ops Diagnostic (entry, range 4,999-25,000) ──
_DIAGNOSTIC = ServiceOffering(
    id="governed_revenue_ops_diagnostic",
    name_ar="تشخيص عمليات الإيراد المحكومة",
    name_en="Governed Revenue Ops Diagnostic",
    price_sar=4999.0,  # equal to the range minimum — keeps consumers safe
    price_mode="range",
    price_sar_min=4999.0,
    price_sar_max=25000.0,
    price_unit="one_time",
    duration_days=10,
    deliverables=(
        "Revenue Workflow Map",
        "CRM / source quality review",
        "Pipeline risk map",
        "Follow-up gap analysis",
        "Decision passport",
        "Proof-of-value opportunities",
        "Recommended Sprint / Retainer",
    ),
    kpi_commitment_ar=(
        "نسلّم خريطة سير عمل الإيراد ومراجعة جودة البيانات خلال ١٠ أيام عمل."
    ),
    kpi_commitment_en=(
        "We deliver the revenue workflow map and data-quality review within "
        "10 business days."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إذا لم تُسلَّم المخرجات.",
    refund_policy_en="Full 100% refund within 14 days if deliverables are not met.",
    action_modes_used=("suggest_only", "draft_only", "approval_required"),
    hard_gates=_HARD_GATES,
    customer_journey_stage="discovery",
)


# ── 2 — Revenue Intelligence Sprint (recommended_draft) ─────────────
_REVENUE_INTELLIGENCE_SPRINT = ServiceOffering(
    id="revenue_intelligence_sprint",
    name_ar="سبرنت ذكاء الإيراد",
    name_en="Revenue Intelligence Sprint",
    price_sar=0.0,  # recommended_draft — quoted per scope
    price_mode="recommended_draft",
    price_unit="one_time",
    duration_days=14,
    deliverables=(
        "Account prioritization",
        "Deal-risk scoring",
        "Next-best-action drafts",
        "Follow-up templates",
        "Revenue opportunity ledger",
        "Decision passport",
        "Proof pack",
    ),
    kpi_commitment_ar="نسلّم مخرجات السبرنت السبعة ضمن نطاق متفق عليه.",
    kpi_commitment_en="We deliver the seven sprint outputs within an agreed scope.",
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إذا لم تُسلَّم المخرجات.",
    refund_policy_en="Full 100% refund within 14 days if deliverables are not met.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="first_paid",
)


# ── 3 — Governed Ops Retainer (recommended_draft, per_month) ────────
_GOVERNED_OPS_RETAINER = ServiceOffering(
    id="governed_ops_retainer",
    name_ar="ريتينر العمليات المحكومة",
    name_en="Governed Ops Retainer",
    price_sar=0.0,  # recommended_draft — quoted per month
    price_mode="recommended_draft",
    price_unit="per_month",
    duration_days=30,
    deliverables=(
        "Monthly revenue review",
        "Pipeline quality review",
        "AI decision review",
        "Approved follow-up queue",
        "Risk register",
        "Value report",
        "Board memo",
    ),
    kpi_commitment_ar="نسلّم مراجعة شهرية محكومة لعمليات الإيراد.",
    kpi_commitment_en="We deliver a governed monthly review of revenue operations.",
    refund_policy_ar="استرداد تناسبي للأشهر غير المستخدمة عند عدم تسليم المخرجات.",
    refund_policy_en="Pro-rata refund of unused months if deliverables are not met.",
    action_modes_used=(
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_manual",
    ),
    hard_gates=_HARD_GATES,
    customer_journey_stage="monthly",
)


# ── 4 — AI Governance for Revenue Teams (recommended_draft) ─────────
_AI_GOVERNANCE_FOR_REVENUE = ServiceOffering(
    id="ai_governance_for_revenue_teams",
    name_ar="حوكمة الذكاء الاصطناعي لفِرق الإيراد",
    name_en="AI Governance for Revenue Teams",
    price_sar=0.0,
    price_mode="recommended_draft",
    price_unit="one_time",
    duration_days=14,
    deliverables=(
        "Allowed AI actions",
        "Forbidden AI actions",
        "Approval boundaries",
        "Source rules",
        "No-autonomous-external-send policy",
        "Evidence logging",
    ),
    kpi_commitment_ar="نسلّم سياسة حوكمة ذكاء اصطناعي قابلة للتدقيق.",
    kpi_commitment_en="We deliver an auditable AI governance policy.",
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إذا لم تُسلَّم المخرجات.",
    refund_policy_en="Full 100% refund within 14 days if deliverables are not met.",
    action_modes_used=("suggest_only", "draft_only", "approval_required"),
    hard_gates=_HARD_GATES,
    customer_journey_stage="executive",
)


# ── 5 — CRM / Data Readiness for AI (recommended_draft) ─────────────
_CRM_DATA_READINESS = ServiceOffering(
    id="crm_data_readiness_for_ai",
    name_ar="جاهزية بيانات وCRM للذكاء الاصطناعي",
    name_en="CRM / Data Readiness for AI",
    price_sar=0.0,
    price_mode="recommended_draft",
    price_unit="one_time",
    duration_days=14,
    deliverables=(
        "CRM hygiene report",
        "Source mapping",
        "Missing fields",
        "Duplicate accounts",
        "Bad lifecycle stages",
        "Data-readiness score",
        "AI-readiness recommendation",
    ),
    kpi_commitment_ar="نسلّم تقرير جاهزية بيانات قبل أي أتمتة بالذكاء الاصطناعي.",
    kpi_commitment_en=(
        "We deliver a data-readiness report before any AI automation."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إذا لم تُسلَّم المخرجات.",
    refund_policy_en="Full 100% refund within 14 days if deliverables are not met.",
    action_modes_used=("suggest_only", "draft_only", "approval_required"),
    hard_gates=_HARD_GATES,
    customer_journey_stage="expansion",
)


# ── 6 — Board Decision Memo (recommended_draft) ─────────────────────
_BOARD_DECISION_MEMO = ServiceOffering(
    id="board_decision_memo",
    name_ar="مذكرة قرار مجلس الإدارة",
    name_en="Board Decision Memo",
    price_sar=0.0,
    price_mode="recommended_draft",
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "Top revenue decisions",
        "Pipeline risks",
        "AI governance risks",
        "Capital allocation",
        "Build / hold / kill recommendations",
    ),
    kpi_commitment_ar="نسلّم مذكرة قرار محكومة مدعومة بالأدلة.",
    kpi_commitment_en="We deliver a governed, evidence-backed decision memo.",
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إذا لم تُسلَّم المخرجات.",
    refund_policy_en="Full 100% refund within 14 days if deliverables are not met.",
    action_modes_used=("suggest_only", "draft_only", "approval_required"),
    hard_gates=_HARD_GATES,
    customer_journey_stage="support_addon",
)


# ── 7 — Trust Pack Lite (recommended_draft, signal-only) ────────────
_TRUST_PACK_LITE = ServiceOffering(
    id="trust_pack_lite",
    name_ar="حزمة الثقة المختصرة",
    name_en="Trust Pack Lite",
    price_sar=0.0,
    price_mode="recommended_draft",
    price_unit="one_time",
    duration_days=7,
    deliverables=(
        "AI action policy",
        "Approval matrix",
        "Evidence handling",
        "Forbidden actions",
        "Agent safety rules",
        "Trust boundaries",
    ),
    kpi_commitment_ar="نسلّم حزمة ثقة عند وجود إشارة أمان أو مراجعة امتثال.",
    kpi_commitment_en=(
        "We deliver a trust pack on a security or compliance-review signal."
    ),
    refund_policy_ar="استرداد كامل ١٠٠٪ خلال ١٤ يومًا إذا لم تُسلَّم المخرجات.",
    refund_policy_en="Full 100% refund within 14 days if deliverables are not met.",
    action_modes_used=("suggest_only", "draft_only", "approval_required"),
    hard_gates=_HARD_GATES,
    customer_journey_stage="channel",
)


# Canonical 7-offering registry (order = catalog display order).
# The first three are the headline offers — lead with these.
OFFERINGS: tuple[ServiceOffering, ...] = (
    _DIAGNOSTIC,
    _REVENUE_INTELLIGENCE_SPRINT,
    _GOVERNED_OPS_RETAINER,
    _AI_GOVERNANCE_FOR_REVENUE,
    _CRM_DATA_READINESS,
    _BOARD_DECISION_MEMO,
    _TRUST_PACK_LITE,
)

# The three headline offers, in the order the founder should lead with.
HEADLINE_SERVICE_IDS: tuple[str, ...] = (
    "governed_revenue_ops_diagnostic",
    "revenue_intelligence_sprint",
    "governed_ops_retainer",
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
