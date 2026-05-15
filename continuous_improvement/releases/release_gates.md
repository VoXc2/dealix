# Release Gates Standard

## Policy

- All gate-linked tests pass for changed layers.
- Eval thresholds meet release policy.
- Observability baseline has no unresolved critical alert.
- Rollback target verified in current release window.

## Control Gates

| Gate ID | Requirement | Evidence ID | Test ID |
|---|---|---|---|
| G-CI01-001 | policy applied in release process | E-CI01-001 | T-CI01-001 |
| G-CI01-002 | evidence retained for audit | E-CI01-002 | T-CI01-002 |
| G-CI01-003 | non-compliance blocks promotion | E-CI01-003 | T-CI01-003 |
