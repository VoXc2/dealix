# Delivery Capacity Review — مراجعة قدرة التسليم

*Date: 2026-06-03 | Source: `company_os/delivery/capacity.json`*
*Generated/validated by: `python dealix.py delivery-capacity`*

---

## الاستغلال الحالي

```txt
total_capacity_hours_per_week = 40
committed_hours_per_week      = 24
utilization                   = 60.0%
scale_block_threshold         = 80%
hard_block_threshold          = 100%
```

**الحالة: صحي (60% < 80%) — يمكن رفع الإرسال تدريجيًا.**

---

## نموذج الأنظمة

| النظام | ساعات | تعقيد | مخاطرة مراجعة | تدخّل المؤسس | تفويض | هامش |
|--------|------:|-------|---------------|--------------|:-----:|-----:|
| Proposal & Proof OS | 6 | low | low | low | ✅ | 80% |
| Follow-up Recovery OS | 5 | low | low | low | ✅ | 82% |
| Lead Qualification OS | 6 | low | low | medium | ✅ | 78% |
| Client Onboarding OS | 8 | medium | medium | medium | ✅ | 72% |
| Executive Command OS | 8 | medium | medium | high | ❌ | 70% |

---

## أسرع أنظمة للتسليم

```txt
1. Follow-up Recovery OS (5h)
2. Proposal & Proof OS (6h)
3. Lead Qualification OS (6h)
```

عند الحاجة لرفع الحجم، ركّز على هذه الأنظمة (ساعات أقل، هامش أعلى، قابلة للتفويض).

---

## Scale Rule

```txt
إذا utilization > 80% → لا ترفع الإرسال، ركّز على التسليم أو فوّض.
حاليًا 60% → ضمن النطاق الآمن.
```

---

## توصيات

```txt
1. وثّق runbook لكل نظام can_delegate = true لتمكين التفويض.
2. راقب Executive Command OS (تدخّل مؤسس عالٍ، غير قابل للتفويض).
3. أعد التقييم أسبوعيًا مع نمو الصفقات المربوحة.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
