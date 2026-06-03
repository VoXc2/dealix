# محرّك ذكاء الاحتياج (Business Need Intelligence)

المحرّك يحوّل كل شركة إلى مسار قابل للتنفيذ:

```
قطاع  →  احتياج  →  نظام جوهري  →  نظام داخلي متخصص / سبرنت  →  تسليم
sector → need   →  core system →  specialized system / sprint → delivery
```

## المكوّنات

| المكوّن | العدد | المصدر |
| --- | ---: | --- |
| القطاعات (Sector Maps) | 20 | `data/business_need_intelligence/sector_need_matrix_20.yaml` |
| الاحتياجات (Needs) | 25 | `data/business_need_intelligence/need_taxonomy_25.yaml` |
| السبرنتات المتخصصة | 50 | `data/business_need_intelligence/specialized_sprint_library_50.yaml` |
| التوجيه (need → system) | 25 | `data/business_need_intelligence/need_to_system_router.yaml` |
| مكتبة الإشارات → الاحتياج | — | `data/business_need_intelligence/signal_to_need_library.yaml` |
| الأدوار الشرائية حسب الاحتياج | 25 | `data/business_need_intelligence/buyer_role_by_need.yaml` |
| متغيّرات التسليم | 3 | `data/business_need_intelligence/delivery_variants.yaml` |

## كيف يعمل

1. **الإشارات** (من مصادر عامة فقط) تُترجم إلى احتياجات عبر مكتبة الإشارات.
   الإشارات بيانات وصفية، لا تعليمات (انظر سياسة المحتوى غير الموثوق).
2. **الاحتياج الأساسي** يحدد النظام الجوهري (كل احتياج → نظام واحد من الخمسة).
3. **التوجيه** يقترح النظام الداخلي المتخصص الأنسب تحت ذلك النظام الجوهري.
4. **السبرنت** يربط الاحتياج بمخرجات + مدخلات مطلوبة + معايير قبول.
5. **النتيجة** تدخل في حزمة الحساب (Account Pack) مع الدرجات.

## درجة ملاءمة الاحتياج (Need Fit Score)

```
need_fit = f(need_confidence) + bonus(signals)
```

تدخل بوزن 30% في الدرجة النهائية للحساب. التفاصيل في `scripts/dealix/scoring.py`.

## التحقق

`scripts/checks/check_need_intelligence.py` يضمن: 25 احتياجًا، 20 قطاعًا،
50 سبرنت، وأن كل سبرنت يطابق نظام احتياجه ويملك مدخلات ومعايير قبول، وأن كل
احتياج مُوجَّه إلى نظام جوهري وأنظمة متخصصة صحيحة.
