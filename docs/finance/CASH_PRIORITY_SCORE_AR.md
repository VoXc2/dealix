# درجة أولوية النقد (Cash Priority Score)

ترتّب الحسابات حسب قربها من نقد فعلي، لا حسب الإعجاب بها.

## الصيغة

```
Cash Priority Score =
    urgency          × 0.40   (إلحاح الاحتياج)
  + ticket_potential × 0.30   (حجم الصفقة المحتمل)
  + speed_to_cash    × 0.30   (سرعة الوصول للنقد)
```

كل مكوّن في النطاق 0..100، والناتج 0..100. التطبيق في
`scripts/dealix/scoring.py` والبيانات في
`data/finance/cash_priority_scores.jsonl`.

## الاستخدام

تدخل هذه الدرجة بوزن **25%** في الدرجة النهائية للحساب، وتظهر في «أمر المؤسس
اليومي» لترتيب من تتصل به ومن تعرض له أولًا.

## التقارير

- `reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md` (فرصة الإيراد اليومية)
- `reports/metrics/DAILY_METRICS_DASHBOARD.md` (لوحة المؤشرات)
