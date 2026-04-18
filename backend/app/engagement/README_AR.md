# Dealix — إطار عمل Engagement Agents (متعدد القنوات)

> الوثيقة الرسمية لمطوري فريق Dealix — محدَّثة: أبريل 2026

---

## نظرة عامة

هذا الإطار يوحّد كل قنوات التواصل الخارجي في بنية واحدة قابلة للتوسعة:

```
backend/app/engagement/
├── base.py              ← BaseEngagementAgent (الفئة الأساسية المجردة)
├── memory.py            ← ConversationMemory (قاعدة بيانات SQLite)
├── llm.py               ← LLMGateway (Groq + OpenAI)
├── orchestrator.py      ← EngagementOrchestrator (منسّق التسلسلات)
├── channels/
│   ├── whatsapp.py      ← WhatsAppAgent (Twilio)
│   ├── email.py         ← EmailAgent (SendGrid + Gmail API)
│   ├── linkedin.py      ← LinkedInAgent (Unipile)
│   ├── sms.py           ← SMSAgent (Twilio SMS)
│   ├── voice.py         ← VoiceAgent (Retell/Vapi — مرحلة 2)
│   └── social.py        ← SocialListener (X + Instagram)
├── prompts/             ← ملفات النظام العربية
│   ├── system_base_ar.md
│   ├── whatsapp_outbound_ar.md
│   ├── whatsapp_inbound_ar.md
│   ├── email_cold_ar.md
│   ├── email_followup_ar.md
│   ├── linkedin_connect_ar.md
│   ├── linkedin_followup_ar.md
│   ├── sms_reminder_ar.md
│   └── qualifier_ar.md
└── playbooks/           ← تسلسلات YAML
    ├── ecommerce_outbound.yaml
    ├── agency_outbound.yaml
    └── real_estate_outbound.yaml
```

---

## كيفية إضافة قناة جديدة

### الخطوات:

1. **أنشئ ملفاً جديداً** في `channels/` (مثل `channels/telegram.py`).

2. **امتد من `BaseEngagementAgent`** وحدّد خاصية `channel`:

```python
from ..base import BaseEngagementAgent, ChannelType, AgentContext, DeliveryReceipt, IncomingMessage

class TelegramAgent(BaseEngagementAgent):
    channel = ChannelType.TELEGRAM  # أضف القيمة إلى enum ChannelType في base.py

    async def send(self, to: str, message: str, context: AgentContext) -> DeliveryReceipt:
        # تنفيذ الإرسال عبر Telegram Bot API
        ...

    async def receive(self, payload: dict) -> IncomingMessage:
        # تحويل payload الـ webhook إلى IncomingMessage
        ...
```

3. **أضف القناة إلى `ChannelType` enum** في `base.py`:
```python
class ChannelType(str, Enum):
    TELEGRAM = "telegram"  # أضف هنا
```

4. **سجّل الـ Agent في الـ Orchestrator**:
```python
orchestrator.register_agent(ChannelType.TELEGRAM, TelegramAgent(settings=settings))
```

5. **أضف الـ Agent إلى `channels/__init__.py`**.

6. **اختبر** في `tests/engagement/test_channels.py`.

---

## كيفية تخصيص النماذج (Prompts)

### الملفات الموجودة في `prompts/`:

| المفتاح | الاستخدام |
|---|---|
| `system_base_ar` | القواعد المشتركة لجميع الوكلاء |
| `whatsapp_outbound_ar` | التواصل البارد عبر واتساب |
| `whatsapp_inbound_ar` | الرد على الرسائل الواردة |
| `email_cold_ar` | البريد الإلكتروني البارد |
| `email_followup_ar` | متابعة البريد الإلكتروني |
| `linkedin_connect_ar` | طلب الاتصال على LinkedIn |
| `linkedin_followup_ar` | متابعة LinkedIn |
| `sms_reminder_ar` | رسائل SMS |
| `qualifier_ar` | تأهيل BANT + MEDDPICC |

### لإضافة نموذج جديد:

```bash
# 1. أنشئ ملف markdown
echo "# نموذجي الجديد\n..." > backend/app/engagement/prompts/my_new_ar.md

# 2. استخدمه في الكود
system = llm.get_system_prompt("my_new_ar")
```

### لدمج نماذج متعددة:

```python
# يجمع system_base_ar + qualifier_ar في prompt واحد
system = llm.compose_prompt("system_base_ar", "qualifier_ar")
```

