# Rollback Requirements (Release 1)

## Objective

Every pilot release must be reversible without data integrity loss or prolonged downtime.

## Rollback policy

1. No release ships without a tested rollback plan.
2. Rollback owner is assigned before deployment starts.
3. Trigger conditions are predefined (error budget breach, policy violation spike, workflow failure spike).
4. Rollback execution must be logged and post-reviewed.

## Rollback scope

- API release rollback
- workflow configuration rollback
- policy/rules rollback
- database migration rollback strategy (or forward-fix plan when down migration is unsafe)

## Standard rollback runbook

1. Detect issue and classify severity.
2. Freeze new risky actions.
3. Execute rollback target version/config.
4. Validate health checks and core workflow smoke path.
5. Confirm audit and trace continuity.
6. Publish incident summary with root-cause follow-up.

## Required drill cadence

- At least one rollback drill per release train.
- Drill must include:
  - synthetic failure trigger,
  - rollback execution,
  - recovery verification,
  - captured metrics (MTTD, MTTR, workflow recovery rate).

## Acceptance checklist (Release 1)

- [ ] Rollback plan exists for pilot stack
- [ ] Rollback trigger conditions are documented
- [ ] One rollback drill has been executed and recorded
- [ ] Post-rollback smoke checks are defined
- [ ] Incident review template is linked to release process
