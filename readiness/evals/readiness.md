# Evaluation Layer — readiness

- Owner: `Quality + Product`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `eval_automation_coverage_rate`
  - `regression_detection_rate`
  - `hallucination_flag_rate`
  - `workflow_success_rate`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `eval_suites_automated` — Evaluation assets and scripts are automated.
  - [ ] `regression_tests_passing` — Regression guard tests are present.
  - [ ] `hallucination_monitored` — Knowledge/business answer quality eval exists.
  - [ ] `workflow_success_measured` — Workflow success metrics are measured.
  - [ ] `business_kpis_tracked` — Business KPI dashboard specs exist.

