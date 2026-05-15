# العربية

Owner: قائد المنصة (Platform Lead)

## درجة الطبقة

طبقة الأساس (Layer 1): **78 من 100 — نطاق تجربة عميل**.

درجات المعايير الفرعية: الأساس 78، الهوية 80، تعدد المستأجرين 76، الأمن 77، النشر 79.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `platform/foundation/architecture.md`، `dealix/governance/`، `api/`، `alembic/` |
| جاهزية | متوفر | هذه الوثيقة و`platform/foundation/readiness.md` |
| اختبارات | متوفر | `readiness/foundation/tests.md`، `platform/foundation/tests.md` |
| مراقبة | متوفر | `dealix/observability/otel.py`، `platform/foundation/observability.md` |
| حوكمة | متوفر | `dealix/governance/approvals.py`، `dealix/trust/policy.py` |
| تراجع | متوفر | `platform/foundation/rollback.md`، `platform/deployment/rollback_plan.md` |
| مقاييس | متوفر | `platform/foundation/scorecard.yaml` |
| مالك | متوفر | قائد المنصة |

## الفجوات المحددة

- **تمرين استعادة من النسخ الاحتياطية:** غير موثَّق على وتيرة دورية متحقَّقة. المعيار الفرعي "النسخ والاستعادة" عند 65.
- **تمرين حذف مستأجر:** عزل المستأجر مُنفَّذ في الكود، لكن حذفاً متحقَّقاً يثبت إزالة البيانات من التخزين والفهارس غير مُسجَّل.
- **تمرين تدوير المفاتيح:** الأسرار والتشفير قائمان، لكن تدويراً دورياً بلا انقطاع غير موثَّق.

هذه الفجوات تُبقي الطبقة في نطاق تجربة عميل. إغلاقها بأدلة متحقَّقة شرط للانتقال إلى "جاهز للمؤسسات".

## روابط ذات صلة

- `readiness/foundation/tests.md`
- `readiness/foundation/scorecard.yaml`
- `readiness/cross_layer/tenant_agent_memory_test.md`
- `readiness/cross_layer/rag_permission_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Platform Lead

## Layer score

Foundation layer (Layer 1): **78 out of 100 — client pilot band**.

Sub-criteria scores: Foundation 78, Identity 80, Multi-tenant 76, Security 77, Deployment 79.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `platform/foundation/architecture.md`, `dealix/governance/`, `api/`, `alembic/` |
| readiness | present | this document and `platform/foundation/readiness.md` |
| tests | present | `readiness/foundation/tests.md`, `platform/foundation/tests.md` |
| observability | present | `dealix/observability/otel.py`, `platform/foundation/observability.md` |
| governance | present | `dealix/governance/approvals.py`, `dealix/trust/policy.py` |
| rollback | present | `platform/foundation/rollback.md`, `platform/deployment/rollback_plan.md` |
| metrics | present | `platform/foundation/scorecard.yaml` |
| owner | present | Platform Lead |

## Specific gaps

- **Backup restore drill:** not documented on a verified periodic cadence. The "backup and restore" sub-criterion sits at 65.
- **Tenant-deletion drill:** tenant isolation is implemented in code, but a verified deletion proving data removal from storage and indexes is not recorded.
- **Key rotation drill:** secrets and encryption exist, but a periodic, no-outage rotation is not documented.

These gaps keep the layer in the client-pilot band. Closing them with verified evidence is a precondition for moving to enterprise-ready.

## Related links

- `readiness/foundation/tests.md`
- `readiness/foundation/scorecard.yaml`
- `readiness/cross_layer/tenant_agent_memory_test.md`
- `readiness/cross_layer/rag_permission_test.md`

Estimated value is not Verified value.
