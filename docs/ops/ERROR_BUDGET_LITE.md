# Error Budget (Lite)

## Definition
- For V1: error budget = 1% of operations fail
- For V2: tighten to 0.5%

## What counts
- Failed operator steps
- Failed backups
- Failed integrations

## How to track
- Daily operator prints success rate
- Backup script prints archive size
- Each script's exit code is logged

## When to act
- 3 consecutive failures → page founder
- 1 week > 1% error rate → review runbooks
- 1 month > 1% error rate → revisit architecture
