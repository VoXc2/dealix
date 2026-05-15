"""AI Opportunity Report — the founder-led enterprise sales artifact.

For a target company, produces 5 concrete AI opportunities with an expected
impact hypothesis (time / conversion / cost / risk), each mapped to one of
the enterprise transformation programs, plus a recommended program + tier.

Deterministic composition (no LLM, no external HTTP) — CI-safe and
reproducible. Article 8 holds: impact is an *estimate / hypothesis*, never
a guarantee. The report is approval-gated; the founder reviews before any
outreach.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

# Impact areas an AI opportunity can move (estimate-only, never guaranteed).
ImpactArea = str  # time_saved | conversion_lift | cost_reduction
#                   risk_reduction | revenue_visibility


@dataclass(frozen=True, slots=True)
class AIOpportunity:
    id: str
    title_ar: str
    title_en: str
    workstream: str
    impact_area: ImpactArea
    impact_hypothesis_ar: str
    impact_hypothesis_en: str
    mapped_program_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AIOpportunityReport:
    company: str
    sector: str
    region: str
    opportunities: list[AIOpportunity]
    recommended_program_id: str
    recommended_tier_id: str
    markdown_ar_en: str
    approval_status: str = "approval_required"
    is_estimate: bool = True
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["opportunities"] = [o.to_dict() for o in self.opportunities]
        return d


# ── Opportunity templates ────────────────────────────────────────────
# Each is a hypothesis the founder validates with the prospect — never a
# promise. Keyed by a stable id; selected per sector below.
_OPP = AIOpportunity


def _o(
    id: str,
    title_ar: str,
    title_en: str,
    workstream: str,
    impact_area: str,
    hyp_ar: str,
    hyp_en: str,
    program: str,
) -> AIOpportunity:
    return _OPP(
        id=id,
        title_ar=title_ar,
        title_en=title_en,
        workstream=workstream,
        impact_area=impact_area,
        impact_hypothesis_ar=hyp_ar,
        impact_hypothesis_en=hyp_en,
        mapped_program_id=program,
    )


_LEAD_QUALIFICATION = _o(
    "lead_qualification",
    "تأهيل العملاء المحتملين آليًا",
    "Automated lead qualification",
    "Sales agent",
    "conversion_lift",
    "قد يرفع تركيز الفريق على الفرص الأعلى جاهزية ويقلّل الوقت الضائع.",
    "May raise focus on higher-fit opportunities and cut wasted time.",
    "ai_revenue_transformation",
)
_WHATSAPP_FOLLOWUP = _o(
    "whatsapp_followup",
    "متابعة منظَّمة عبر واتساب (بموافقة)",
    "Structured WhatsApp follow-up (consent-based)",
    "WhatsApp follow-up",
    "conversion_lift",
    "قد يقلّل تسرّب العملاء بين أول تواصل والحجز.",
    "May reduce prospect drop-off between first contact and booking.",
    "ai_revenue_transformation",
)
_CRM_CLEANUP = _o(
    "crm_cleanup",
    "تنظيف بيانات الـCRM وإزالة التكرار",
    "CRM cleanup and deduplication",
    "CRM cleanup",
    "time_saved",
    "قد يخفّض الوقت اليدوي في إدارة البيانات ويحسّن دقة التقارير.",
    "May cut manual data-admin time and improve report accuracy.",
    "ai_revenue_transformation",
)
_KNOWLEDGE_ASSISTANT = _o(
    "knowledge_assistant",
    "مساعد معرفة داخلي للموظفين",
    "Internal employee knowledge assistant",
    "Employee assistant",
    "time_saved",
    "قد يقلّل وقت البحث عن السياسات والإجراءات والعقود.",
    "May cut time spent searching policies, procedures and contracts.",
    "ai_knowledge_platform",
)
_PROPOSAL_ASSISTANT = _o(
    "proposal_assistant",
    "مساعد إعداد العروض والمقترحات",
    "Proposal drafting assistant",
    "Policy & proposal assistant",
    "time_saved",
    "قد يسرّع إعداد العروض مع اتساق أعلى في الصياغة.",
    "May speed up proposal drafting with more consistent language.",
    "ai_knowledge_platform",
)
_SUPPORT_TRIAGE = _o(
    "support_triage",
    "تصنيف وتوجيه طلبات الدعم",
    "Support request triage and routing",
    "Support agent",
    "time_saved",
    "قد يقلّل وقت الردّ الأول ويخفّف عبء الفريق في الذروة.",
    "May cut first-response time and ease team load at peak.",
    "ai_operating_system",
)
_PROCESS_AUTOMATION = _o(
    "process_automation",
    "أتمتة عملية تشغيلية متكررة",
    "Recurring operational workflow automation",
    "Workflow build",
    "cost_reduction",
    "قد يخفّض التكلفة التشغيلية للعملية المتكررة المختارة.",
    "May reduce the operating cost of the selected recurring process.",
    "ai_operations_automation",
)
_APPROVALS_FLOW = _o(
    "approvals_flow",
    "مسار موافقات بحلقة بشرية",
    "Human-in-the-loop approvals flow",
    "Approvals",
    "risk_reduction",
    "قد يقلّل أخطاء التنفيذ ويحسّن وضوح المساءلة.",
    "May reduce execution errors and improve accountability clarity.",
    "ai_operations_automation",
)
_EXEC_DASHBOARD = _o(
    "exec_dashboard",
    "لوحة تنفيذية لقياس الأثر",
    "Executive impact dashboard",
    "Executive dashboard",
    "revenue_visibility",
    "قد يعطي الإدارة رؤية أوضح للوقت الموفّر وفرص الإيراد.",
    "May give leadership clearer visibility of time saved and revenue.",
    "ai_operating_system",
)
_AI_GOVERNANCE = _o(
    "ai_governance",
    "إطار حوكمة لاستخدام الذكاء الاصطناعي",
    "AI usage governance framework",
    "AI policy",
    "risk_reduction",
    "قد يقلّل مخاطر الاستخدام غير المنضبط ويسرّع التبنّي الآمن.",
    "May reduce ungoverned-usage risk and speed safe adoption.",
    "ai_governance_program",
)


# Sector → curated 5 opportunities + recommended program.
_SECTOR_PLAYBOOK: dict[str, tuple[tuple[AIOpportunity, ...], str]] = {
    "real_estate": (
        (
            _LEAD_QUALIFICATION,
            _WHATSAPP_FOLLOWUP,
            _CRM_CLEANUP,
            _EXEC_DASHBOARD,
            _PROCESS_AUTOMATION,
        ),
        "ai_revenue_transformation",
    ),
    "b2b_services": (
        (
            _LEAD_QUALIFICATION,
            _PROPOSAL_ASSISTANT,
            _KNOWLEDGE_ASSISTANT,
            _PROCESS_AUTOMATION,
            _EXEC_DASHBOARD,
        ),
        "enterprise_transformation_sprint",
    ),
    "training_consulting": (
        (
            _KNOWLEDGE_ASSISTANT,
            _PROPOSAL_ASSISTANT,
            _SUPPORT_TRIAGE,
            _PROCESS_AUTOMATION,
            _EXEC_DASHBOARD,
        ),
        "ai_knowledge_platform",
    ),
    "healthcare_clinic": (
        (
            _SUPPORT_TRIAGE,
            _PROCESS_AUTOMATION,
            _APPROVALS_FLOW,
            _AI_GOVERNANCE,
            _EXEC_DASHBOARD,
        ),
        "ai_operations_automation",
    ),
}

_DEFAULT_PLAYBOOK: tuple[tuple[AIOpportunity, ...], str] = (
    (
        _LEAD_QUALIFICATION,
        _KNOWLEDGE_ASSISTANT,
        _PROCESS_AUTOMATION,
        _EXEC_DASHBOARD,
        _AI_GOVERNANCE,
    ),
    "enterprise_transformation_sprint",
)


def list_opportunity_sectors() -> list[str]:
    return sorted(_SECTOR_PLAYBOOK.keys())


def _render_markdown(
    *,
    company: str,
    sector: str,
    region: str,
    opportunities: list[AIOpportunity],
    program_id: str,
    tier_id: str,
) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md: list[str] = []
    md.append(f"# AI Opportunity Report — {company}")
    md.append("")
    md.append(f"> **Date:** {today} · **Sector:** `{sector}` · **Region:** `{region}`")
    md.append("> Generated by Dealix — founder review required before outreach.")
    md.append("")
    md.append("## القراءة السريعة (عربي)")
    md.append("")
    md.append(
        f"حلّلنا قطاع **{company}** وحدّدنا **5 فرص ذكاء اصطناعي** قد توفّر وقتًا "
        "وتزيد التحويل وتخفّض التكلفة. كل رقم تقديري ويُتحقَّق منه في التدقيق."
    )
    md.append("")
    for i, opp in enumerate(opportunities, 1):
        md.append(f"{i}. **{opp.title_ar}** — {opp.impact_hypothesis_ar}")
    md.append("")
    md.append("## Executive summary (English)")
    md.append("")
    md.append(
        f"We reviewed **{company}** and surfaced **5 AI opportunities** that may "
        "save time, lift conversion and cut cost. Every number is an estimate, "
        "validated during the audit."
    )
    md.append("")
    for i, opp in enumerate(opportunities, 1):
        md.append(
            f"{i}. **{opp.title_en}** ({opp.impact_area}) — "
            f"{opp.impact_hypothesis_en}"
        )
    md.append("")
    md.append("## Recommended program")
    md.append("")
    md.append(
        f"- **Program:** `{program_id}` · **Tier:** `{tier_id}`"
    )
    md.append(
        "- Next step: a 20-minute call, then an enterprise proposal with "
        "Basic / Growth / Enterprise tiers."
    )
    md.append("")
    md.append("## What we will NOT do")
    md.append("- لا إرسال رسائل بلا موافقة، ولا جمع بيانات غير مصرّح به.")
    md.append("- No outreach without consent; no unauthorized data collection.")
    md.append("- لا وعود بأرقام مؤكدة — التزام بالعمل، والأرقام تقديرية.")
    md.append("- No promised numbers — commitment to the work; figures are estimates.")
    md.append("")
    md.append("> Founder review required before this report is sent.")
    return "\n".join(md)


def generate_opportunity_report(
    *,
    company: str,
    sector: str = "b2b_services",
    region: str = "ksa",
    recommended_tier_id: str = "",
) -> AIOpportunityReport:
    """Build an AI Opportunity Report for one target company."""
    if not company.strip():
        raise ValueError("company is required")
    opportunities, program_id = _SECTOR_PLAYBOOK.get(sector, _DEFAULT_PLAYBOOK)
    opp_list = list(opportunities)
    tier_id = recommended_tier_id or _default_tier_for(program_id)
    md = _render_markdown(
        company=company,
        sector=sector,
        region=region,
        opportunities=opp_list,
        program_id=program_id,
        tier_id=tier_id,
    )
    return AIOpportunityReport(
        company=company,
        sector=sector,
        region=region,
        opportunities=opp_list,
        recommended_program_id=program_id,
        recommended_tier_id=tier_id,
        markdown_ar_en=md,
    )


def _default_tier_for(program_id: str) -> str:
    """Growth tier is the default enterprise recommendation."""
    return {
        "enterprise_transformation_sprint": "sprint_growth",
        "ai_operating_system": "ai_os_growth",
        "ai_revenue_transformation": "rev_growth",
        "ai_knowledge_platform": "kn_growth",
        "ai_operations_automation": "ops_growth",
        "ai_governance_program": "gov_growth",
    }.get(program_id, "")


__all__ = [
    "AIOpportunity",
    "AIOpportunityReport",
    "generate_opportunity_report",
    "list_opportunity_sectors",
]
