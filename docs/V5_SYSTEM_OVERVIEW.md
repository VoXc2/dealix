# Dealix v5 — نظرة عامة على النظام / System Overview

> صفحة واحدة تربط **كل** قطعة في الـ repo. ابدأ من هنا.
> One page mapping every component. Start here.

---

## 1. Contracts of truth (read-only sources)

| Source | What it defines | Touch via |
|---|---|---|
| `docs/registry/SERVICE_READINESS_MATRIX.yaml` | 32 services + 6 bundles + 8 quality gates | `scripts/verify_service_readiness_matrix.py` |
| `core/config/settings.py` | Every env-bound flag (incl. `whatsapp_allow_live_send=False` default) | `pydantic-settings` |
| `tests/test_landing_forbidden_claims.py::FORBIDDEN_PATTERNS` | The 7 forbidden marketing tokens | per-file ALLOWLIST |
| `auto_client_acquisition/agent_governance/policy.py::FORBIDDEN_TOOLS` | The 5 platform-forbidden tools | `evaluate_action()` |
| `docs/EXECUTIVE_DECISION_PACK.md` | The 10 founder decisions (B1-B5 + S1-S5) | manual sign-off |

If you change one of these, you've changed policy. Everything else is mechanical composition.

---

## 2. The 12 v5 layers — module map

| # | Layer | Module path | Router prefix |
|---|---|---|---|
| 1 | Customer Loop | `auto_client_acquisition/customer_loop/` | `/api/v1/customer-loop` |
| 2 | Role Command OS | `auto_client_acquisition/role_command_os/` | `/api/v1/role-command` |
| 3 | Service Quality | `auto_client_acquisition/service_quality/` | `/api/v1/service-quality` |
| 4 | Agent Governance | `auto_client_acquisition/agent_governance/` | `/api/v1/agent-governance` |
| 5 | Reliability OS | `auto_client_acquisition/reliability_os/` | `/api/v1/reliability` |
| 6 | Vertical Playbooks | `auto_client_acquisition/vertical_playbooks/` | `/api/v1/vertical-playbooks` |
| 7 | Customer Data Plane | `auto_client_acquisition/customer_data_plane/` | `/api/v1/customer-data` |
| 8 | Finance OS | `auto_client_acquisition/finance_os/` | `/api/v1/finance` |
| 9 | Delivery Factory | `auto_client_acquisition/delivery_factory/` | `/api/v1/delivery-factory` |
| 10 | Proof Ledger | `auto_client_acquisition/proof_ledger/` | `/api/v1/proof-ledger` |
| 11 | GTM OS | `auto_client_acquisition/gtm_os/` | `/api/v1/gtm` |
| 12 | Security & Privacy | `auto_client_acquisition/security_privacy/` | `/api/v1/security-privacy` |

### Cross-cutting modules

| Layer | Module | Router |
|---|---|---|
| Self-Growth OS (12 sub-modules) | `auto_client_acquisition/self_growth_os/` | `/api/v1/self-growth` |
| Diagnostic Engine | `auto_client_acquisition/diagnostic_engine/` | `/api/v1/diagnostic` |
| Founder aggregate | (composes all of the above) | `/api/v1/founder` |
| CompanyBrain | `auto_client_acquisition/company_brain/` | `/api/v1/company-brain` |

### Executive overlay (10-layer dominance map)

- `docs/architecture/ORGANIZATIONAL_INTELLIGENCE_DOMINANCE_AR.md`
- Runtime registry: `auto_client_acquisition/dealix_master_layers/registry.py::OI_DOMINANCE_LAYERS`

---

## 3. CLIs — founder-facing

| Script | Purpose | When to run |
|---|---|---|
| `scripts/dealix_status.py` | Local bilingual snapshot of every layer | Each morning |
| `scripts/dealix_smoke_test.py` | Cross-platform smoke against any deploy | After redeploy |
| `scripts/dealix_snapshot.py` | Write JSON audit trail to `docs/snapshots/<date>.json` | Daily (cron) |
| `scripts/dealix_diagnostic.py` | Bilingual Diagnostic brief generator | When warm intro lands |
| `scripts/dealix_invoice.py` | Manual Moyasar invoice (refuses sk_live_) | When customer says yes |
| `scripts/dealix_morning_digest.py` | Daily founder digest email | Daily (cron) |
| `bash scripts/post_redeploy_verify.sh` | 22-point Production verifier | After Railway redeploy |

---

## 4. Workflows — automated

