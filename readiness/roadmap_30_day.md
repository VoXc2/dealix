# 30-Step Implementation Roadmap (Execution-Focused)

## Goal

Deliver one complete governed workflow proving `CLIENT_PILOT_READY`.

## Phase A — Baseline Controls (Steps 1–10)

1. Freeze canonical gate IDs and scoring model.
2. Register critical workflow (`sales_lead_qualification_v1`).
3. Enforce tenant guard checks for intake and retrieval.
4. Enforce RBAC deny-by-default on workflow actions.
5. Define action risk matrix and approval rule mapping.
6. Enable approval pause/resume states.
7. Attach audit events to all governance decisions.
8. Enable trace propagation for all workflow steps.
9. Define baseline alerts for governance and failures.
10. Verify rollback procedure for workflow version.

## Phase B — Governed Workflow Proof (Steps 11–20)

11. Run inbound lead happy path.
12. Run high-risk approval path.
13. Run approval rejection path.
14. Run cross-tenant retrieval block path.
15. Validate citation coverage for key claims.
16. Validate idempotent execution on retry.
17. Validate CRM update + compensation on failure.
18. Generate eval report for workflow behavior.
19. Generate governance compliance report.
20. Generate executive ROI snapshot.

## Phase C — Readiness Closure (Steps 21–30)

21. Execute full `CLV-E2E-001` scenario.
22. Validate evidence completeness chain.
23. Execute rollback drill and validate integrity.
24. Validate alerting + incident workflow.
25. Produce readiness scorecard.
26. Produce client pilot checklist outcome.
27. Document open risks with owners.
28. Lock release candidate and publish notes.
29. Conduct operational handover.
30. Mark status: `CLIENT_PILOT_READY` only if all critical gates pass.
