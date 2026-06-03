# Revenue Experiments Review — مراجعة تجارب الإيرادات

*Date: 2026-06-03 | Source: `company_os/experiments/experiments.json`*
*Generated/validated by: `python dealix.py experiment-review`*

---

## التجارب المسجّلة

| ID | النوع | المتغيّر | الحالة | المقياس | موافقة الإرسال |
|----|------|----------|--------|---------|:--------------:|
| EXP-001 | sector | sector | running | reply_rate | ✅ |
| EXP-002 | cta | cta | queued | positive_reply_rate | ✅ |
| EXP-003 | offer | offer | queued | close_rate | ✅ |

---

## التحقق من قاعدة المتغيّر الواحد

| ID | عدد المتغيّرات | الحالة |
|----|---------------:|:------:|
| EXP-001 | 1 | ✅ |
| EXP-002 | 1 | ✅ |
| EXP-003 | 1 | ✅ |

**كل التجارب تلتزم بقاعدة "متغيّر واحد فقط".**

---

## التجربة النشطة

```txt
EXP-001 (sector)
Hypothesis: Training companies reply faster than clinics to the lead-recovery angle.
Control:    Marketing Agencies
Variants:   Training Companies, Clinics
Metric:     reply_rate
Status:     running
```

النتيجة تُغذّي `reports/scale/SECTOR_EXPANSION_DECISION.md` و
`reports/experiments/WEEKLY_REVENUE_EXPERIMENTS.md`.

---

## القاعدة

```txt
لا تغيّر كل شيء مرة واحدة. متغيّر واحد لكل تجربة.
كل إرسال في التجربة يحتاج موافقة المؤسس.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
