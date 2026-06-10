<div align="center">

# 🏢 Dealix — Saudi B2B Revenue Engine

### AI revenue, growth, and compliance engine for Saudi B2B — PDPL-native, ZATCA-aware, approval-first.
### محرّك إيرادات ونمو وامتثال بـ AI للشركات السعودية — PDPL أصلاً، ZATCA-aware، والموافقة أولاً.

[![CI](https://github.com/VoXc2/dealix/actions/workflows/ci.yml/badge.svg)](https://github.com/VoXc2/dealix/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![PDPL: native](https://img.shields.io/badge/PDPL-native-success)](integrations/pdpl.py)

**[العربية](README.ar.md)** · **English**

### [🚀 Launch](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md) · [✅ Production](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) · [💼 Go-Live](docs/ops/COMMERCIAL_GO_LIVE_GATE.md) · [📡 Domain](docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md) · [🧭 Gap Audit](docs/architecture/REPO_GAP_AUDIT.md)

</div>

---

## What Dealix is

Dealix is a Saudi-first B2B revenue operating system with three core engines:

1. **Lead Engine** — Saudi B2B lead discovery, enrichment, ICP scoring, duplicate suppression, and PDPL-aware usage controls.
2. **Service Engine** — productized AI services for diagnostics, sales assistance, decision packs, customer health, proof curation, growth signals, and executive command.
3. **Trust Engine** — approval-first execution, audit trails, evidence packs, policy checks, and compliance registers for Saudi operating requirements.

It is **not** a generic CRM, chatbot, or blind sales automation tool. Its operating rule is:

> AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.

---

## What is in this repository

| Area | Contents |
|---|---|
| Backend | FastAPI, SQLAlchemy async, Postgres-oriented persistence, routers across sales, compliance, analytics, agents, and webhooks. |
| Frontend | Static landing assets plus a Next.js app under `apps/web`. |
| Trust/compliance | PDPL-aware controls, no-overclaim register, Saudi compliance register, approval classes, and audit/evidence concepts. |
| Operations | Docker, docker-compose, Makefile, CI, production readiness docs, deploy/runbook material. |
| Commercial kit | Pricing, service catalog, onboarding, Saudi B2B accounts, outreach/channel material, and service packaging docs. |

---

## Quick start

```bash
git clone https://github.com/VoXc2/dealix.git
cd dealix
make setup
cp .env.example .env
# edit .env, then:
make run
# API docs: http://localhost:8000/docs
```

Full local stack:

```bash
make docker-up
curl http://localhost:8000/health
```

Production-style verification bundle:

```bash
make prod-verify
```

Useful verification commands:

```bash
make env-check             # checks backend and frontend env templates
make api-contract-check    # checks OpenAPI contract stability
make security-smoke        # dependency-free repository security smoke
make production-smoke      # smoke production API when PRODUCTION_BASE_URL is set
make dependency-inventory  # export lightweight dependency inventory
make release-manifest      # export production release manifest
make test                  # test suite with project pytest defaults
make security              # Bandit + detect-secrets baseline scan when configured
```

---

## Live production gates

Before paid traffic, public demos, or enterprise pilots, review these in order:

| Gate | Document / command |
|---|---|
| Launch operator runbook | [`docs/ops/LAUNCH_OPERATOR_RUNBOOK.md`](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md) |
| Production readiness | [`docs/ops/PRODUCTION_READINESS_CHECKLIST.md`](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) |
| Commercial go-live | [`docs/ops/COMMERCIAL_GO_LIVE_GATE.md`](docs/ops/COMMERCIAL_GO_LIVE_GATE.md) |
| Domain operations | [`docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md`](docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md) |
| Frontend production | [`docs/ops/FRONTEND_PRODUCTION_RUNBOOK.md`](docs/ops/FRONTEND_PRODUCTION_RUNBOOK.md) |
| Server hardening | [`docs/ops/SERVER_HARDENING_CHECKLIST.md`](docs/ops/SERVER_HARDENING_CHECKLIST.md) |
| Monitoring | [`docs/ops/MONITORING_MATRIX.md`](docs/ops/MONITORING_MATRIX.md) |
| Incident drill | [`docs/ops/LIVE_DOMAIN_INCIDENT_DRILL.md`](docs/ops/LIVE_DOMAIN_INCIDENT_DRILL.md) |
| Founder rhythm | [`docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md`](docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md) |
| Finalization status | [`docs/ops/PRODUCTION_FINALIZATION_STATUS.md`](docs/ops/PRODUCTION_FINALIZATION_STATUS.md) |

---

## Public endpoints

Public endpoints intentionally available without application auth include:

- `/health`
- `/api/v1/public/demo-request`
- `/api/v1/pricing/plans`
- `/api/v1/checkout`
- `/api/v1/webhooks/moyasar`

Admin, customer, and privileged operational routes must remain protected by their configured API-key or future RBAC boundary.

---

## Repository operating controls

Dealix now has explicit repository controls for the most important production risks:

| Control | File / command |
|---|---|
| Python and web CI | `.github/workflows/ci.yml` |
| CodeQL and dependency review | `.github/workflows/security.yml` |
| Secret and filesystem vulnerability scans | `.github/workflows/repository-hardening.yml` |
| OpenSSF Scorecard | `.github/workflows/scorecard.yml` |
| Web lockfile generation workflow | `.github/workflows/generate-web-lockfile.yml` |
| Environment contract validation | `scripts/check_env_contract.py`, `make env-check` |
| OpenAPI contract export/check | `scripts/export_openapi.py`, `scripts/check_openapi_contract.py` |
| Dependency inventory | `scripts/export_dependency_inventory.py`, `make dependency-inventory` |
| Release manifest | `scripts/export_release_manifest.py`, `make release-manifest` |
| Production launch checklist | `docs/ops/PRODUCTION_READINESS_CHECKLIST.md` |
| Repository gap register | `docs/architecture/REPO_GAP_AUDIT.md` |
| Production verification bundle | `make prod-verify` |

---

## Architecture model

Dealix is organized into five planes. Features should cross planes through explicit contracts, not hidden shared state.

| Plane | Responsibility | Example modules |
|---|---|---|
| Decision | Agents, reasoning, synthesis, recommendation, evidence assembly | `auto_client_acquisition/`, `autonomous_growth/`, `core/agents/` |
| Execution | Deterministic workflows, retries, compensation, external commitments | `auto_client_acquisition/pipeline.py`, `dealix/execution/` |
| Trust | Policy, approval, audit, verification, evidence packs | `dealix/trust/`, `dealix/registers/` |
| Data | Operational source of truth, lineage, metrics, integrations | `db/`, `integrations/` |
| Operating | CI/CD, Docker, release discipline, repo governance, runbooks | `.github/`, `Dockerfile`, `Makefile`, `docs/ops/` |

Full blueprint: [`docs/blueprint/master-architecture.md`](docs/blueprint/master-architecture.md).

---

## Trust and safety posture

Dealix is designed around:

- Structured outputs with approval, reversibility, and sensitivity classes.
- Policy evaluation before high-impact external actions.
- Human approval for pricing commitments, contract changes, sensitive exports, legal/regulatory messages, and other high-stakes actions.
- Evidence packs for decisions that need traceability.
- Public claim tracking through [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml).

Security posture includes `.env`-based configuration, sensitive settings patterns, webhook verification where implemented, Docker hardening, CI checks, and local/CI-compatible security commands. Keep README/security claims aligned with actual configured CI jobs.

---

## Saudi compliance posture

Designed from inception for Saudi B2B operating constraints, including:

- PDPL consent, lawful basis, retention, suppression, breach, and transfer posture.
- Saudi-specific business language, SAR pricing, Riyadh-time operations, and Arabic/English workflows.
- Compliance mappings and registers under [`dealix/registers/`](dealix/registers/).

Compliance documentation does not replace legal review. Production launch requires evidence from tests, controls, logs, and operational procedures.

---

## Development workflow

```bash
make install-dev
make lint
make test
make env-check
make api-contract-check
```

Before a production release:

```bash
make prod-verify
```

Then review:

- [`docs/ops/LAUNCH_OPERATOR_RUNBOOK.md`](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md)
- [`docs/ops/PRODUCTION_READINESS_CHECKLIST.md`](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)
- [`docs/ops/COMMERCIAL_GO_LIVE_GATE.md`](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)
- [`docs/architecture/REPO_GAP_AUDIT.md`](docs/architecture/REPO_GAP_AUDIT.md)
- [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml)

---

## Key docs

| Purpose | Document |
|---|---|
| Master architecture | [`docs/blueprint/master-architecture.md`](docs/blueprint/master-architecture.md) |
| API map | [`docs/architecture/API_MAP.md`](docs/architecture/API_MAP.md) |
| API contract policy | [`docs/architecture/API_CONTRACT_POLICY.md`](docs/architecture/API_CONTRACT_POLICY.md) |
| Gap audit | [`docs/architecture/REPO_GAP_AUDIT.md`](docs/architecture/REPO_GAP_AUDIT.md) |
| Launch operator runbook | [`docs/ops/LAUNCH_OPERATOR_RUNBOOK.md`](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md) |
| Production readiness | [`docs/ops/PRODUCTION_READINESS_CHECKLIST.md`](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) |
| Commercial go-live | [`docs/ops/COMMERCIAL_GO_LIVE_GATE.md`](docs/ops/COMMERCIAL_GO_LIVE_GATE.md) |
| Deploy runbook | [`docs/ops/DEPLOY_RUNBOOK.md`](docs/ops/DEPLOY_RUNBOOK.md) |
| Domain operations | [`docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md`](docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md) |
| Frontend production | [`docs/ops/FRONTEND_PRODUCTION_RUNBOOK.md`](docs/ops/FRONTEND_PRODUCTION_RUNBOOK.md) |
| Server hardening | [`docs/ops/SERVER_HARDENING_CHECKLIST.md`](docs/ops/SERVER_HARDENING_CHECKLIST.md) |
| Monitoring | [`docs/ops/MONITORING_MATRIX.md`](docs/ops/MONITORING_MATRIX.md) |
| Founder operating rhythm | [`docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md`](docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md) |
| Supply chain policy | [`docs/ops/SBOM_AND_SUPPLY_CHAIN_POLICY.md`](docs/ops/SBOM_AND_SUPPLY_CHAIN_POLICY.md) |
| No-overclaim register | [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml) |
| Saudi compliance register | [`dealix/registers/compliance_saudi.yaml`](dealix/registers/compliance_saudi.yaml) |

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**[🚀 Launch](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md)** · **[✅ Production](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)** · **[💼 Go-Live](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)** · **[🧭 Gap Audit](docs/architecture/REPO_GAP_AUDIT.md)** · **[🇸🇦 Compliance](dealix/registers/compliance_saudi.yaml)**

</div>
