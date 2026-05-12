# Docs index

The single map of where every doc lives. If a contributor can't find
something in 30 seconds, add a row here.

## Top-level

| Path | Purpose |
| --- | --- |
| [README.md](../README.md) | Entry point. Badges, quick deploy, entry points. |
| [README.ar.md](../README.ar.md) | Arabic mirror of the above. |
| [QUICK_START.md](../QUICK_START.md) | One-command bootstrap. |
| [CHANGELOG.md](../CHANGELOG.md) | Tagged releases. |
| [DEPLOYMENT.md](../DEPLOYMENT.md) | Production deploy targets + RLS doc. |
| [SECURITY.md](../SECURITY.md) | Vulnerability disclosure + key rotation. |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute. |
| [AGENTS.md](../AGENTS.md) | Conventions for AI + human contributors. |
| [LICENSE](../LICENSE) | MIT. |
| [THIRD_PARTY_LICENSES.md](../THIRD_PARTY_LICENSES.md) | Attribution. |

## QA + architecture

| Path | Purpose |
| --- | --- |
| [docs/QA_REVIEW.md](QA_REVIEW.md) | Cross-cutting audit + addendums. |
| [docs/sla.md](sla.md) | Service-level commitments. |
| [docs/adr/index.md](adr/index.md) | Architecture Decision Records. |
| [docs/architecture/*.md](architecture/) | Mermaid flow diagrams (data, auth, billing, enrichment, workflows). |
| [docs/product/CORE_WORKFLOWS.md](product/CORE_WORKFLOWS.md) | The Top-3 workflows. |
| [docs/product/ROADMAP.json](product/ROADMAP.json) | Public roadmap source. |

## Operations

| Path | Purpose |
| --- | --- |
| [docs/ops/incident_response.md](ops/incident_response.md) | SEV playbook. |
| [docs/ops/postmortem_template.md](ops/postmortem_template.md) | Blameless template. |
| [docs/ops/OPS_ROTATION.md](ops/OPS_ROTATION.md) | On-call rotation. |
| [docs/ops/dr_drill.md](ops/dr_drill.md) | Quarterly DR drill. |
| [docs/ops/saudi_region.md](ops/saudi_region.md) | Saudi-region migration. |
| [docs/ops/quality.md](ops/quality.md) | Mutation testing + CI playbook. |
| [docs/ops/connection_pooling.md](ops/connection_pooling.md) | PgBouncer tuning. |

## Compliance

| Path | Purpose |
| --- | --- |
| [docs/compliance/CONTROLS.md](compliance/CONTROLS.md) | SOC 2 controls map. |
| [docs/compliance/GDPR_PDPL_MAPPING.md](compliance/GDPR_PDPL_MAPPING.md) | GDPR + PDPL article mapping. |
| [docs/compliance/SUB_PROCESSORS.md](compliance/SUB_PROCESSORS.md) | Canonical sub-processor list. |
| [docs/legal/DPA.md](legal/DPA.md) | Data Processing Agreement template. |
| [docs/CROSS_BORDER_TRANSFER_ADDENDUM.md](CROSS_BORDER_TRANSFER_ADDENDUM.md) | PDPL Article 29 addendum. |
| [docs/DATA_RETENTION_POLICY.md](DATA_RETENTION_POLICY.md) | Retention windows. |

## Product / GTM

| Path | Purpose |
| --- | --- |
| [docs/customer-success/CASE_STUDY_TEMPLATE.md](customer-success/CASE_STUDY_TEMPLATE.md) | Case-study template. |
| [docs/marketing/onboarding_emails.md](marketing/onboarding_emails.md) | Loops trigger contracts. |
| [docs/llm/models.md](llm/models.md) | Model registry. |

## API

| Path | Purpose |
| --- | --- |
| [docs/api/overview.mdx](api/overview.mdx) | Mintlify start page. |
| [docs/api/auth.mdx](api/auth.mdx) | Bearer JWT / API key / SSO. |
| [docs/api/errors.mdx](api/errors.mdx) | Status codes + detail tokens. |
| [docs/api/rate-limits.mdx](api/rate-limits.mdx) | Per-bucket caps. |
| [docs/api/customers.mdx](api/customers.mdx) | Tenant data plane. |
| [docs/api/billing.mdx](api/billing.mdx) | Stripe + Moyasar. |
| [docs/api/onboarding.mdx](api/onboarding.mdx) | Self-serve flow. |
| [docs/api/support.mdx](api/support.mdx) | Plain + Resend fallback. |
| [docs/api/audit-logs.mdx](api/audit-logs.mdx) | Audit reads + CSV export. |
| [docs/api/sso.mdx](api/sso.mdx) | WorkOS. |
| [docs/api/pdpl.mdx](api/pdpl.mdx) | DSR endpoints. |
| [docs/api/realtime.mdx](api/realtime.mdx) | SSE stream. |
| [docs/api/benchmarks.mdx](api/benchmarks.mdx) | Sector benchmarks. |
| [docs/api/changelog.mdx](api/changelog.mdx) | Release notes. |
| [docs/api/examples/](api/examples/) | Python + TypeScript code samples. |

## Inventories

| Path | Purpose |
| --- | --- |
| [api/routers/INVENTORY.md](../api/routers/INVENTORY.md) | Every router classified. |
| [auto_client_acquisition/INVENTORY.md](../auto_client_acquisition/INVENTORY.md) | Every ACA subpackage. |

## Repository

| Path | Purpose |
| --- | --- |
| [docs/repo/branch_protection.md](repo/branch_protection.md) | GitHub repo settings. |
