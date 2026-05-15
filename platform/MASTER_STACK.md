# Dealix Operational Infrastructure Master Stack

هذا الملف يربط طبقات البنية التشغيلية (Infrastructure) بالتنفيذ الفعلي في الكود.

## Runtime implementation

- Core runtime: `dealix_infrastructure/runtime.py`
- Enterprise readiness drill: `dealix_infrastructure/readiness.py`
- API endpoint: `POST /api/v1/infrastructure/readiness-test`
- Minimum governed workflow spec: `workflows/sales/lead_qualification.workflow.yaml`

## Tier mapping

1. Foundation: `TenantBoundary`, `PermissionEngine`, `IdentityPrincipal`
2. Workflow Infrastructure: `WorkflowEngine`, `WorkflowDefinition`, `WorkflowStep`
3. Agent Runtime: role/scope-bound execution via `PermissionEngine`
4. Governance Runtime: `GovernanceRuntime` + `ApprovalRegistry`
5. Memory + Knowledge: `OperationalMemory` (citations + lineage)
6. Observability: `ObservabilityRuntime` (traces, metrics, alerts, replay)
7. Evals: readiness eval report from `EnterpriseReadinessHarness`
8. Executive Layer: `ExecutiveReporter`
9. Delivery Machine: `DeliveryPlaybooks`

## Non-negotiables enforced

- No cross-tenant retrieval.
- No external high-risk action without decision passport.
- Approval-gated steps enforced at runtime.
- Every workflow step emits audit envelope + trace + metrics.
- Rollback drill is executed as part of readiness test.
