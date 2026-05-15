# العربية

**Owner:** مالك محرّك سير العمل (Workflow Engine Platform Lead) — قسم هندسة المنصة.

## الغرض

الطبقة 3 — محرّك سير العمل — تحوّل العمليات التشغيلية في Dealix إلى مسارات قابلة للتنفيذ والقياس وإعادة المحاولة والتحسين. كل عملية يدوية متكررة (تأهيل عميل محتمل، متابعة، تحديث CRM، حلّ تذكرة، تصعيد، تقرير أسبوعي، توجيه موافقة) تُعرَّف كسير عمل معلن: محفّز ثم خطوات ثم مخرج نهائي. المحرّك لا يرسل رسائل خارجية بنفسه؛ أي خطوة تنشئ تواصلاً خارجياً تنتج مسودة وتمر عبر خطوة موافقة بشرية أولاً.

## المكوّنات

- **معرّفات سير العمل (Workflow Definitions):** ملفات YAML معلنة. المرجع القائم في `data/workflows/` (diagnostic.yaml, onboarding.yaml, outreach_draft.yaml, support.yaml, expansion.yaml, lead_radar.yaml, proof_pack.yaml)، والمجموعة الجديدة تحت `workflows/`.
- **نموذج المراحل (Workflow Model):** مراحل حتمية عبر `auto_client_acquisition/workflow_os/workflow_model.py` (`WorkflowStage`, `WORKFLOW_STAGE_ORDER`).
- **مخطّط الخدمات (Workflow Mapper):** يربط الخدمة بمراحلها الافتراضية عبر `auto_client_acquisition/workflow_os/workflow_mapper.py`.
- **محرّك التنفيذ المعمّر (Durable Execution):** يستضيف دورة حياة التشغيل عبر `dealix/execution/`.
- **طبقة الموثوقية (Reliability):** إعادة المحاولة عبر `dealix/reliability/retry.py`، طابور الرسائل الميتة عبر `dealix/reliability/dlq.py`، منع التكرار عبر `dealix/reliability/idempotency.py`.
- **تدفّق الموافقات (Approval Flow):** خطوات الموافقة عبر `auto_client_acquisition/workflow_os/approval_flow.py` وسياسة الموافقة في `auto_client_acquisition/approval_center/approval_policy.py`.
- **طابور العمل (Work Queue):** بنود العمل المنتظرة عبر `auto_client_acquisition/full_ops/work_queue.py` و`work_item.py`.
- **مقاييس سير العمل (Workflow Metrics):** مفاتيح القياس عبر `auto_client_acquisition/workflow_os/workflow_metrics.py`.

## تدفّق البيانات

1. يصل محفّز (حدث وارد، جدول زمني، أو طلب يدوي) إلى المحرّك.
2. يحمّل المحرّك معرّف سير العمل ويثبّت إصداره.
3. تُنفَّذ الخطوات بالترتيب؛ كل خطوة تنتج أثراً في السجل.
4. الخطوة الفاشلة تمر على سياسة إعادة المحاولة؛ عند استنفاد المحاولات تُدفع إلى DLQ مع تشغيل خطوة تعويض إن وُجدت.
5. أي خطوة عالية المخاطر (إرسال خارجي، تصدير بيانات) تتوقف عند خطوة موافقة بشرية ولا تكمل قبل الموافقة.
6. عند اكتمال الخطوات يُسجَّل المخرج النهائي وتُحدَّث المقاييس.

## الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي في المستودع |
|---|---|
| نموذج مراحل سير العمل | `auto_client_acquisition/workflow_os/workflow_model.py` |
| مخطّط الخدمات إلى المراحل | `auto_client_acquisition/workflow_os/workflow_mapper.py` |
| تدفّق الموافقات | `auto_client_acquisition/workflow_os/approval_flow.py` |
| مقاييس سير العمل | `auto_client_acquisition/workflow_os/workflow_metrics.py` |
| محرّك التنفيذ المعمّر | `dealix/execution/` |
| إعادة المحاولة بالتراجع الأسّي | `dealix/reliability/retry.py` |
| طابور الرسائل الميتة | `dealix/reliability/dlq.py` |
| منع التكرار | `dealix/reliability/idempotency.py` |
| طابور بنود العمل | `auto_client_acquisition/full_ops/work_queue.py` |
| سياسة الموافقة | `auto_client_acquisition/approval_center/approval_policy.py` |
| تعريفات سير العمل القائمة | `data/workflows/*.yaml` |

