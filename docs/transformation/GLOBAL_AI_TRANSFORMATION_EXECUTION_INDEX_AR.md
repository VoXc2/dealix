# فهرس تنفيذ — Global AI Company Transformation

مرجع تنفيذي لخطة التحول الشاملة (12 مبادرة + محاور A–L + 4 مراحل).

## بوابة الدخول

- `ENTERPRISE CONTROL PLANE: PASS` (شرط مسبق)
- ثم: `bash scripts/run_global_ai_transformation_bundle.sh`

## المبادرات الـ 12

| ID | وثيقة | تحقق |
|----|-------|------|
| doctrine-lock | [01_doctrine_lock.md](01_doctrine_lock.md) | `--check doctrine-lock` |
| gap-closure | [02_gap_closure_matrix.md](02_gap_closure_matrix.md) | `--check gap-closure` |
| enterprise-package | [03_enterprise_package.md](03_enterprise_package.md) | `--check enterprise-package` |
| governance-expansion | [04_governance_expansion.md](04_governance_expansion.md) | `--check governance-expansion` |
| data-flywheel | [05_data_flywheel_operationalization.md](05_data_flywheel_operationalization.md) | `--check data-flywheel` |
| reliability-program | [06_reliability_program.md](06_reliability_program.md) | `--check reliability-program` |
| observability-contracts | [07_observability_contracts.md](07_observability_contracts.md) | `--check observability-contracts` |
| gtm-system | [08_gtm_system_playbook.md](08_gtm_system_playbook.md) | `--check gtm-system` |
| unit-economics | [09_unit_economics_governance.md](09_unit_economics_governance.md) | `--check unit-economics` |
| delivery-control-tower | [10_delivery_control_tower.md](10_delivery_control_tower.md) | `--check delivery-control-tower` |
| org-operating-system | [11_org_operating_system.md](11_org_operating_system.md) | `--check org-operating-system` |
| category-dominance | [12_category_dominance.md](12_category_dominance.md) | `--check category-dominance` |

## محاور الخطة (A–L)

| محور | مبادرات |
|------|---------|
| A منتج ومنصة | gap-closure, delivery-control-tower |
| B ثقة وحوكمة | doctrine-lock, governance-expansion |
| C بيانات وذكاء | data-flywheel |
| D موثوقية | reliability-program |
| E ملاحظة | observability-contracts |
| F GTM وفئة | gtm-system, category-dominance, enterprise-package |
| G–J إيراد وتمويل وتنظيم | unit-economics, org-operating-system |

التفاصيل: [`global_ai_transformation_index.yaml`](../../dealix/transformation/global_ai_transformation_index.yaml)

## حوكمة موسّعة

- سجل المجالات: `auto_client_acquisition/governance_os/governance_workflow_inventory.yaml`
- قواعد التحكم: `workflow_control_registry.py` (≥10 مجالات)

## إيقاع تشغيل

| إيقاع | أمر |
|-------|-----|
| أسبوعي | `bash scripts/run_executive_weekly_checklist.sh` |
| تحقق كامل | `bash scripts/run_global_ai_transformation_bundle.sh` |
| قبل توسع | `bash scripts/run_pre_scale_gate_bundle.sh` |

## تعريف «تم التحول»

- اكتساب وتسليم وحوكمة وإثبات واحتفاظ وتوسعة enterprise **بنظام تشغيل** — ليس بطلاقة فردية.
- كل إجراء AI حرج: traceable، approval-bounded، tenant-isolated، value-measured.
