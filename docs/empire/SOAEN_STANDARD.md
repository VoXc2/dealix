# The SOAEN Standard — معيار SOAEN

## English

SOAEN is the automation-readiness standard of Dealix. It names five elements
every workflow must have before it is fit for automation or sold as an AI
workflow. The five are: **Source, Owner, Approval, Evidence, Next Action.**

**Source / مصدر.** Where the work came from is named and recorded.
*Present:* a campaign name, a referral, an inbound channel — written down.
*Missing:* "a lead arrived" with no recorded origin. A source-less workflow
cannot be measured and cannot be repeated.

**Owner / مالك.** One named person is responsible for what happens next.
*Present:* a single name attached to the lead or task.
*Missing:* "the team" owns it, which means no one does. A lead with no owner
is not a pipeline.

**Approval / موافقة.** Every external action is approved by a human before it
is sent. *Present:* a reviewer signs off the message, scope, or AI output.
*Missing:* the action goes out automatically. An AI action with no approval is
risk, not operations.

**Evidence / دليل.** The result is logged: what was sent, what was replied,
what changed. *Present:* a record a reviewer can read later.
*Missing:* a follow-up that nobody can confirm happened. A follow-up with no
evidence is not operations.

**Next Action / خطوة تالية.** The workflow ends with a decision about what
happens next. *Present:* a named step with an owner and a date.
*Missing:* a dashboard that reports a number and stops. A dashboard with no
next action is a report only.

**The rule.** Any workflow missing even one of the five is **not fit for
automation** and **must not be sold as an AI workflow.** This is non-negotiable.
A four-out-of-five workflow is not "almost ready"; it is unready until the
fifth element is added. Automating an incomplete workflow does not save time —
it scales an ungoverned process and removes the human able to catch the error.

**The four tests.** SOAEN is checked with the four category sentences:
Lead with no owner = not a pipeline. AI action with no approval = risk.
Dashboard with no next action = a report only. Follow-up with no evidence =
not operations.

**Reviewer checklist.** Run this against any candidate workflow:

- Is the Source named and written down? Yes / No.
- Is there exactly one named Owner? Yes / No.
- Does every external action pass through human Approval? Yes / No.
- Is there an Evidence record a reviewer can read later? Yes / No.
- Does the workflow end with a defined Next Action? Yes / No.

Five "Yes" answers: the workflow is SOAEN-complete and may be automated or
sold as an AI workflow. Any "No": stop, name the gap, and close it first.

See [`DEALIX_METHOD.md`](DEALIX_METHOD.md), [`OFFER_LADDER.md`](OFFER_LADDER.md),
and [`../governance/FORBIDDEN_ACTIONS.md`](../governance/FORBIDDEN_ACTIONS.md).

## العربية

SOAEN هو معيار جاهزية الأتمتة في Dealix. يسمّي خمسة عناصر يجب أن يحملها كل
workflow قبل أن يصبح صالحًا للأتمتة أو يُباع كـAI workflow. الخمسة هي:
**مصدر، مالك، موافقة، دليل، خطوة تالية.**

**مصدر / Source.** من أين أتى العمل، يُسمّى ويُسجّل.
*موجود:* اسم حملة، أو إحالة، أو قناة واردة — مكتوبة.
*غائب:* «وصل ليد» دون أصل مسجّل. الـworkflow بلا مصدر لا يُقاس ولا يتكرّر.

**مالك / Owner.** شخص واحد مُسمّى مسؤول عمّا يحدث تاليًا.
*موجود:* اسم واحد مرتبط بالليد أو المهمة.
*غائب:* «الفريق» يملكه، وهذا يعني لا أحد. الليد بلا مالك ليس pipeline.

**موافقة / Approval.** كل إجراء خارجي يعتمده إنسان قبل إرساله.
*موجود:* مراجِع يعتمد الرسالة أو النطاق أو مخرج الـAI.
*غائب:* يخرج الإجراء تلقائيًا. إجراء AI بلا موافقة خطر، لا تشغيل.

**دليل / Evidence.** تُسجّل النتيجة: ما أُرسل، وما الردّ، وما تغيّر.
*موجود:* سجلّ يستطيع المراجِع قراءته لاحقًا.
*غائب:* متابعة لا يستطيع أحد تأكيد حدوثها. متابعة بلا دليل ليست تشغيلًا.

**خطوة تالية / Next Action.** ينتهي الـworkflow بقرار عمّا يحدث تاليًا.
*موجود:* خطوة مُسمّاة لها مالك وتاريخ.
*غائب:* لوحة تعرض رقمًا وتتوقف. لوحة بلا خطوة تالية تقرير فقط.

**القاعدة.** أي workflow ينقصه ولو عنصر واحد من الخمسة **غير صالح للأتمتة**
و**يجب ألّا يُباع كـAI workflow.** هذا غير قابل للتفاوض. الـworkflow بأربعة من
خمسة ليس «شبه جاهز»؛ هو غير جاهز حتى يُضاف العنصر الخامس. أتمتة workflow ناقص
لا توفّر وقتًا — بل تُوسّع عملية بلا حوكمة وتزيل الإنسان القادر على ضبط الخطأ.

**الاختبارات الأربعة.** يُفحص SOAEN بجمل الفئة الأربع:
ليد بلا مالك ليس pipeline. إجراء AI بلا موافقة = خطر. لوحة بلا خطوة تالية =
تقرير فقط. متابعة بلا دليل ليست تشغيلًا.

**قائمة فحص المراجِع.** طبّقها على أي workflow مرشّح:

- هل المصدر مُسمّى ومكتوب؟ نعم / لا.
- هل يوجد مالك واحد مُسمّى بالضبط؟ نعم / لا.
- هل يمرّ كل إجراء خارجي عبر موافقة بشرية؟ نعم / لا.
- هل يوجد سجلّ دليل يستطيع المراجِع قراءته لاحقًا؟ نعم / لا.
- هل ينتهي الـworkflow بخطوة تالية محدّدة؟ نعم / لا.

خمس إجابات «نعم»: الـworkflow مكتمل وفق SOAEN ويجوز أتمتته أو بيعه كـAI
workflow. أي «لا»: توقّف، سمِّ الفجوة، وأغلقها أولًا.

انظر [`DEALIX_METHOD.md`](DEALIX_METHOD.md) و[`OFFER_LADDER.md`](OFFER_LADDER.md)
و[`../governance/FORBIDDEN_ACTIONS.md`](../governance/FORBIDDEN_ACTIONS.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
