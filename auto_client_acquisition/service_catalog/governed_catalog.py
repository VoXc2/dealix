"""Governed-tier service catalog — "Governed Revenue & AI Operations" (doctrine §4).

Added *alongside* the 7 canonical offerings in ``registry.py`` (which is left
untouched). This tier is priced as ranges, evidence-gated, and carries explicit
allowed / forbidden next actions. Services 4–7 are scoped per engagement
(``price_unit="custom"``) — no invented price.

Article 8: commitment language only — never "نضمن" / "guaranteed".
Article 4: ``action_modes`` never include ``live_send`` or ``live_charge``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GovernedPriceUnit = Literal["one_time", "per_month", "custom"]


class GovernedService(BaseModel):
    """One governed-revenue service. Read-only data record."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., min_length=1, max_length=64)
    name_ar: str = Field(..., min_length=1, max_length=160)
    name_en: str = Field(..., min_length=1, max_length=160)
    price_min_sar: float = Field(..., ge=0)
    price_max_sar: float = Field(..., ge=0)
    price_unit: GovernedPriceUnit = "one_time"
    summary_ar: str
    summary_en: str
    deliverables: tuple[str, ...] = Field(..., min_length=1)
    inputs_required: tuple[str, ...] = Field(..., min_length=1)
    evidence_level_required: str = Field(..., min_length=1)
    allowed_next_action_ar: str
    allowed_next_action_en: str
    forbidden_actions: tuple[str, ...] = Field(..., min_length=1)
    kpi_commitment_ar: str
    kpi_commitment_en: str
    action_modes_used: tuple[str, ...] = Field(..., min_length=1)
    hard_gates: tuple[str, ...] = Field(..., min_length=1)
    is_headline: bool = False
    is_estimate: bool = True


_COMMON_FORBIDDEN: tuple[str, ...] = (
    "send_externally_without_approval",
    "guaranteed_sales_claim",
    "fake_proof",
    "scraping",
    "cold_whatsapp",
)
_COMMON_MODES: tuple[str, ...] = ("suggest_only", "draft_only", "approval_required")
_COMMON_GATES: tuple[str, ...] = (
    "no_cold_whatsapp",
    "no_scraping",
    "no_guaranteed_sales_claims",
    "no_fake_proof",
    "external_action_requires_approval",
)


_DIAGNOSTIC = GovernedService(
    id="governed_revenue_ops_diagnostic",
    name_ar="تشخيص تشغيل الإيراد المحكوم",
    name_en="Governed Revenue Ops Diagnostic",
    price_min_sar=4999.0,
    price_max_sar=25000.0,
    price_unit="one_time",
    summary_ar=(
        "تشخيص يربط الذكاء الاصطناعي بالإيراد: وضوح المصادر، خريطة المخاطر، "
        "فجوات المتابعة، وجواز قرار."
    ),
    summary_en=(
        "Diagnostic that ties AI to revenue: source clarity, pipeline risk map, "
        "follow-up gaps, and a decision passport."
    ),
    deliverables=(
        "Revenue Workflow Map",
        "CRM / Source Quality Review",
        "Pipeline Risk Map",
        "Follow-up Gap Analysis",
        "Decision Passport",
        "Proof-of-Value Opportunities",
        "Recommended Sprint / Retainer",
    ),
    inputs_required=("CRM export", "current revenue workflow notes"),
    evidence_level_required="L2",
    allowed_next_action_ar="عرض Sprint استخبارات الإيراد.",
    allowed_next_action_en="Offer the Revenue Intelligence Sprint.",
    forbidden_actions=_COMMON_FORBIDDEN,
    kpi_commitment_ar="نسلّم التشخيص خلال الإطار المتفق عليه مع جواز قرار واضح.",
    kpi_commitment_en="We deliver the diagnostic within the agreed window with a clear decision passport.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
    is_headline=True,
)


