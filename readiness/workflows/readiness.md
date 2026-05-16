# Workflow Engine Layer — readiness

- Owner: `Delivery + Platform`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `workflow_success_rate`
  - `workflow_retry_success_rate`
  - `workflow_failure_recovery_time_minutes`
  - `queue_backlog_age_minutes`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `workflows_deterministic` — Workflow contracts and schemas are deterministic.
  - [ ] `workflows_retryable` — Retry paths exist for workflow execution.
  - [ ] `workflows_auditable` — Workflow execution can be audited.
  - [ ] `failure_recovery_tested` — Failure recovery paths are explicitly tested.
  - [ ] `workflows_observable` — Workflow metrics and traces are available.
  - [ ] `workflow_versioning_defined` — Workflow loading/version hooks exist.

