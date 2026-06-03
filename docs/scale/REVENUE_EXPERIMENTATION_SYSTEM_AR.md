# Revenue Experimentation System — نظام تجارب الإيرادات (نظرة التوسع)

> كل أسبوع نجرّب زاوية مختلفة، لكن بشكل مضبوط. التفاصيل الكاملة في
> `docs/experiments/REVENUE_EXPERIMENTATION_SYSTEM_AR.md`. هذا الملف يربط
> التجارب بطبقة التوسع.

---

## لماذا التجارب جزء من التوسع؟

التوسع بلا تعلّم = مضاعفة الخطأ. التجارب الأسبوعية ترفع جودة الاستهداف
والتحويل قبل أن نضاعف الحجم، فيصبح التوسع مبنيًا على معرفة لا على حماس.

---

## التجارب الأسبوعية

| Experiment | مثال |
|------------|------|
| Sector | Training vs Clinics vs Agencies |
| Need | follow-up vs proposal vs whatsapp |
| Offer | Sprint 7 days vs diagnostic first |
| CTA | "أرسل Mini Proposal؟" vs "مكالمة 15 دقيقة؟" |
| Buyer | Founder vs Marketing Manager |
| Price | 3,000 vs 4,500 starter |
| Proof | sample output vs checklist |

المصدر: `company_os/experiments/experiments.json`.

---

## القاعدة

```txt
لا تغير كل شيء مرة واحدة.
كل تجربة تغير متغيرًا واحدًا.
```

يتحقق منها `python dealix.py experiment-review` (يرفض أي تجربة تغيّر أكثر من متغيّر).

---

## ربط التجارب بقرار التوسع

```txt
نتيجة تجربة قطاع قوية → دخول القطاع (Sector Expansion).
نتيجة تجربة زاوية قوية → تثبيتها قبل رفع الإرسال.
نتيجة تجربة عرض قوية → تحديث العرض الافتراضي.
```

تُغذّى النتائج في:
- `reports/experiments/WEEKLY_REVENUE_EXPERIMENTS.md`
- `reports/scale/WEEKLY_SCALE_REVIEW.md`

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
