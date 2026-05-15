"""Dealix enterprise transformation programs — the high-value catalog.

Dealix does not sell chatbots. It sells governed AI transformation programs:
large tiered contracts (setup + monthly retainer) that build an operating
layer connecting sales, support, knowledge and operations.

Constitution still binds:
- Article 4: action_modes never include 'live_send' / 'live_charge'.
- Article 8: KPI language is commitment ("نلتزم … نشتغل بدون مقابل حتى"),
  never guarantee ("نضمن" / "guaranteed"). Every numeric is_estimate=True.
- Article 11: pricing changes are 1-line edits to this file.

Five programs + one flagship, each quoted per PricingTier
(Basic / Growth / Enterprise). The flat 7-offering ladder lives in
``registry.py``; this file is the parallel enterprise catalog.
"""

from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import (
    EnterpriseOffering,
    PricingTier,
)

# Shared governance posture for every enterprise program.
_ENTERPRISE_ACTION_MODES = (
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
)
_ENTERPRISE_HARD_GATES = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp",
    "no_linkedin_auto",
    "no_scraping",
    "no_fake_proof",
    "no_fake_revenue",
    "no_blast",
)


def _tier(
    *,
    id: str,
    name_ar: str,
    name_en: str,
    setup_sar: float,
    monthly_sar: float,
    min_duration_days: int,
    deliverables: tuple[str, ...],
    kpi_ar: str,
    kpi_en: str,
    exclusions: tuple[str, ...] = (),
) -> PricingTier:
    return PricingTier(
        id=id,
        name_ar=name_ar,
        name_en=name_en,
        setup_sar=setup_sar,
        monthly_sar=monthly_sar,
        min_duration_days=min_duration_days,
        deliverables=deliverables,
        kpi_commitment_ar=kpi_ar,
        kpi_commitment_en=kpi_en,
        exclusions=exclusions,
    )


# ── 1. AI Operating System for Business ──────────────────────────────
_AI_OPERATING_SYSTEM = EnterpriseOffering(
    id="ai_operating_system",
    name_ar="نظام التشغيل بالذكاء الاصطناعي للشركات",
    name_en="AI Operating System for Business",
    category="operating_system",
    summary_ar=(
        "نبني طبقة تشغيل ذكية فوق شركتك: Company Brain، وكلاء مبيعات ودعم "
        "وعمليات، لوحة تنفيذية، أتمتة، تكاملات، حوكمة، وقياس ROI."
    ),
    summary_en=(
        "A governed AI operating layer over your company: Company Brain, "
        "sales/support/operations agents, an executive dashboard, workflow "
        "automation, integrations, governance and ROI tracking."
    ),
    workstreams=(
        "AI opportunity audit",
        "Company Brain",
        "Sales agent",
        "Support agent",
        "Operations agent",
        "Executive dashboard",
        "Workflow automation",
        "Integrations",
        "Governance & security",
        "ROI tracking",
    ),
    tiers=(
        _tier(
            id="ai_os_basic",
            name_ar="أساسي",
            name_en="Basic",
            setup_sar=50_000.0,
            monthly_sar=10_000.0,
            min_duration_days=120,
            deliverables=(
                "Company Brain on your files",
                "One AI agent (sales OR support)",
                "Executive dashboard v1",
                "2 workflow automations",
                "1 integration (WhatsApp / CRM / Email)",
                "Governance & audit layer",
                "Monthly ROI report",
            ),
            kpi_ar=(
                "نسلّم النظام خلال 60 يومًا. إن لم يظهر أثر تشغيلي قابل للقياس "
                "في 90 يومًا، نشتغل بدون مقابل حتى يظهر."
            ),
            kpi_en=(
                "Delivered within 60 days. If no measurable operational impact "
                "appears within 90 days, we work for free until it does."
            ),
        ),
        _tier(
            id="ai_os_growth",
            name_ar="نمو",
            name_en="Growth",
            setup_sar=120_000.0,
            monthly_sar=25_000.0,
            min_duration_days=180,
            deliverables=(
                "Everything in Basic",
                "Two AI agents (sales + support)",
                "5 workflow automations",
                "3 integrations",
                "Knowledge Center with citations",
                "Quarterly executive review",
            ),
            kpi_ar=(
                "نلتزم بأتمتة عمليتين متكررتين على الأقل وخفض وقتهما، "
                "ونواصل التحسين بدون مقابل حتى يتحقق الالتزام."
            ),
            kpi_en=(
                "Commit to automating at least 2 recurring processes and "
                "cutting their cycle time; we keep tuning for free until met."
            ),
        ),
        _tier(
            id="ai_os_enterprise",
            name_ar="مؤسسي",
            name_en="Enterprise",
            setup_sar=250_000.0,
            monthly_sar=60_000.0,
            min_duration_days=365,
            deliverables=(
                "Everything in Growth",
                "Operations agent + multi-department agents",
                "Unlimited workflow automations in scope",
                "Full integration hub",
                "Dedicated governance & security review",
                "Executive command center + board pack",
            ),
            kpi_ar=(
                "نلتزم بطبقة تشغيل مؤسسية كاملة بحوكمة ومراجعة تدقيق، "
                "ونشتغل بدون مقابل حتى تكتمل معايير القبول المتفق عليها."
            ),
            kpi_en=(
                "Commit to a full governed enterprise operating layer with "
                "audit review; we work for free until agreed acceptance "
                "criteria are met."
            ),
        ),
    ),
    action_modes_used=_ENTERPRISE_ACTION_MODES,
    hard_gates=_ENTERPRISE_HARD_GATES,
)


