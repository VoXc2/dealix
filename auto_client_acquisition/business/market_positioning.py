"""Competitive positioning — deterministic reference data."""

from __future__ import annotations

from typing import Any, Literal

Segment = Literal["founder", "sme", "enterprise", "agency"]


def compare_competitors() -> list[dict[str, Any]]:
    """High-level comparison; not exhaustive feature matrices."""
    return [
        {
            "name": "HubSpot",
            "strengths": ["Wide CRM/marketing suite", "AI + context narrative (2026)"],
            "weaknesses_sa_gcc": ["Not Arabic-native operator", "Generic B2B, not Saudi revenue graph"],
            "dealix_wins": ["Arabic Chief of Staff", "PDPL-first posture", "WhatsApp approval-native flows"],
            "do_not_copy": ["Boil-the-ocean suite creep"],
            "borrow": ["Context-rich AI positioning", "agent + deal progression story"],
        },
        {
            "name": "Salesforce",
            "strengths": ["Enterprise platform depth"],
            "weaknesses_sa_gcc": ["Heavy ops", "Slow founder-led adoption", "Arabic UX gap"],
            "dealix_wins": ["Founder speed", "Saudi signal packs", "Outcome pricing option"],
            "do_not_copy": ["Customization trap without outcomes"],
            "borrow": ["Account-centric revenue thinking"],
        },
        {
            "name": "Gong",
            "strengths": ["Revenue intelligence", "expanding to enablement + AM (Mission Andromeda narrative)"],
            "weaknesses_sa_gcc": ["Call-centric origins", "Arabic market nuance"],
            "dealix_wins": ["WhatsApp-first reality", "why-now radar + Arabic drafts"],
            "do_not_copy": ["Recording-heavy compliance risk without clear PDPL story"],
            "borrow": ["Revenue OS narrative breadth beyond raw calls"],
        },
        {
            "name": "Apollo / ZoomInfo",
            "strengths": ["Prospecting data scale"],
            "weaknesses_sa_gcc": ["Cold outreach culture", "Compliance friction in GCC"],
            "dealix_wins": ["Approval gates", "contactability OS", "Saudi context"],
            "do_not_copy": ["Spray-and-pray automation"],
            "borrow": ["Structured prospect lists as input, not autopilot"],
        },
        {
            "name": "Zoho / Odoo",
            "strengths": ["Price + ERP breadth"],
            "weaknesses_sa_gcc": ["Not a revenue memory + operator system"],
            "dealix_wins": ["Strategic operator + proof pack + market radar"],
            "do_not_copy": ["ERP generalism as core story"],
            "borrow": ["SMB packaging discipline"],
        },
        {
            "name": "WhatsApp automation tools",
            "strengths": ["Channel reach"],
            "weaknesses_sa_gcc": ["Cold spam risk", "weak PDPL story"],
            "dealix_wins": ["Opt-in + approval + audit", "Arabic relationship operator"],
            "do_not_copy": ["Auto-send cold campaigns"],
            "borrow": ["Interactive buttons — max 3 per message; two-step flows"],
        },
        {
            "name": "Boardy-style intro tools",
            "strengths": ["Accept/skip UX for intros"],
            "weaknesses_sa_gcc": ["Limited Saudi B2B + revenue proof loop"],
            "dealix_wins": ["Revenue memory + command center + compliance + Arabic"],
            "do_not_copy": ["Shallow CRM replacement claims"],
            "borrow": ["Relationship card UX patterns"],
        },
        {
            "name": "SocraticCode-style indexing",
            "strengths": ["Repo understanding"],
            "weaknesses_sa_gcc": ["Not revenue + market + Arabic operator"],
            "dealix_wins": ["Project intelligence + strategic memory + GTM"],
            "do_not_copy": ["Dev-only scope"],
            "borrow": ["Chunking + local index before vectors"],
        },
    ]


def dealix_differentiators() -> list[str]:
    return [
        "Governed Revenue & AI Operations positioning",
        "Approval-first external action safety",
        "Decision Passport + evidence-led operating rhythm",
        "Source-backed ROI narrative (no vanity metrics)",
        "Service-led to platform learning loop",
        "Arabic-first + Saudi/GCC localization",
        "Trust moat: no autonomous external send",
        "Workflow moat: repeated delivery playbooks",
    ]


def positioning_statement(segment: Segment) -> str:
    statements: dict[Segment, str] = {
        "founder": (
            "Dealix شركة Governed Revenue & AI Operations: نحوّل تجارب AI وعمليات الإيراد "
            "إلى workflow محكوم بالمصدر والموافقة والدليل قبل أي إجراء خارجي."
        ),
        "sme": (
            "للشركات المتوسطة: Dealix يبني طبقة تشغيل تربط CRM والمتابعة والحوكمة مع "
            "Decision Passport وProof Pack لإثبات قيمة قابلة للقياس."
        ),
        "enterprise": (
            "للمؤسسات: Dealix طبقة تشغيل محكومة تجمع approvals وevidence وauditability "
            "لوكلاء AI وعمليات الإيراد ضمن حدود ثقة واضحة."
        ),
        "agency": (
            "لشركاء التنفيذ: نبدأ بخدمات Revenue Ops محكومة ثم نحوّل التشغيل المتكرر إلى "
            "playbooks ومنصة داخلية بدل بيع أتمتة AI غير منضبطة."
        ),
    }
    return statements.get(segment, statements["founder"])
