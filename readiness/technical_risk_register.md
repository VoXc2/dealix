# Technical Risk Register (Enterprise Infrastructure)

| Risk ID | Risk | Likelihood | Impact | Layer | Mitigation | Verification Test |
|---|---|---|---|---|---|---|
| R-001 | cross-tenant data leakage | medium | critical | multi-tenant | strict tenant guard + isolation tests | T-TNT-002, T-TNT-003 |
| R-002 | RBAC bypass on privileged route | medium | critical | identity/rbac | deny-by-default + auth audit logs | T-RBAC-001, T-RBAC-004 |
| R-003 | high-risk action executed without approval | low | critical | governance | approval engine hard gate | T-APR-001 |
| R-004 | uncited high-impact recommendation | medium | high | knowledge | citation enforcement + blocking fallback | T-CIT-004 |
| R-005 | workflow duplicate side effects on retry | medium | high | workflow engine | idempotency keys + compensation | T-WFE-002, T-WFE-004 |
| R-006 | missing traceability across layers | medium | high | observability | mandatory trace context + alerts | T-OBS-T-001 |
| R-007 | regression released without eval quality check | medium | high | evals/release | release gate threshold enforcement | T-RLS-001 |
| R-008 | rollback failure during incident | low | critical | continuous evolution | frequent rollback drills | T-RBK-001..004 |
| R-009 | integration downtime causes silent workflow failure | medium | high | execution/integrations | retries + alerting + incident workflow | T-ALT-001 |
| R-010 | policy drift from intended governance rules | medium | high | governance | versioned policy registry + policy tests | T-POL-003 |

## Priority Focus

- Immediate (`P0`): R-001, R-002, R-003, R-008
- Near-term (`P1`): R-004, R-005, R-006, R-007
- Growth (`P2`): R-009, R-010
