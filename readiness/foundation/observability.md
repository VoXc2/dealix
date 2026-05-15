# Foundation Layer — observability

- Required signals:
  - Layer score trend
  - Missing evidence paths
  - Failed cross-layer checks tied to this layer

- Runtime artifacts to monitor:
  - `api/routers/auth.py`
  - `api/security/rbac.py`
  - `api/middleware/tenant_isolation.py`

- Reporting:
  - Include this layer status in executive readiness brief.