| Workflow | Cron | What it does |
|---|---|---|
| `.github/workflows/daily_digest.yml` | 4AM UTC daily | Email founder daily digest |
| `.github/workflows/daily_snapshot.yml` | 5AM UTC daily | Commit JSON snapshot to `docs/snapshots/` |
| `.github/workflows/scheduled_healthcheck.yml` | Periodic | Hit `/health` |
| `.github/workflows/railway_deploy.yml` | On push to main | Build + deploy |

---

## 5. Test bundles — what guarantees what

| Test file | Guarantees |
|---|---|
| `tests/test_v5_end_to_end_journey.py` | The full 12-layer journey works for one customer |
| `tests/test_v5_endpoint_perimeter.py` | All v5 endpoints reachable + advertise guardrails (34 cases) |
| `tests/test_v5_layers*.py` | Per-layer unit tests (156 tests across pt1-pt4) |
| `tests/test_landing_forbidden_claims.py` | No forbidden marketing claim in landing site |
| `tests/test_no_guaranteed_claims.py` | No forbidden claim in `docs/**/*.md` |
| `tests/test_seo_audit.py` | Required SEO tags on every customer-facing page |
| `tests/test_live_gates_default_false.py` | Live-action gates default OFF |
| `tests/test_safe_action_gateway.py` | SafeAgentRuntime blocks forbidden actions |
| `tests/test_whatsapp_policy.py` | `assess_contactability` blocks cold WA |
| `tests/test_founder_dashboard.py` | Founder aggregate endpoint healthy + live_gates BLOCKED |
| `tests/test_founder_html_page.py` | Founder HTML page is internal-only + bilingual |
| `tests/test_diagnostic_engine.py` + `test_diagnostic_router.py` | Diagnostic API healthy |
| `tests/test_dealix_status_cli.py` + `test_dealix_smoke_test_cli.py` + `test_dealix_snapshot_cli.py` + `test_dealix_diagnostic_cli.py` + `test_dealix_invoice_cli.py` + `test_dealix_morning_digest.py` | All CLIs work |

Run everything: `python -m pytest --no-cov -q` — should print `≥958 passed, ≤8 skipped, ≤3 xfailed`.

---

## 6. Hard rules — the "do NOT" list

These are tested invariants. Breaking them fails CI.

- ❌ NO live charge (no `MOYASAR_ALLOW_LIVE_CHARGE` env, no env combination unlocks it).
- ❌ NO live WhatsApp send (`whatsapp_allow_live_send=False` default; tested).
- ❌ NO live email send (no `*_ALLOW_LIVE_*` env exists for email).
- ❌ NO LinkedIn automation (`FORBIDDEN_TOOLS.LINKEDIN_AUTOMATION`).
- ❌ NO scraping (`FORBIDDEN_TOOLS.SCRAPE_WEB`).
- ❌ NO cold WhatsApp (compliance_os blocks default).
- ❌ NO forbidden marketing claims (`نضمن`, `guaranteed`, `blast` regex).
- ❌ NO PII in proof ledger without redaction.
- ❌ NO customer name in evidence export without `consent_for_publication=True`.
- ❌ NO service marked `live` without all 8 quality gates passing.

---

## 7. Founder operating cadence (bridge to runbook)

For the day-to-day operating cadence (7AM daily / Monday weekly /
end-of-month / first-customer pilot), see
`docs/V5_FOUNDER_RUNBOOK.md`. For the first-customer step-by-step,
see `docs/V5_PHASE_E_CHECKLIST.md`. For the 10 founder decisions,
see `docs/EXECUTIVE_DECISION_PACK.md`.

---

## 8. Where to add things

| If you're adding... | Put it here |
|---|---|
| A new service | YAML matrix + new file in `auto_client_acquisition/<existing layer>/` |
| A new role brief | `auto_client_acquisition/role_command_os/role_briefs.py::_<role>_brief()` |
| A new sector playbook | `auto_client_acquisition/vertical_playbooks/catalog.py` + a `Playbook(...)` entry |
| A new health probe | `auto_client_acquisition/reliability_os/health_matrix.py::_PROBES` |
| A new pricing tier | `auto_client_acquisition/finance_os/pricing_catalog.py::_CATALOG` (founder approval first) |
| A new event type | `auto_client_acquisition/proof_ledger/schemas.py::ProofEventType` |
| A new GTM idea | `auto_client_acquisition/gtm_os/content_calendar.py` |
| A new safety check | new `tests/test_*_policy.py` (xfail if runtime gap) |
| A new founder CLI | `scripts/dealix_*.py` + `tests/test_dealix_*_cli.py` |

If your change crosses 2+ existing modules, it's probably wrong.
Refactor the seam first.

---

— V5 System Overview v1.0 · 2026-05-04 · Dealix
