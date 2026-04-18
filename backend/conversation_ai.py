"""
Dealix Conversation AI
======================
Full conversation engine with state machine for:
- Auto-reply to inbound messages
- Multi-stage negotiation (greet → qualify → pitch → objections → meeting → close)
- Arabic Saudi Gulf dialect
- Shares contact info + calendar booking link when appropriate

Used by:
- WhatsApp webhook (auto-reply on inbound)
- AI suggest endpoint (suggests 3 replies to human operator)
- Outreach engine (generates personalized opening messages)
"""
from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any, Optional

import aiosqlite
import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

log = logging.getLogger("dealix.conversation_ai")

DB_PATH = os.getenv("DEALIX_DB_PATH", "/home/user/workspace/dealix-clean/dealix_leads.db")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Sales contact info (per-tenant override later via settings)
DEFAULT_SALES_PHONE = os.getenv("SALES_CONTACT_PHONE", "+966570327724")
DEFAULT_SALES_EMAIL = os.getenv("SALES_CONTACT_EMAIL", "sami.assiri11@gmail.com")
DEFAULT_SALES_NAME = os.getenv("SALES_CONTACT_NAME", "سامي العسيري")
DEFAULT_CALENDAR_URL = os.getenv("SALES_CALENDAR_URL", "https://calendar.app.google/PLACEHOLDER")


# ─── Conversation stage model ────────────────────────────────────────────────
STAGES = [
    "new",          # First contact
    "engaged",      # They replied — we're building rapport
    "qualifying",   # Discovering fit (size, budget, timeline)
    "pitched",      # We explained the solution
    "objection",    # They raised concerns
    "meeting",      # Meeting scheduled
    "proposal",     # Proposal sent
    "closing",      # Final close
    "won",
    "lost",
]


INTENT_KEYWORDS = {
    "interested": [r"مهتم", r"ابي\s+اعرف", r"ابغى", r"ابي", r"كيف\s+يعمل", r"ابغي", r"حب(يت|ّيت)",
                   r"interested", r"tell\s+me\s+more", r"how\s+does"],
    "price": [r"سعر", r"اسعار", r"كلف", r"تكلفة", r"كم\s+ريال", r"كم\s+يبغى", r"price", r"cost", r"pricing"],
    "meeting": [r"اجتماع", r"مقابلة", r"مكالمة", r"اتصل", r"موعد", r"احجز", r"متى\s+نلتقي",
                r"meeting", r"call", r"schedule", r"demo", r"عرض"],
    "contact_request": [r"كلمني", r"رقمك", r"اتصل\s+فيك", r"ابغى\s+اكلمك", r"phone", r"number", r"call\s+me"],
    "objection_time": [r"مشغول", r"وقت\s+لاحق", r"الحين\s+مو", r"بعدين", r"ما\s+عندي\s+وقت"],
    "objection_price": [r"غالي", r"مكلف", r"اغلى", r"ما\s+نقدر", r"خارج\s+الميزانية", r"too\s+expensive"],
    "objection_need": [r"ما\s+نحتاج", r"مالنا\s+فيه", r"مو\s+الحين", r"not\s+needed"],
    "unsubscribe": [r"الغ", r"ما\s+تبعث", r"stop", r"remove\s+me", r"unsubscribe"],
    "yes": [r"^(ايه|اي|نعم|اوك|اوكي|تمام|طيب|اكيد|yes|ok|sure|yep)$"],
    "no": [r"^(لا|مافي|no|nope|nah)$"],
}


def detect_intents(text: str) -> list[str]:
    if not text:
        return []
    text_lower = text.lower().strip()
    found = []
    for intent, patterns in INTENT_KEYWORDS.items():
        for p in patterns:
            if re.search(p, text_lower, re.IGNORECASE):
                found.append(intent)
                break
    return found


