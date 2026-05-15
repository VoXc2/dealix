# العربية

Owner: قائد المعرفة والذاكرة (Knowledge & Memory Lead)

## درجة الطبقة

طبقة الذاكرة والمعرفة (Layer 4): **79 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `platform/knowledge/architecture.md`، `auto_client_acquisition/knowledge_os/`، `auto_client_acquisition/company_brain/`، `core/memory/` |
| جاهزية | متوفر | هذه الوثيقة و`platform/knowledge/readiness.md` |
| اختبارات | متوفر | `readiness/memory/tests.md` |
| مراقبة | متوفر | `dealix/observability/`، `platform/knowledge/tests.md` |
| حوكمة | متوفر | `auto_client_acquisition/knowledge_os/answer_with_citations.py`، `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml` |
| تراجع | متوفر | `platform/knowledge/source_lineage.md`، إعادة بناء الفهرس من المصدر |
| مقاييس | متوفر | `readiness/memory/scorecard.yaml` |
| مالك | متوفر | قائد المعرفة والذاكرة |

## الفجوات المحددة

- **تمرين حذف مستأجر للفهارس:** عزل الفهرس مُنفَّذ، لكن تمريناً متحقَّقاً يثبت إزالة شرائح مستأجر من فهرس البحث غير مُسجَّل (مشترك مع طبقة الأساس).
- **اختبار أذونات الاسترجاع:** ربط الاسترجاع بأذونات المستخدم يحتاج اختباراً عابراً مُنفَّذاً (انظر `readiness/cross_layer/rag_permission_test.md`).

## روابط ذات صلة

- `readiness/memory/tests.md`
- `readiness/memory/scorecard.yaml`
- `readiness/cross_layer/rag_permission_test.md`
- `readiness/cross_layer/tenant_agent_memory_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Knowledge & Memory Lead

## Layer score

Memory & Knowledge layer (Layer 4): **79 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `platform/knowledge/architecture.md`, `auto_client_acquisition/knowledge_os/`, `auto_client_acquisition/company_brain/`, `core/memory/` |
| readiness | present | this document and `platform/knowledge/readiness.md` |
| tests | present | `readiness/memory/tests.md` |
| observability | present | `dealix/observability/`, `platform/knowledge/tests.md` |
| governance | present | `auto_client_acquisition/knowledge_os/answer_with_citations.py`, `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml` |
| rollback | present | `platform/knowledge/source_lineage.md`, index rebuild from source |
| metrics | present | `readiness/memory/scorecard.yaml` |
| owner | present | Knowledge & Memory Lead |

## Specific gaps

- **Tenant-deletion drill for indexes:** index isolation is implemented, but a verified drill proving a tenant's chunks are removed from the search index is not recorded (shared with the Foundation layer).
- **Retrieval permission test:** linking retrieval to user permissions needs an executed cross-layer test (see `readiness/cross_layer/rag_permission_test.md`).

## Related links

- `readiness/memory/tests.md`
- `readiness/memory/scorecard.yaml`
- `readiness/cross_layer/rag_permission_test.md`
- `readiness/cross_layer/tenant_agent_memory_test.md`

Estimated value is not Verified value.
