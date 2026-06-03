# اجتماع المؤسس الأسبوعي — قرار واحد + انحراف واحد

**الغرض:** منع 15 مبادرة متوازية — إيقاع أسبوعي يتفوق على الحدس غير المُحصى (ممارسة B2B SaaS + Dealix).

---

## 30 دقيقة (قالب)

| دقيقة | سؤال | مخرجة |
|-------|------|--------|
| 0–5 | ما مقياس **الانحراف** الوحيد هذا الأسبوع؟ | رقم أو حدث واحد |
| 5–15 | ماذا يقول [scorecard](../commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md) + Evidence؟ | حقيقة فقط |
| 15–25 | ما **القرار الواحد** الذي يخدم المرحلة 0–5؟ | جملة واحدة |
| 25–30 | ماذا **توقف** عن فعله؟ | قائمة stop (≤3) |

---

## ملف الأسبوع

```bash
py -3 scripts/founder_weekly_decision_init.py
# يكتب: data/founder_weekly/decision_YYYY-Www.yaml (gitignored — من القالب في operations/)
```

**حقول إلزامية:** `deviation_metric` · `one_decision` · `stop_list`

**بعد الاجتماع:** شغّل `founder_cadence --weekly` يوم الجمعة.

---

## ربط بالخطة الشاملة

- المرحلة الحالية: [FOUNDER_PHASE_0_1_GATE_AR.md](FOUNDER_PHASE_0_1_GATE_AR.md)
- ترميز GTM: [FOUNDER_GTM_CODIFICATION_AR.md](../commercial/operations/FOUNDER_GTM_CODIFICATION_AR.md)

---

*آخر تحديث: 2026-05-18*
