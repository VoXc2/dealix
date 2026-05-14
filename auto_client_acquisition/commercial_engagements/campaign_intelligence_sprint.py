"""Deterministic campaign angles + audited copy snippets (no LLM)."""

from __future__ import annotations

from auto_client_acquisition.commercial_engagements.schemas import (
    CampaignIntelligenceSprintInput,
    CampaignIntelligenceSprintReport,
)
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text


def run_campaign_intelligence_sprint(
    inp: CampaignIntelligenceSprintInput | dict,
) -> CampaignIntelligenceSprintReport:
    if isinstance(inp, dict):
        inp = CampaignIntelligenceSprintInput.model_validate(inp)

    title = inp.offer_title.strip()
    sector = inp.sector.strip() or "القطاع المستهدف"

    if inp.locale == "ar":
        angles = [
            f"ربط العرض «{title}» بأثر تشغيلي واضح في {sector}.",
            "تسليط الضوء على الامتثال والموافقات قبل التوسع في الحملات.",
            "قصة عميل داخلي أو نتيجة قابلة للتحقق بدل ادعاءات عامة.",
        ]
        hooks = [
            "هل تبحثون عن تقليل تسرب الصفقات دون زيادة ضوضاء التسويق؟",
            "جاهزية البيانات أولاً: ما الذي يمنعكم من توسيع الاستهداف اليوم؟",
        ]
        d1 = (
            f"مسودّة — عنوان: {title}. نقدّم جلسة تشخيص قصيرة لفهم نضج البيانات "
            f"في قطاع {sector} قبل أي حملة مدفوعة."
        )
        d2 = (
            "مسودّة — ندعوكم لمراجعة سياسة الموافقات على الرسائل الخارجية "
            "لضمان عدم إرسال أي تسويق بارد عبر واتساب أو أتمتة لينكدإن."
        )
    else:
        angles = [
            f"Tie «{title}» to measurable ops impact in {sector}.",
            "Lead with compliance and approvals before scaling paid reach.",
            "Prefer verified outcomes over generic claims.",
        ]
        hooks = [
            "Are pipeline leaks coming from data quality or follow-up?",
            "What blocks you from expanding targeting safely this quarter?",
        ]
        d1 = (
            f"Draft — {title}: a short diagnostic to assess data readiness in "
            f"{sector} before scaling paid campaigns."
        )
        d2 = (
            "Draft — we recommend an approval policy for outbound messages; "
            "no cold WhatsApp or LinkedIn automation."
        )

    snippets = [
        {"label": "primary", "text": d1, "issues": audit_draft_text(d1)},
        {"label": "compliance", "text": d2, "issues": audit_draft_text(d2)},
    ]
    risk_flags: list[str] = []
    for s in snippets:
        risk_flags.extend(s["issues"])

    return CampaignIntelligenceSprintReport(
        angles=angles,
        message_hooks=hooks,
        risk_flags=risk_flags,
        draft_snippets=snippets,
    )
