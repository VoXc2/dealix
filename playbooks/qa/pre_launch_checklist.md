# Pre-Launch QA Checklist (Enterprise Workflow)

## Critical QA Checklist

- [ ] Tenant isolation tests passed.
- [ ] RBAC deny-by-default tests passed.
- [ ] Workflow idempotency and retry tests passed.
- [ ] High-risk approval path tested (approve and reject).
- [ ] Citation coverage threshold met.
- [ ] End-to-end trace available and correlated.
- [ ] Critical alerts tested.
- [ ] Eval thresholds passed.
- [ ] Rollback drill completed.
- [ ] Executive impact panel updated.

## Required Test Bundle

| Test Group | Required |
|---|---|
| workflow execution cases | yes |
| governance high-risk cases | yes |
| retrieval citation cases | yes |
| cross-layer validation suite | yes |
| rollback drill | yes |

Release is blocked until all critical checklist items are complete.