# ── 2. AI Revenue Transformation ─────────────────────────────────────
_AI_REVENUE_TRANSFORMATION = EnterpriseOffering(
    id="ai_revenue_transformation",
    name_ar="تحوّل الإيراد بالذكاء الاصطناعي",
    name_en="AI Revenue Transformation",
    category="revenue",
    summary_ar=(
        "نحوّل عملية المبيعات: تحليل ICP، ذكاء العملاء المحتملين، وكيل مبيعات، "
        "تنظيف CRM، تقييم الفرص، متابعة عبر واتساب، ولوحة pipeline."
    ),
    summary_en=(
        "We transform the sales engine: ICP analysis, lead intelligence, a "
        "sales agent, CRM cleanup, lead scoring, WhatsApp follow-up and a "
        "pipeline dashboard."
    ),
    workstreams=(
        "ICP analysis",
        "Lead intelligence",
        "Sales agent",
        "CRM cleanup",
        "Lead scoring",
        "WhatsApp follow-up",
        "Pipeline dashboard",
        "Weekly revenue insights",
    ),
    tiers=(
        _tier(
            id="rev_basic",
            name_ar="أساسي",
            name_en="Basic",
            setup_sar=25_000.0,
            monthly_sar=5_000.0,
            min_duration_days=120,
            deliverables=(
                "ICP analysis + scoring model",
                "CRM cleanup (deduplicated lead board)",
                "Sales agent (draft-only outreach)",
                "Pipeline dashboard v1",
                "Weekly revenue insights",
            ),
            kpi_ar=(
                "نلتزم برفع جودة الـpipeline وتنظيف البيانات خلال 45 يومًا، "
                "ونواصل العمل بدون مقابل حتى يتحقق الالتزام."
            ),
            kpi_en=(
                "Commit to lifting pipeline quality and cleaning the data "
                "within 45 days; we work for free until met."
            ),
        ),
        _tier(
            id="rev_growth",
            name_ar="نمو",
            name_en="Growth",
            setup_sar=55_000.0,
            monthly_sar=15_000.0,
            min_duration_days=180,
            deliverables=(
                "Everything in Basic",
                "WhatsApp follow-up workflows (approval-gated)",
                "Objection handling library",
                "CRM integration (HubSpot)",
                "Monthly pipeline audit",
            ),
            kpi_ar=(
                "نلتزم بزيادة معدل الردود وتسريع المتابعة، ونشتغل بدون مقابل "
                "حتى يتحقق الالتزام المتفق عليه."
            ),
            kpi_en=(
                "Commit to lifting reply rate and follow-up speed; we work "
                "for free until the agreed commitment is met."
            ),
        ),
        _tier(
            id="rev_enterprise",
            name_ar="مؤسسي",
            name_en="Enterprise",
            setup_sar=100_000.0,
            monthly_sar=30_000.0,
            min_duration_days=365,
            deliverables=(
                "Everything in Growth",
                "Multi-channel sales agents",
                "Full revenue command center",
                "Quarterly revenue strategy review",
                "Dedicated governance review",
            ),
            kpi_ar=(
                "نلتزم بمنظومة إيراد مؤسسية مقيسة بالكامل، ونشتغل بدون مقابل "
                "حتى تكتمل معايير القبول."
            ),
            kpi_en=(
                "Commit to a fully measured enterprise revenue system; we "
                "work for free until acceptance criteria are met."
            ),
        ),
    ),
    action_modes_used=_ENTERPRISE_ACTION_MODES,
    hard_gates=_ENTERPRISE_HARD_GATES,
)


