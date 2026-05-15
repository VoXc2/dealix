# Module Consolidation Registry

_آخر تحديث: 2026-05-15. مرجع واحد لانضباط سطح الكود — Phase 4 (تضخّم معتدل)._

المستودع راكَم 162 وحدة `OS` تحت `auto_client_acquisition/`. هذا السجل هو
المصدر الوحيد لقرارات التجميد والتوحيد. **لا حذف** — تعليم وتوثيق فقط.

## 1. حارس الإصدارات

`scripts/check_no_new_vn_modules.py` يفشل CI إذا أُنشئت وحدة `*_vN` جديدة.
16 وحدة إصدارية مجمّدة حالياً. القاعدة: **مدّد الوحدة الـcanonical، لا تفرّع
نسخة جديدة.**

## 2. العائلات المكرّرة — الوحدة الـcanonical

| العائلة | Canonical (المعتمدة) | نسخ بديلة / legacy |
|---------|----------------------|---------------------|
| company_brain | `company_brain` + `company_brain_mvp` (مسارا قراءة/ingest) | `company_brain_v6` |
| observability | `observability_v10` (+ `observability_v6` موصولة حالياً) | توحيد لاحق على v10 |
| ai_workforce | `ai_workforce_v10` | `ai_workforce` (v1) |
| knowledge | `knowledge_v10` | `knowledge_os` (غير موصولة) |
| crm | `crm_v10` | — |
| llm_gateway | `llm_gateway_v10` | — |
| compliance | `compliance_os` | `compliance_os_v12` (غير موصولة) |

## 3. وحدات غير موصولة بأي مدخل إنتاج

39 وحدة لا يصلها أي راوتر `api/` ولا سكربت `scripts/` ولا `core/` — لا مباشرةً
ولا عبر استيراد عابر. **مرشّحة لمراجعة التوحيد** (قد تكون scaffolding مستقبلي
أو مستخدمة من الاختبارات فقط). محسوبة آلياً؛ أعد الحساب قبل أي إجراء.

```
agent_identity_access_os      institutional_control_os
agentic_operations_os         institutional_os
ai_estate_os                  institutional_scaling_os
board_decision_os             intelligence_compounding_os
board_ready_os                intelligence_os
business_ops                  investment_os
client_maturity_os            knowledge_os
command_os                    learning_flywheel
dealix_master_layers          meta_os
dominance_os                  moat_os
ecosystem_os                  observability_adapters
enterprise_os                 operating_finance_os
enterprise_rollout_os         operating_rhythm_os
execution_os                  reporting_os
holding_os                    responsible_ai_os
                              risk_resilience_os
                              saudi_layer
                              scale_os
                              scorecards
                              standards_os
                              ultimate_manual_os
                              value_capture_os
                              workflow_os
```

> ملاحظة: `business_ops` غير موصولة بالإنتاج لكنها مغطّاة باختبارات
> (`tests/test_offer_ladder.py`)؛ أبقِها حتى تُوصَل أو تُدمَج في `service_catalog`.

## 4. القاعدة من الآن

1. لا وحدة `*_vN` جديدة (يفرضه الحارس).
2. أي وحدة جديدة يجب أن تُوصَل براوتر أو سكربت خلال نفس الـPR، وإلا تُسجَّل هنا.
3. التوحيد الفعلي (حذف/دمج) قرار مؤسس لاحق — هذا السجل يُبقيه مرئياً.
