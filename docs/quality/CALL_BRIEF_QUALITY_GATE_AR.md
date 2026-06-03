# بوابة جودة موجز الاتصال (Call Brief Quality Gate)

> كل إيميل يُنتج Call Brief قابلًا للتسليم لشخص يتابع بالاتصال.
> AI drafts. Human approves. System logs.

---

## 1. سجل تسليم الإيميل (Email Handoff Record)

```txt
company
email_subject
email_summary
recommended_system
likely_pain
best_contact_role
call_priority
call_opener
call_questions
expected_objection
next_step
owner
due_date
```

---

## 2. أولوية الاتصال

```txt
P1 = ملاءمة عالية + ألم واضح + قدرة دفع
P2 = مناسبة لكن الدليل متوسط
P3 = تحتاج nurture
P4 = لا تتصل الآن
```

---

## 3. متى تفشل البوابة (Gate fails if)

تفشل البوابة إذا نقص أي عنصر (fail conditions):

```txt
لا يوجد opening line
لا توجد أسئلة (discovery questions)
لا يوجد expected objection
لا يوجد next step
```

> أي Call Brief لا يجتاز هذه البوابة لا يُسلَّم لـ call_owner.

---

## 4. المخرج

Call Brief Queue يوميًا في `reports/sales_ops/SALES_OPS_BOARD_STATUS.md` (القسم 3)، ويُولَّد عبر `scripts/commercial-daily-plan.js`. الاعتراضات تُسحب من `company_os/revenue/objections.json`.

---

## 5. حدود الأمان

- لا اتصال آلي. الـ AI يجهّز الموجز فقط؛ الإنسان يتصل.
- الموجز لا يحتوي وعودًا مضمونة ولا أسماء وحدات داخلية.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
