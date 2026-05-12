# SOC 2 Controls — Code Path Mapping

> Living document. Used by procurement, the founder, and a future
> Vanta/Drata sync. Every control points at the file(s) that implement
> it so a security review can verify the claim in seconds, not days.

| Control | Status | Code path / evidence | Owner |
| --- | --- | --- | --- |
| **CC1.1** Code of Conduct | Documented | `CODE_OF_CONDUCT.md` | Founder |
| **CC1.2** Security policy in place | Documented | `SECURITY.md`, `docs/sla.md` | Founder |
| **CC2.1** Communication of policies | Documented | `README.md`, `landing/trust/`, `docs/compliance/CONTROLS.md` (this file) | Founder |
| **CC2.2** Access reviews — quarterly | Manual | `docs/ops/dr_drill.md` table mirrors the cadence; access review runbook TBD | Founder |
| **CC3.1** Risk assessment | Documented | `docs/QA_REVIEW.md` punch list + verified findings | Founder |
| **CC4.1** Monitoring of controls | Tooling | Sentry (errors), Langfuse (LLM), OpenTelemetry (latency), BetterStack (uptime) | Platform |
| **CC5.1** Logical access controls | Code | `api/middleware/tenant_isolation.py`, `api/security/rbac.py`, `core/authz.py`, `cerbos/policies/dealix_resources.yaml` | Platform |
| **CC5.2** Encryption in transit | Infra | All deploys behind TLS (Railway/Render); HSTS via `SecurityHeadersMiddleware` | Platform |
| **CC5.3** Encryption at rest | Infra | Postgres / Redis providers (Railway/Supabase) — see DEPLOYMENT.md | Platform |
| **CC5.4** Key management | Code | `Infisical` integration (`dealix/integrations/infisical_client.py`) — see env vars `INFISICAL_*` | Platform |
| **CC6.1** Provisioning/de-provisioning | Code | `api/routers/onboarding.py`, `api/routers/customer.py` team invite + revoke | Platform |
| **CC6.2** Authentication | Code | `api/routers/auth.py` (JWT, MFA via TOTP, refresh rotation), `api/routers/sso.py` (WorkOS SAML/OIDC) | Platform |
| **CC6.3** Authorization | Code | `core/authz.py`, `cerbos/policies/*.yaml` | Platform |
| **CC6.4** System monitoring | Tooling | `/api/v1/status`, BetterStack heartbeat, Sentry, Langfuse | Platform |
| **CC6.5** Change management | Process | `.github/workflows/ci.yml` (hard-fail Codecov/Trivy), `.github/workflows/api_lint.yml` (Spectral), branch protection | Platform |
| **CC6.6** Network controls | Infra | SSRF guard (`api/security/ssrf_guard.py`), CORS allowlist (`api/main.py`), rate limit (`api/security/rate_limit.py`) | Platform |
| **CC6.7** Vulnerability management | Tooling | Dependabot (weekly), Trivy on Docker push (`.github/workflows/docker-build.yml`), Bandit pre-commit, gitleaks pre-commit | Platform |
| **CC6.8** Endpoint protection | Infra | Container scans (Trivy), non-root Docker user, multi-stage build | Platform |
| **CC7.1** Backup & recovery | Code + runbook | `scripts/infra/backup_pg.sh`, `scripts/infra/dr_restore_drill.sh`, `docs/ops/dr_drill.md` | Founder |
| **CC7.2** Disaster recovery | Tested | Quarterly drill cadence in `docs/ops/dr_drill.md` (RPO ≤24h, RTO ≤4h) | Founder |
| **CC8.1** Change tracking | Process | Git, semantic versioning, CHANGELOG.md, `.github/workflows/api_lint.yml` | Platform |
| **CC9.1** Vendor management | Documented | Sub-processor list in `docs/sla.md` §8 + `landing/trust/` | Founder |
| **CC9.2** DPA execution | Code | Onboarding step 3 `/api/v1/onboarding/dpa` captures signer + timestamp; persisted in `TenantRecord.meta_json.onboarding.dpa` | Platform |
| **PI1.1** Data classification | Code | `api/middleware/bopla_redaction.py` frozen sensitive-field catalog | Platform |
| **C1.1** Confidentiality | Code | Tenant isolation + RBAC + Cerbos + audit log + redaction | Platform |
| **A1.1** Availability commitments | Documented | `docs/sla.md` (99.5% target, SEV-1/2/3 MTTA/MTTR) | Founder |
| **A1.2** Capacity planning | Tooling | LLM cost tracking (`/api/v1/admin/costs`), Portkey per-tenant cost dashboard | Founder |
| **P1.1** Privacy notice | Documented | `landing/trust/index.html`, `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` | Founder |
| **P2.1** Choice and consent | Code | PDPL consent flow (`api/routers/pdpl.py`), opt-out enforcement (`auto_client_acquisition/compliance_os/contactability.py`) | Platform |
| **P3.1** Data minimization | Code | BOPLA redaction, allowed_use enforcement, suppression list (`SuppressionRecord`) | Platform |
| **P4.1** Right to access / delete | Code | `/api/v1/audit-logs` (read), soft-delete on `UserRecord.deleted_at`, PDPL request handlers in `pdpl.py` | Platform |
| **P5.1** Disclosure / retention | Documented | `docs/DATA_RETENTION_POLICY.md`, audit log retention via `AuditLogRecord` indexes | Founder |

## How this list is maintained

- **Add** a row whenever a new control becomes relevant (e.g. when we
  adopt a new vendor).
- **Update** the `Status` column on a quarterly cadence; statuses are
  one of: Documented (writeup exists), Code (implemented + tested),
  Tooling (third-party platform), Infra (cloud-provider feature),
  Manual (no automation yet), Process (operational, not codified).
- **Verify** each "Code" row in the security review by clicking through
  the path and confirming the test that exercises it.
- **Sync** to Vanta when `VANTA_API_KEY` is set — the controls table
  becomes the source of truth; Vanta becomes the observer.

## Audit prep checklist (Type I → Type II)

- [ ] Engage SOC 2 auditor (Type I window: 30 days; Type II: 6 months).
- [ ] Verify access reviews for the last 90 days are recorded.
- [ ] Verify backup restore drill recorded in `docs/ops/dr_drill.md` log.
- [ ] Verify quarterly vulnerability scan results in CI artifacts.
- [ ] Verify DPA for every paying customer is captured under
      `TenantRecord.meta_json.onboarding.dpa`.
- [ ] Verify sub-processor list matches contracts.
- [ ] Verify incident response runbook (TBD — Q2 2026).
