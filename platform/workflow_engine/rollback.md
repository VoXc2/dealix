# Workflow Engine Layer Rollback

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

Version-pin to last stable workflow definition and drain in-flight runs safely.

## Rollback Tests

| Test ID | Scenario | Expected Result |
|---|---|---|
| T-WFE-040 | hot rollback in staging | layer recovers without policy regression |
| T-WFE-041 | production-safe rollback rehearsal | critical workflows remain stable |

## Control Linkage (WFE)

- Gate ID: G-WFE-900
- Evidence ID: E-WFE-900
- Test ID: T-WFE-900

