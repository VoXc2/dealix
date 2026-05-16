# Foundation Layer — readiness

- Owner: `Platform + Security`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `tenant_isolation_pass_rate`
  - `auth_failure_rate`
  - `backup_restore_success_rate`
  - `deployment_rollback_mtta_minutes`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `tenant_isolation_tested` — Tenant isolation has explicit automated test coverage.
  - [ ] `rbac_tested` — RBAC controls are implemented and validated.
  - [ ] `audit_logs_working` — Security and runtime actions are auditable.
  - [ ] `backups_tested` — Backup verification exists and is executable.
  - [ ] `rollback_tested` — Rollback process is defined and recoverable.
  - [ ] `infra_observable` — Infrastructure has monitoring/incident visibility.

