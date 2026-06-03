# Call Brief System — دليل المتصل البشري

**الهدف:** الشخص الذي يتابع بالاتصال يحتاج **Call Brief** لا مجرد رقم. يفتح الملف فيعرف: أكلّم أي دور؟ أبدأ بأي جملة؟ أسأل وش؟ أتوقع أي اعتراض وكيف أرد؟ وش الخطوة التالية؟

> **مهم:** كل Call Brief مخصّص **لمتصل بشري**. لا يوجد اتصال آلي بالعملاء إطلاقًا (`automated_calling = false`, `caller_type = "human"`).

- **Schema:** [`schemas/call_brief.schema.json`](../../schemas/call_brief.schema.json)
- **البيانات:** [`data/acquisition/call_briefs.jsonl`](../../data/acquisition/call_briefs.jsonl)
- **الطابور:** [`reports/acquisition/CALL_FOLLOWUP_QUEUE.md`](../../reports/acquisition/CALL_FOLLOWUP_QUEUE.md)

---

## 1. الحقول

| الحقل | المعنى |
|------|--------|
| `brief_id` | معرّف (CB-001 …) |
| `company`, `contact_role` | الشركة والدور المستهدف |
| `recommended_system` | النظام المقترح |
| `likely_pain` | الألم المرجّح |
| `email_sent_summary` | ملخص ما أُرسل (أو مسودة بانتظار الموافقة) |
| `call_objective` | هدف المكالمة (عادة: تأكيد الألم + حجز اكتشاف) |
| `opening_line` | جملة الافتتاح |
| `discovery_questions` | أسئلة الاكتشاف (≥ 1) |
| `expected_objection` / `best_response` | الاعتراض المتوقع والرد الأفضل |
| `next_step` | الخطوة التالية |
| `caller_type` | **human** ثابت |
| `automated_calling` | **false** ثابت |

---

## 2. كيف يستخدمه المتصل؟

```txt
1. افتح Call Brief الخاص بالشركة من CALL_FOLLOWUP_QUEUE.md
2. تأكد أن المسودة (البريد) اعتُمدت أو أن المكالمة بادرة منفصلة
3. ابدأ بـ opening_line
4. اطرح discovery_questions بالترتيب
5. عند الاعتراض المتوقع، استخدم best_response
6. أغلق بـ next_step (عادة: مكالمة 20 دقيقة)
```

## 3. مثال (مولّد فعليًا — Revenue Operating System)

```txt
Company: CloudShift Consulting
Contact role: Head of Sales
Objective: التحقق من فرضية الألم وحجز مكالمة اكتشاف لـ 7-Day Revenue Operating Sprint.
Opening: تواصلنا لأن الشركات في وضعكم غالبًا تملك طلبًا جيدًا لكن جزءًا من الإيراد يتسرب بين الاستفسار والإغلاق بسبب غياب نظام موحد.
Q1: هل عندكم مصدر واحد واضح لكل الفرص أم موزعة على أكثر من مكان؟
Q2: هل كل فرصة (lead) لها حالة وخطوة تالية محددة؟
Q3: هل تصل الإدارة تقرير أسبوعي واضح عن الفرص والإيراد؟
Expected objection: عندنا CRM بالفعل
Best response: لا نستبدل أدواتكم؛ نرتب ما لديكم في نظام تشغيل يعطي كل فرصة خطوة تالية وتقريرًا واحدًا للإدارة…
Next step: مكالمة 20 دقيقة لفهم مصادر الفرص وقنوات التواصل.
```

---

## 4. قواعد صارمة

- الفحص **C03** يضمن أن لكل Brief `opening_line` و`discovery_questions`.
- الفحص **C10** يضمن `automated_calling = false` و`caller_type = "human"`.
- مكتبة الجُمل والأسئلة الكاملة في [CALL_SCRIPT_LIBRARY_AR.md](CALL_SCRIPT_LIBRARY_AR.md).
