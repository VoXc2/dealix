# Weekly Revenue Experiments — تجارب الإيرادات الأسبوعية

*Week of: 2026-06-03 | Source: `company_os/experiments/experiments.json`*

---

## التجارب هذا الأسبوع

| ID | النوع | الفرضية | الحالة | المقياس |
|----|------|---------|--------|---------|
| EXP-001 | sector | Training أسرع ردًا من Clinics لزاوية استرجاع الفرص | running | reply_rate |
| EXP-002 | cta | Mini Proposal CTA يتفوّق على مكالمة 15 دقيقة | queued | positive_reply_rate |
| EXP-003 | offer | Sprint 7 days يتفوّق على diagnostic first | queued | close_rate |

---

## النتائج (تُحدَّث مع جريان التجارب)

| ID | إرساليات | ردود | معدل | الحكم |
|----|--------:|-----:|-----:|-------|
| EXP-001 | — | — | — | قيد الجريان |
| EXP-002 | — | — | — | في الطابور |
| EXP-003 | — | — | — | في الطابور |

---

## قاعدة الانضباط

```txt
متغيّر واحد لكل تجربة (تحقّقه check_revenue_experiments.py).
كل إرسال بموافقة المؤسس.
```

---

## القرارات

```txt
- أكمل EXP-001 قبل تشغيل EXP-002 لتجنّب تداخل المتغيّرات.
- بعد النتائج: ثبّت الأفضل، أوقف الأضعف، جرّب متغيّرًا جديدًا.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Cadence: Weekly*
