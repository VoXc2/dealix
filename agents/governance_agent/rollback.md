# Governance Agent Rollback Plan

## Rollback Triggers

- Repeated gate failure in production.
- Confirmed policy or approval bypass.
- KPI degradation beyond agreed tolerance.

## Procedure

1. Freeze new version activation.
2. Repoint runtime to last known-good `governance_agent` release.
3. Re-run smoke checks for permissions and policy adherence.
4. Confirm no unauthorized external effects occurred.
5. Publish rollback evidence bundle.

## Rollback Tests

| Test ID | Scenario | Expected |
|---|---|---|
| T-AGT-GOV-070 | runtime version rollback | prior behavior restored |
| T-AGT-GOV-071 | policy-safe fallback | no approval bypass |
| T-AGT-GOV-072 | KPI stabilization check | metrics return within tolerance |
