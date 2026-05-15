# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead).

## الغرض

مواصفة اختبار للطبقة 2 — وقت تشغيل الوكلاء. كل حالة لها معيار قبول واضح. لا تحتوي هذه الوثيقة على شيفرة؛ هي مرجع للمُختبِر.

## حالات اختبار التعريف والسجل

### TC-AR-01 — وكيل بلا تعريف مرفوض
- **الخطوات:** محاولة تحميل وكيل لا يملك `agents/<name>/agent.yaml`.
- **معيار القبول:** التحميل يفشل؛ يُكتب حدث رفض في الأثر؛ الوكيل لا يدخل `running`.

### TC-AR-02 — تحقق بطاقة الوكيل
- **الخطوات:** تمرير `AgentCard` بحقل `owner` فارغ.
- **معيار القبول:** `agent_card_valid(...)` تُرجع `False`؛ التسجيل مرفوض.

### TC-AR-03 — كل الوكلاء الخمسة مسجّلون
- **الخطوات:** فحص سجل الوكلاء.
- **معيار القبول:** `sales_agent`, `support_agent`, `ops_agent`, `executive_agent`, `governance_agent` كلها موجودة بـ `owner` و`risk_level`.

## حالات اختبار الأدوات والصلاحيات

### TC-AR-04 — أداة إرسال خارجي ليست في allowed_tools
- **الخطوات:** فحص كل `agent.yaml`.
- **معيار القبول:** `send_email_live` و`send_whatsapp_live` لا تظهر أبداً في `allowed_tools`؛ تظهر فقط في `requires_approval_for`.

### TC-AR-05 — أداة ممنوعة مرفوضة
- **الخطوات:** طلب وكيل استدعاء `scrape_web` أو `linkedin_automation`.
- **معيار القبول:** الاستدعاء مرفوض عند حدود الأدوات؛ تنبيه؛ لا تنفيذ.

### TC-AR-06 — أداة requires_approval تنتظر الموافقة
- **الخطوات:** وكيل يستدعي `send_email_live`.
- **معيار القبول:** يُنشأ طلب موافقة بمهلة؛ الإرسال لا يحدث قبل موافقة موثَّقة.

## حالات اختبار التصعيد

### TC-AR-07 — انتهاء مهلة الموافقة = رفض
- **الخطوات:** ترك طلب موافقة دون رد حتى انتهاء المهلة.
- **معيار القبول:** الإجراء لا يُنفَّذ؛ يُكتب `escalation.expired`.

### TC-AR-08 — الإجراء الممنوع يُرفض لا يُصعَّد
- **الخطوات:** طلب يلامس `forbidden_actions`.
- **معيار القبول:** رفض فوري عند البوّابة؛ لا يُنشأ طلب موافقة.

## حالات اختبار دورة الحياة والإيقاف

### TC-AR-09 — الإيقاف الفوري
- **الخطوات:** استدعاء `activate_kill_switch()` أثناء تشغيل وكيل.
- **معيار القبول:** ترفض الاستدعاءات الجديدة خلال أقل من ثانية؛ تُلغى الاستدعاءات المعلّقة؛ يُكتب `agent.stopped`.

### TC-AR-10 — انتقال حالة غير مسموح مرفوض
- **الخطوات:** محاولة `defined → running` مباشرة.
- **معيار القبول:** `can_transition(...)` تُرجع `False`؛ الانتقال مرفوض.

## حالات اختبار الذاكرة والإصدارات

### TC-AR-11 — عزل نطاق الذاكرة
- **الخطوات:** وكيل يحاول قراءة `customer_memory` لمستأجر آخر.
- **معيار القبول:** القراءة مرفوضة؛ يُكتب `memory.scope_violation`.

### TC-AR-12 — مقارنة v1 مقابل v2
- **الخطوات:** تشغيل تقييم مقارن قبل ترقية الحلقة.
- **معيار القبول:** الترقية مرفوضة إن انخفض أي مؤشر جودة.