_SPRINT = GovernedService(
    id="revenue_intelligence_sprint_25000",
    name_ar="سبرنت استخبارات الإيراد",
    name_en="Revenue Intelligence Sprint",
    price_min_sar=25000.0,
    price_max_sar=25000.0,
    price_unit="one_time",
    summary_ar=(
        "العرض الرئيسي بعد التشخيص: ترتيب الحسابات، تسجيل مخاطر الصفقات، "
        "مسودات الفعل التالي، وحزمة إثبات."
    ),
    summary_en=(
        "The headline offer after the diagnostic: account prioritization, deal "
        "risk scoring, next-best-action drafts, and a proof pack."
    ),
    deliverables=(
        "Account Prioritization",
        "Deal Risk Scoring",
        "Next-Best-Action Drafts",
        "Follow-up Templates",
        "Revenue Opportunity Ledger",
        "Decision Passport",
        "Proof Pack",
    ),
    inputs_required=("approved diagnostic", "CRM export", "founder review slot"),
    evidence_level_required="L3",
    allowed_next_action_ar="عرض Retainer العمليات المحكومة.",
    allowed_next_action_en="Offer the Governed Ops Retainer.",
    forbidden_actions=_COMMON_FORBIDDEN,
    kpi_commitment_ar="نسلّم مخرجات السبرنت مع حزمة إثبات قابلة للمراجعة.",
    kpi_commitment_en="We deliver the sprint outputs with a reviewable proof pack.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
    is_headline=True,
)


_RETAINER = GovernedService(
    id="governed_ops_retainer",
    name_ar="ريتينر العمليات المحكومة",
    name_en="Governed Ops Retainer",
    price_min_sar=4999.0,
    price_max_sar=35000.0,
    price_unit="per_month",
    summary_ar="بوابة الإيراد المتكرر: مراجعة شهرية للإيراد والـpipeline وقرارات الذكاء الاصطناعي.",
    summary_en="The recurring-revenue gateway: monthly revenue, pipeline, and AI-decision review.",
    deliverables=(
        "Monthly Revenue Review",
        "Pipeline Quality Review",
        "AI Decision Review",
        "Approved Follow-up Queue",
        "Risk Register",
        "Value Report",
        "Board Memo",
    ),
    inputs_required=("successful sprint or diagnostic", "monthly CRM export"),
    evidence_level_required="L4",
    allowed_next_action_ar="مراجعة إشارة المنصة عند تكرار workflow ٣ مرات.",
    allowed_next_action_en="Review platform signal once a workflow repeats 3 times.",
    forbidden_actions=_COMMON_FORBIDDEN,
    kpi_commitment_ar="نسلّم مراجعة شهرية وتقرير قيمة لكل دورة.",
    kpi_commitment_en="We deliver a monthly review and a value report each cycle.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
    is_headline=True,
)


_AI_GOVERNANCE = GovernedService(
    id="ai_governance_for_revenue_teams",
    name_ar="حوكمة الذكاء الاصطناعي لفِرق الإيراد",
    name_en="AI Governance for Revenue Teams",
    price_min_sar=0.0,
    price_max_sar=0.0,
    price_unit="custom",
    summary_ar="سياسات الأفعال المسموحة والممنوعة وحدود الموافقة لفرق المبيعات التي تستخدم AI.",
    summary_en="Allowed / forbidden AI actions, approval boundaries and evidence logging for revenue teams.",
    deliverables=(
        "Allowed AI Actions",
        "Forbidden AI Actions",
        "Approval Boundaries",
        "Source Rules",
        "No Autonomous External Send Policy",
        "Evidence Logging",
    ),
    inputs_required=("list of AI tools in use", "current sales workflow"),
    evidence_level_required="L2",
    allowed_next_action_ar="ربط السياسات بمركز الموافقات.",
    allowed_next_action_en="Wire the policy into the Approval Center.",
    forbidden_actions=_COMMON_FORBIDDEN,
    kpi_commitment_ar="نسلّم مصفوفة سياسات قابلة للتطبيق ومربوطة بالموافقات.",
    kpi_commitment_en="We deliver an enforceable policy matrix wired to approvals.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
)