def pick_next_stage(current_stage: str, intents: list[str], message_count: int) -> str:
    """Simple state machine — picks the next stage based on current + intents."""
    if "unsubscribe" in intents:
        return "lost"
    if "meeting" in intents or "contact_request" in intents:
        return "meeting"
    if "objection_price" in intents or "objection_time" in intents or "objection_need" in intents:
        return "objection"
    if "price" in intents:
        return "pitched"
    if "interested" in intents and current_stage in ("new", "engaged"):
        return "qualifying"
    if current_stage == "new":
        return "engaged"
    if current_stage == "engaged" and message_count >= 4:
        return "qualifying"
    if current_stage == "qualifying" and message_count >= 6:
        return "pitched"
    return current_stage


# ─── System prompts per stage ────────────────────────────────────────────────
BASE_SYSTEM = """أنت مساعد مبيعات ذكي لمنصة Dealix — منصة سعودية للذكاء الاصطناعي في المبيعات.

القيم الأساسية للردود:
1. باللهجة الخليجية السعودية المهذبة (ليست الفصحى المتكلفة، ولا العامية المفرطة)
2. قصيرة وواضحة — 2-4 أسطر فقط
3. اسأل سؤال في النهاية إذا كان مناسباً — لتبقى المحادثة حية
4. استخدم اسم المحاور إذا تعرفه
5. لا تكرر نفس العبارة من رسائل سابقة
6. لا تستخدم إيموجي أكثر من واحد لكل رسالة (أو بدون)

ممنوعات صارمة (لا يجوز أبداً ذكرها):
- لا تذكر أي أسعار أو أرقام ريالات أو باقات بأسعار محددة (Dealix في مرحلة التدشين ولسّا التسعير غير معلن). إذا سألوا عن السعر قل: "التسعير حسب حجم شركتك وعمليات المبيعات، نفضل نتفاهم في مكالمة قصيرة علشان نعطيك عرض مناسب."
- لا تذكر شهادات أو اعتمادات (ISO/SOC2/bank-grade) — النظام ما اعتمد بعد
- لا تعد بنسب نجاح محددة (مثل "100% تحويل" أو "زيادة 3x") كأرقام قطعية — استخدم صيغة تقريبية: "ممكن يساعد في تقليل وقت الرد بشكل ملحوظ"
- لا تدّعي ميزات غير مذكورة في وصف Dealix أدناه

عن Dealix:
- منصة AI سعودية تساعد شركات B2B على تسريع المبيعات
- وكلاء ذكيين يردّون على العملاء تلقائياً بالعربي على واتساب/إيميل/SMS
- اكتشاف leads تلقائي من 20+ مصدر (قوقل، لينكدإن، خرائط، سجلات شركات)
- تأهيل + تفاوض تلقائي بالذكاء الصناعي
- لوحة تحكم عربية كاملة RTL
- تركيز خليجي: السعودية أولاً ثم بقية دول الخليج

أنواع العملاء المستهدفين: شركات لوجستيات، عقار، SaaS B2B، تجزئة، بنوك، تأمين.

معلومات التواصل (استخدمها فقط إذا العميل طلب أو كانت الإشارة واضحة أنه جاهز):
- الاتصال: {sales_phone}
- البريد: {sales_email}
- حجز اجتماع Google Meet: {calendar_url}
- المسؤول: {sales_name}
"""

