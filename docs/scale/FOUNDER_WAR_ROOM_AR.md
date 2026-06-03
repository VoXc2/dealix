# Founder War Room — غرفة عمليات المؤسس

> مركز القرار اليومي والأسبوعي. الوكلاء يرفعون القرار، والمؤسس يقرّر.
> لا يُنفَّذ قرار من War Room تلقائيًا.

---

## Daily War Room — يجب أن يقول

```txt
1. أهم قرار اليوم
2. أكبر فرصة نقدية
3. أكبر خطر
4. أفضل 10 شركات اليوم
5. أفضل 5 عروض تنتظر موافقة
6. الصفقات المتوقفة
7. التسليمات المتأخرة
8. هل نرفع أو نخفض الإنتاج؟
9. ماذا نتعلم من السوق؟
```

يُولَّد عبر:

```bash
python dealix.py war-room --dry-run   # عرض فقط، بدون كتابة ملف أو أي إجراء
python dealix.py war-room             # يكتب reports/founder/FOUNDER_WAR_ROOM_DAILY.md
```

---

## Weekly War Room — يجب أن يقول

```txt
best sector
best need
best sprint
highest reply angle
highest conversion offer
best delivery margin
worst bottleneck
next week focus
```

يُوثّق في `reports/founder/FOUNDER_WAR_ROOM_WEEKLY.md`.

---

## مصادر البيانات

| القسم | المصدر |
|-------|--------|
| أفضل الشركات | `company_os/revenue/prospects.csv` |
| العروض المعلّقة | `company_os/governance/approval_queue.json` |
| قرار الإنتاج | `capacity.json` + `deliverability_state.json` |
| التعلّم | `company_os/experiments/experiments.json` |
| الوضع الحالي | `company_os/scale/scale_state.json` |

---

## قاعدة الحوكمة

```txt
War Room يرفع القرار.
War Room لا ينفّذ.
كل إرسال/اتصال/تسعير/تعاقد/بدء تسليم → موافقة المؤسس.
```

الوكيل المسؤول `Founder Command Agent` بمستوى L2 (Advise): يرفع ولا ينفّذ.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Cadence: Daily + Weekly*