_DATA_READINESS = GovernedService(
    id="crm_data_readiness_for_ai",
    name_ar="جاهزية بيانات الـCRM للذكاء الاصطناعي",
    name_en="CRM / Data Readiness for AI",
    price_min_sar=0.0,
    price_max_sar=0.0,
    price_unit="custom",
    summary_ar="فحص نظافة البيانات قبل تشغيل AI فوقها — لأن AI فوق بيانات سيئة = قرارات سيئة أسرع.",
    summary_en="Data hygiene review before AI runs on it — bad data + AI = faster bad decisions.",
    deliverables=(
        "CRM Hygiene Report",
        "Source Mapping",
        "Missing Fields",
        "Duplicate Accounts",
        "Bad Lifecycle Stages",
        "Data Readiness Score",
        "AI Readiness Recommendation",
    ),
    inputs_required=("CRM export", "field/stage definitions"),
    evidence_level_required="L2",
    allowed_next_action_ar="عرض التشخيص أو السبرنت بعد رفع الجاهزية.",
    allowed_next_action_en="Offer the diagnostic or sprint once readiness improves.",
    forbidden_actions=_COMMON_FORBIDDEN,
    kpi_commitment_ar="نسلّم درجة جاهزية بيانات وتوصية واضحة.",
    kpi_commitment_en="We deliver a data readiness score and a clear recommendation.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
)


_BOARD_MEMO = GovernedService(
    id="board_decision_memo",
    name_ar="مذكرة قرار مجلس الإدارة",
    name_en="Board Decision Memo",
    price_min_sar=0.0,
    price_max_sar=0.0,
    price_unit="custom",
    summary_ar="مذكرة للإدارة والشركاء تحوّل Dealix من منفّذ إلى شريك قيادة.",
    summary_en="A memo for executives and partners — turns Dealix from executor into a leadership partner.",
    deliverables=(
        "Top Revenue Decisions",
        "Pipeline Risks",
        "AI Governance Risks",
        "Capital Allocation",
        "Build / Hold / Kill Recommendations",
    ),
    inputs_required=("retainer or sprint outputs", "board context"),
    evidence_level_required="L3",
    allowed_next_action_ar="مراجعة المذكرة في اجتماع المجلس.",
    allowed_next_action_en="Review the memo in the board meeting.",
    forbidden_actions=_COMMON_FORBIDDEN,
    kpi_commitment_ar="نسلّم مذكرة قرار مبنية على أدلة قابلة للتتبع.",
    kpi_commitment_en="We deliver a decision memo built on traceable evidence.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
)


_TRUST_PACK_LITE = GovernedService(
    id="trust_pack_lite",
    name_ar="حزمة الثقة المختصرة",
    name_en="Trust Pack Lite",
    price_min_sar=0.0,
    price_max_sar=0.0,
    price_unit="custom",
    summary_ar="تُباع فقط عند وجود إشارة أمان/ثقة من العميل — سياسة أفعال ومصفوفة موافقات.",
    summary_en="Sold only when the customer raises a security/trust signal — action policy and approval matrix.",
    deliverables=(
        "AI Action Policy",
        "Approval Matrix",
        "Evidence Handling",
        "Forbidden Actions",
        "Agent Safety Rules",
        "Trust Boundaries",
    ),
    inputs_required=("explicit security/trust request from the customer",),
    evidence_level_required="L3",
    allowed_next_action_ar="ربط حدود الثقة بمركز الموافقات.",
    allowed_next_action_en="Wire trust boundaries into the Approval Center.",
    forbidden_actions=_COMMON_FORBIDDEN + ("sell_before_trust_signal",),
    kpi_commitment_ar="نسلّم حزمة ثقة قابلة للتطبيق عند طلب أمان صريح.",
    kpi_commitment_en="We deliver an enforceable trust pack on an explicit security request.",
    action_modes_used=_COMMON_MODES,
    hard_gates=_COMMON_GATES,
)


GOVERNED_SERVICES: tuple[GovernedService, ...] = (
    _DIAGNOSTIC,
    _SPRINT,
    _RETAINER,
    _AI_GOVERNANCE,
    _DATA_READINESS,
    _BOARD_MEMO,
    _TRUST_PACK_LITE,
)

GOVERNED_SERVICE_IDS: frozenset[str] = frozenset(s.id for s in GOVERNED_SERVICES)


def list_governed_services() -> tuple[GovernedService, ...]:
    """All 7 governed-tier services in catalog display order."""
    return GOVERNED_SERVICES


def list_headline_services() -> tuple[GovernedService, ...]:
    """The 3 headline offers presented to the market (Diagnostic → Sprint → Retainer)."""
    return tuple(s for s in GOVERNED_SERVICES if s.is_headline)


def get_governed_service(service_id: str) -> GovernedService | None:
    """Return one governed service by id, or None if not found."""
    for s in GOVERNED_SERVICES:
        if s.id == service_id:
            return s
    return None
