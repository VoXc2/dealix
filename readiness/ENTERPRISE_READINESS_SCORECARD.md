# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## الغرض

هذه البطاقة المُجمَّعة لجاهزية منصة دياليكس عبر الطبقات الثلاث عشرة. الدرجات أدناه مأخوذة مباشرة من ملفات `scorecard.yaml` لكل طبقة، وليست تقديرات يدوية. درجة المنصة هي المتوسط البسيط للطبقات 1–12.

## درجات الطبقات والنطاقات

| الطبقة | الاسم | الدرجة | النطاق |
|---|---|---|---|
| 1 | الأساس | 78 | تجربة عميل |
| 2 | زمن تشغيل الوكيل | 75 | تجربة عميل |
| 3 | محرك سير العمل | 79 | تجربة عميل |
| 4 | الذاكرة والمعرفة | 79 | تجربة عميل |
| 5 | الحوكمة | 79 | تجربة عميل |
| 6 | التنفيذ والتكاملات | 79 | تجربة عميل |
| 7 | المراقبة | 75 | تجربة عميل |
| 8 | التقييم | 78 | تجربة عميل |
| 9 | الذكاء التنفيذي | 71 | تجربة داخلية |
| 10 | تسليم العميل | 78 | تجربة عميل |
| 11 | التحول | 70 | تجربة داخلية |
| 12 | التطور المستمر | 81 | تجربة عميل |
| 13 | الجاهزية والتحقق العابر للطبقات | 74 | تجربة داخلية |

### المعايير الفرعية للطبقة 1 (الأساس)

| المعيار الفرعي | الدرجة |
|---|---|
| الأساس | 78 |
| الهوية | 80 |
| تعدد المستأجرين | 76 |
| الأمن | 77 |
| النشر | 79 |

## الحكم على مستوى المنصة

- **درجة المنصة: 77 من 100.**
- **النطاق: تجربة عميل (client pilot).**
- **التفسير:** المنصة جاهزة لتشغيل مُراقَب مع عميل واحد تحت إشراف. ليست جاهزة للمؤسسات بعد، ولا حرجة للمهمة.

الطبقة الثالثة عشرة عند 74 (تجربة داخلية) لأنها طبقة وصفية أُنشئت حديثاً؛ اختباراتها العابرة للطبقات مُحدَّدة لكنها لم تُنفَّذ بعد على وتيرة متحقَّقة. درجة الطبقة 13 لا تُحتسب في متوسط المنصة.

## قائمة الفجوات المُرتَّبة حسب الأولوية للوصول إلى "جاهز للمؤسسات"

الفجوة المتكررة عبر الطبقات هي غياب التمارين الدورية الموثَّقة والمتحقَّقة، إضافة إلى مقارنة آلية بين الإصدارات. ترتيب المعالجة:

| # | الفجوة | الطبقات المتأثرة | معيار الإغلاق |
|---|---|---|---|
| 1 | تمرين استعادة من النسخ الاحتياطية | 1 | استعادة متحقَّقة موثَّقة كل ربع سنة، بزمن وسلامة بيانات مُسجَّلين. |
| 2 | تمرين حذف مستأجر | 1، 4 | حذف متحقَّق يثبت إزالة بيانات المستأجر من التخزين والفهارس. |
| 3 | تمرين تراجع وإعادة تشغيل قائمة الرسائل الميتة (DLQ) | 12، 2، 3، 5 | تراجع متحقَّق يستعيد الوكيل وسير العمل والموجِّه والسياسة معاً. |
| 4 | تمرين استجابة للحوادث | 7 | تمرين متحقَّق يثبت أن فشل تكامل يظهر في لوحة المراقبة وينبّه المالك. |
| 5 | تمرين تدوير المفاتيح والأسرار | 1 | تدوير متحقَّق بلا انقطاع خدمة، موثَّق بوتيرة دورية. |
| 6 | مقارنة آلية بين الإصدار 1 والإصدار 2 | 8، 12 | مقارنة آلية تمنع طرح إصدار يتراجع في التقييم. |
| 7 | تنفيذ الاختبارات العابرة للطبقات الستة على وتيرة متحقَّقة | 13 وكل الطبقات | الاختبارات الستة في `readiness/cross_layer/` تعمل في CI بسجل مُؤرَّخ. |

