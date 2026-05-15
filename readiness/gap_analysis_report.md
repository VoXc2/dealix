# Dealix Enterprise Gap Analysis (v1)

## Method

Assessment categories:
- `Existing`: implemented and test-backed.
- `Partial`: present but not fully governed or cross-layer connected.
- `Missing`: required for readiness but not yet implemented.

## Layer-by-Layer Assessment

| Layer | Existing | Partial | Missing | Risk | Priority | Recommended Implementation |
|---|---|---|---|---|---|---|
| Foundation | tenant contracts, auth/security modules, migrations | backup/restore and rollback drills not centralized in readiness model | unified foundation gate runner | medium | P0 | formalize gates + drill cadence + evidence registry |
| Identity / RBAC | security deps and role-aware routes | RBAC policy not yet standardized in one operating contract | global deny-by-default matrix + release gate checks | high | P0 | introduce central RBAC policy map + tests in release gates |
| Multi-tenancy | tenant-themed routes and tenant-aware schemas | retrieval and integration layers need consistent tenant guard proof | cross-layer tenant leak tests for every critical workflow | high | P0 | enforce tenant test pack in CI |
| Agent Runtime | agent_os, registry modules, secure runtime tests | per-agent production control pack not consistently documented | agent pack files for all production agents | high | P0 | generate per-agent control manifests and promotion gates |
| Workflow Engine | workflow modules and workflow tests | workflows not uniformly expressed in one schema + readiness evidence | governed workflow catalog and compensation coverage map | medium | P1 | adopt canonical workflow schema and versioned catalog |
| Knowledge / Memory | company brain and retrieval-related modules | citation lineage and permission-aware retrieval not consistently scored | retrieval gate suite with threshold enforcement | high | P0 | run retrieval evals as mandatory release checks |
| Governance | policy/approval/risk routers and docs exist | runtime orchestration across risk->policy->approval->audit varies by path | unified governance decision ledger across all critical actions | high | P0 | enforce governance pipeline middleware contract |
| Execution / Integrations | CRM/webhook/payment adapters exist | integration actions vary in approval/idempotency coverage | execution safety policy per integration class | high | P1 | classify integrations by risk + enforce compensation hooks |
| Observability | observability modules and routers exist | trace/metric/log requirements not centralized by gate IDs | mandatory OTel-aligned coverage for target workflow | medium | P1 | adopt observability requirement doc as release criterion |
| Evals | multiple tests and quality docs exist | eval assets are fragmented by domain | unified eval gates tied to deployment | high | P0 | add eval threshold checks to CI/CD blockers |
| Executive Intelligence | executive routes/reports exist | ROI linkage to workflow and eval signals not fully standardized | standard executive impact schema and weekly board packet | medium | P2 | define KPI contract and publish automated reports |
| Delivery Playbooks | many vertical playbooks exist | enterprise delivery flow needs single governed template | repeatable pilot-to-enterprise delivery path | medium | P1 | use Revenue OS delivery playbook as canonical template |
| Continuous Evolution | changelog/releases/docs exist | staged rollout and rollback governance not yet enforced end-to-end | mandatory pre-prod simulation + rollback freshness policy | high | P0 | enforce release process gates and rollback drill policy |
| Cross-Layer Validation | components exist separately | no single canonical cross-layer acceptance protocol | full end-to-end readiness test with evidence chain | critical | P0 | run `CLV-E2E-001` as hard go-live gate |

## Most Critical Gaps (P0)

1. Cross-layer validation as a hard release gate.
2. Unified governance pipeline enforcement for all side-effect actions.
3. Central eval thresholds integrated into release blocking.
4. Standardized per-agent control manifests before production promotion.
