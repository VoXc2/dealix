# العربية

**Owner:** مهندس الموثوقية (Reliability Engineer).

## الغرض

يحدّد هذا المستند كيف يتعامل محرّك سير العمل مع فشل خطوة: متى يعيد المحاولة، ومتى يتراجع، ومتى يدفع إلى طابور الرسائل الميتة. المنطق مبني على `dealix/reliability/retry.py` و`dealix/reliability/dlq.py`.

## سياسة إعادة المحاولة

عند فشل خطوة قابلة لإعادة المحاولة:

1. يحسب المحرّك تأخيراً بتراجع أسّي: `base_delay * 2^(attempt-1)` محدوداً بـ `max_delay`.
2. يُضاف عامل تشويش (jitter) لتفادي تزامن المحاولات.
3. الحد الأقصى الافتراضي ثلاث محاولات (`max_attempts=3`).
4. عند نجاح أي محاولة يكمل سير العمل من الخطوة التالية.

## تصنيف الأخطاء

- **خطأ عابر (Transient):** انقطاع شبكة، مهلة، حد معدّل مؤقت — قابل لإعادة المحاولة.
- **خطأ دائم (Permanent):** بيانات غير صالحة، رفض صلاحية، شرط أعمال غير محقَّق — لا يُعاد؛ ينتقل مباشرة إلى المسار البديل أو التعويض.
- **خطأ يحتاج تدخلاً (Needs intervention):** فشل يتطلب قراراً بشرياً — يخلق بند عمل في الطابور.

## المسار البديل (Fallback)

لكل خطوة يجوز تعريف مسار بديل: إجراء أبسط أو تصعيد بشري. مثال: إذا فشل إثراء العميل المحتمل آلياً يُحوَّل إلى مراجعة يدوية بدل إيقاف سير العمل بالكامل.

## طابور الرسائل الميتة

عند استنفاد إعادة المحاولة دون نجاح ودون مسار بديل، يُدفع البند إلى DLQ عبر `dealix/reliability/dlq.py` مع المصدر والحمولة والخطأ وعدد المحاولات. الطوابير المعيارية: `webhooks`, `outbound`, `enrichment`, `crm_sync`. تُراجَع عمق الطوابير يومياً وتُعاد المعالجة عبر `drain()`.

## منع التكرار

كل خطوة قابلة لإعادة التنفيذ يجب أن تكون idempotent. إعادة المحاولة لا يجوز أن تضاعف الأثر — تحديث CRM مرتين، إنشاء تذكرتين. يُستخدم `dealix/reliability/idempotency.py` بمفتاح ثابت لكل خطوة.

انظر أيضاً: `platform/workflow_engine/compensation.md`، `platform/workflow_engine/observability.md`.

---

# English

**Owner:** Reliability Engineer.

## Purpose

This document defines how the workflow engine handles a step failure: when it retries, when it falls back, and when it pushes to the dead-letter queue. The logic is built on `dealix/reliability/retry.py` and `dealix/reliability/dlq.py`.

## Retry policy

When a retryable step fails:

1. The engine computes an exponential backoff delay: `base_delay * 2^(attempt-1)` capped by `max_delay`.
2. A jitter factor is added to avoid synchronized retries.
3. The default ceiling is three attempts (`max_attempts=3`).
4. On any successful attempt the workflow continues from the next step.

## Error classification

- **Transient error:** network blip, timeout, temporary rate limit — retryable.
- **Permanent error:** invalid data, permission denial, unmet business condition — not retried; moves straight to fallback or compensation.
- **Needs intervention:** a failure requiring a human decision — creates a work item in the queue.

## Fallback path

Each step may define a fallback path: a simpler action or a human escalation. Example: if automated lead enrichment fails, route to manual review instead of stopping the whole workflow.

## Dead-letter queue

When retries are exhausted without success and without a fallback, the item is pushed to the DLQ via `dealix/reliability/dlq.py` with source, payload, error, and attempt count. Canonical queues: `webhooks`, `outbound`, `enrichment`, `crm_sync`. Queue depth is reviewed daily and items are reprocessed via `drain()`.

## Deduplication

Every retryable step must be idempotent. A retry must not double the side effect — updating the CRM twice, creating two tickets. `dealix/reliability/idempotency.py` is used with a stable key per step.

See also: `platform/workflow_engine/compensation.md`, `platform/workflow_engine/observability.md`.