# ── 3. AI Knowledge & Decision Platform ──────────────────────────────
_AI_KNOWLEDGE_PLATFORM = EnterpriseOffering(
    id="ai_knowledge_platform",
    name_ar="منصة المعرفة والقرار بالذكاء الاصطناعي",
    name_en="AI Knowledge & Decision Platform",
    category="knowledge",
    summary_ar=(
        "نربط ملفات شركتك في Company Brain: مساعد داخلي للموظفين والإدارة، "
        "بحث بالعقود والسياسات، استشهادات بالمصدر، صلاحيات، وسجلّات تدقيق."
    ),
    summary_en=(
        "We connect your company files into a Company Brain: an internal "
        "assistant for staff and leadership, contract/policy search, source "
        "citations, permissions and audit logs."
    ),
    workstreams=(
        "Company file connection",
        "Employee assistant",
        "Leadership assistant",
        "Policy & proposal assistant",
        "Knowledge search with citations",
        "Permissions & RBAC",
        "Audit logs",
        "Usage reporting",
    ),
    tiers=(
        _tier(
            id="kn_basic",
            name_ar="أساسي",
            name_en="Basic",
            setup_sar=30_000.0,
            monthly_sar=8_000.0,
            min_duration_days=120,
            deliverables=(
                "Company Brain on your documents",
                "Employee knowledge assistant",
                "Source citations on every answer",
                "Role-based permissions",
                "Monthly usage report",
            ),
            kpi_ar=(
                "نلتزم بمساعد معرفة يجيب باستشهادات من مصادرك، ونواصل التحسين "
                "بدون مقابل حتى تتحقق جودة البحث المتفق عليها."
            ),
            kpi_en=(
                "Commit to a knowledge assistant that answers with citations "
                "from your sources; we tune for free until agreed search "
                "quality is met."
            ),
        ),
        _tier(
            id="kn_growth",
            name_ar="نمو",
            name_en="Growth",
            setup_sar=75_000.0,
            monthly_sar=20_000.0,
            min_duration_days=180,
            deliverables=(
                "Everything in Basic",
                "Leadership decision assistant",
                "Proposal & contract search",
                "Drive / Sheets integration",
                "Knowledge Center UI",
            ),
            kpi_ar=(
                "نلتزم بتغطية مصادر المعرفة الأساسية وصلاحيات دقيقة، "
                "ونشتغل بدون مقابل حتى يتحقق الالتزام."
            ),
            kpi_en=(
                "Commit to covering core knowledge sources with precise "
                "permissions; we work for free until met."
            ),
        ),
        _tier(
            id="kn_enterprise",
            name_ar="مؤسسي",
            name_en="Enterprise",
            setup_sar=150_000.0,
            monthly_sar=40_000.0,
            min_duration_days=365,
            deliverables=(
                "Everything in Growth",
                "Multi-department knowledge spaces",
                "Advanced governance & redaction",
                "Audit framework + access reviews",
                "Quarterly knowledge-quality review",
            ),
            kpi_ar=(
                "نلتزم بمنصة معرفة مؤسسية محوكمة بالكامل، ونشتغل بدون مقابل "
                "حتى تكتمل معايير القبول."
            ),
            kpi_en=(
                "Commit to a fully governed enterprise knowledge platform; "
                "we work for free until acceptance criteria are met."
            ),
        ),
    ),
    action_modes_used=_ENTERPRISE_ACTION_MODES,
    hard_gates=_ENTERPRISE_HARD_GATES,
)


