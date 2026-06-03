# Delivery Capacity Planning — تخطيط قدرة التسليم

> لا تبع أكثر من قدرتك على التسليم. البيع الزائد عن القدرة = تأخير + سمعة سيئة
> + هامش يتآكل. الإرسال يجب أن يتوقف قبل أن تنهار القدرة.

---

## لكل نظام احسب

```txt
estimated_delivery_hours
complexity
required_inputs_difficulty
revision_risk
founder_involvement
can_delegate
gross_margin
```

المصدر الرسمي: `company_os/delivery/capacity.json`.

---

## معادلة الاستغلال

```txt
utilization = committed_hours_per_week / total_capacity_hours_per_week * 100
```

| النطاق | الحالة | الإجراء |
|--------|--------|---------|
| < 80% | صحي | يمكن رفع الإرسال تدريجيًا |
| 80–100% | محذّر | لا ترفع الإرسال — ركّز على التسليم أو فوّض |
| > 100% | خطر | فوق القدرة — أوقف القبول، وظّف/فوّض فورًا |

---

## Scale Rule

```txt
إذا Delivery Capacity Utilization > 80%
لا ترفع الإرسال.
ركز على التسليم أو وظف/فوّض.
```

يتحقق منها `python dealix.py delivery-capacity`.

---

## أسرع أنظمة للتسليم

```txt
1. Proposal & Proof OS
2. Follow-up Recovery OS
3. Lead Qualification OS
4. Client Onboarding OS
5. Executive Command OS
```

عند الحاجة لرفع الحجم بسرعة، ركّز على الأنظمة منخفضة الساعات وعالية الهامش
والقابلة للتفويض.

---

## مبادئ التفويض

| العامل | يدفع نحو التفويض | يدفع نحو الاحتفاظ بالمؤسس |
|--------|-------------------|----------------------------|
| founder_involvement | منخفض | عالٍ |
| complexity | منخفض | عالٍ |
| revision_risk | منخفض | عالٍ |
| can_delegate | true | false |

كل نظام `can_delegate = true` يجب توثيق runbook له لتمكين التفويض دون فقدان الجودة.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
