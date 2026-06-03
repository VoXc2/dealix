"""Warm Intro Generator — draft outreach for Saudi B2B prospects.

Produces 5 WhatsApp variants + 3 email variants per prospect.
Constitutional gate: NO_LIVE_SEND — all drafts stored as approval_required.
Never triggers any external message send.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

_NO_LIVE_SEND = True  # hard constitutional gate — never set to False


class WarmIntroRequest(BaseModel):
    prospect_name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    pain_context: str = ""
    previous_interaction: str = ""
    founder_name: str = "سامي"
    language: str = "ar"


class OutreachDraft(BaseModel):
    channel: str  # "whatsapp" | "email"
    variant: int
    subject_line: str = ""
    body_ar: str
    body_en: str
    tone: str  # "direct" | "empathetic" | "urgency" | "social_proof" | "question"
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
    governance_decision: str = "pending"  # pending | approved | rejected
    llm_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class WarmIntroGenerator:
    """Generates bilingual warm intro drafts — approval required before use."""

    def generate(self, req: WarmIntroRequest) -> OutreachDraftBundle:
        assert _NO_LIVE_SEND, "NO_LIVE_SEND constitutional gate violated"

        import hashlib
        bundle_id = hashlib.sha256(
            f"{req.company_name}{req.prospect_name}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]

        llm_used = False
        wa_drafts = self._llm_whatsapp(req)
        email_drafts = self._llm_email(req)
        if wa_drafts and email_drafts:
            llm_used = True
        else:
            wa_drafts = self._template_whatsapp(req)
            email_drafts = self._template_email(req)

        return OutreachDraftBundle(
            bundle_id=bundle_id,
            prospect_name=req.prospect_name,
            company_name=req.company_name,
            whatsapp_drafts=wa_drafts,
            email_drafts=email_drafts,
            llm_used=llm_used,
        )

    def _llm_whatsapp(self, req: WarmIntroRequest) -> list[OutreachDraft]:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            return []
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            prompt = (
                f"أنت مستشار مبيعات B2B سعودي. اكتب 5 رسائل واتساب للتواصل مع "
                f"'{req.prospect_name}' من شركة '{req.company_name}' في قطاع '{req.sector}'. "
                f"السياق: {req.pain_context or 'لا سياق محدد'}. "
                f"المرسل: {req.founder_name}.\n\n"
                f"كل رسالة: 3 أسطر حد أقصى، واتساب-فريندلي، عربي-أول.\n"
                f"النبرات: [direct, empathetic, urgency, social_proof, question]\n"
                f"أرجع JSON مصفوفة من 5 كائنات: "
                f"{{tone, body_ar, body_en}}"
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
            return [
                OutreachDraft(
                    channel="whatsapp",
                    variant=i + 1,
                    body_ar=d.get("body_ar", ""),
                    body_en=d.get("body_en", ""),
                    tone=d.get("tone", "direct"),
                    character_count=len(d.get("body_ar", "")),
                )
                for i, d in enumerate(data[:5])
            ]
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
                f"اكتب 3 رسائل بريد إلكتروني للتواصل مع '{req.prospect_name}' "
                f"من '{req.company_name}'. النبرات: [professional, story, direct_ask]. "
                f"كل رسالة: عنوان + جسم (5-6 جمل). عربي-أول مع ترجمة إنجليزية. "
                f"أرجع JSON: [{{tone, subject_ar, subject_en, body_ar, body_en}}]"
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
            return [
                OutreachDraft(
                    channel="email",
                    variant=i + 1,
                    subject_line=d.get("subject_ar", ""),
                    body_ar=d.get("body_ar", ""),
                    body_en=d.get("body_en", ""),
                    tone=d.get("tone", "professional"),
                    character_count=len(d.get("body_ar", "")),
                )
                for i, d in enumerate(data[:3])
            ]
        except Exception as exc:
            log.warning("warm_intro_email_llm_failed error=%s", exc)
            return []

    def _template_whatsapp(self, req: WarmIntroRequest) -> list[OutreachDraft]:
        name = req.prospect_name
        company = req.company_name
        founder = req.founder_name
        templates = [
            {
                "tone": "direct",
                "body_ar": f"أهلاً {name}،\nأنا {founder} من Dealix — نساعد شركات {req.sector} على أتمتة عمليات الإيراد.\nهل لديك 10 دقائق هذا الأسبوع؟",
                "body_en": f"Hi {name},\nI'm {founder} from Dealix — we help {req.sector} companies automate revenue ops.\nDo you have 10 mins this week?",
            },
            {
                "tone": "empathetic",
                "body_ar": f"السلام عليكم {name}،\nأتفهم تحديات {req.sector} — خاصة في جانب {req.pain_context or 'الإيراد'}.\nDealix حلّت هذه المشكلة لشركات مشابهة. هل تريد تشخيصاً مجانياً؟",
                "body_en": f"Hello {name},\nI understand {req.sector} challenges — especially around {req.pain_context or 'revenue'}.\nDealix solved this for similar companies. Want a free diagnostic?",
            },
            {
                "tone": "urgency",
                "body_ar": f"مرحباً {name} —\nموعد ZATCA Wave 24 قادم (30 يونيو 2026).\nشركات مثل {company} تحتاج التجهيز الآن.\nأرسل لك تقييماً مجانياً؟",
                "body_en": f"Hi {name} —\nZATCA Wave 24 deadline is approaching (June 30, 2026).\nCompanies like {company} need to prepare now.\nShall I send you a free assessment?",
            },
            {
                "tone": "social_proof",
                "body_ar": f"أهلاً {name}،\nDealix بنت نظام تشغيل الإيراد الخاص بها من الصفر باستخدام أدواتنا.\nنفس النظام متاح لـ {company}.\nمهتم تشوف كيف؟",
                "body_en": f"Hi {name},\nDealix built its own revenue OS from scratch using our tools.\nThe same system is available for {company}.\nInterested to see how?",
            },
            {
                "tone": "question",
                "body_ar": f"مرحباً {name}،\nسؤال مباشر: ما أكبر تحدي يواجهه فريق المبيعات في {company} الآن؟\nنسأل لأن معظم شركات {req.sector} تواجه نفس 3 تحديات — وعندنا حلول جاهزة.",
                "body_en": f"Hi {name},\nDirect question: what's the biggest challenge facing {company}'s sales team right now?\nWe ask because most {req.sector} companies face the same 3 challenges — and we have ready solutions.",
            },
        ]
        return [
            OutreachDraft(
                channel="whatsapp",
                variant=i + 1,
                body_ar=t["body_ar"],
                body_en=t["body_en"],
                tone=t["tone"],
                character_count=len(t["body_ar"]),
            )
            for i, t in enumerate(templates)
        ]

    def _template_email(self, req: WarmIntroRequest) -> list[OutreachDraft]:
        name = req.prospect_name
        company = req.company_name
        founder = req.founder_name
        templates = [
            {
                "tone": "professional",
                "subject_line": f"تشخيص مجاني لعمليات {company} | Free Diagnostic for {company}",
                "body_ar": (
                    f"السلام عليكم {name}،\n\n"
                    f"اسمي {founder}، مؤسس Dealix — نظام تشغيل الإيراد للشركات السعودية B2B.\n"
                    f"نساعد شركات {req.sector} على اكتشاف فجوات الإيراد وأتمتة عمليات المبيعات.\n\n"
                    f"أودّ تقديم تشخيص مجاني لـ {company} (30 دقيقة) لاكتشاف أكبر 3 فرص نمو.\n\n"
                    f"هل تناسبك هذا الأسبوع؟\n\nمع التحية،\n{founder}"
                ),
                "body_en": (
                    f"Dear {name},\n\n"
                    f"My name is {founder}, founder of Dealix — the Revenue OS for Saudi B2B companies.\n"
                    f"We help {req.sector} companies discover revenue gaps and automate sales operations.\n\n"
                    f"I'd like to offer {company} a free diagnostic (30 minutes) to uncover the top 3 growth opportunities.\n\n"
                    f"Does this week work for you?\n\nBest regards,\n{founder}"
                ),
            },
            {
                "tone": "story",
                "subject_line": f"كيف أتمتنا 80% من عمليات المبيعات في 7 أيام | How we automated 80% of sales ops in 7 days",
                "body_ar": (
                    f"مرحباً {name}،\n\n"
                    f"منذ 3 أشهر، واجهنا نفس التحديات في Dealix: فريق صغير، فرص كثيرة، ووقت محدود.\n"
                    f"قررنا بناء نظامنا الخاص — والنتيجة: 80% من المهام المتكررة أصبحت تلقائية.\n\n"
                    f"اليوم، هذا النظام متاح لشركات مثل {company}.\n"
                    f"هل ترغب في رؤية كيف؟\n\n{founder}"
                ),
                "body_en": (
                    f"Hi {name},\n\n"
                    f"3 months ago, Dealix faced the same challenges: small team, many opportunities, limited time.\n"
                    f"We decided to build our own system — result: 80% of repetitive tasks became automated.\n\n"
                    f"Today, this system is available for companies like {company}.\n"
                    f"Would you like to see how?\n\n{founder}"
                ),
            },
            {
                "tone": "direct_ask",
                "subject_line": f"طلب: 15 دقيقة لـ {company} | Request: 15 mins for {company}",
                "body_ar": (
                    f"أهلاً {name}،\n\n"
                    f"لن أطيل — Dealix تحل مشكلة {req.pain_context or 'الإيراد'} لشركات {req.sector}.\n"
                    f"أطلب 15 دقيقة فقط لأريك كيف.\n"
                    f"متاح الاثنين أو الثلاثاء القادم؟\n\n{founder}"
                ),
                "body_en": (
                    f"Hi {name},\n\n"
                    f"I'll be brief — Dealix solves {req.pain_context or 'revenue'} for {req.sector} companies.\n"
                    f"I'm asking for just 15 minutes to show you how.\n"
                    f"Are you available next Monday or Tuesday?\n\n{founder}"
                ),
            },
        ]
        return [
            OutreachDraft(
                channel="email",
                variant=i + 1,
                subject_line=t["subject_line"],
                body_ar=t["body_ar"],
                body_en=t["body_en"],
                tone=t["tone"],
                character_count=len(t["body_ar"]),
            )
            for i, t in enumerate(templates)
        ]