عند إغلاق هذه الفجوات بأدلة متحقَّقة، يُتوقَّع أن تنتقل المنصة إلى نطاق "جاهز للمؤسسات". هذا توقّع مشروط بالأدلة، لا وعد.

## روابط ذات صلة

- `readiness/enterprise_readiness_model.md`
- `readiness/scoring_system.md`
- `readiness/cross_layer/`
- `platform/README.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Purpose

This is the rolled-up readiness scorecard for the Dealix platform across all thirteen layers. The scores below are taken directly from each layer's `scorecard.yaml` files, not estimated by hand. The platform score is the simple mean of Layers 1–12.

## Layer scores and bands

| Layer | Name | Score | Band |
|---|---|---|---|
| 1 | Foundation | 78 | client pilot |
| 2 | Agent Runtime | 75 | client pilot |
| 3 | Workflow Engine | 79 | client pilot |
| 4 | Memory & Knowledge | 79 | client pilot |
| 5 | Governance | 79 | client pilot |
| 6 | Execution & Integrations | 79 | client pilot |
| 7 | Observability | 75 | client pilot |
| 8 | Evaluation | 78 | client pilot |
| 9 | Executive Intelligence | 71 | internal beta |
| 10 | Client Delivery | 78 | client pilot |
| 11 | Transformation | 70 | internal beta |
| 12 | Continuous Evolution | 81 | client pilot |
| 13 | Readiness & Cross-Layer Validation | 74 | internal beta |

### Layer 1 (Foundation) sub-criteria

| Sub-criterion | Score |
|---|---|
| Foundation | 78 |
| Identity | 80 |
| Multi-tenant | 76 |
| Security | 77 |
| Deployment | 79 |

## Platform-level verdict

- **Platform score: 77 out of 100.**
- **Band: client pilot.**
- **Interpretation:** the platform is ready for a supervised, monitored run with a single client. It is not yet enterprise-ready, and not mission-critical.

Layer 13 sits at 74 (internal beta) because it is a newly created meta-layer; its cross-layer tests are specified but have not yet been executed on a verified cadence. Layer 13's score is excluded from the platform mean.

## Prioritized gap list to reach enterprise-ready

The recurring gap across layers is the absence of periodic, documented, verified drills, plus automated version comparison. Order of work:

| # | Gap | Affected layers | Closure criterion |
|---|---|---|---|
| 1 | Backup restore drill | 1 | A verified restore documented quarterly, with recorded time and data integrity. |
| 2 | Tenant-deletion drill | 1, 4 | A verified deletion proving tenant data is removed from storage and indexes. |
| 3 | Rollback / DLQ-replay drill | 12, 2, 3, 5 | A verified rollback that restores agent, workflow, prompt, and policy together. |
| 4 | Incident-response drill | 7 | A verified drill proving an integration failure surfaces on the dashboard and alerts the owner. |
| 5 | Key / secret rotation drill | 1 | A verified rotation with no service outage, documented on a periodic cadence. |
| 6 | Automated v1/v2 comparison | 8, 12 | An automated comparison that blocks rollout of a version that regresses on evals. |
| 7 | Run the six cross-layer tests on a verified cadence | 13 and all layers | The six tests in `readiness/cross_layer/` run in CI with a dated log. |

When these gaps are closed with verified evidence, the platform is expected to move into the enterprise-ready band. This is an evidence-conditional expectation, not a promise.

## Related links

- `readiness/enterprise_readiness_model.md`
- `readiness/scoring_system.md`
- `readiness/cross_layer/`
- `platform/README.md`

Estimated value is not Verified value.
