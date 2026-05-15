# Business Impact Evals — Risk Model

## Risk tier

**medium**

## Risk factors

- Failure mode: incorrect or unavailable output from Business Impact Evals.
- Governance exposure: any action here must still pass the governance chain
  (risk score -> policy -> approval -> execution -> audit).
- Data exposure: must respect `tenant_id` isolation and permission-aware access.

## Scoring

Each action routed through this system is scored by
`auto_client_acquisition/risk_resilience_os` and
`auto_client_acquisition/governance_os/runtime_decision.py`. Actions above the
**medium** threshold escalate (see `platform/escalation`).

## Mitigations

- Retries + compensation (`platform/workflow_engine`).
- Rollback (`rollback.md`).
- Continuous evals (Phase 6).
- Human above the loop for high/critical actions.