# ── 4. AI Operations Automation ──────────────────────────────────────
_AI_OPERATIONS_AUTOMATION = EnterpriseOffering(
    id="ai_operations_automation",
    name_ar="أتمتة العمليات بالذكاء الاصطناعي",
    name_en="AI Operations Automation",
    category="operations",
    summary_ar=(
        "نرسم عمليات شركتك المتكررة ونؤتمتها: workflows، موافقات، تذكيرات، "
        "تقارير، تكاملات، حلقة بشرية، ومراقبة أخطاء."
    ),
    summary_en=(
        "We map your recurring operations and automate them: workflows, "
        "approvals, reminders, reports, integrations, human-in-the-loop and "
        "error monitoring."
    ),
    workstreams=(
        "Process mapping",
        "Automation opportunity scan",
        "Workflow build",
        "Approvals",
        "Reminders & reports",
        "Integrations",
        "Human-in-the-loop",
        "Error monitoring",
    ),
    tiers=(
        _tier(
            id="ops_basic",
            name_ar="أساسي",
            name_en="Basic",
            setup_sar=40_000.0,
            monthly_sar=8_000.0,
            min_duration_days=120,
            deliverables=(
                "Process map of core operations",
                "3 automated workflows",
                "Approval + human handoff gates",
                "Error monitoring + logs",
                "Monthly operations report",
            ),
            kpi_ar=(
                "نلتزم بأتمتة 3 عمليات متكررة خلال 45 يومًا، ونواصل العمل "
                "بدون مقابل حتى يتحقق الالتزام."
            ),
            kpi_en=(
                "Commit to automating 3 recurring processes within 45 days; "
                "we work for free until met."
            ),
        ),
        _tier(
            id="ops_growth",
            name_ar="نمو",
            name_en="Growth",
            setup_sar=95_000.0,
            monthly_sar=18_000.0,
            min_duration_days=180,
            deliverables=(
                "Everything in Basic",
                "8 automated workflows",
                "Cross-tool integrations",
                "Operations dashboard",
                "Quarterly optimization review",
            ),
            kpi_ar=(
                "نلتزم بخفض الوقت اليدوي في العمليات المشمولة، ونشتغل بدون "
                "مقابل حتى يتحقق الالتزام."
            ),
            kpi_en=(
                "Commit to cutting manual time across in-scope operations; "
                "we work for free until met."
            ),
        ),
        _tier(
            id="ops_enterprise",
            name_ar="مؤسسي",
            name_en="Enterprise",
            setup_sar=200_000.0,
            monthly_sar=35_000.0,
            min_duration_days=365,
            deliverables=(
                "Everything in Growth",
                "Enterprise-wide workflow program",
                "Full integration hub",
                "Dedicated governance & error SLA",
                "Operations command center",
            ),
            kpi_ar=(
                "نلتزم ببرنامج أتمتة مؤسسي محوكم، ونشتغل بدون مقابل حتى "
                "تكتمل معايير القبول."
            ),
            kpi_en=(
                "Commit to a governed enterprise-wide automation program; "
                "we work for free until acceptance criteria are met."
            ),
        ),
    ),
    action_modes_used=_ENTERPRISE_ACTION_MODES,
    hard_gates=_ENTERPRISE_HARD_GATES,
)


