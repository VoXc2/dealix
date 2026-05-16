# Security Architecture

## Core Controls

- authentication and token integrity
- RBAC authorization checks
- tenant boundary enforcement
- secret handling and redaction
- auditability for privileged actions

## Readiness Gates

- `G-SEC-001`: authentication integrity checks pass
- `G-SEC-002`: authorization denial checks pass
- `G-SEC-003`: cross-tenant access attempts are blocked
- `G-SEC-004`: security events are logged and trace-correlated
