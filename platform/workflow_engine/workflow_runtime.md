# العربية

**Owner:** مهندس وقت تشغيل سير العمل (Workflow Runtime Engineer).

## الغرض

يصف هذا المستند دورة حياة تشغيل سير العمل: كيف ينتقل تشغيل واحد من المحفّز إلى المخرج النهائي، وأين يُحتجز، وكيف يُستأنف. وقت التشغيل مبني على `dealix/execution/` للتنفيذ المعمّر و`auto_client_acquisition/full_ops/work_queue.py` لطابور بنود العمل.

## حالات التشغيل

كل تشغيل سير عمل يمر بحالات معلنة:

- `pending` — محفّز مستلَم، لم تبدأ الخطوات بعد.
- `running` — خطوة قيد التنفيذ.
- `waiting_approval` — متوقف عند خطوة موافقة بشرية.
- `retrying` — خطوة فشلت وضمن نافذة إعادة المحاولة.
- `compensating` — تشغيل خطوة تعويض بعد فشل غير قابل للاسترداد.
- `completed` — وصل إلى المخرج النهائي.
- `failed` — استنفد إعادة المحاولة والتعويض؛ دُفع إلى DLQ.
- `cancelled` — أوقفه مالك بشري.

## دورة الحياة

1. **استلام المحفّز:** يُسجَّل التشغيل بمعرّف فريد وإصدار سير العمل المثبَّت ومعرّف المستأجر.
2. **فحص منع التكرار:** يُفحص مفتاح التشغيل عبر `dealix/reliability/idempotency.py`؛ المحفّز المكرر يُرفض بسلام.
3. **تنفيذ الخطوات:** تُنفَّذ الخطوات بالترتيب من معرّف YAML. كل خطوة لها مالك (`system_auto` أو دور بشري) ومستوى مخاطر.
4. **بوابة الموافقة:** الخطوة عالية المخاطر تنقل التشغيل إلى `waiting_approval` وتنشئ بند عمل في الطابور.
5. **الاستئناف:** عند الموافقة يعود التشغيل إلى `running` من الخطوة التالية مباشرة دون إعادة الخطوات المكتملة.
6. **الإنهاء:** يُسجَّل المخرج النهائي وتُحدَّث المقاييس عبر `auto_client_acquisition/workflow_os/workflow_metrics.py`.

## الاستمرارية والاستئناف

التنفيذ المعمّر يعني أن حالة كل خطوة محفوظة. عند إعادة تشغيل العملية المضيفة يُستأنف التشغيل من آخر خطوة مكتملة، لا من البداية. الخطوات يجب أن تكون قابلة لإعادة التنفيذ (idempotent) لتفادي ازدواج الأثر.

## الطوابير

بنود العمل البشرية (مراجعة، موافقة، تصعيد) تُوضع في `WorkQueue` معزولة بـ `tenant_id`. الإدراج عبر معرّف البند ثابت ومانع للتكرار. تُرتَّب البنود بالأولوية عبر `auto_client_acquisition/full_ops/prioritizer.py`.

انظر أيضاً: `platform/workflow_engine/triggers.md`، `platform/workflow_engine/actions.md`، `platform/workflow_engine/retries.md`.

---

# English

**Owner:** Workflow Runtime Engineer.

## Purpose

This document describes the workflow run lifecycle: how a single run moves from trigger to final output, where it parks, and how it resumes. The runtime is built on `dealix/execution/` for durable execution and `auto_client_acquisition/full_ops/work_queue.py` for the work-item queue.

## Run states

Every workflow run passes through declared states:

- `pending` — trigger received, steps not yet started.
- `running` — a step is executing.
- `waiting_approval` — halted at a human-approval step.
- `retrying` — a step failed and is within its retry window.
- `compensating` — running a compensation step after a non-recoverable failure.
- `completed` — reached the final output.
- `failed` — exhausted retry and compensation; pushed to the DLQ.
- `cancelled` — stopped by a human owner.

## Lifecycle

1. **Trigger intake:** the run is recorded with a unique id, pinned workflow version, and tenant id.
2. **Deduplication check:** the run key is checked via `dealix/reliability/idempotency.py`; a duplicate trigger is rejected gracefully.
3. **Step execution:** steps run in order from the YAML definition. Each step has an owner (`system_auto` or a human role) and a risk level.
4. **Approval gate:** a high-risk step moves the run to `waiting_approval` and creates a work item in the queue.
5. **Resume:** on approval the run returns to `running` from the next step directly, without re-running completed steps.
6. **Finalization:** the final output is recorded and metrics are updated via `auto_client_acquisition/workflow_os/workflow_metrics.py`.

## Durability and resume

Durable execution means each step's state is persisted. When the host process restarts, the run resumes from the last completed step, not from the start. Steps must be idempotent to avoid duplicated side effects.

## Queues

Human work items (review, approval, escalation) are placed in a `WorkQueue` partitioned by `tenant_id`. Insert by stable item id is idempotent. Items are ordered by priority via `auto_client_acquisition/full_ops/prioritizer.py`.

See also: `platform/workflow_engine/triggers.md`, `platform/workflow_engine/actions.md`, `platform/workflow_engine/retries.md`.
