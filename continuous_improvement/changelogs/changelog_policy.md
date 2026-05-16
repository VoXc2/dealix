# Changelog Policy

## Policy

- Every release records what changed and why.
- Entries include impacted layer, gate IDs, and risk class.
- Behavioral changes must include migration notes.
- Rollback references are mandatory for production releases.

## Control Gates

| Gate ID | Requirement | Evidence ID | Test ID |
|---|---|---|---|
| G-CI02-001 | policy applied in release process | E-CI02-001 | T-CI02-001 |
| G-CI02-002 | evidence retained for audit | E-CI02-002 | T-CI02-002 |
| G-CI02-003 | non-compliance blocks promotion | E-CI02-003 | T-CI02-003 |