انظر أيضاً: `platform/workflow_engine/workflow_runtime.md`، `platform/workflow_engine/readiness.md`، `platform/agent_runtime/architecture.md`.

---

# English

**Owner:** Workflow Engine Platform Lead — Platform Engineering.

## Purpose

Layer 3 — Workflow Engine — turns Dealix operations into paths that can be executed, measured, retried, and improved. Every repeated manual operation (lead qualification, follow-up, CRM update, ticket resolution, escalation, weekly report, approval routing) is declared as an explicit workflow: trigger, then steps, then final output. The engine never sends external messages itself; any step that produces external communication generates a draft and passes through a human-approval step first.

## Components

- **Workflow Definitions:** declarative YAML files. Existing reference set in `data/workflows/` (diagnostic.yaml, onboarding.yaml, outreach_draft.yaml, support.yaml, expansion.yaml, lead_radar.yaml, proof_pack.yaml), and the new set under `workflows/`.
- **Workflow Model:** deterministic stages via `auto_client_acquisition/workflow_os/workflow_model.py` (`WorkflowStage`, `WORKFLOW_STAGE_ORDER`).
- **Workflow Mapper:** binds a service to its default stages via `auto_client_acquisition/workflow_os/workflow_mapper.py`.
- **Durable Execution:** hosts the run lifecycle via `dealix/execution/`.
- **Reliability layer:** retry via `dealix/reliability/retry.py`, dead-letter queue via `dealix/reliability/dlq.py`, deduplication via `dealix/reliability/idempotency.py`.
- **Approval Flow:** approval steps via `auto_client_acquisition/workflow_os/approval_flow.py` and approval policy in `auto_client_acquisition/approval_center/approval_policy.py`.
- **Work Queue:** pending work items via `auto_client_acquisition/full_ops/work_queue.py` and `work_item.py`.
- **Workflow Metrics:** metric keys via `auto_client_acquisition/workflow_os/workflow_metrics.py`.

## Data flow

1. A trigger (inbound event, schedule, or manual request) reaches the engine.
2. The engine loads the workflow definition and pins its version.
3. Steps execute in order; each step emits a log trace.
4. A failed step passes the retry policy; on exhausted attempts it is pushed to the DLQ and a compensation step runs if one exists.
5. Any high-risk step (external send, data export) halts at a human-approval step and does not continue before approval.
6. When steps complete, the final output is recorded and metrics are updated.

## Mapping to existing code

| Component | Real repo path |
|---|---|
| Workflow stage model | `auto_client_acquisition/workflow_os/workflow_model.py` |
| Service-to-stage mapper | `auto_client_acquisition/workflow_os/workflow_mapper.py` |
| Approval flow | `auto_client_acquisition/workflow_os/approval_flow.py` |
| Workflow metrics | `auto_client_acquisition/workflow_os/workflow_metrics.py` |
| Durable execution engine | `dealix/execution/` |
| Exponential-backoff retry | `dealix/reliability/retry.py` |
| Dead-letter queue | `dealix/reliability/dlq.py` |
| Deduplication | `dealix/reliability/idempotency.py` |
| Work item queue | `auto_client_acquisition/full_ops/work_queue.py` |
| Approval policy | `auto_client_acquisition/approval_center/approval_policy.py` |
| Existing workflow definitions | `data/workflows/*.yaml` |

See also: `platform/workflow_engine/workflow_runtime.md`, `platform/workflow_engine/readiness.md`, `platform/agent_runtime/architecture.md`.
