# Dealix Global AI Transformation Program

This directory is the execution spine for the comprehensive transformation from a strong AI product repository into a category-defining governed AI company.

## Program scope

- Strategic doctrine lock
- Hardening gap closure
- Enterprise package standardization
- Governance expansion beyond systems 26–35
- Data and learning flywheel operationalization
- Reliability and mission-critical operations
- Observability contracts and trace discipline
- Founder-led GTM systemization
- Unit-economics governance
- Delivery control tower
- Organization operating system
- Category dominance and regional expansion

## File map

- `01_doctrine_lock.md`
- `02_gap_closure_matrix.md`
- `03_enterprise_package.md`
- `04_governance_expansion.md`
- `05_data_flywheel_operationalization.md`
- `06_reliability_program.md`
- `07_observability_contracts.md`
- `08_gtm_system_playbook.md`
- `09_unit_economics_governance.md`
- `10_delivery_control_tower.md`
- `11_org_operating_system.md`
- `12_category_dominance.md`

## Control artifacts

- `dealix/transformation/todo_registry.yaml`
- `dealix/transformation/kpi_registry.yaml`
- `dealix/transformation/ownership_matrix.yaml`
- `dealix/transformation/risk_register.yaml`
- `dealix/transformation/jsonl_migration_catalog.yaml`
- `dealix/transformation/reliability_drills.yaml`
- `dealix/transformation/category_expansion_gates.yaml`
- `dealix/transformation/ceo_signal_os.yaml`
- `dealix/transformation/engineering_cutover_policy.yaml`
- `dealix/transformation/kpi_baselines.yaml`

## CEO Signal OS (market proof loop)

- Taxonomy and targets: `dealix/transformation/ceo_signal_os.yaml`
- Weekly dated proof pack: `bash scripts/run_ceo_signal_weekly_loop.sh`
- **Executive operating checklist (weekly):** `bash scripts/run_executive_weekly_checklist.sh` — يولّد الـ proof pack، يشغّل `verify_global_ai_transformation.py`، ويسجّل سطرًا في `docs/transformation/evidence/weekly_ops_checklist.log`.
- **دليل تشغيل تنفيذي (عربي):** [EXECUTIVE_OPERATING_CHECKLIST_AR.md](EXECUTIVE_OPERATING_CHECKLIST_AR.md)
- **خطة الجلسة الواحدة + مقارنة سوقية:** [CEO_ONE_SESSION_MASTER_PLAN_AR.md](CEO_ONE_SESSION_MASTER_PLAN_AR.md)
- **قبل التوسع القطاعي/الإقليمي:** `bash scripts/run_pre_scale_gate_bundle.sh` (بوابات التوسع + `verify_ceo_signal_readiness.sh category_gates`).
- **دليل القطع الهندسي (إشارة خارجية + PR):** [ENGINEERING_CUTOVER_RUNBOOK_AR.md](ENGINEERING_CUTOVER_RUNBOOK_AR.md)
- Pick verification gate: `bash scripts/verify_ceo_signal_readiness.sh transformation|control_plane|revenue_os|category_gates|all`
- Standalone category gate script (also covered by `run_pre_scale_gate_bundle.sh`): `bash scripts/verify_category_expansion_before_scale.sh`

## Verification

- `python3 scripts/verify_global_ai_transformation.py`
- `bash scripts/verify_global_ai_transformation.sh`
- `python3 scripts/generate_weekly_operating_proof_pack.py --out docs/transformation/evidence/weekly_proof_latest.md`
