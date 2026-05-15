# Release Process (Governed AI Infrastructure)

## Release Flow

1. Design/Change proposal linked to layer gates.
2. Implement change with version tag.
3. Run automated tests + targeted evals.
4. Run simulation in staging.
5. Validate observability signals.
6. Validate rollback readiness.
7. Limited rollout.
8. Production rollout.
9. Post-release review and score update.

## Mandatory Release Gates

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-RLS-001 | layer tests and mandatory evals pass | T-RLS-001 |
| G-RLS-002 | governance thresholds met | T-RLS-002 |
| G-RLS-003 | observability baseline healthy | T-RLS-003 |
| G-RLS-004 | rollback drill fresh and verified | T-RLS-004 |
| G-RLS-005 | cross-layer validation score >= 90 | T-RLS-005 |

## Fail-Fast Rule

If any release gate fails, deployment is blocked automatically.

## Evidence Required Per Release

- Test report bundle
- Eval report bundle
- Trace sample for critical workflow
- Risk acceptance notes (if any)
- Rollback reference version
