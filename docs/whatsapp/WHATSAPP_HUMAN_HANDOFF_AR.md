# التسليم البشري في واتساب (Human Handoff)
## متى يحدث، كيف يعمل، وما هو إلزامي

> **الغرض:** يوثّق هذا المستند بروتوكول التسليم البشري في قناة واتساب — متى يُفعَّل تلقائيًا، متى يختاره العميل، وما هي الحالات التي تُلزم به (السعر النهائي، الدفع، القانوني/التعاقدي).  
> مرجع السكيمة: `schemas/human_handoff.schema.json`.  
> بيانات مثال: `data/whatsapp/handoffs.jsonl` (HHO-0001).

---

## 1. المبدأ الأساسي

**التسليم البشري دائمًا متاح — نقرة واحدة في أي لحظة.**

العميل لا يحتاج سببًا لطلبه. "كلّمني بشري" خيار دائم في كل تدفق (`human_handoff` في قائمة `always_available` بـ`flows.yaml`).

---

## 2. متى يُفعَّل التسليم البشري؟

### أ. إلزامي (يُفعَّل تلقائيًا بدون اختيار العميل)

| الموقف | `reason` في السكيمة |
|---|---|
| العميل يطلب السعر النهائي | `final_price` |
| إرسال رابط دفع أو تأكيد صفقة | `payment_send` |
| أي سؤال قانوني أو بند تعاقدي | `legal_or_contract` |
| الذكاء يفقد الثقة بالرد (< حد معين) | `low_confidence` |
| موضوع خارج نطاق Dealix | `out_of_scope` |
| بيانات حساسة (امتثال، PII) | `compliance_sensitive` |

### ب. اختياري (بطلب صريح من العميل)

| الموقف | `reason` |
|---|---|
| "كلّمني بشري" في أي وقت | `client_requested` |
| شكوى أو استياء | `complaint` |
| أي سبب آخر | `other` |

---

## 3. كيف يعمل التسليم؟

```
المشغّل (تلقائي أو بطلب العميل)
            │
            ▼
    إنشاء سجل HHO-xxxx
    ─────────────────────
    reason:      [السبب]
    from_channel: whatsapp
    urgency:     [low/medium/high/critical]
    status:      open
    assigned_to: founder (افتراضي)
    sla_due_at:  [حسب الاستعجال]
            │
            ▼
    تغيير حالة الجلسة: status → handoff
            │
            ▼
    رسالة إلى العميل في واتساب:
    "وصلني طلبك — راح يكلّمك أحد من الفريق قريبًا. [SLA]"
            │
            ▼
    إشعار للمؤسس/المسؤول في طابور الموافقات
```

---

## 4. حقول سكيمة Human Handoff

| الحقل | النوع | الوصف |
|---|---|---|
| `id` | string | نمط `HHO-[A-Za-z0-9_-]+` |
| `session_id` | string/null | معرّف جلسة واتساب المرتبطة |
| `company` | string | اسم الشركة |
| `reason` | enum | سبب التسليم (انظر §2) |
| `from_channel` | enum | `whatsapp` / `portal` / `email` |
| `urgency` | enum | `low` / `medium` / `high` / `critical` |
| `assigned_to` | string/null | المسؤول البشري |
| `sla_due_at` | datetime/null | الموعد النهائي حسب SLA |
| `status` | enum | `open` → `assigned` → `in_progress` → `resolved` → `closed` |
| `context` | string | ملخص نصي (بدون أسرار أو PII) |

---

## 5. جداول SLA

| urgency | وقت الاستجابة المستهدف | مثال |
|---|---|---|
| `critical` | < 1 ساعة | شكوى حادة، خطأ دفع |
| `high` | < 4 ساعات | سعر نهائي، تعاقد |
| `medium` | < 8 ساعات (نفس اليوم) | سؤال دفع، طلب عميل |
| `low` | < 24 ساعة | استفسار عام |

`sla_due_at` يُحسب تلقائيًا عند إنشاء سجل HHO.

---

## 6. ما يُمنع قبل اكتمال التسليم

عند `status: handoff`، النظام الآلي:
- لا يُرسل أي رسالة جديدة
- لا يُصدر رابط بوابة جديد
- لا يُنشئ عرضًا أو Proof Pack
- لا يُنفّذ أي إجراء L4/L5

**الاستثناء الوحيد:** رسالة تأكيد استلام الطلب للعميل.

---

## 7. مثال حقيقي — HHO-0001 (TrainMe KSA)

```json
{
  "id": "HHO-0001",
  "session_id": "WAS-0002",
  "company": "TrainMe KSA",
  "reason": "final_price",
  "from_channel": "whatsapp",
  "urgency": "medium",
  "assigned_to": "founder",
  "sla_due_at": "2026-06-03T18:00:00+03:00",
  "status": "open",
  "context": "Client asked for a final price. Routed to founder for pricing decision; no price quoted in chat."
}
```

لاحظ: لا سعر مذكور في `context`، لا أسرار، `status: open` بانتظار تدخّل المؤسس.

---

## 8. العودة للأتمتة بعد حل التسليم

عند `status: resolved`:
1. المسؤول البشري يُحدّث السجل → `status: closed`
2. يمكن إعادة تفعيل الجلسة إذا أراد العميل المتابعة
3. الجلسة تبدأ من نقطة مناسبة (لا تُعيد فحص الجاهزية من الصفر)

---

## مراجع

- `schemas/human_handoff.schema.json`
- `data/whatsapp/handoffs.jsonl` (مثال: HHO-0001)
- `data/whatsapp/flows.yaml` (تدفقات: `support_escalation`, `payment_handoff`)
- `data/whatsapp/templates.yaml` (قالب: `support_escalation`, `payment_handoff_notice`)
- `AGENTS.md §2` (الخطوط الحمراء) و`§4` (L4/L5)
- `docs/whatsapp/HUMAN_HANDOFF_UX_AR.md` (تجربة المستخدم)
- `docs/whatsapp/WHATSAPP_SUPPORT_ESCALATION_AR.md` (تذاكر الدعم)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
