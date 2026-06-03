# تذكرة الدعم والتصعيد (Support Escalation)
## تدفق الدعم، السكيمة، وSLA

> **الغرض:** يوثّق هذا المستند كيفية رفع تذكرة دعم من محادثة واتساب، تصنيف التذاكر، وتعريفات SLA لكل مستوى خطورة.  
> مرجع السكيمة: `schemas/support_ticket.schema.json`.  
> بيانات مثال: `data/whatsapp/support_tickets.jsonl` (SUP-0001).

---

## 1. متى تُرفع تذكرة دعم؟

| الموقف | كيف يُفعَّل |
|---|---|
| العميل يختار "أحتاج مساعدة" في أي بطاقة | خيار مباشر |
| العميل يختار "كلّمني بشري" | يُنشئ `HHO-xxxx` + قد يُنشئ `SUP-xxxx` |
| الذكاء لا يفهم الطلب (3 محاولات فاشلة) | تلقائي |
| الطلب خارج نطاق المحادثة الآلية | تلقائي |

---

## 2. تدفق رفع التذكرة

```
القالب: support_escalation
──────────────────────────
"وصلني طلبك، راح أحوّلك لزميل بشري يكمل معك.
 ممكن تختصر لي المطلوب؟ (بدون أي بيانات حساسة)"

خيارات:
  [1] كتبت المطلوب → submitted

           │
           ▼
    إنشاء SUP-xxxx:
    ─────────────────
    category:   [من الجدول أدناه]
    severity:   [حسب الموقف]
    channel:    whatsapp
    summary:    ملخص موجز (بلا أسرار/PII)
    status:     open
    sla_due_at: [حسب severity]

           │
           ▼
    إشعار المسؤول في طابور الموافقات

           │
           ▼
    رسالة للعميل:
    "وصلت تذكرتك (#SUP-xxxx). نعود لك قريبًا [وقت SLA]."
```

---

## 3. تصنيفات التذاكر (`category`)

| التصنيف | الوصف | أمثلة |
|---|---|---|
| `onboarding` | مشاكل بداية التشغيل | لا أعرف كيف أبدأ checklist |
| `access_permission` | مشاكل الوصول والصلاحيات | صعوبة في منح صلاحية البوابة |
| `report` | تقرير غير واضح أو مفقود | لم أتلق تقرير الأسبوع |
| `billing` | فواتير أو دفع | سؤال عن فاتورة |
| `bug` | خطأ تقني | البوابة لا تفتح |
| `scope_question` | سؤال عن نطاق الخدمة | هل يشمل العقد X؟ |
| `feature_request` | طلب ميزة جديدة | أريد تقريرًا أسبوعيًا بصيغة PDF |
| `other` | أي شيء آخر | — |

---

## 4. مستويات الخطورة وSLA

| severity | وقت الاستجابة | وقت الحل المستهدف |
|---|---|---|
| `critical` | < 1 ساعة | < 4 ساعات |
| `high` | < 4 ساعات | < 8 ساعات |
| `medium` | < 8 ساعات | < 24 ساعة |
| `low` | < 24 ساعة | < 48 ساعة |

**تعريفات Severity:**
- `critical`: توقف خدمة، خطأ في دفع، خرق خصوصية محتمل
- `high`: مشكلة تمنع استمرار التسليم
- `medium`: مشكلة تؤخر العمل
- `low`: استفسار، توضيح، طلب ميزة

---

## 5. حقول سكيمة Support Ticket

| الحقل | النوع | الوصف |
|---|---|---|
| `id` | string | نمط `SUP-[A-Za-z0-9_-]+` |
| `company` | string | اسم الشركة |
| `category` | enum | تصنيف التذكرة |
| `severity` | enum | مستوى الخطورة |
| `channel` | enum | `whatsapp` / `portal` / `email` |
| `summary` | string | ملخص موجز (بلا أسرار/PII) |
| `assigned_to` | string/null | المسؤول |
| `sla_due_at` | datetime/null | موعد SLA |
| `status` | enum | `open` → `in_progress` → `waiting_client` → `resolved` → `closed` |
| `linked_handoff_id` | string/null | رابط لـ HHO-xxxx إن وُجد |

---

## 6. دورة حياة التذكرة

```
open
  │
  ├─ المسؤول يتولّاها    → in_progress
  │      │
  │      ├─ يحتاج ردًا من العميل → waiting_client
  │      │                              │
  │      │                              └─ رد العميل → in_progress
  │      │
  │      └─ المشكلة حُلّت → resolved
  │                          │
  │                          └─ تأكيد العميل → closed
  │
  └─ لم يُستجَب → تصعيد تلقائي (SLA يُخطِر المؤسس)
```

---

## 7. مثال حقيقي — SUP-0001 (Digital Rise Agency)

```json
{
  "id": "SUP-0001",
  "company": "Digital Rise Agency",
  "category": "access_permission",
  "severity": "low",
  "channel": "whatsapp",
  "summary": "Client unsure how to grant read-only access; needs guidance via portal.",
  "assigned_to": "founder",
  "sla_due_at": "2026-06-04T11:30:00+03:00",
  "status": "open",
  "linked_handoff_id": null
}
```

العميل محتاج توجيه — `severity: low`، لا بيانات حساسة في الملخص.

---

## 8. الحالات التي تتحول لـ Human Handoff

إذا تطلبت التذكرة:
- قرار تسعير
- أي تعهد قانوني/تعاقدي
- إعادة تهيئة أنظمة

تُنشأ تلقائيًا سجل `HHO-xxxx` مرتبط بـ`linked_handoff_id` وتُعطى أولوية أعلى.

---

## مراجع

- `schemas/support_ticket.schema.json`
- `data/whatsapp/support_tickets.jsonl` (مثال: SUP-0001)
- `data/whatsapp/flows.yaml` (تدفق: `support_escalation`)
- `data/whatsapp/templates.yaml` (قالب: `support_escalation`)
- `docs/whatsapp/WHATSAPP_HUMAN_HANDOFF_AR.md`
- `AGENTS.md §3` (الثوابت الدائمة)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