# ── 5. AI Governance & Readiness Program ─────────────────────────────
_AI_GOVERNANCE_PROGRAM = EnterpriseOffering(
    id="ai_governance_program",
    name_ar="برنامج حوكمة وجاهزية الذكاء الاصطناعي",
    name_en="AI Governance & Readiness Program",
    category="governance",
    summary_ar=(
        "نبني للشركة إطار حوكمة AI: سياسة، حوكمة بيانات، قواعد استخدام "
        "النماذج، مصفوفة مخاطر، إرشادات الموظفين، جاهزية PDPL، وإطار تدقيق."
    ),
    summary_en=(
        "We build the company's AI governance frame: policy, data "
        "governance, model-usage rules, a risk matrix, employee AI "
        "guidelines, PDPL readiness and an audit framework."
    ),
    workstreams=(
        "AI policy",
        "Data governance",
        "Model usage rules",
        "Risk matrix",
        "Employee AI guidelines",
        "Vendor risk review",
        "PDPL readiness",
        "Approval workflows",
        "Audit framework",
        "Executive AI roadmap",
    ),
    tiers=(
        _tier(
            id="gov_basic",
            name_ar="أساسي",
            name_en="Basic",
            setup_sar=35_000.0,
            monthly_sar=0.0,
            min_duration_days=45,
            deliverables=(
                "AI policy + model usage rules",
                "Employee AI guidelines",
                "Risk matrix v1",
                "PDPL readiness checklist",
                "Executive AI roadmap",
            ),
            kpi_ar=(
                "نسلّم إطار الحوكمة خلال 45 يومًا، ونواصل التعديل بدون مقابل "
                "حتى يعتمده مجلس الإدارة."
            ),
            kpi_en=(
                "We deliver the governance frame within 45 days and keep "
                "revising for free until the board adopts it."
            ),
        ),
        _tier(
            id="gov_growth",
            name_ar="نمو",
            name_en="Growth",
            setup_sar=70_000.0,
            monthly_sar=5_000.0,
            min_duration_days=120,
            deliverables=(
                "Everything in Basic",
                "Data governance + approval workflows",
                "Vendor risk review",
                "Audit framework",
                "Quarterly governance review",
            ),
            kpi_ar=(
                "نلتزم بإطار حوكمة قابل للتدقيق وموافقات مفعّلة، ونواصل العمل "
                "بدون مقابل حتى يتحقق الالتزام."
            ),
            kpi_en=(
                "Commit to an auditable governance frame with live approval "
                "workflows; we work for free until met."
            ),
        ),
        _tier(
            id="gov_enterprise",
            name_ar="مؤسسي",
            name_en="Enterprise",
            setup_sar=120_000.0,
            monthly_sar=10_000.0,
            min_duration_days=365,
            deliverables=(
                "Everything in Growth",
                "Enterprise risk & compliance program",
                "Continuous audit + access reviews",
                "Board-level AI governance reporting",
                "Annual readiness re-assessment",
            ),
            kpi_ar=(
                "نلتزم ببرنامج حوكمة مؤسسي مستمر، ونواصل العمل بدون مقابل "
                "حتى تكتمل معايير القبول."
            ),
            kpi_en=(
                "Commit to a continuous enterprise governance program; we "
                "work for free until acceptance criteria are met."
            ),
        ),
    ),
    action_modes_used=_ENTERPRISE_ACTION_MODES,
    hard_gates=_ENTERPRISE_HARD_GATES,
)


