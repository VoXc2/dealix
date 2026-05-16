# Workflow Engine Layer — tests

- Required test evidence paths:
  - `tests/test_workflow_os_v10.py`
  - `tests/test_delivery_workflows_v2.py`
  - `tests/test_diagnostic_workflow.py`

- Verification command:
  - `python3 scripts/verify_enterprise_layer_readiness.py --strict`

- Expected outcome:
  - `LAYER_WORKFLOWS_STATUS=PASS`
