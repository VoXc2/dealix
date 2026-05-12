# SOC 2 Type I — readiness statement

> **Status:** SOC 2 Type I audit in progress (target: Q3 2026).
> **Auditor:** to be confirmed.
> **Scope:** Trust Services Criteria — Security, Availability, Confidentiality.

Procurement teams can use this document to assess our security
controls before the formal report lands.

## Mapped controls

Every CC* control maps to a code path. The full map lives in
`docs/compliance/CONTROLS.md`; the procurement-relevant subset is
summarised below.

| Control | What we enforce | Where it lives |
| --- | --- | --- |
| CC1.1 Governance | Documented org structure + RACI | `docs/ops/OPS_ROTATION.md`, `.github/CODEOWNERS` |
| CC2.1 Communication | Internal + customer comms templates | `docs/legal/DPA.md`, `landing/legal/` |
| CC3.1 Risk assessment | Periodic threat-modelling reviews | `docs/adr/`, `.github/workflows/security_lint.yml` |
| CC4.1 Monitoring | OTel + Sentry + Langfuse + Prometheus | `dealix/observability/` |
| CC5.1 Logical access | JWT + MFA + WorkOS SSO + Cerbos | `api/routers/auth.py`, `dealix/identity/workos_client.py`, `cerbos/policies/` |
| CC5.2 Authentication | Argon2 password hashes, MFA enforced | `api/routers/auth.py` |
| CC5.3 Authorisation | Policy-as-code via Cerbos | `cerbos/policies/dealix_resources.yaml` |
| CC6.1 System operations | Helm + Terraform IaC | `infra/terraform/live/`, `deploy/helm/` |
| CC6.2 Change management | PR-required reviews + CI gates | `.github/workflows/`, `docs/repo/branch_protection.md` |
| CC6.3 Tamper-evident logs | Audit log append-only | `db/models.AuditLogRecord` |
| CC6.5 Incident management | SEV-1/2/3 escalation matrix | `docs/ops/incident_response.md` |
| CC7.1 Threat detection | Semgrep + Bandit pre-commit | `.semgrep/dealix.yaml`, `.pre-commit-config.yaml` |
| CC7.2 Vulnerability mgmt | Snyk daily scans + Renovate PRs | `.github/workflows/snyk.yml`, `renovate.json5` |
| CC8.1 BC / DR | Quarterly DR drill | `scripts/infra/dr_restore_drill.sh` |
| A1.1 Availability target | 99.5 % uptime, p95 ≤ 500 ms | `docs/sla.md` |
| C1.1 Confidentiality | TLS-everywhere, BYOK option | `dealix/audit/byok.py` |
| C1.2 Data classification | PDPL ROPA generated quarterly | `auto_client_acquisition/compliance_os/` |

## Pre-audit evidence the founder collects

Run quarterly:

- `scripts/infra/backup_pg.sh` log for the past quarter.
- `scripts/infra/dr_restore_drill.sh` execution log.
- GitHub branch-protection diff (no force-push to `main`).
- PagerDuty incident export (or Knock fallback log).
- WorkOS Directory Sync export (SCIM provisioning audit).
- Snyk + Semgrep weekly report.

## Open items

- Production WAF (Cloudflare → ingress) cutover.
- Quarterly access review (90-day cadence).
- Customer-data deletion attestation (post-PDPL DSR).
