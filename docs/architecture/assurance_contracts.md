# Assurance Contracts

Contract rules:

- Missing contract => `deny`
- Failed precondition => `deny`
- External action => `escalate` + approval required
- Irreversible action without rollback plan => `deny`

Contracts are tenant-scoped and agent/action specific.