### TC-AR-13 — تغطية الأثر
- **الخطوات:** تشغيل قرار مهم لكل وكيل.
- **معيار القبول:** يوجد أثر قابل للتدقيق مع `agent_name` و`agent_version` و`approval_status`.

## معايير القبول الشاملة

- كل الحالات أعلاه تمر قبل ترقية أي وكيل إلى الحلقة العامة.
- صفر إجراء خارجي منفَّذ بلا موافقة.
- صفر استدعاء أداة ممنوعة منفَّذ.

---

# English

**Owner:** Agent Runtime Platform Lead.

## Purpose

A test specification for Layer 2 — Agent Runtime. Each case has a clear acceptance criterion. This document contains no code; it is a reference for the tester.

## Definition and registry test cases

### TC-AR-01 — Agent with no definition rejected
- **Steps:** Attempt to load an agent with no `agents/<name>/agent.yaml`.
- **Acceptance:** The load fails; a rejection event is written to the trace; the agent does not enter `running`.

### TC-AR-02 — Agent card validation
- **Steps:** Pass an `AgentCard` with an empty `owner` field.
- **Acceptance:** `agent_card_valid(...)` returns `False`; registration is rejected.

### TC-AR-03 — All five agents registered
- **Steps:** Inspect the Agent Registry.
- **Acceptance:** `sales_agent`, `support_agent`, `ops_agent`, `executive_agent`, `governance_agent` are all present with an `owner` and a `risk_level`.

## Tools and permissions test cases

### TC-AR-04 — External-send tool not in allowed_tools
- **Steps:** Inspect every `agent.yaml`.
- **Acceptance:** `send_email_live` and `send_whatsapp_live` never appear in `allowed_tools`; they appear only in `requires_approval_for`.

### TC-AR-05 — Forbidden tool rejected
- **Steps:** An agent requests `scrape_web` or `linkedin_automation`.
- **Acceptance:** The call is rejected at the tool boundary; an alert fires; no execution.

### TC-AR-06 — requires_approval tool waits for approval
- **Steps:** An agent calls `send_email_live`.
- **Acceptance:** An approval request with a TTL is created; the send does not happen before a documented approval.

## Escalation test cases

### TC-AR-07 — Expired approval TTL means denial
- **Steps:** Leave an approval request unanswered until the TTL expires.
- **Acceptance:** The action is not executed; `escalation.expired` is written.

### TC-AR-08 — Forbidden action rejected, not escalated
- **Steps:** A request matching `forbidden_actions`.
- **Acceptance:** Immediate rejection at the gateway; no approval request is created.

## Lifecycle and stop test cases

### TC-AR-09 — Instant stop
- **Steps:** Call `activate_kill_switch()` while an agent is running.
- **Acceptance:** New calls are rejected within under one second; pending calls are cancelled; `agent.stopped` is written.

### TC-AR-10 — Illegal state transition rejected
- **Steps:** Attempt `defined → running` directly.
- **Acceptance:** `can_transition(...)` returns `False`; the transition is rejected.

## Memory and versioning test cases

### TC-AR-11 — Memory scope isolation
- **Steps:** An agent attempts to read another tenant's `customer_memory`.
- **Acceptance:** The read is rejected; `memory.scope_violation` is written.

### TC-AR-12 — v1 vs v2 comparison
- **Steps:** Run a comparative evaluation before a ring promotion.
- **Acceptance:** The promotion is rejected if any quality indicator drops.

### TC-AR-13 — Trace coverage
- **Steps:** Run an important decision for each agent.
- **Acceptance:** An auditable trace exists with `agent_name`, `agent_version`, and `approval_status`.

## Overall acceptance criteria

- All cases above pass before any agent is promoted to the general ring.
- Zero external actions executed without approval.
- Zero forbidden tool calls executed.
