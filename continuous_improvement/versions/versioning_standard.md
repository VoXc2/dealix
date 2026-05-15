# Versioning Standard

## Policy

- Use semantic versioning for agents, workflows, and layer contracts.
- Major increments for breaking behavior or policy semantics.
- Minor increments for backward-compatible capabilities.
- Patch increments for fixes without contract change.

## Control Gates

| Gate ID | Requirement | Evidence ID | Test ID |
|---|---|---|---|
| G-CI03-001 | policy applied in release process | E-CI03-001 | T-CI03-001 |
| G-CI03-002 | evidence retained for audit | E-CI03-002 | T-CI03-002 |
| G-CI03-003 | non-compliance blocks promotion | E-CI03-003 | T-CI03-003 |
