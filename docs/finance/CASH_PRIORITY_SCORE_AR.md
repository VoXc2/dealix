# Cash Priority Score — درجة أولوية الكاش

أي فرصة تتحول إلى كاش أسرع وأسهل؟ درجة من 100 لكل Account Pack.

---

## 1. المعايير والأوزان

| المعيار | الوزن | كيف يُحسب |
|---------|------:|-----------|
| Ability to pay | 25 | low=9 · medium=17 · high=25 |
| Urgency | 25 | low=8 · medium=16 · high=25 |
| Ease of delivery | 20 | حسب النظام (10–20) |
| Upsell potential | 15 | حسب النظام (10–15) |
| Contact availability | 15 | C0=3 … C4=15 |

المرجع التنفيذي: `scripts/dealix_account_lib.py:compute_cash_priority`.

---

## 2. المخرج

```
data/finance/cash_priority_scores.jsonl   (لكل 400 فرصة)
reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md
```

كل سجل يحمل أيضًا: السعر الافتتاحي المتوقع، تعقيد التسليم، الساعات التقديرية، إشارة الهامش، إمكانية الـUpsell، وتفصيل الدرجة.

---

## 3. الاستخدام في قرار المؤسس

`DAILY_SUPER_COMMAND.md` يعرض:
- **قيمة Top 100 المحتملة** (مجموع الأسعار الافتتاحية).
- **أعلى 30 فرصة كاش**.
- **قيمة الفرص حسب النظام**.

هكذا يعرف المؤسس **من أين يبدأ اليوم** لأقصى كاش بأقل احتكاك.

---

## 4. سلامة الحساب

مجموع `cash_priority_breakdown` = `cash_priority_score` بالضبط، والنتيجة بين 0 و100.
يتحقق المدقّق من ذلك لكل 400 سجل.

---

*Version 1.0 — يقرأ مع STARTER_SPRINT_MARGIN_MODEL_AR و ACCOUNT_SCORING_MODEL_AR*
