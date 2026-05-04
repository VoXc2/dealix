"""Static registry of named agents with their governance contracts."""
from __future__ import annotations

from auto_client_acquisition.agent_governance.schemas import (
    AgentSpec,
    AutonomyLevel,
    ToolCategory,
)


# 12 named agents that mirror auto_client_acquisition/v3/agents.py
# AgentName entries, each with an explicit governance spec. New
# agents must be added here OR they fail evaluation.
AGENT_REGISTRY: dict[str, AgentSpec] = {
    "prospecting": AgentSpec(
        agent_id="prospecting",
        purpose_ar="اكتشاف شركات سعوديّة عالية الملاءمة من مصادر مرخّصة فقط.",
        purpose_en="Find high-fit Saudi companies from licensed sources only.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[
            ToolCategory.READ_PUBLIC_WEB,
            ToolCategory.READ_INTERNAL_DOCS,
        ],
        forbidden_tools=[
            ToolCategory.SCRAPE_WEB,
            ToolCategory.LINKEDIN_AUTOMATION,
            ToolCategory.SEND_WHATSAPP_LIVE,
        ],
        notes="No directory scraping. Public business data only.",
    ),
    "signal": AgentSpec(
        agent_id="signal",
        purpose_ar="رصد إشارات شراء (why-now) من بيانات مرخّصة.",
        purpose_en="Detect why-now buying triggers from licensed data.",
        max_autonomy=AutonomyLevel.L1_DRAFT_ONLY,
        allowed_tools=[ToolCategory.READ_PUBLIC_WEB, ToolCategory.READ_INTERNAL_DOCS],
        forbidden_tools=[ToolCategory.SCRAPE_WEB],
    ),
    "enrichment": AgentSpec(
        agent_id="enrichment",
        purpose_ar="إثراء سياق الشركة من مصادر مرخّصة.",
        purpose_en="Enrich company/contact context from licensed providers.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.READ_PUBLIC_WEB, ToolCategory.READ_INTERNAL_DOCS],
        forbidden_tools=[ToolCategory.SCRAPE_WEB],
    ),
    "personalization": AgentSpec(
        agent_id="personalization",
        purpose_ar="صياغة مسوّدات تواصل عربيّة وإنجليزيّة بإشراف بشري.",
        purpose_en="Draft Arabic/English outreach with human review.",
        max_autonomy=AutonomyLevel.L1_DRAFT_ONLY,
        allowed_tools=[
            ToolCategory.DRAFT_MESSAGE,
            ToolCategory.DRAFT_EMAIL,
            ToolCategory.DRAFT_WHATSAPP_REPLY,
            ToolCategory.READ_INTERNAL_DOCS,
        ],
        forbidden_tools=[
            ToolCategory.SEND_WHATSAPP_LIVE,
            ToolCategory.SEND_EMAIL_LIVE,
            ToolCategory.LINKEDIN_AUTOMATION,
        ],
    ),
    "compliance": AgentSpec(
        agent_id="compliance",
        purpose_ar="حظر الإجراءات غير المتوافقة مع PDPL/SDAIA قبل التنفيذ.",
        purpose_en="Block PDPL/SDAIA-non-compliant actions before execution.",
        max_autonomy=AutonomyLevel.L4_INTERNAL_AUTOMATION_ONLY,
        allowed_tools=[ToolCategory.READ_INTERNAL_DOCS],
        forbidden_tools=[
            ToolCategory.SEND_WHATSAPP_LIVE,
            ToolCategory.SEND_EMAIL_LIVE,
            ToolCategory.SCRAPE_WEB,
            ToolCategory.LINKEDIN_AUTOMATION,
            ToolCategory.CHARGE_PAYMENT_LIVE,
        ],
    ),
    "outreach": AgentSpec(
        agent_id="outreach",
        purpose_ar="تجهيز رسائل تواصل تحتاج موافقة قبل أيّ إرسال.",
        purpose_en="Queue approved messages — never auto-send.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[
            ToolCategory.DRAFT_MESSAGE,
            ToolCategory.DRAFT_EMAIL,
            ToolCategory.DRAFT_WHATSAPP_REPLY,
            ToolCategory.READ_INTERNAL_DOCS,
        ],
        forbidden_tools=[
            ToolCategory.SEND_WHATSAPP_LIVE,
            ToolCategory.SEND_EMAIL_LIVE,
            ToolCategory.LINKEDIN_AUTOMATION,
        ],
    ),
    "reply": AgentSpec(
        agent_id="reply",
        purpose_ar="تصنيف ردود العملاء واقتراح المسار التالي.",
        purpose_en="Classify replies + suggest next step.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.READ_INTERNAL_DOCS, ToolCategory.DRAFT_MESSAGE],
    ),
    "meeting": AgentSpec(
        agent_id="meeting",
        purpose_ar="تحويل الردود الإيجابيّة إلى اجتماعات مُجدوَلة بالموافقة.",
        purpose_en="Turn positive replies into approved meetings.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.DRAFT_EMAIL, ToolCategory.READ_INTERNAL_DOCS],
        forbidden_tools=[ToolCategory.SEND_EMAIL_LIVE],
    ),
    "deal_coach": AgentSpec(
        agent_id="deal_coach",
        purpose_ar="اقتراح أفضل خطوة قادمة لكلّ صفقة بناءً على البيانات.",
        purpose_en="Recommend next best deal action.",
        max_autonomy=AutonomyLevel.L1_DRAFT_ONLY,
        allowed_tools=[ToolCategory.READ_INTERNAL_DOCS],
    ),
    "customer_success": AgentSpec(
        agent_id="customer_success",
        purpose_ar="تتبّع تسليم العميل وتجهيز Proof Pack.",
        purpose_en="Track customer delivery and prepare the Proof Pack.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[
            ToolCategory.READ_INTERNAL_DOCS,
            ToolCategory.GENERATE_PROOF_PACK,
            ToolCategory.DRAFT_EMAIL,
        ],
        forbidden_tools=[ToolCategory.SEND_EMAIL_LIVE],
    ),
    "executive_analyst": AgentSpec(
        agent_id="executive_analyst",
        purpose_ar="تجهيز ملخّصات تنفيذيّة عربيّة من البيانات.",
        purpose_en="Build Arabic executive summaries from data.",
        max_autonomy=AutonomyLevel.L1_DRAFT_ONLY,
        allowed_tools=[ToolCategory.READ_INTERNAL_DOCS],
    ),
    "finance_assistant": AgentSpec(
        agent_id="finance_assistant",
        purpose_ar="تجهيز مسوّدات الفواتير ومتابعة حالة الدفع — بدون خصم تلقائي.",
        purpose_en="Draft invoices + track payment status — no auto-charge.",
        max_autonomy=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[
            ToolCategory.CREATE_INVOICE_DRAFT,
            ToolCategory.READ_INTERNAL_DOCS,
        ],
        forbidden_tools=[ToolCategory.CHARGE_PAYMENT_LIVE],
    ),
}


def list_agents() -> list[str]:
    return sorted(AGENT_REGISTRY.keys())


def get_agent(agent_id: str) -> AgentSpec:
    if agent_id not in AGENT_REGISTRY:
        raise KeyError(f"unknown agent: {agent_id}")
    return AGENT_REGISTRY[agent_id]