STAGE_PROMPTS = {
    "new": """الحالة: أول تواصل.
المهمة: رحّب ترحيب قصير، عرّف بـ Dealix في جملة واحدة، اسأل عن نشاطهم لفهم الملاءمة.""",

    "engaged": """الحالة: العميل رد وتتبنى المحادثة.
المهمة: اشكره، اسأل سؤال مفتوح واحد عن عمليات المبيعات لديهم أو التحديات الحالية.""",

    "qualifying": """الحالة: تأهيل — تبغى تعرف الحجم، القطاع، التحديات، الميزانية.
المهمة: اسأل سؤال ذكي واحد يكشف الـ fit (مثلاً: كم عدد leads شهرياً؟ كم فريق المبيعات؟ أي القنوات الأكثر استخداماً؟).""",

    "pitched": """الحالة: العميل سأل عن التفاصيل أو السعر.
المهمة: اشرح 2-3 نقاط قيمة ملموسة (مثل: رد تلقائي ذكي بالعربي على واتساب، تأهيل leads تلقائي، متابعة بدون نسيان)، ثم اعرض demo مباشر.
إذا سأل عن السعر: قل حرفياً "التسعير يعتمد على حجم شركتك وعدد leads الشهري، نفضل نتفاهم في مكالمة قصيرة علشان نعطيك عرض مناسب" — ممنوع تذكر أي رقم.""",

    "objection": """الحالة: اعتراض.
المهمة: تعاطف مع اعتراضه أولاً، ثم اعرض زاوية مختلفة:
- اعتراض سعر: اعرض pilot تجريبي مدفوع بخصم مع ضمان استرداد
- اعتراض وقت: اعرض مكالمة قصيرة 15 دقيقة الأسبوع القادم
- اعتراض حاجة: اسأل عن مشكلة واحدة ملموسة حالياً في المبيعات""",

    "meeting": """الحالة: العميل طلب اجتماع أو اتصال.
المهمة: وفّر خيارين:
1. رابط الحجز المباشر Google Meet: {calendar_url}
2. اتصال فوري على: {sales_phone}
اختم بـ: "أي وقت يناسبك هذا الأسبوع؟""",

    "proposal": """الحالة: نرسل/أرسلنا عرض.
المهمة: لخّص العرض في 3 نقاط، اذكر الخطوة التالية بوضوح، اسأل عن وقت للمراجعة المشتركة.""",

    "closing": """الحالة: قريب من الإغلاق.
المهمة: اذكر ملخص فائدة واحدة، اعرض تسهيل (pilot مخفّض / بداية سريعة)، اطلب الخطوة النهائية.""",
}


def _build_system_prompt(stage: str, tenant_contact: dict) -> str:
    base = BASE_SYSTEM.format(
        sales_phone=tenant_contact.get("phone", DEFAULT_SALES_PHONE),
        sales_email=tenant_contact.get("email", DEFAULT_SALES_EMAIL),
        sales_name=tenant_contact.get("name", DEFAULT_SALES_NAME),
        calendar_url=tenant_contact.get("calendar_url", DEFAULT_CALENDAR_URL),
    )
    stage_prompt = STAGE_PROMPTS.get(stage, STAGE_PROMPTS["engaged"]).format(
        sales_phone=tenant_contact.get("phone", DEFAULT_SALES_PHONE),
        calendar_url=tenant_contact.get("calendar_url", DEFAULT_CALENDAR_URL),
    )
    return base + "\n\n" + stage_prompt


# ─── Context loading ─────────────────────────────────────────────────────────
async def _load_conversation_context(
    phone: str, tenant_id: str, limit: int = 12
) -> tuple[list[dict], dict, str]:
    """Returns (history_messages, lead_dict_or_empty, current_stage)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Messages
        msg_rows = await (await db.execute(
            "SELECT direction, body FROM messages "
            "WHERE phone=? AND tenant_id=? ORDER BY id DESC LIMIT ?",
            (phone, tenant_id, limit),
        )).fetchall()
        history = []
        for r in reversed(msg_rows):
            role = "user" if r["direction"] == "in" else "assistant"
            history.append({"role": role, "content": r["body"]})

        # Lead lookup
        lead_row = await (await db.execute(
            "SELECT * FROM leads WHERE phone=? AND tenant_id=? LIMIT 1",
            (phone, tenant_id),
        )).fetchone()
        lead = dict(lead_row) if lead_row else {}

        # Stage comes from lead.stage, default 'new'
        stage = (lead.get("stage") or "new").lower()
        if stage not in STAGES:
            stage = "engaged"

        return history, lead, stage


async def _load_tenant_contact(tenant_id: str) -> dict:
    """Load per-tenant sales contact overrides (fallback to env defaults)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        try:
            row = await (await db.execute(
                "SELECT api_keys FROM users WHERE tenant_id=? AND role='admin' LIMIT 1",
                (tenant_id,),
            )).fetchone()
            if row and row["api_keys"]:
                keys = json.loads(row["api_keys"] or "{}")
                return {
                    "phone": keys.get("sales_phone") or DEFAULT_SALES_PHONE,
                    "email": keys.get("sales_email") or DEFAULT_SALES_EMAIL,
                    "name": keys.get("sales_name") or DEFAULT_SALES_NAME,
                    "calendar_url": keys.get("calendar_url") or DEFAULT_CALENDAR_URL,
                }
        except Exception as e:
            log.debug("load_tenant_contact: %s", e)
    return {
        "phone": DEFAULT_SALES_PHONE,
        "email": DEFAULT_SALES_EMAIL,
        "name": DEFAULT_SALES_NAME,
        "calendar_url": DEFAULT_CALENDAR_URL,
    }


