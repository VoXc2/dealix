# Observability Layer — tests

- Required test evidence paths:
  - `tests/test_observability_v10.py`
  - `tests/test_observability_v6.py`
  - `tests/test_agent_observability_integration.py`

- Verification command:
  - `python3 scripts/verify_enterprise_layer_readiness.py --strict`

- Expected outcome:
  - `LAYER_OBSERVABILITY_STATUS=PASS`
