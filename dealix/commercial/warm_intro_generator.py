"""Warm Intro Generator — approval-gated Saudi B2B outreach drafts.

Produces WhatsApp and email variants for warm, inbound, referral, or otherwise
approved prospects. It never sends messages and never permits fabricated proof,
guaranteed outcomes, stale deadlines, or access claims.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

_NO_LIVE_SEND = True
_DEFAULT_FOUNDER_NAME = "سامي محمد عسيري"
_FORBIDDEN_CLAIM_MARKERS = (
    "80%",
    "حلّت هذه المشكلة لشركات مشابهة",
    "solved this for similar companies",
    "zatca wave 24",
    "30 يونيو 2026",
    "june 30, 2026",
    "نتائج مضمونة",
    "guaranteed results",
    "وصول حكومي",
    "government access",
)


class WarmIntroRequest(BaseModel):
    prospect_name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    pain_context: str = ""
    previous_interaction: str = ""
    founder_name: str = _DEFAULT_FOUNDER_NAME
    language: str = "ar"


class OutreachDraft(BaseModel):
    channel: str
    variant: int
    subject_line: str = ""
    body_ar: str
    body_en: str
    tone: str
    character_count: int = 0
    approval_status: str = "approval_required"


class OutreachDraftBundle(BaseModel):
    bundle_id: str
    prospect_name: str
    company_name: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    whatsapp_drafts: list[OutreachDraft]
    email_drafts: list[OutreachDraft]
    approval_status: str = "approval_required"
    governance_decision: str = "pending"
    llm_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


def _contains_forbidden_claim(text: str) -> bool:
    normalized = text.casefold()
    return any(marker.casefold() in normalized for marker in _FORBIDDEN_CLAIM_MARKERS)


def _request_context_values(req: WarmIntroRequest) -> list[str]:
    values = (
        req.prospect_name,
        req.company_name,
        req.sector,
        req.pain_context,
        req.previous_interaction,
        req.founder_name,
    )
    return sorted({value.strip() for value in values if value.strip()}, key=len, reverse=True)


def _request_context_contains_forbidden_marker(req: WarmIntroRequest) -> bool:
    return any(_contains_forbidden_claim(value) for value in _request_context_values(req))


def _without_user_context(text: str, req: WarmIntroRequest) -> str:
    cleaned = text
    for value in _request_context_values(req):
        cleaned = cleaned.replace(value, "[USER_CONTEXT]")
    return cleaned


def _drafts_are_safe(drafts: list[OutreachDraft], req: WarmIntroRequest | None = None) -> bool:
    for draft in drafts:
        text = "\n".join((draft.subject_line, draft.body_ar, draft.body_en))
        if req is not None:
            text = _without_user_context(text, req)
        if _contains_forbidden_claim(text):
            return False
    return True


class WarmIntroGenerator:
    """Generate bilingual warm-intro drafts; founder approval is mandatory."""

    def generate(self, req: WarmIntroRequest) -> OutreachDraftBundle:
        assert _NO_LIVE_SEND, "NO_LIVE_SEND constitutional gate violated"

        import hashlib

        bundle_id = hashlib.sha256(
            f"{req.company_name}{req.prospect_name}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]

        context_requires_templates = _request_context_contains_forbidden_marker(req)
        whatsapp: list[OutreachDraft] = []
        email: list[OutreachDraft] = []
        if not context_requires_templates:
            whatsapp = self._llm_whatsapp(req)
            email = self._llm_email(req)

        llm_used = bool(whatsapp and email)
        if not llm_used:
            whatsapp = self._template_whatsapp(req)
            email = self._template_email(req)

        assert _drafts_are_safe(whatsapp + email, req), "Unsupported commercial claim detected"
        return OutreachDraftBundle(
            bundle_id=bundle_id,
            prospect_name=req.prospect_name,
            company_name=req.company_name,
            whatsapp_drafts=whatsapp,
            email_drafts=email,
            llm_used=llm_used,
        )

    @staticmethod
    def _llm_rules(req: WarmIntroRequest) -> str:
        context = req.previous_interaction or "warm/inbound/referral context not specified"
        return (
            "This is a draft-only warm outreach task. Do not claim past client results, "
            "percentages, guaranteed ROI, government access, certifications, deadlines, "
            "or customer proof unless explicitly supplied in the request. Do not invent facts. "
            "Start with a bounded diagnostic. Only after discovery may you propose a 30-day "
            "Revenue Command Pilot with a documented quote. Never state a fixed public price. "
            f"Previous interaction: {context}. Founder: {req.founder_name}."
        )

    def _llm_whatsapp(self, req: WarmIntroRequest) -> list[OutreachDraft]:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            return []
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)
            prompt = (
                f"اكتب 5 مسودات واتساب قصيرة لـ {req.prospect_name} من شركة "
                f"{req.company_name} في قطاع {req.sector}. المشكلة المحتملة: "
                f"{req.pain_context or 'تحتاج اكتشافًا أوليًا'}.\n"
                f"{self._llm_rules(req)}\n"
                "النبرات: direct, discovery, evidence_first, snapshot, pilot. "
                "أرجع JSON فقط: [{tone, body_ar, body_en}]."
            )
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = msg.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw)
            drafts = [
                OutreachDraft(
                    channel="whatsapp",
                    variant=index + 1,
                    body_ar=item.get("body_ar", ""),
                    body_en=item.get("body_en", ""),
                    tone=item.get("tone", "direct"),
                    character_count=len(item.get("body_ar", "")),
                )
                for index, item in enumerate(data[:5])
            ]
            return drafts if _drafts_are_safe(drafts, req) else []
        except Exception as exc:
            log.warning("warm_intro_llm_failed error=%s", exc)
            return []

    def _llm_email(self, req: WarmIntroRequest) -> list[OutreachDraft]:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            return []
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)
            prompt = (
                f"اكتب 3 مسودات بريد لـ {req.prospect_name} من {req.company_name}. "
                f"السياق: {req.pain_context or 'اكتشاف فجوة المتابعة والإيراد'}.\n"
                f"{self._llm_rules(req)}\n"
                "النبرات: professional, evidence_first, direct_ask. "
                "أرجع JSON فقط: [{tone, subject_ar, body_ar, body_en}]."
            )
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = msg.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw)
            drafts = [
                OutreachDraft(
                    channel="email",
                    variant=index + 1,
                    subject_line=item.get("subject_ar", ""),
                    body_ar=item.get("body_ar", ""),
                    body_en=item.get("body_en", ""),
                    tone=item.get("tone", "professional"),
                    character_count=len(item.get("body_ar", "")),
                )
                for index, item in enumerate(data[:3])
            ]
            return drafts if _drafts_are_safe(drafts, req) else []
        except Exception as exc:
            log.warning("warm_intro_email_llm_failed error=%s", exc)
            return []

    @staticmethod
    def _template_whatsapp(req: WarmIntroRequest) -> list[OutreachDraft]:
        name = req.prospect_name
        company = req.company_name
        founder = req.founder_name
        pain = req.pain_context or "ترتيب المتابعة وتحويل الفرص"
        templates = [
            (
                "direct",
                f"السلام عليكم {name}، أنا {founder} مؤسس Dealix.\n"
                f"نرتب للشركات مسار الفرص والمتابعة بشكل عملي. هل أرسل لك ملخصًا من صفحة واحدة يناسب {company}؟",
                f"Hi {name}, I am {founder}, founder of Dealix.\n"
                f"We structure opportunity and follow-up operations. May I send a one-page snapshot for {company}?",
            ),
            (
                "discovery",
                f"أهلًا {name}، سؤال مباشر: أين تضيع أكثر الفرص عند {company}—الرد، المتابعة، أم العرض؟\n"
                f"أنا {founder} من Dealix، وأجهز تشخيصًا مبنيًا على الواقع بدون تغيير أنظمتكم.",
                f"Hi {name}, a direct question: where do opportunities leak most at {company}—response, follow-up, or proposals?\n"
                f"I am {founder} from Dealix; we prepare a practical diagnostic without replacing your systems.",
            ),
            (
                "evidence_first",
                f"مرحبًا {name}، نبدأ بتشخيص مختصر لفهم فجوة تشغيل واحدة قبل تحديد أي نطاق أو سعر.\n"
                f"هل {pain} أولوية حالية لدى {company}؟",
                f"Hi {name}, we start with a bounded diagnostic to understand one operating gap before setting scope or price.\n"
                f"Is {pain} a current priority for {company}?",
            ),
            (
                "snapshot",
                f"السلام عليكم {name}، أقدر أجهز لـ {company} لقطة مختصرة توضح: أين تضيع الفرص، ما الإجراء التالي، وما الدليل المطلوب.\n"
                "هل أرسلها لك للمراجعة؟",
                f"Hi {name}, I can prepare a short snapshot for {company}: where opportunities leak, the next action, and required proof.\n"
                "Should I send it for review?",
            ),
            (
                "pilot",
                f"أهلًا {name}، Dealix تعمل فوق الأدوات الحالية مثل CRM وواتساب بدل استبدالها.\n"
                f"إذا كان مناسبًا، نبدأ مع {company} بألم واحد ونتيجة قابلة للقياس.",
                f"Hi {name}, Dealix works over existing tools such as CRM and WhatsApp rather than replacing them.\n"
                f"For {company}, we can start with one pain point and a measurable outcome.",
            ),
        ]
        return [
            OutreachDraft(
                channel="whatsapp",
                variant=index + 1,
                body_ar=body_ar,
                body_en=body_en,
                tone=tone,
                character_count=len(body_ar),
            )
            for index, (tone, body_ar, body_en) in enumerate(templates)
        ]

    @staticmethod
    def _template_email(req: WarmIntroRequest) -> list[OutreachDraft]:
        name = req.prospect_name
        company = req.company_name
        founder = req.founder_name
        pain = req.pain_context or "فجوة المتابعة وتحويل الفرص"
        templates = [
            {
                "tone": "professional",
                "subject_line": f"لقطة عملية لمسار الفرص في {company}",
                "body_ar": (
                    f"السلام عليكم {name}،\n\nأنا {founder}، مؤسس Dealix. "
                    f"نساعد فرق B2B على ترتيب الفرص والمتابعة فوق أدواتهم الحالية.\n\n"
                    f"أستطيع تجهيز ملخص من صفحة واحدة لـ {company} يوضح الفجوة المحتملة، الإجراء التالي، والدليل المطلوب قبل أي التزام.\n\n"
                    f"هل أرسله لك؟\n\nمع التحية،\n{founder}"
                ),
                "body_en": (
                    f"Dear {name},\n\nI am {founder}, founder of Dealix. We help B2B teams structure opportunities and follow-up over their existing tools.\n\n"
                    f"I can prepare a one-page snapshot for {company} showing the likely gap, next action, and evidence required before any commitment.\n\n"
                    f"May I send it?\n\nBest regards,\n{founder}"
                ),
            },
            {
                "tone": "evidence_first",
                "subject_line": f"تشخيص مسار الإيراد في {company}",
                "body_ar": (
                    f"مرحبًا {name}،\n\nDealix تبدأ بتشخيص مختصر لفهم مشكلة تشغيل واحدة قبل تحديد النطاق أو السعر. "
                    f"بالنسبة لـ {company}، الفرضية الأولية هي: {pain}.\n\n"
                    "بعد جلسة الاكتشاف نجهّز نطاق Revenue Command Pilot ومدة ومعايير قبول خاصة بالعميل وquote موثقًا للمراجعة؛ لا نعد بنتيجة إيراد.\n\n"
                    f"هل يناسبك تشخيص مختصر؟\n\n{founder}"
                ),
                "body_en": (
                    f"Hi {name},\n\nDealix starts with a bounded diagnostic to understand one operating problem before setting scope or price. "
                    f"For {company}, the initial hypothesis is: {pain}.\n\n"
                    "After discovery, we prepare a customer-specific Revenue Command Pilot scope, duration, acceptance criteria, and documented quote for review; we do not promise revenue outcomes.\n\n"
                    f"Would a short diagnostic be useful?\n\n{founder}"
                ),
            },
            {
                "tone": "direct_ask",
                "subject_line": f"سؤال واحد عن المتابعة في {company}",
                "body_ar": (
                    f"أهلًا {name}،\n\nسؤال واحد: هل أكبر فجوة لدى {company} الآن في سرعة الرد، انتظام المتابعة، أم تحويل العرض إلى قرار؟\n\n"
                    "أبني توصية فقط بعد معرفة الإجابة، وبدون تغيير CRM الحالي.\n\n"
                    f"تحياتي،\n{founder}"
                ),
                "body_en": (
                    f"Hi {name},\n\nOne question: is {company}'s biggest gap currently response speed, follow-up consistency, or converting proposals into decisions?\n\n"
                    "I only prepare a recommendation after understanding the answer, without replacing the current CRM.\n\n"
                    f"Regards,\n{founder}"
                ),
            },
        ]
        return [
            OutreachDraft(
                channel="email",
                variant=index + 1,
                subject_line=item["subject_line"],
                body_ar=item["body_ar"],
                body_en=item["body_en"],
                tone=item["tone"],
                character_count=len(item["body_ar"]),
            )
            for index, item in enumerate(templates)
        ]
