# العربية

# تحقيق القيمة — الطبقة ١١

**المالك:** قائد التحويل في Dealix بالاشتراك مع راعي العميل التنفيذي.

## الغرض

تحقيق القيمة هو الجواب على السؤال الذي يطرحه كل راعٍ تنفيذي: «ماذا حصلنا مقابل ما أنفقنا؟» لا يكتمل أي تحويل عند نشر سير العمل؛ يكتمل عند تسجيل القيمة وعرضها بشكل قابل للتدقيق. هذا الملف يصف كيف تتحوّل فرضية العائد إلى قيمة موثّقة.

## أربع طبقات للقيمة

تُصنَّف كل قيمة عبر `auto_client_acquisition/value_os/value_ledger.py`:

| الطبقة | التعريف | المصدر |
|---|---|---|
| مُقدَّرة | فرضية عائد قبل التنفيذ | حالة استخدام في الخريطة |
| مُلاحَظة | مقياس مُسجَّل أثناء التشغيل | سجل القيمة |
| مُتحقَّقة | مقياس راجعه قائد التحويل | مراجعة شهرية |
| مؤكَّدة من العميل | الراعي وقّع على الرقم | تقرير القيمة الشهري |

## دورة تحقيق القيمة

١. **فرضية العائد:** تُكتب كل حالة استخدام كفرضية في خريطة التحويل.
٢. **التسجيل:** كل سير عمل مُعاد تصميمه يكتب أحداثه في سجل القيمة.
٣. **التلخيص الشهري:** يُنتَج تقرير القيمة عبر `auto_client_acquisition/value_os/monthly_report.py`.
٤. **التأكيد التنفيذي:** يراجع الراعي التقرير ويوقّع على الأرقام المؤكَّدة.

## بناء حالة العمل

كل عميل يحصل على حالة عمل: قائمة حالات الاستخدام، فرضية العائد لكل منها، تكلفة كل مرحلة، والقيمة المُلاحَظة حتى الآن. حالة العمل تُحدَّث شهرياً، فلا تبقى وعداً ثابتاً بل سجلّاً حياً.

## ربط القيمة بمسار البيع

- **التدقيق:** قيمة مُقدَّرة فقط — فرضيات في خريطة التحويل.
- **التجربة:** أول قيمة مُلاحَظة من حالة استخدام واحدة.
- **التحويل:** قيمة مُتحقَّقة عبر سير عمل متعدد.
- **العقد الدوري:** تقرير قيمة شهري مؤكَّد من العميل.

## القاعدة غير القابلة للتفاوض

القيمة المُقدَّرة فرضية، لا وعد. لا يُعرض رقم على أنه مُتحقَّق قبل مراجعته، ولا على أنه مؤكَّد قبل توقيع العميل. لا تُربط أي حالة استخدام بعائد مضمون.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# Value Realization — Layer 11

**Owner:** Dealix Transformation Lead, jointly with the client Executive Sponsor.

## Purpose

Value realization answers the question every executive sponsor asks: "What did we get for what we spent?" No transformation is complete when a workflow ships; it is complete when value is recorded and shown in an auditable form. This file describes how an ROI hypothesis becomes documented value.

## Four tiers of value

Every value entry is classified through `auto_client_acquisition/value_os/value_ledger.py`:

| Tier | Definition | Source |
|---|---|---|
| Estimated | ROI hypothesis before execution | Use case in the map |
| Observed | Metric recorded during operation | Value ledger |
| Verified | Metric reviewed by the Transformation Lead | Monthly review |
| Client-confirmed | Sponsor has signed off on the figure | Monthly value report |

## The value realization cycle

1. **ROI hypothesis:** Each use case is written as a hypothesis in the transformation map.
2. **Recording:** Every redesigned workflow writes its events into the value ledger.
3. **Monthly summary:** The value report is produced through `auto_client_acquisition/value_os/monthly_report.py`.
4. **Executive confirmation:** The sponsor reviews the report and signs off on confirmed figures.

## Building the business case

Every client receives a business case: the list of use cases, the ROI hypothesis for each, the cost of each phase, and the observed value so far. The business case is updated monthly, so it never stays a fixed promise but a living record.

## Mapping value to the sales path

- **Audit:** Estimated value only — hypotheses in the transformation map.
- **Pilot:** First observed value from a single use case.
- **Transformation:** Verified value across multiple workflows.
- **Retainer:** A monthly value report, client-confirmed.

## Non-negotiable

Estimated value is a hypothesis, not a promise. No figure is presented as verified before review, nor as confirmed before the client signs. No use case is tied to a guaranteed return.

Estimated value is not Verified value.
