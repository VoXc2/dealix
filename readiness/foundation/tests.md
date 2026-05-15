# Foundation Layer — tests

- Required test evidence paths:
  - `tests/unit/test_auth_flow.py`
  - `tests/test_tenant_isolation_v1.py`
  - `tests/test_secure_agent_runtime.py`

- Verification command:
  - `python3 scripts/verify_enterprise_layer_readiness.py --strict`

- Expected outcome:
  - `LAYER_FOUNDATION_STATUS=PASS`
