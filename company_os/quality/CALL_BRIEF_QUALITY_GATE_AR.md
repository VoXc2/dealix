# بوابة جودة موجز المكالمة — Call Brief Quality Gate

كل إيميل يُرسَل يولّد Call Brief، حتى يتابع شخص آخر بالاتصال دون شرح إضافي. المنطق:
`callGate` في `scripts/lib/commercial.js`. القائمة: `reports/sales_ops/CALL_FOLLOWUP_QUEUE.md`.

---

## محتوى Call Brief

```
opening_line       سطر الافتتاح
questions[]         أسئلة الاكتشاف (واحد على الأقل)
expected_objection الاعتراض المتوقع
next_step           الخطوة التالية
```

## تفشل البوابة إذا

| السبب | الوصف |
|------|-------|
| `no_opening_line` | لا يوجد سطر افتتاح |
| `no_discovery_questions` | لا توجد أسئلة |
| `no_expected_objection` | لا يوجد اعتراض متوقع |
| `no_next_step` | لا توجد خطوة تالية |

---

## أولوية المكالمة (Call Priority)

| الأولوية | المعنى |
|----------|--------|
| P1 | ملاءمة عالية + ألم واضح + قدرة دفع |
| P2 | مناسبة لكن الدليل متوسط |
| P3 | تحتاج nurture |
| P4 | لا تتصل الآن |

تُرتَّب قائمة الـ Top 30 مكالمات تصاعديًا حسب الأولوية (P1 أولًا).

---

## الحدود

لا اتصال آلي (no automated calling). الاتصال فعل بشري؛ Dealix يجهّز الموجز فقط.
