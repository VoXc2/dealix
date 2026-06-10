# CTO backlog — 12 مبادرة التحول

مرجع تنفيذ مرتب بالمبادرات في [GLOBAL_AI_TRANSFORMATION_EXECUTION_INDEX_AR.md](GLOBAL_AI_TRANSFORMATION_EXECUTION_INDEX_AR.md).

## تحقق مجمّع

```bash
bash scripts/run_cto_pillar_verify_bundle.sh
```

## المبادرات

| ID | وثيقة | مالك افتراضي | دليل إغلاق | تحقق |
| --- | --- | --- | --- | --- |
| doctrine-lock | [01_doctrine_lock.md](01_doctrine_lock.md) | Trust | — | `--check doctrine-lock` |
| gap-closure | [02_gap_closure_matrix.md](02_gap_closure_matrix.md) | Platform | [evidence/gap_closure_*.md](evidence/) | `--check gap-closure` |
| enterprise-package | [03_enterprise_package.md](03_enterprise_package.md) | GTM + Delivery | [gap_closure_enterprise_package.md](evidence/gap_closure_enterprise_package.md) | `--check enterprise-package` |
| governance-expansion | [04_governance_expansion.md](04_governance_expansion.md) | Trust | — | `--check governance-expansion` |
| data-flywheel | [05_data_flywheel_operationalization.md](05_data_flywheel_operationalization.md) | Platform | [gap_closure_legacy_jsonl.md](evidence/gap_closure_legacy_jsonl.md) | `--check data-flywheel` |
| reliability-program | [06_reliability_program.md](06_reliability_program.md) | Reliability | [gap_closure_drills_automation.md](evidence/gap_closure_drills_automation.md) | `--check reliability-program` |
| observability-contracts | [07_observability_contracts.md](07_observability_contracts.md) | Observability | [gap_closure_trace_telemetry.md](evidence/gap_closure_trace_telemetry.md) | `--check observability-contracts` |
| gtm-system | [08_gtm_system_playbook.md](08_gtm_system_playbook.md) | GTM | — | `--check gtm-system` |
| unit-economics | [09_unit_economics_governance.md](09_unit_economics_governance.md) | Finance | — | `--check unit-economics` |
| delivery-control-tower | [10_delivery_control_tower.md](10_delivery_control_tower.md) | Delivery | — | `--check delivery-control-tower` |
| org-operating-system | [11_org_operating_system.md](11_org_operating_system.md) | People ops | [ownership_matrix.yaml](../../dealix/transformation/ownership_matrix.yaml) | `--check org-operating-system` |
| category-dominance | [12_category_dominance.md](12_category_dominance.md) | Strategy | [category_expansion_gates.yaml](../../dealix/transformation/category_expansion_gates.yaml) | `--check category-dominance` |

## صفوف مصفوفة الفجوات (6)

| Gap | Evidence |
| --- | --- |
| In-memory fallback | [gap_closure_in_memory_fallback.md](evidence/gap_closure_in_memory_fallback.md) |
| Legacy JSONL | [gap_closure_legacy_jsonl.md](evidence/gap_closure_legacy_jsonl.md) |
| Enterprise UI | [gap_closure_enterprise_ui.md](evidence/gap_closure_enterprise_ui.md) |
| Trace / telemetry | [gap_closure_trace_telemetry.md](evidence/gap_closure_trace_telemetry.md) |
| Enterprise package | [gap_closure_enterprise_package.md](evidence/gap_closure_enterprise_package.md) |
| Drills automation | [gap_closure_drills_automation.md](evidence/gap_closure_drills_automation.md) |

## تعريف «أخضر» للـ CTO

- `GLOBAL AI TRANSFORMATION: PASS` من `verify_global_ai_transformation.py`
- `ENTERPRISE CONTROL PLANE: PASS` عند تغيير واجهات المشغّل
- كل صف مصفوفة فجوات له ملف evidence مع سجل تحقق محدّث
