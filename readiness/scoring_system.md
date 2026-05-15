# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## الغرض

تشرح هذه الوثيقة نظام التقييم المستخدم في الطبقة الثالثة عشرة. النظام أداة قياس، لا أداة تسويق. درجة الطبقة وصف للأدلة المتوفرة، وليست وعداً بأداء. أي درجة بلا دليل قابل للتحقق تُعامل كصفر في معيارها الفرعي.

## النطاقات الخمسة

يُصنَّف كل عنصر — طبقة فرعية أو طبقة أو المنصة ككل — على مقياس من خمسة نطاقات:

| النطاق | الدرجة | المعنى |
|---|---|---|
| نموذج أولي (prototype) | 0–59 | الفكرة قائمة، لكن لا أدلة كافية على السلوك. |
| تجربة داخلية (internal beta) | 60–74 | تعمل داخلياً، لكن ينقصها التحقق الدوري الموثّق. |
| تجربة عميل (client pilot) | 75–84 | جاهزة لتشغيل مُراقَب مع عميل واحد تحت إشراف. |
| جاهز للمؤسسات (enterprise-ready) | 85–94 | تمارين متحقَّقة على وتيرة دورية وتغطية مراقبة كاملة. |
| حرجة للمهمة (mission-critical) | 95+ | تشغيل واسع تحت ضمانات تشغيلية مُثبتة. |

## كيف تُوزَّن المعايير الفرعية

كل طبقة لها ملف `scorecard.yaml` يحتوي قائمة معايير فرعية، لكل منها:

- `name` — اسم المعيار الفرعي.
- `score` — درجة من 0 إلى 100 مدعومة بدليل في الكود أو الوثائق.
- `weight` — وزن نسبي؛ مجموع الأوزان داخل الطبقة يساوي 1.0.

درجة الطبقة هي المتوسط المُرجَّح: `overall_score = Σ(score × weight)`. الأوزان تعكس المخاطر: عزل المستأجر وحدود الأدوات والموافقة على الأفعال الخارجية تأخذ أوزاناً أعلى من العناصر التجميلية.

درجة المنصة هي المتوسط البسيط لدرجات الطبقات 1–12. الطبقة الثالثة عشرة لا تُحتسب في متوسط المنصة لأنها الراصد لا المرصود.

## كيف تؤثر الاختبارات العابرة للطبقات في الدرجة

الاختبارات العابرة للطبقات (في `readiness/cross_layer/`) تختبر سلوكاً يمتد عبر طبقتين أو أكثر — مثل: هل يستخدم الوكيل ذاكرة المستأجر الصحيح فقط. هذه الاختبارات تطبّق سقفاً، لا تطبّق إضافة:

- اختبار عابر فاشل يضع سقفاً على كل طبقة مشاركة عند نطاق "تجربة عميل" (84 كحد أقصى)، مهما بلغت درجاتها الفرعية.
- اختبار عابر مُحدَّد لكنه لم يُنفَّذ على وتيرة دورية متحقَّقة يمنع المنصة من تجاوز نطاق "تجربة عميل".
- لا يرفع أي اختبار عابر درجة طبقة فوق ما تستحقه معاييرها الفرعية.

هذا هو سبب توقّف منصة دياليكس عند 77 (تجربة عميل): المعايير الفرعية قوية، لكن التمارين المتحقَّقة الدورية لا تزال ناقصة.

## ما لا يفعله هذا النظام

- لا يحوّل وثيقة إلى دليل. الوثيقة تصف، والاختبار المُنفَّذ يثبت.
- لا يسجّل أرقاماً مضمونة. كل مقياس له مصدر وحد نجاح.
- لا يستبدل الكود. الكود هو مصدر الحقيقة عند أي تعارض.

## روابط ذات صلة

- `readiness/enterprise_readiness_model.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`
- `readiness/cross_layer/`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Purpose

This document explains the scoring system used by Layer 13. The system is a measurement tool, not a marketing tool. A layer's score describes the evidence on hand; it is not a promise of performance. Any score without verifiable evidence is treated as zero in its sub-criterion.

## The five bands

Every item — a sub-criterion, a layer, or the platform as a whole — is classified on a five-band scale:

| Band | Score | Meaning |
|---|---|---|
| prototype | 0–59 | The idea exists, but there is not enough evidence of behavior. |
| internal beta | 60–74 | Works internally, but lacks documented periodic verification. |
| client pilot | 75–84 | Ready for a supervised, monitored run with a single client. |
| enterprise-ready | 85–94 | Verified drills on a periodic cadence and full observability coverage. |
| mission-critical | 95+ | Broad operation under proven operational guarantees. |

## How sub-criteria are weighted

Each layer has a `scorecard.yaml` file holding a list of sub-criteria, each with:

- `name` — the name of the sub-criterion.
- `score` — a 0 to 100 score backed by evidence in code or documentation.
- `weight` — a relative weight; weights within a layer sum to 1.0.

The layer score is the weighted mean: `overall_score = Σ(score × weight)`. Weights reflect risk: tenant isolation, tool boundaries, and approval for external actions carry higher weight than cosmetic items.

The platform score is the simple mean of Layer 1–12 scores. Layer 13 is excluded from the platform mean because it is the observer, not the observed.

## How cross-layer tests affect the score

Cross-layer tests (under `readiness/cross_layer/`) exercise behavior that spans two or more layers — for example, whether an agent uses only the correct tenant's memory. These tests apply a cap, not a bonus:

- A failing cross-layer test caps every participating layer at the client-pilot band (84 maximum), regardless of its sub-criteria scores.
- A cross-layer test that is specified but not executed on a verified periodic cadence prevents the platform from exceeding the client-pilot band.
- No cross-layer test raises a layer above what its sub-criteria earn.

This is why the Dealix platform stops at 77 (client pilot): the sub-criteria are strong, but periodic verified drills are still missing.

## What this system does not do

- It does not turn a document into evidence. A document describes; an executed test proves.
- It does not record guaranteed numbers. Every metric has a source and a pass threshold.
- It does not replace code. Code is the source of truth in any conflict.

## Related links

- `readiness/enterprise_readiness_model.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`
- `readiness/cross_layer/`

Estimated value is not Verified value.