---

## كيفية تعريف Playbook جديد

الـ Playbook هو ملف YAML يحدد تسلسل التواصل خطوة بخطوة.

### البنية الأساسية:

```yaml
name: my_playbook
description: وصف التسلسل
target_sector: fintech  # أو أي قطاع

channel_priority:
  - whatsapp
  - email
  - linkedin

steps:
  - channel: whatsapp
    delay_days: 0          # 0 = فوري
    prompt_key: whatsapp_outbound_ar
    condition: null        # أو no_reply / connection_accepted
    max_retries: 1

  - channel: email
    delay_days: 5
    prompt_key: email_cold_ar
    condition: no_reply

  # يمكن استخدام قالب ثابت بدل LLM
  - channel: whatsapp
    delay_days: 10
    prompt_key: whatsapp_outbound_ar
    message_template: >
      مرحباً {name}، آخر متابعة من طرفنا...
```

### متغيرات القالب المتاحة:

| المتغير | المصدر |
|---|---|
| `{name}` | اسم الشخص |
| `{company}` | اسم الشركة |
| `{sector}` | القطاع |
| `{city}` | المدينة |

### تحميل واستخدام الـ Playbook:

```python
from app.engagement.orchestrator import Playbook, EngagementOrchestrator

playbook = Playbook.from_yaml("app/engagement/playbooks/my_playbook.yaml")
result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)
```

---

## كيفية التشغيل محلياً

### 1. تثبيت المتطلبات:

```bash
cd dealix-clean/backend
pip install aiosqlite httpx pydantic-settings twilio sendgrid pyyaml pytest pytest-asyncio
```

### 2. إعداد متغيرات البيئة (`.env`):

```env
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk_...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_SMS_NUMBER=+14155238886
SENDGRID_API_KEY=SG...
DEALIX_DB=dealix_engagement.db
```

### 3. تشغيل سريع (Python):

```python
import asyncio
from app.engagement import ConversationMemory, LLMGateway
from app.engagement.base import EngagementSettings
from app.engagement.channels.whatsapp import WhatsAppAgent
from app.engagement.orchestrator import EngagementOrchestrator, Lead, Playbook

async def main():
    settings = EngagementSettings()
    memory = ConversationMemory(db_path=settings.dealix_db)
    await memory.init()
    llm = LLMGateway(settings=settings)
    wa = WhatsAppAgent(settings=settings, memory=memory, llm=llm)

    orchestrator = EngagementOrchestrator(settings=settings, memory=memory, llm=llm)
    orchestrator.register_agent(wa.channel, wa)

    lead = Lead(id="test_001", name="أحمد", company="متجر الأفق", phone="+966500000000")
    playbook = Playbook.from_yaml("app/engagement/playbooks/ecommerce_outbound.yaml")
    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)
    print(result)

asyncio.run(main())
```

### 4. تشغيل FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. اختبار Webhook واتساب:

```bash
# كشف المنفذ عبر cloudflared
cloudflared tunnel --url http://localhost:8000

# الصق الرابط في Twilio Sandbox:
# https://<your-tunnel>.trycloudflare.com/api/v1/webhooks/whatsapp
```

### 6. تشغيل الاختبارات:

```bash
cd dealix-clean/backend
pytest tests/engagement/ -v
```

---

## المتطلبات والتبعيات

| الحزمة | الوظيفة |
|---|---|
| `aiosqlite` | قاعدة بيانات SQLite async |
| `httpx` | HTTP client async للـ APIs |
| `pydantic-settings` | قراءة إعدادات من `.env` |
| `pyyaml` | تحميل ملفات Playbook |
| `twilio` | SDK واتساب + SMS (اختياري — الكود يستخدم httpx مباشرة) |

---

## ملاحظات الامتثال (Compliance)

- **PDPL:** لا ترسل بدون موافقة مسبقة (`opt_in=True`).
- **WhatsApp Policy:** استخدم القوالب المعتمدة خارج نافذة 24 ساعة.
- **LinkedIn ToS:** استخدم Unipile فقط — لا استخراج بيانات مباشر.
- **SMS:** أضف دائماً تعليمات إلغاء الاشتراك للرسائل التسويقية.
- **ساعات الهدوء:** النظام يحظر الإرسال من 10 مساءً حتى 8 صباحاً تلقائياً.
