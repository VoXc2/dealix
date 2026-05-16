# Rollback Policy

## Objective

Recover safely from regressions in agents, workflows, prompts, policies, or integrations.

## Rollback Triggers

- critical policy violation
- approval bypass
- major reliability degradation
- business-impacting data corruption
- failed post-release validation

## Rollback Procedure

1. Declare rollback event and incident owner.
2. Freeze new releases for affected domain.
3. Repoint to previous known-good version.
4. Validate critical workflow health.
5. Confirm governance and observability continuity.
6. Publish incident + remediation summary.

## Drill Cadence

- At minimum once per 30 days for production-critical workflows.
- Mandatory before enterprise onboarding milestone.

## Mandatory Rollback Tests

| Test ID | Scenario | Pass Criteria |
|---|---|---|
| T-RBK-001 | workflow version rollback | old version restored and runs safely |
| T-RBK-002 | agent version rollback | approved tool boundaries unchanged |
| T-RBK-003 | policy rollback | deny/approval behavior remains correct |
| T-RBK-004 | observability continuity after rollback | trace + logs + alerts still active |
