# العربية

# اختبارات — طبقة الذكاء التنفيذي (الطبقة التاسعة)

> مواصفة حالات الاختبار ومعايير القبول لطبقة الذكاء التنفيذي. هذه مواصفة، لا كود.

## 1. النطاق

تغطي هذه المواصفة: محرّك الموجزات، لوحة عائد الاستثمار، تقارير المخاطر، محرّك التوقّعات، العرض الآمن للعميل، والحوكمة.

## 2. حالات اختبار محرّك الموجزات

| # | الحالة | معيار القبول |
|---|---|---|
| BRF-1 | حلول نافذة التوليد الأسبوعي | يُولَّد الموجز آلياً وتُسجَّل بداية ونهاية التوليد. |
| BRF-2 | بند موجز بلا مصدر بيانات | يُرفض البند ولا يظهر في الموجز. |
| BRF-3 | الموجز يحوي رقماً تقديرياً | يظهر الرقم موسوماً "تقديري" مع مدى الثقة. |
| BRF-4 | موجز موجَّه للعميل | يمرّ عبر `customer_safe_renderer.py` وينتهي بإفصاح القيمة التقديرية. |
| BRF-5 | فشل مصدر بيانات أثناء التوليد | يُكمل الموجز ببقية المصادر ويُوسَم القسم الناقص "بيانات غير متاحة". |

## 3. حالات اختبار لوحة عائد الاستثمار

| # | الحالة | معيار القبول |
|---|---|---|
| ROI-1 | خدمة مفعَّلة | تظهر لها قصة عائد بساعات موفَّرة مرصودة ونافذة قياس. |
| ROI-2 | خدمة بلا بيانات قيمة | تُعرض الحالة "لا توجد بيانات كافية بعد"، لا رقم مفبرك. |
| ROI-3 | عرض الفرص | يُستخدَم مصطلح "فرص مُثبتة بأدلة"، لا "مبيعات مضمونة". |
| ROI-4 | كل بند عائد | مرتبط بحدث من `value_ledger` قابل للتتبّع. |

## 4. حالات اختبار تقارير المخاطر

| # | الحالة | معيار القبول |
|---|---|---|
| RSK-1 | خطر مفتوح | يحمل مالكاً ودرجة احتمالية ودرجة أثر وإجراءً مقترحاً. |
| RSK-2 | خطر عالي الأثر بلا مالك خلال 24 ساعة | يُطلَق تنبيه. |
| RSK-3 | درجة أثر معروضة | موسومة "تقديري" صراحةً. |
| RSK-4 | تقرير مخاطر موجَّه للعميل | لا يحوي أي بيانات تعريف شخصية ويمرّ عبر العارض الآمن. |

## 5. حالات اختبار التوقّعات

| # | الحالة | معيار القبول |
|---|---|---|
| FCT-1 | أي توقّع منتَج | يُعرض كمدى (حدّ أدنى وأعلى) مع مدى ثقة معلن. |
| FCT-2 | توقّع بنافذة بيانات قصيرة جداً | يُوسَم "ثقة منخفضة". |
| FCT-3 | لغة التوقّع | لا تحوي "مضمون" أو "سنحقّق"؛ تستخدم "الاتجاه المرصود يشير إلى". |
| FCT-4 | كل توقّع | يذكر نافذة البيانات وأفق الإسقاط. |

## 6. حالات اختبار الحوكمة والعرض الآمن

| # | الحالة | معيار القبول |
|---|---|---|
| GOV-1 | تقرير موجَّه للعميل بلا موافقة بشرية | يُحجَب الإرسال حتى الموافقة الموثَّقة. |
| GOV-2 | تقرير قطاع | يعرض المنهجية والأنماط المجمَّعة فقط، بلا مقاييس سرّية. |
| GOV-3 | أي تقرير موجَّه للعميل | يُسجَّل قيد تدقيق عبر `dealix/trust/audit.py`. |
| GOV-4 | محتوى يصف تواصلاً خارجياً نيابة عن العميل | يُرفض ما لم تكن هناك موافقة صريحة. |

