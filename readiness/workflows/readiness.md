# العربية

Owner: قائد محرك سير العمل (Workflow Engine Lead)

## درجة الطبقة

طبقة محرك سير العمل (Layer 3): **79 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `platform/workflow_engine/architecture.md`، `auto_client_acquisition/workflow_os/`، `auto_client_acquisition/execution_os/`، `dealix/execution/` |
| جاهزية | متوفر | هذه الوثيقة و`platform/workflow_engine/readiness.md` |
| اختبارات | متوفر | `readiness/workflows/tests.md` |
| مراقبة | متوفر | `platform/workflow_engine/observability.md`، `dealix/observability/` |
| حوكمة | متوفر | `auto_client_acquisition/execution_os/gates.py`، `auto_client_acquisition/governance_os/approval_matrix.py` |
| تراجع | متوفر | `platform/workflow_engine/compensation.md`، `dealix/reliability/dlq.py` |
| مقاييس | متوفر | `readiness/workflows/scorecard.yaml` |
| مالك | متوفر | قائد محرك سير العمل |

## الفجوات المحددة

- **تمرين إعادة تشغيل قائمة الرسائل الميتة (DLQ):** `dealix/reliability/dlq.py` و`retry.py` قائمان، لكن تمرين إعادة تشغيل متحقَّق دوري غير مُسجَّل.
- **بوابات الموافقة عالية الخطورة:** ربط بوابات `execution_os/gates.py` بالموافقة البشرية يحتاج اختباراً عابراً مُنفَّذاً (انظر `readiness/cross_layer/workflow_governance_test.md`).

## روابط ذات صلة

- `readiness/workflows/tests.md`
- `readiness/workflows/scorecard.yaml`
- `readiness/cross_layer/workflow_governance_test.md`
- `readiness/cross_layer/rollback_drill.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Workflow Engine Lead

## Layer score

Workflow Engine layer (Layer 3): **79 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `platform/workflow_engine/architecture.md`, `auto_client_acquisition/workflow_os/`, `auto_client_acquisition/execution_os/`, `dealix/execution/` |
| readiness | present | this document and `platform/workflow_engine/readiness.md` |
| tests | present | `readiness/workflows/tests.md` |
| observability | present | `platform/workflow_engine/observability.md`, `dealix/observability/` |
| governance | present | `auto_client_acquisition/execution_os/gates.py`, `auto_client_acquisition/governance_os/approval_matrix.py` |
| rollback | present | `platform/workflow_engine/compensation.md`, `dealix/reliability/dlq.py` |
| metrics | present | `readiness/workflows/scorecard.yaml` |
| owner | present | Workflow Engine Lead |

## Specific gaps

- **DLQ-replay drill:** `dealix/reliability/dlq.py` and `retry.py` exist, but a verified periodic replay drill is not recorded.
- **High-risk approval gates:** linking `execution_os/gates.py` gates to human approval needs an executed cross-layer test (see `readiness/cross_layer/workflow_governance_test.md`).

## Related links

- `readiness/workflows/tests.md`
- `readiness/workflows/scorecard.yaml`
- `readiness/cross_layer/workflow_governance_test.md`
- `readiness/cross_layer/rollback_drill.md`

Estimated value is not Verified value.
