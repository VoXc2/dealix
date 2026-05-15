# العربية

**Owner:** مهندس الموثوقية (Reliability Engineer).

## الغرض

التعويض (compensation) هو الإجراء الذي يعكس أثر خطوة مكتملة عندما يفشل سير العمل لاحقاً. هذا يضمن أن التشغيل الفاشل لا يترك حالة جزئية غير متّسقة.

## متى يُطبَّق التعويض

عندما تكتمل خطوة لها أثر جانبي ثم تفشل خطوة لاحقة فشلاً دائماً لا يقبل المسار البديل، ينتقل التشغيل إلى حالة `compensating`. يشغّل المحرّك خطوات التعويض بترتيب عكسي للخطوات المكتملة.

## نمط التعويض

كل خطوة ذات أثر جانبي يجوز أن تعلن خطوة تعويض مقابلة في تعريف YAML عبر مفتاح `compensation`. أمثلة:

| خطوة أصلية | خطوة التعويض |
|---|---|
| إنشاء سجل CRM | وسم السجل بـ `voided` مع سبب |
| حجز موعد مبدئي | إلغاء الحجز وإشعار المالك |
| إنشاء تذكرة دعم | إغلاق التذكرة بحالة `superseded` |
| تخصيص بند عمل | إعادة البند إلى الطابور |

## الخطوات غير القابلة للتعويض

التواصل الخارجي بعد الموافقة لا يمكن "إلغاء إرساله". لذلك تُوضع خطوة الإرسال الخارجي دائماً كآخر خطوة ذات أثر، وبعد كل الخطوات الداخلية القابلة للفشل. هذا يقلّص الحاجة إلى تعويض غير ممكن.

## التعويض والتدقيق

كل خطوة تعويض تنتج أثراً في السجل بنفس معرّف التشغيل، موسومة `compensation=true`. هذا يجعل أي تراجع مرئياً بالكامل في سجلات سير العمل.

## العلاقة بطابور الرسائل الميتة

إذا فشلت خطوة التعويض نفسها، يُدفع التشغيل إلى DLQ مع وسم `compensation_failed` ويُخلق بند عمل بأولوية عالية لمراجعة بشرية فورية.

انظر أيضاً: `platform/workflow_engine/retries.md`، `platform/workflow_engine/observability.md`.

---

# English

**Owner:** Reliability Engineer.

## Purpose

Compensation is the action that reverses the effect of a completed step when the workflow later fails. It ensures a failed run does not leave inconsistent partial state.

## When compensation applies

When a step with a side effect completes and a later step then fails permanently with no acceptable fallback, the run moves to state `compensating`. The engine runs compensation steps in reverse order of the completed steps.

## Compensation pattern

Each side-effecting step may declare a matching compensation step in the YAML definition via the `compensation` key. Examples:

| Original step | Compensation step |
|---|---|
| Create CRM record | Mark the record `voided` with a reason |
| Hold a tentative meeting slot | Cancel the hold and notify the owner |
| Create a support ticket | Close the ticket with state `superseded` |
| Assign a work item | Return the item to the queue |

## Non-compensable steps

External communication after approval cannot be "un-sent". For this reason the external send step is always placed as the last side-effecting step, after all internal fallible steps. This minimizes the need for impossible compensation.

## Compensation and audit

Every compensation step emits a log trace under the same run id, tagged `compensation=true`. This makes any rollback fully visible in the workflow logs.

## Relation to the dead-letter queue

If a compensation step itself fails, the run is pushed to the DLQ tagged `compensation_failed` and a high-priority work item is created for immediate human review.

See also: `platform/workflow_engine/retries.md`, `platform/workflow_engine/observability.md`.
