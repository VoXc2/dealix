# Revenue Experimentation System — نظام تجارب الإيرادات

> كل أسبوع نجرّب زاوية مختلفة بشكل مضبوط، ونغيّر **متغيّرًا واحدًا فقط** في كل تجربة.

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

المصدر الآلي: `company_os/experiments/experiments.json`.

---

## القاعدة الذهبية

```txt
لا تغير كل شيء مرة واحدة.
كل تجربة تغير متغيرًا واحدًا.
```

يفرضها `check_revenue_experiments.py`: أي تجربة `variables_changed` فيها ≠ 1
تُرفض (exit 1).

---

## بنية التجربة

```txt
id, type, hypothesis, variable, variables_changed (length = 1),
control, variants, metric, status, owner, start_date,
requires_approval_for_send
```

---

## دورة التجربة

```txt
1. صُغ فرضية واضحة (Hypothesis).
2. حدّد المتغيّر الواحد والـ control.
3. اختر مقياس النجاح (reply_rate / positive_reply / close_rate ...).
4. شغّل التجربة (الإرسال بموافقة المؤسس).
5. سجّل النتائج في reports/experiments/.
6. قرّر: ثبّت / أوقف / كرّر بمتغيّر جديد.
```

---

## الحوكمة

```txt
- كل إرسال في التجربة يحتاج موافقة (requires_approval_for_send = true).
- لا تجربة تكسر قواعد deliverability أو الخطوط الحمراء للوكلاء.
- النتائج تُغذّي Weekly Learning Loop.
```

---

## التقارير المرتبطة

- `reports/experiments/WEEKLY_REVENUE_EXPERIMENTS.md`
- `reports/experiments/EMAIL_ANGLE_RESULTS.md`
- `reports/experiments/OFFER_CONVERSION_REVIEW.md`

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Cadence: Weekly*