# ─── LLM call ────────────────────────────────────────────────────────────────
async def _call_groq(messages: list[dict], temperature: float = 0.6) -> str:
    if not GROQ_API_KEY:
        return ""
    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            r = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": 400,
                },
            )
            r.raise_for_status()
            data = r.json()
            return (data.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        log.warning("[groq] error: %s", e)
        return ""


def _fallback_reply(stage: str, intents: list[str], tenant_contact: dict) -> str:
    """Fallback when Groq is unavailable."""
    phone = tenant_contact.get("phone", DEFAULT_SALES_PHONE)
    cal = tenant_contact.get("calendar_url", DEFAULT_CALENDAR_URL)
    if "meeting" in intents or "contact_request" in intents:
        return (
            f"يسعدنا التواصل معك. تقدر تحجز وقت يناسبك عبر الرابط:\n{cal}\n"
            f"أو اتصل مباشرة على: {phone}"
        )
    if "price" in intents:
        return (
            "الباقات تبدأ من مستوى مدروس حسب حجم العملية. "
            f"بنرتب لك اجتماع 15 دقيقة نعطيك تقدير دقيق — تقدر تحجز هنا:\n{cal}"
        )
    if "unsubscribe" in intents:
        return "تم إلغاء الاشتراك. شكراً لوقتك."
    return (
        f"شكراً لتواصلك. نساعد شركات B2B في السعودية على تسريع مبيعاتها عبر AI. "
        f"حابب أعرف أكثر عن نشاطكم — أي قطاع أنتم؟"
    )


# ─── Main generation function ────────────────────────────────────────────────
async def generate_reply(
    *,
    phone: str,
    tenant_id: str,
    inbound_text: Optional[str] = None,
    override_stage: Optional[str] = None,
) -> dict:
    """
    Generate a single AI reply. Returns:
      {
        "text": "...",
        "stage": "pitched",
        "intents": ["price"],
        "should_share_contact": bool,
        "should_share_calendar": bool,
      }
    """
    history, lead, current_stage = await _load_conversation_context(phone, tenant_id)
    tenant_contact = await _load_tenant_contact(tenant_id)

    # Detect intents from the last inbound message
    last_inbound = inbound_text or next(
        (m["content"] for m in reversed(history) if m["role"] == "user"), ""
    )
    intents = detect_intents(last_inbound)

    # Decide new stage
    msg_count = len(history)
    next_stage = override_stage or pick_next_stage(current_stage, intents, msg_count)

    should_share_contact = "contact_request" in intents or "meeting" in intents
    should_share_calendar = "meeting" in intents or next_stage in ("meeting", "closing")

    system = _build_system_prompt(next_stage, tenant_contact)
    lead_context = ""
    if lead:
        lead_context = (
            f"\n\nمعلومات العميل:\n"
            f"- الاسم: {lead.get('name') or 'غير معروف'}\n"
            f"- الشركة: {lead.get('company_name_ar') or lead.get('company_name') or 'غير معروفة'}\n"
            f"- القطاع: {lead.get('sector') or 'غير محدد'}\n"
            f"- الحجم: {lead.get('employees') or 'غير محدد'} موظف\n"
            f"- المرحلة الحالية: {current_stage} → {next_stage}"
        )

    messages = [{"role": "system", "content": system + lead_context}]
    messages.extend(history[-10:])
    if inbound_text and (not history or history[-1]["content"] != inbound_text):
        messages.append({"role": "user", "content": inbound_text})

    text = await _call_groq(messages, temperature=0.6)
    if not text:
        text = _fallback_reply(next_stage, intents, tenant_contact)

    return {
        "text": text,
        "stage": next_stage,
        "previous_stage": current_stage,
        "intents": intents,
        "should_share_contact": should_share_contact,
        "should_share_calendar": should_share_calendar,
        "contact": {
            "phone": tenant_contact.get("phone"),
            "email": tenant_contact.get("email"),
            "calendar_url": tenant_contact.get("calendar_url"),
        },
    }


async def generate_suggestions(
    *,
    phone: str,
    tenant_id: str,
    count: int = 3,
) -> list[str]:
    """Generate N alternative replies for the human operator to pick from."""
    history, lead, current_stage = await _load_conversation_context(phone, tenant_id)
    tenant_contact = await _load_tenant_contact(tenant_id)
    intents = detect_intents(
        next((m["content"] for m in reversed(history) if m["role"] == "user"), "")
    )
    next_stage = pick_next_stage(current_stage, intents, len(history))

    system = _build_system_prompt(next_stage, tenant_contact) + (
        f"\n\nالمهمة الخاصة: أعطني {count} ردود مختلفة النبرة:"
        "\n1. رد ودي هادئ"
        "\n2. رد مباشر قصير"
        "\n3. رد يدفع نحو اجتماع"
        "\nاكتبهم مرقّمين 1. 2. 3. فقط، بدون عناوين."
    )

    messages = [{"role": "system", "content": system}]
    messages.extend(history[-8:])

    raw = await _call_groq(messages, temperature=0.8)
    if not raw:
        return [_fallback_reply(next_stage, intents, tenant_contact)] * count

    # Parse "1. ...\n2. ...\n3. ..."
    parts = re.split(r"\n\s*\d+[\.\)]\s*", "\n" + raw)
    suggestions = [p.strip() for p in parts if p.strip()][:count]
    if len(suggestions) < count:
        # Fallback: split by double newlines
        suggestions = [p.strip() for p in raw.split("\n\n") if p.strip()][:count]
    if len(suggestions) < count:
        suggestions += [_fallback_reply(next_stage, intents, tenant_contact)] * (count - len(suggestions))
    return suggestions


async def update_lead_stage(phone: str, tenant_id: str, new_stage: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE leads SET stage=?, updated_at=? WHERE phone=? AND tenant_id=?",
            (new_stage, datetime.now(timezone.utc).isoformat(), phone, tenant_id),
        )
        await db.commit()


# ─── Router ──────────────────────────────────────────────────────────────────
class ReplyGenRequest(BaseModel):
    phone: str
    inbound_text: Optional[str] = None


class StageOverrideRequest(BaseModel):
    phone: str
    stage: str


def register(app, get_current_user):
    """Wire conversation-AI endpoints into the main app."""

    @app.post("/api/v1/ai/reply", tags=["ai"])
    async def api_generate_reply(body: ReplyGenRequest, user=Depends(get_current_user)):
        """Generate a single contextual reply + updated stage."""
        result = await generate_reply(
            phone=body.phone,
            tenant_id=user["tenant_id"],
            inbound_text=body.inbound_text,
        )
        # Update lead stage if it changed
        if result["stage"] != result["previous_stage"]:
            try:
                await update_lead_stage(body.phone, user["tenant_id"], result["stage"])
            except Exception as e:
                log.warning("stage update failed: %s", e)
        return result

    @app.post("/api/v1/ai/suggestions", tags=["ai"])
    async def api_suggestions(body: ReplyGenRequest, user=Depends(get_current_user)):
        """Generate 3 alternative replies for the human operator."""
        items = await generate_suggestions(
            phone=body.phone, tenant_id=user["tenant_id"]
        )
        return {"suggestions": items}

    @app.get("/api/v1/ai/stages", tags=["ai"])
    async def list_stages():
        return {"stages": STAGES}

    @app.get("/api/v1/ai/config", tags=["ai"])
    async def get_config(user=Depends(get_current_user)):
        tc = await _load_tenant_contact(user["tenant_id"])
        return {
            "contact": tc,
            "has_llm": bool(GROQ_API_KEY),
            "model": GROQ_MODEL if GROQ_API_KEY else None,
        }
