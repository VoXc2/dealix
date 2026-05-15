# Enterprise Readiness Model

## Definition of "Done"

Dealix is "done" for this phase only when all of the following hold:

1. API imports without errors.
2. Every operational object has `tenant_id`.
3. Every state-changing action emits an audit/control event.
4. Every high-risk action requires approval.
5. Every agent has contract + autonomy limit + kill switch path.
6. Every workflow run has trace continuity.
7. Every measured value metric has `source_ref`.
8. Rollback finalization requires and respects approval.
9. Every control-plane subsystem has tests.
10. One full governed workflow passes end-to-end.

## Stage Matrix

- Stage 1: Code Health Ready
- Stage 2: Control Plane Ready
- Stage 3: Agent Governance Ready
- Stage 4: Operational Safety Ready
- Stage 5: Value Proof Ready
- Stage 6: Client Pilot Ready
- Stage 7: Enterprise Ready
