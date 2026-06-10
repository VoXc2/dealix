# Agent #12 — Dealix Infrastructure, Reliability, and Deployment Agent

**Repository:** https://github.com/Dealix-sa/dealix.git
**Date defined:** 2026-06-03
**Status:** REGISTERED — gap audit pending

---

## Context

Previous agents built the market, business, WhatsApp, commercial, operations,
security, founder control, QA, analytics, customer success, partnerships, and
product strategy layers. This agent makes Dealix **deployable, observable,
reliable, recoverable, and safe to operate** across staging and production.

## Role

- DevOps Architect
- SRE
- Deployment Engineer
- Reliability Lead
- Secrets Management Reviewer
- Observability Architect
- Incident Response Operator

## Mission

Build **Dealix Infrastructure & Reliability OS**:

```
Environment Policy
+ Staging/Production Separation
+ Secrets Management
+ Health Checks
+ Observability
+ Logging Policy
+ Error Monitoring
+ Backup/Restore
+ Rollback
+ Deployment Gates
+ Reliability Runbooks
+ Incident Response
+ Cost Control
```

## Non-Negotiable Rules

- Do not deploy production.
- Do not modify production secrets.
- Do not print secrets.
- Do not commit `.env` files.
- Do not weaken CI.
- Do not make destructive migrations.
- Do not enable external sends.
- Staging first.
- Production requires founder approval.
- All sensitive actions must be documented and dry-run by default.
- Every deployment must have rollback.
- Every production action must have audit log.
- No secrets in logs / reports / prompts.

## Phases

### Phase 0 — Infra Gap Audit
Inspect: README, AGENTS.md, .github/workflows/, Railway/deploy config,
Dockerfile / docker-compose, api/, frontend/, apps/web/, scripts/,
docs/deployment, docs/infra, env examples, tests/, Makefile, pyproject/package
files. Create `reports/infra/INFRA_GAP_AUDIT.md`.

### Phase 1 — Environment Policy
Create / improve:
- `docs/infra/ENVIRONMENT_POLICY_AR.md`
- `docs/infra/STAGING_PRODUCTION_POLICY_AR.md`
- `docs/infra/ENV_CONTRACT_AR.md`
- `docs/infra/SECRETS_MANAGEMENT_AR.md`
- `docs/infra/CONFIGURATION_DRIFT_POLICY_AR.md`
- `reports/infra/ENVIRONMENT_READINESS_REVIEW.md`

### Phase 2 — Health Checks & Readiness
- `docs/infra/HEALTH_CHECKS_AR.md`
- `docs/infra/READINESS_LIVENESS_POLICY_AR.md`
- `docs/infra/PRODUCTION_READINESS_CHECKLIST_AR.md`
- `reports/infra/PRODUCTION_READINESS_REVIEW.md`

### Phase 3 — Observability
- `docs/infra/OBSERVABILITY_OS_AR.md`
- `docs/infra/LOGGING_POLICY_AR.md`
- `docs/infra/METRICS_POLICY_AR.md`
- `docs/infra/ERROR_MONITORING_RUNBOOK_AR.md`
- `docs/infra/ALERTING_POLICY_AR.md`
- `reports/infra/OBSERVABILITY_GAP_REVIEW.md`

### Phase 4 — Backup, Restore, Rollback
- `docs/infra/BACKUP_RESTORE_AR.md`
- `docs/infra/ROLLBACK_POLICY_AR.md`
- `docs/infra/DATA_EXPORT_POLICY_AR.md`
- `docs/infra/DISASTER_RECOVERY_AR.md`
- `reports/infra/BACKUP_RESTORE_READINESS.md`
- `reports/infra/ROLLBACK_READINESS.md`

### Phase 5 — CI/CD Hardening
- `docs/infra/CICD_POLICY_AR.md`
- `docs/infra/DEPLOYMENT_APPROVAL_POLICY_AR.md`
- `docs/infra/RELEASE_CHECKLIST_AR.md`
- `reports/infra/CICD_REVIEW.md`

### Phase 6 — Final Report
`reports/infra/INFRA_FINAL_REPORT.md`

## Threat-Model Notes (Agentic Workflow Injection)

Per recent research (arXiv 2605.07135, 2604.11790), tool-augmented agents and
GitHub Actions are vulnerable to indirect prompt injection through issue bodies,
PR comments, fetched web content, MCP server responses, and skill files. The
hardening rule for this agent is:

- **Defense lives at tool-call boundaries**, not in the model.
- Every workflow that uses `pull_request_target`, `workflow_run`, or accepts
  untrusted input MUST have an allowlist of permitted actions and a manual
  approval gate for production-affecting steps.
- No secret may be exposed to a step that also ingests untrusted text.

## Verification

Run feasible (when permitted):
- `make doctor`
- `make env-check`
- `make security-smoke`
- frontend build if touched
- backend tests if touched
- **No production deploy.**

Do not fake results.
