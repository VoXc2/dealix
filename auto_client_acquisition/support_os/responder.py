"""V12 Support OS — bilingual reply drafter.

Always ``draft_only``. NEVER sends. NEVER invents policy. If the
knowledge base is empty for a category, returns
``insufficient_evidence`` and recommends escalation.
"""
from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.support_os.classifier import (
    ClassificationResult,
)
from auto_client_acquisition.support_os.escalation import (
    EscalationDecision,
    should_escalate,
)
from auto_client_acquisition.support_os.knowledge_answer import (
    KnowledgeAnswer,
    answer_from_knowledge_base,
)


@dataclass
class ReplyDraft:
    action_mode: str
    text_ar: str
    text_en: str
    sources: list[str]
    insufficient_evidence: bool
    escalation: EscalationDecision


def draft_response(
    *, message: str, classification: ClassificationResult
) -> ReplyDraft:
    esc = should_escalate(classification=classification, message=message)
    answer: KnowledgeAnswer = answer_from_knowledge_base(classification.category)

    if esc.should_escalate:
        ar = (
            "شكراً على تواصلك. هذا الموضوع يحتاج مراجعة بشريّة من المؤسس "
            "قبل أي إجراء، وسنرجع لك بأسرع وقت. لا نُرسل أي ردّ آلي على "
            "هذه الفئة."
        )
        en = (
            "Thanks for reaching out. This topic requires founder review "
            "before any action; we'll get back to you as soon as possible. "
            "No automated reply is sent for this category."
        )
        return ReplyDraft(
            action_mode="approval_required",
            text_ar=ar,
            text_en=en,
            sources=answer.sources,
            insufficient_evidence=answer.insufficient_evidence,
            escalation=esc,
        )

    if answer.insufficient_evidence:
        ar = (
            "شكراً على رسالتك. حتّى نقدر نجاوبك بدقّة، نحتاج نراجع التفاصيل "
            "مع المؤسس. نرجع لك خلال ساعات العمل القادمة. (insufficient_evidence)"
        )
        en = (
            "Thanks for your message. To answer accurately we need to "
            "review with the founder; we'll respond during business "
            "hours. (insufficient_evidence)"
        )
        return ReplyDraft(
            action_mode="approval_required",
            text_ar=ar,
            text_en=en,
            sources=[],
            insufficient_evidence=True,
            escalation=esc,
        )

    ar = (
        "شكراً على سؤالك. هذه نقاط من سياسة Dealix الموثّقة (مسودّة "
        "للمراجعة قبل الإرسال). المؤسس يعتمد المسودّة قبل الردّ النهائي. "
        f"المصادر: {', '.join(answer.sources) or 'docs/knowledge-base/'}"
    )
    en = (
        "Thanks for your question. The points below are from Dealix's "
        "documented policy (draft for review before sending). The "
        "founder approves the draft before any final reply. "
        f"Sources: {', '.join(answer.sources) or 'docs/knowledge-base/'}"
    )
    return ReplyDraft(
        action_mode="draft_only",
        text_ar=ar,
        text_en=en,
        sources=answer.sources,
        insufficient_evidence=False,
        escalation=esc,
    )
