# Governance Layer — tests

- Required test evidence paths:
  - `tests/test_governance_runtime_decision.py`
  - `tests/test_governance_approval_matrix.py`
  - `tests/test_governance_policy_check.py`
  - `tests/test_governance_os_draft_gate.py`

- Verification command:
  - `python3 scripts/verify_enterprise_layer_readiness.py --strict`

- Expected outcome:
  - `LAYER_GOVERNANCE_STATUS=PASS`
