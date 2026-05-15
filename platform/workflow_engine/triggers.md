# العربية

**Owner:** مهندس وقت تشغيل سير العمل (Workflow Runtime Engineer).

## الغرض

يحدّد هذا المستند كيف يبدأ سير العمل. المحفّز هو الحدث الذي يخلق تشغيلاً جديداً. كل سير عمل له محفّز واحد معلن في مفتاح `trigger` ضمن ملف التعريف.

## أنواع المحفّزات

- **محفّز حدثي (Event trigger):** حدث وارد من نظام مصدر — مثل `new_inbound_lead` أو `new_support_ticket`. يصل عادةً عبر webhook ويُسجَّل في `dealix/reliability/idempotency.py` لمنع التكرار.
- **محفّز مجدول (Schedule trigger):** وقت معلن — مثل `weekly_monday_08_00` للتقرير الأسبوعي. لا يعتمد على حدث خارجي.
- **محفّز يدوي (Manual trigger):** يبدأه دور بشري عبر طلب صريح — مثل `manual_escalation_request`.
- **محفّز متسلسل (Chained trigger):** اكتمال سير عمل آخر يحفّز التالي — مثل `lead_qualification` يحفّز `follow_up`.

## الشروط

المحفّز قد يحمل شروط دخول تُقيَّم قبل بدء الخطوات. إن لم تتحقق الشروط يُغلق التشغيل بحالة `skipped` مع أثر في السجل. أمثلة:

- شرط ملكية: العميل المحتمل ضمن نطاق ICP المعتمد.
- شرط قنوات: القناة مسموحة في سياسة المستأجر.
- شرط موافقة: DPA موقَّع قبل أي خطوة تواصل.

## قواعد الحوكمة على المحفّزات

- لا محفّز يبدأ تواصلاً خارجياً تلقائياً؛ المحفّز يبدأ مسار مسوّدة فقط.
- لا محفّز يعتمد على بيانات مكتسبة عبر كشط (scraping) أو أتمتة LinkedIn.
- كل محفّز حدثي يمر بفحص منع التكرار قبل خلق تشغيل.
- المحفّز المجدول يُسجَّل مع المنطقة الزمنية الصريحة لتفادي الالتباس.

انظر أيضاً: `platform/workflow_engine/workflow_runtime.md`، `platform/workflow_engine/actions.md`.

---

# English

**Owner:** Workflow Runtime Engineer.

## Purpose

This document defines how a workflow starts. A trigger is the event that creates a new run. Every workflow has exactly one declared trigger in the `trigger` key of its definition file.

## Trigger types

- **Event trigger:** an inbound event from a source system — for example `new_inbound_lead` or `new_support_ticket`. It typically arrives via webhook and is recorded in `dealix/reliability/idempotency.py` to prevent duplication.
- **Schedule trigger:** a declared time — for example `weekly_monday_08_00` for the weekly report. It does not depend on an external event.
- **Manual trigger:** started by a human role through an explicit request — for example `manual_escalation_request`.
- **Chained trigger:** the completion of one workflow triggers the next — for example `lead_qualification` triggers `follow_up`.

## Conditions

A trigger may carry entry conditions evaluated before steps start. If conditions are not met the run closes with state `skipped` and a log trace. Examples:

- Ownership condition: the lead is within the approved ICP scope.
- Channel condition: the channel is allowed in the tenant policy.
- Consent condition: the DPA is signed before any outreach step.

## Governance rules on triggers

- No trigger starts external communication automatically; a trigger starts a draft path only.
- No trigger depends on data acquired through scraping or LinkedIn automation.
- Every event trigger passes a deduplication check before a run is created.
- A schedule trigger is recorded with an explicit time zone to avoid ambiguity.

See also: `platform/workflow_engine/workflow_runtime.md`, `platform/workflow_engine/actions.md`.
