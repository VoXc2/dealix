# Feedback Loop Standard

## Policy

- Collect operator incidents, policy denies, and eval misses weekly.
- Classify into quality, safety, reliability, or business impact.
- Map each item to owner, gate, and release target.
- Close loop only after verification test is passing.

## Control Gates

| Gate ID | Requirement | Evidence ID | Test ID |
|---|---|---|---|
| G-CI04-001 | policy applied in release process | E-CI04-001 | T-CI04-001 |
| G-CI04-002 | evidence retained for audit | E-CI04-002 | T-CI04-002 |
| G-CI04-003 | non-compliance blocks promotion | E-CI04-003 | T-CI04-003 |
