# الجسر: من رد الإيميل الإيجابي إلى محادثة واتساب
## Email Positive Reply → WhatsApp Consent Bridge

> **الغرض:** يوضّح هذا المستند كيفية تحويل رد إيميل إيجابي من عميل محتمل إلى جلسة واتساب مشروعة — بما يشمل: التحقق من الأهلية، تسجيل الموافقة (`consent_basis=positive_reply`)، وفتح المحادثة.  
> هذا الجسر يُطبِّق `AGENTS.md §5` (أساس الموافقة).

---

## 1. تعريف "الرد الإيجابي"

الرد الإيجابي من إيميل = أي رد يُبدي اهتمامًا أو يطلب متابعة، مثل:

| نوع الرد | أمثلة |
|---|---|
| طلب معلومات أكثر | "أريد معرفة المزيد"، "كيف يعمل هذا؟" |
| فتح نقاش | "هذا يبدو مثيرًا للاهتمام، نقدر نتكلم؟" |
| طلب اجتماع | "ممكن نحجز اجتماعًا؟" |
| موافقة صريحة | "نعم، أرسلوا لي التفاصيل" |

**ليس ردًا إيجابيًا:** "أوقفوا الرسائل"، "لا شكرًا"، أي رد سلبي أو صامت.

---

## 2. المسار الكامل

```
إيميل يُرسَل من Dealix (outreach)
           │
           ▼
   العميل يرد بشكل إيجابي
           │
           ▼
  تسجيل الرد في النظام:
  consent_basis     = positive_reply
  consent_source    = email_reply
  consent_timestamp = [وقت الرد]
           │
           ▼
  التحقق الثلاثي:
  ─────────────────
  ✅ consent_basis ∈ القائمة المسموح بها؟
  ✅ consent_timestamp موثّق؟
  ✅ consent_source واضح؟
  → إذا فشل أي منها: لا تُفتح جلسة واتساب
           │
           ▼
  إنشاء جلسة WAS-xxxx:
  ─────────────────────
  status: active
  dry_run: true
  send_enabled: false
  locale: ar
           │
           ▼
  تدفق: welcome_after_consent
  (أول رسالة واتساب)
```

---

## 3. ماذا يحدث إذا كان الرد غامضًا؟

إذا لم يكن الرد صريحًا بالموافقة على التواصل عبر واتساب:

**الخطوة 1:** رسالة إيميل تأكيد قبل الانتقال لواتساب:
```
"شكرًا لردك. نودّ التواصل معك عبر واتساب لمناقشة
كيف نساعدك في تحسين إيرادات شركتك.
هل يناسبك ذلك؟
[نعم، تواصلوا عبر واتساب]  [أفضّل الإيميل]"
```

**الخطوة 2:** فقط إذا اختار "نعم، تواصلوا عبر واتساب" → تُحدَّث `consent_basis` لـ`explicit_optin` وتُفتح الجلسة.

---

## 4. مثال حقيقي — Digital Rise Agency (WAS-0001)

```json
// sessions.jsonl — WAS-0001
{
  "id": "WAS-0001",
  "consent": {
    "consent_basis": "positive_reply",
    "consent_source": "email_reply",
    "consent_timestamp": "2026-06-03T09:05:00+03:00",
    "opt_out": false
  },
  "status": "active",
  "notes": "Replied positively to email; no secrets exchanged."
}
```

Digital Rise Agency ردّت على إيميل تسويقي بشكل إيجابي → consent_basis موثّق → جلسة WAS-0001 مفتوحة.

---

## 5. قيود وحمايات

| القيد | الإجراء |
|---|---|
| لا انتظار "رد غير مقروء" | قراءة الإيميل دون رد ≠ موافقة |
| لا استخدام الرد لرسائل جديدة بموضوع مختلف | الجلسة مرتبطة بموضوع المحادثة الأصلية |
| لا مشاركة رقم الجوال قبل الموافقة | رقم الجوال يُطلب فقط بعد تأكيد الاهتمام |
| إذا كشفت المحادثة عن تحفّظ → توقف فوري | انسحاب فعلي = `opt_out = true` |
| الرقم يُخزَّن مُقنَّعًا فقط | `+9665XXXX1234` في الجلسة |

---

## 6. تسجيل الجسر في ai_action_ledger

كل فتح جلسة من رد إيميل يُسجَّل بـ:
```json
{
  "action": "open_whatsapp_session",
  "trigger": "email_positive_reply",
  "consent_basis": "positive_reply",
  "risk_level": "low",
  "dry_run": true,
  "send_enabled": false,
  "requires_approval": false
}
```

يُشار إليه في `AGENTS.md §3` (الثوابت الدائمة: "كل إجراء يُسجَّل في سجل الإجراءات").

---

## 7. الفرق بين أسس الموافقة

| الأساس | مصدر الاهتمام | درجة الوضوح |
|---|---|---|
| `positive_reply` | رد إيميل | متوسط (ضمني) |
| `explicit_optin` | زر موافقة صريح | عالٍ |
| `form_submission` | تعبئة نموذج | عالٍ |
| `booking` | حجز اجتماع | عالٍ جدًا |
| `existing_client` | عقد قائم | الأعلى |

**التوصية:** لأعلى جودة، اعمل على تحويل `positive_reply` لـ`explicit_optin` في أول تفاعل.

---

## مراجع

- `schemas/whatsapp_session.schema.json` (حقول `consent`)
- `data/whatsapp/sessions.jsonl` (مثال: WAS-0001)
- `data/whatsapp/flows.yaml` (تدفق: `welcome_after_consent`)
- `AGENTS.md §5` (أساس الموافقة)
- `docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md`

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
