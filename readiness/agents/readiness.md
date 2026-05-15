# Agent Runtime Layer — readiness

- Owner: `Agent Platform`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `agent_task_success_rate`
  - `agent_escalation_rate`
  - `agent_policy_block_rate`
  - `agent_retry_recovery_rate`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `agent_lifecycle_working` — Agent lifecycle states and transitions exist.
  - [ ] `tools_sandboxed` — Tool use is policy-gated and bounded.
  - [ ] `permissions_enforced` — Agent permissions are implemented and tested.
  - [ ] `retries_and_escalation_working` — Retries and escalation paths are represented.
  - [ ] `memory_isolated` — Agent memory interactions are isolated by context.
  - [ ] `agent_logs_visible` — Agent actions are visible in observability/audit paths.

