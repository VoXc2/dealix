# الأمن والخصوصية في واتساب
## WhatsApp Security & Privacy (PDPL/SDAIA)

> **الغرض:** يوثّق هذا المستند سياسات الأمن والخصوصية المُطبَّقة في قناة واتساب — بما يشمل: حظر الأسرار، الامتثال لنظام PDPL/SDAIA، تقنيع أرقام الجوال، وسياسة الانسحاب (`opt_out`).  
> مراجع الحوكمة: `AGENTS.md §8`, `company_os/governance/pdpl_checklist.md`, `company_os/governance/data_handling_checklist.md`.

---

## 1. حظر الأسرار (No-Secrets Rule)

### ما هو المحظور في أي رسالة واتساب أو سجل؟

| النمط المحظور | مثال (افتراضي) | البديل الصحيح |
|---|---|---|
| مفاتيح API | `sk-...`, `AKIA...` | `portal://vault/...` |
| كلمات المرور | `password=...` | — (البوابة فقط) |
| رموز مصادقة | `Bearer <token>` | — |
| مفاتيح خاصة | `BEGIN PRIVATE KEY` | — |
| أرقام جوال كاملة | `+966501234567` | `+9665XXXX1234` |
| إيميلات شخصية حقيقية | `user@domain.com` | `user@...` مقنَّع |

هذا الحظر يسري أيضًا على: السجلات (`notes`)، الـPrompts، الـJSONL، التقارير، قضايا GitHub، التعليقات.

**التطبيق التلقائي:** سكربت `scripts/client_revenue_delivery_check.py` يفحص هذه الأنماط.  
مرجع: `AGENTS.md §8` (قاعدة "لا أسرار").

---

## 2. الامتثال لنظام حماية البيانات الشخصية (PDPL/SDAIA)

### المبادئ المُطبَّقة

| المبدأ | الإجراء في Dealix |
|---|---|
| **الاحتفاظ المحدود** | حذف البيانات تلقائيًا بعد 90 يومًا (افتراضي) |
| **البيانات داخل السعودية** | البيانات تُخزَّن في نطاق السعودية قدر الإمكان |
| **حقوق صاحب البيانات** | طلبات الاطلاع/التصحيح/الحذف مدعومة |
| **إشعار الخرق** | في حالة خرق: إشعار الجهات المختصة خلال 72 ساعة |
| **الموافقة الصريحة** | لا معالجة بيانات بدون `consent_basis` موثّق |
| **إخفاء الهوية** | إخفاء PII لعملاء العميل قبل أي تحليل |

مراجع تفصيلية: `company_os/governance/pdpl_checklist.md`, `company_os/governance/data_handling_checklist.md`.

---

## 3. تقنيع أرقام الجوال

### الصيغة المعتمدة

```
+9665XXXX1234
```

- الجزء المرئي: رمز السعودية `+966` + مزوّد `5` + آخر 4 أرقام
- الجزء المقنَّع: `XXXX` للأرقام الوسطى

### التطبيق في السكيمة

```json
// schemas/whatsapp_session.schema.json
"phone_masked": {
  "pattern": "^\\+9665[0-9X]{8}$",
  "description": "Masked KSA mobile. Full number lives only in secure store."
}
```

- `wa_contact_ref`: مرجع مبهم للاتصال، لا يُكشف فيه الرقم الكامل
- الرقم الكامل يُخزَّن فقط في المخزن الآمن (portal/vault)

### مثال صحيح من sessions.jsonl

```json
{
  "phone_masked": "+9665XXXX0142",
  "wa_contact_ref": "wac_ref_8f3a"
}
```

---

## 4. سياسة الانسحاب (opt_out)

### كيف يتم الانسحاب؟

العميل يرسل أي من: "إيقاف"، "توقف"، "بلّش"، أو يختار خيار الإلغاء.

### ما الذي يحدث فورًا؟

```
opt_out يُرسَل
      │
      ▼
consent.opt_out = true
consent.opt_out_timestamp = [الوقت الحالي]
      │
      ▼
status: opted_out
      │
      ▼
إرسال قالب opt_out_ack:
"تمام، أوقفنا الرسائل من طرفنا.
 تقدر ترجع لنا أي وقت. شكرًا {first_name}."
      │
      ▼
جميع التدفقات المعلّقة تُلغى فورًا
لا رسائل أخرى تُرسَل
```

**لا استثناء:** حتى رسائل النظام (إخطارات التقرير، التجديد) تتوقف فورًا عند `opt_out`.

---

## 5. بيانات عملاء العميل — حماية مزدوجة

الفرق المهم:
- **بيانات العميل** (TrainMe KSA، Digital Rise Agency): محمية بالسياسات أعلاه.
- **بيانات عملاء العميل** (عملاء TrainMe أو Digital Rise): **ممنوع إدخالها في أي أداة ذكاء اصطناعي عام** — تُخفى قبل أي تحليل.

مرجع: `AGENTS.md §8`.

---

## 6. مستوى المخاطرة وإجراءات الموافقة

| نوع البيانات | risk_level | الإجراء المطلوب |
|---|---|---|
| PII فردية | `high` | إخفاء + موافقة + سجل مدقّق |
| بيانات مالية | `high` – `critical` | تشفير + موافقة المؤسس |
| بيانات اتصال (هاتف/إيميل) | `medium` | تقنيع + portal:// فقط |
| بيانات تشغيلية عامة | `low` | احتياطات قياسية |

---

## 7. سجل الإجراءات (ai_action_ledger)

كل إجراء ذي أثر خارجي يُسجَّل في `ai_action_ledger` بـ:
- `risk_level`
- `dry_run` (هل كان في وضع المحاكاة؟)
- `send_enabled` (هل أُرسل فعلًا؟)
- `approved_by` و`approved_at`

لا يوجد إجراء غير مُسجَّل.

---

## مراجع

- `AGENTS.md §2` (الخطوط الحمراء) و`§8` (الخصوصية والأمن)
- `schemas/whatsapp_session.schema.json`
- `data/whatsapp/sessions.jsonl`
- `data/whatsapp/templates.yaml` (قالب: `opt_out_ack`)
- `company_os/governance/pdpl_checklist.md`
- `company_os/governance/data_handling_checklist.md`
- `docs/security/` و`docs/privacy/`

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
