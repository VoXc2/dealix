# Integrations Layer Rollback

## Rollback Trigger Conditions

- Critical gate failure after deployment.
- Business-impacting regression linked to this layer.
- Governance non-compliance requiring immediate containment.

## Rollback Procedure

1. Freeze new releases touching this layer.
2. Activate previous known-good layer version.
3. Validate dependent workflow health checks.
4. Confirm audit and telemetry continuity.
5. Publish rollback summary with root-cause owner.

## Layer-Specific Action

Roll back connector mapping file and disable unstable adapter routes.

## Rollback Tests

| Test ID | Scenario | Expected Result |
|---|---|---|
| T-INT-040 | hot rollback in staging | layer recovers without policy regression |
| T-INT-041 | production-safe rollback rehearsal | critical workflows remain stable |

## Control Linkage (INT)

- Gate ID: G-INT-900
- Evidence ID: E-INT-900
- Test ID: T-INT-900

