# Evaluation Layer — tests

- Required test evidence paths:
  - `tests/test_output_quality_gate.py`
  - `tests/test_readiness_gates.py`
  - `tests/test_governance_os_draft_gate.py`
  - `tests/test_service_readiness_matrix.py`

- Verification command:
  - `python3 scripts/verify_enterprise_layer_readiness.py --strict`

- Expected outcome:
  - `LAYER_EVALS_STATUS=PASS`