# ── Flagship — Enterprise AI Transformation Sprint (45 days) ─────────
_ENTERPRISE_TRANSFORMATION_SPRINT = EnterpriseOffering(
    id="enterprise_transformation_sprint",
    name_ar="سبرنت التحوّل المؤسسي بالذكاء الاصطناعي (45 يومًا)",
    name_en="Enterprise AI Transformation Sprint (45 days)",
    category="transformation_sprint",
    summary_ar=(
        "خلال 45 يومًا نحوّل المبيعات والدعم والمعرفة والعمليات إلى نظام AI "
        "قابل للقياس ومربوط ببياناتك، مع لوحة ROI وطبقة حوكمة وخطة توسّع."
    ),
    summary_en=(
        "In 45 days we turn sales, support, knowledge and operations into a "
        "measurable AI system wired to your data — with an ROI dashboard, a "
        "governance layer and a 90-day expansion plan."
    ),
    workstreams=(
        "AI opportunity audit",
        "Company Brain",
        "Sales or support agent",
        "1-2 workflow automations",
        "Integrations with your tools",
        "Executive ROI dashboard",
        "Governance & security layer",
        "Team training",
        "90-day expansion plan",
    ),
    tiers=(
        _tier(
            id="sprint_basic",
            name_ar="تحوّل أساسي",
            name_en="Basic Transformation",
            setup_sar=25_000.0,
            monthly_sar=0.0,
            min_duration_days=45,
            deliverables=(
                "AI opportunity audit",
                "Company Brain on your files",
                "One AI agent (sales OR support)",
                "1 workflow automation",
                "1 integration",
                "Executive ROI dashboard v1",
                "Governance layer + team training",
                "90-day expansion plan",
            ),
            kpi_ar=(
                "نسلّم خلال 45 يومًا. إن لم يظهر أثر واضح في الفترة التجريبية، "
                "لا نوسّع المشروع — والقرار قرارك."
            ),
            kpi_en=(
                "Delivered in 45 days. If no clear impact appears in the "
                "trial window, we do not expand the engagement — your call."
            ),
        ),
        _tier(
            id="sprint_growth",
            name_ar="تحوّل نمو",
            name_en="Growth Transformation",
            setup_sar=75_000.0,
            monthly_sar=8_000.0,
            min_duration_days=45,
            deliverables=(
                "Everything in Basic",
                "Two AI agents (sales + support)",
                "2 workflow automations",
                "2-3 integrations",
                "Knowledge Center with citations",
                "Monthly ROI report + review",
            ),
            kpi_ar=(
                "نلتزم بنظام AI مقيس عبر مسارين خلال 45 يومًا، ونواصل العمل "
                "بدون مقابل حتى يتحقق الالتزام المتفق عليه."
            ),
            kpi_en=(
                "Commit to a measured two-track AI system in 45 days; we "
                "work for free until the agreed commitment is met."
            ),
        ),
        _tier(
            id="sprint_enterprise",
            name_ar="تحوّل مؤسسي",
            name_en="Enterprise Transformation",
            setup_sar=150_000.0,
            monthly_sar=20_000.0,
            min_duration_days=45,
            deliverables=(
                "Everything in Growth",
                "Multi-department agents",
                "Full integration hub",
                "Executive command center",
                "Dedicated governance & security review",
                "90-day expansion roadmap with owners",
            ),
            kpi_ar=(
                "نلتزم بطبقة تشغيل AI مؤسسية بحوكمة كاملة، ونشتغل بدون مقابل "
                "حتى تكتمل معايير القبول المتفق عليها."
            ),
            kpi_en=(
                "Commit to a fully governed enterprise AI operating layer; "
                "we work for free until agreed acceptance criteria are met."
            ),
        ),
    ),
    action_modes_used=_ENTERPRISE_ACTION_MODES,
    hard_gates=_ENTERPRISE_HARD_GATES,
)


# Canonical enterprise registry — flagship first (catalog display order).
ENTERPRISE_OFFERINGS: tuple[EnterpriseOffering, ...] = (
    _ENTERPRISE_TRANSFORMATION_SPRINT,
    _AI_OPERATING_SYSTEM,
    _AI_REVENUE_TRANSFORMATION,
    _AI_KNOWLEDGE_PLATFORM,
    _AI_OPERATIONS_AUTOMATION,
    _AI_GOVERNANCE_PROGRAM,
)

ENTERPRISE_OFFERING_IDS: frozenset[str] = frozenset(
    o.id for o in ENTERPRISE_OFFERINGS
)


def list_enterprise_offerings() -> tuple[EnterpriseOffering, ...]:
    """All enterprise programs in catalog display order (flagship first)."""
    return ENTERPRISE_OFFERINGS


def get_enterprise_offering(offering_id: str) -> EnterpriseOffering | None:
    """Return one enterprise program by id, or None if not found."""
    for o in ENTERPRISE_OFFERINGS:
        if o.id == offering_id:
            return o
    return None


def get_enterprise_tier(offering_id: str, tier_id: str) -> PricingTier | None:
    """Return one pricing tier within an enterprise program."""
    offering = get_enterprise_offering(offering_id)
    if offering is None:
        return None
    for t in offering.tiers:
        if t.id == tier_id:
            return t
    return None
