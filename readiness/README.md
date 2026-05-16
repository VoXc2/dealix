# Revenue OS Readiness

Readiness for the first unavoidable workflow is true when:

- tenant isolation denial is enforced
- RBAC denial is enforced
- approval path is enforced for high risk
- rollback compensation is available
- metrics and audit traces are emitted per run

Validation tests:

- `tests/workflows/test_lead_qualification_workflow.py`