## 7. معايير القبول الشاملة

- صفر أرقام مفبركة في كل التقارير الصادرة.
- 100% من بنود التقارير مرتبطة بمصدر بيانات معلن.
- 100% من التقارير الموجَّهة للعميل تمرّ عبر العارض الآمن وتنتهي بالإفصاح.
- 100% من التوقّعات معروضة كمدى مع مدى ثقة.
- صفر بنود تَعِد بنتيجة مضمونة.

روابط: `readiness.md` · `scorecard.yaml` · `architecture.md`

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

# Tests — Executive Intelligence Layer (Layer 9)

> A specification of test cases and acceptance criteria for the Executive Intelligence layer. This is a spec, not code.

## 1. Scope

This spec covers: the Briefing Engine, the ROI Dashboard, Risk Reporting, the Forecasting engine, customer-safe rendering, and governance.

## 2. Briefing Engine test cases

| # | Case | Acceptance criterion |
|---|---|---|
| BRF-1 | The weekly generation window arrives | The brief is generated automatically and the generation start and end are logged. |
| BRF-2 | A brief item without a data source | The item is rejected and does not appear in the brief. |
| BRF-3 | The brief contains an estimated number | The number appears labelled "estimated" with a confidence range. |
| BRF-4 | A customer-facing brief | It passes `customer_safe_renderer.py` and ends with the estimated-value disclosure. |
| BRF-5 | A data source fails during generation | The brief completes with the remaining sources and the missing section is labelled "data unavailable". |

## 3. ROI Dashboard test cases

| # | Case | Acceptance criterion |
|---|---|---|
| ROI-1 | An activated service | Shows an ROI story with observed hours saved and a measurement window. |
| ROI-2 | A service with no value data | The status "not enough data yet" is shown, not a fabricated number. |
| ROI-3 | Opportunity display | The term "evidenced opportunities" is used, not "guaranteed sales". |
| ROI-4 | Every ROI item | Is tied to a traceable event from `value_ledger`. |

## 4. Risk Reporting test cases

| # | Case | Acceptance criterion |
|---|---|---|
| RSK-1 | An open risk | Carries an owner, a likelihood score, an impact score, and a suggested action. |
| RSK-2 | A high-impact risk without an owner for 24 hours | An alert is raised. |
| RSK-3 | A displayed impact score | Is labelled "estimated" explicitly. |
| RSK-4 | A customer-facing risk report | Contains no PII and passes the customer-safe renderer. |

## 5. Forecasting test cases

| # | Case | Acceptance criterion |
|---|---|---|
| FCT-1 | Any produced forecast | Is shown as a range (lower and upper bound) with a stated confidence band. |
| FCT-2 | A forecast with a very short data window | Is labelled "low confidence". |
| FCT-3 | Forecast language | Contains no "guaranteed" or "we will achieve"; uses "the observed trend points to". |
| FCT-4 | Every forecast | States its data window and projection horizon. |

## 6. Governance and customer-safe rendering test cases

| # | Case | Acceptance criterion |
|---|---|---|
| GOV-1 | A customer-facing report without human approval | Sending is blocked until a documented approval. |
| GOV-2 | A sector report | Presents methodology and aggregated patterns only, with no confidential metrics. |
| GOV-3 | Any customer-facing report | An audit entry is recorded via `dealix/trust/audit.py`. |
| GOV-4 | Content describing external communication on the customer's behalf | Rejected unless an explicit consent exists. |

## 7. Overall acceptance criteria

- Zero fabricated numbers across all issued reports.
- 100% of report items tied to a declared data source.
- 100% of customer-facing reports pass the customer-safe renderer and end with the disclosure.
- 100% of forecasts shown as a range with a confidence band.
- Zero items promising a guaranteed outcome.

Links: `readiness.md` · `scorecard.yaml` · `architecture.md`

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
