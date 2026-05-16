# Multi-Tenant Isolation Evidence Pack

## Controls

- Tenant context on control plane runs (`tenant_context.py`)
- Isolation tests: `tests/test_tenant_isolation_systems_26_35.py`
- Agent mesh routing: `tests/test_agent_mesh_tenant_and_routing.py`

## Verification

```bash
APP_ENV=test pytest tests/test_tenant_isolation_systems_26_35.py -q --no-cov
```
