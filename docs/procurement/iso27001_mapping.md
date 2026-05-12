# ISO 27001:2022 control mapping

> Procurement asks: "Are you ISO 27001 certified?"
>
> Answer: not yet. We are aligned with the 2022 control set; the
> formal certification audit is on the Q4 2026 roadmap. This document
> maps every Annex A control to the code path that already enforces
> it, so procurement can decide whether our pre-audit posture clears
> their bar.

## Annex A — control alignment

| Annex A clause | Control | How Dealix enforces it |
| --- | --- | --- |
| 5.1 Policies | Information-security policy | `docs/ops/`, `docs/legal/`, `AGENTS.md` |
| 5.7 Threat intel | Vulnerability monitoring | Snyk daily, Renovate weekly |
| 5.15 Access control | RBAC + ABAC | Cerbos policies + WorkOS SSO |
| 5.16 Identity mgmt | Strong identity | JWT + MFA + SCIM via WorkOS |
| 5.17 Authentication | Argon2 + TOTP MFA | `api/routers/auth.py` |
| 5.23 Cloud services | Cloud-supplier review | `docs/compliance/SUB_PROCESSORS.md` |
| 5.30 ICT readiness | DR drill quarterly | `scripts/infra/dr_restore_drill.sh` |
| 6.3 Awareness | Onboarding playbooks | `docs/ops/runbook_zero_to_prod.md` |
| 8.5 Secure auth | Brute-force throttling | `api/middleware/rate_limit.py` |
| 8.7 Malware | Container scanning | Snyk + Dependabot |
| 8.8 Vulnerability | Pen-test + dep scans | annual pen-test contract pending |
| 8.9 Configuration | IaC for repeatability | `infra/terraform/live/`, `deploy/helm/` |
| 8.11 Data masking | PII redaction | `auto_client_acquisition/compliance_os/redactors.py` |
| 8.12 Data leakage | PDPL DSR API + audit log | `api/routers/pdpl_dsr.py` |
| 8.13 Backup | Nightly pg_dump → S3 | `scripts/infra/backup_pg.sh` |
| 8.15 Logging | Centralised audit log | `db/models.AuditLogRecord` |
| 8.16 Monitoring | OTel + Prometheus + Sentry | `dealix/observability/` |
| 8.22 Network segregation | VPC + private subnets in Helm chart | `deploy/helm/dealix/` |
| 8.24 Cryptography | TLS 1.2+, BYOK option | `dealix/audit/byok.py` |
| 8.25 Secure SDLC | Pre-commit + CI gates | `.pre-commit-config.yaml`, `.github/workflows/` |
| 8.28 Secure coding | mypy strict subset + Semgrep | `pyproject.toml [tool.mypy]`, `.semgrep/dealix.yaml` |
| 8.32 Change mgmt | PR review + CODEOWNERS | `.github/CODEOWNERS` |
| 8.34 Audit testing | Tests gate every PR | `pytest`, `pre-commit` |

## Sub-processor notification clock

Per ISO 27001 5.23, sub-processor changes are notified to customers
on a 30-day right-of-objection clock. The canonical list:

- `docs/compliance/SUB_PROCESSORS.md` — full table.
- `landing/trust/sub-processors.html` — public mirror.
- The Loops `sub_processor_added` event fires the customer email.
