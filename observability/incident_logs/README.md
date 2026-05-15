# العربية

## سجلات الحوادث — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

هذا المجلد يحفظ سجل كل حادث تشغيلي. القاعدة: كل حادث له مسؤول واحد وحالة واضحة، ولا يُغلق دون سبب جذري وإجراءات تصحيحية. السجلات ملحَقة فقط — لا تُعدَّل بعد الإغلاق، بل تُضاف تحديثات.

### تسمية الملفات

`incident_YYYY-MM-DD_NNN.md` حيث `NNN` رقم تسلسلي داخل اليوم. مثال: `incident_2026-05-20_001.md`.

### قالب سجل الحادث

كل سجل حادث يحمل الحقول التالية:

- **المعرّف:** معرّف فريد للحادث.
- **التاريخ والوقت:** وقت الرصد بـ UTC.
- **درجة الخطورة:** SEV-1 / SEV-2 / SEV-3.
- **المسؤول:** اسم دور واحد مسؤول عن الحادث.
- **الحالة:** `open` / `mitigated` / `resolved`.
- **الأثر:** ما الخدمة أو سير العمل المتأثر ومدى الأثر.
- **`trace_id` المرتبط:** للتتبّع من طرف لطرف.
- **الجدول الزمني:** خطوات الرصد والاحتواء والإصلاح بأوقاتها.
- **السبب الجذري:** السبب المكتوب بعد التحقيق.
- **الإجراءات التصحيحية:** خطوات وقائية مع مسؤول لكل خطوة.

### قواعد

- لا يحتوي أي سجل حادث على PII؛ يُشار إلى `request_id` و `trace_id` و `tenant_id` فقط.
- كل حادث SEV-1 يتطلب مراجعة لاحقة بلا لوم موثَّقة.
- لا يُغلق حادث (`resolved`) دون سبب جذري وإجراءات تصحيحية.
- ملف `.gitkeep` يُبقي المجلد ضمن التحكّم بالإصدارات قبل تسجيل أول حادث.

### مستندات ذات صلة

- [`../../platform/observability/incident_response.md`](../../platform/observability/incident_response.md)
- [`../../platform/observability/alerts.md`](../../platform/observability/alerts.md)

# English

## Incident Logs — Layer 7

Owner: Platform Reliability Lead

### Purpose

This directory holds the record of every operational incident. The rule: every incident has a single owner and a clear status, and is never closed without a root cause and corrective actions. Logs are append-only — they are not edited after closure; updates are appended.

### File naming

`incident_YYYY-MM-DD_NNN.md` where `NNN` is a sequential number within the day. Example: `incident_2026-05-20_001.md`.

### Incident log template

Every incident log carries the following fields:

- **ID:** a unique identifier for the incident.
- **Date and time:** detection time in UTC.
- **Severity:** SEV-1 / SEV-2 / SEV-3.
- **Owner:** the name of the single role accountable for the incident.
- **Status:** `open` / `mitigated` / `resolved`.
- **Impact:** which service or workflow is affected and the extent.
- **Linked `trace_id`:** for end-to-end tracing.
- **Timeline:** detection, containment, and remediation steps with timestamps.
- **Root cause:** the written cause after investigation.
- **Corrective actions:** preventive steps with an owner per step.

### Rules

- No incident log contains PII; only `request_id`, `trace_id`, and `tenant_id` are referenced.
- Every SEV-1 incident requires a documented blameless post-incident review.
- An incident is not closed (`resolved`) without a root cause and corrective actions.
- The `.gitkeep` file keeps the directory under version control before the first incident is recorded.

### Related documents

- [`../../platform/observability/incident_response.md`](../../platform/observability/incident_response.md)
- [`../../platform/observability/alerts.md`](../../platform/observability/alerts.md)
