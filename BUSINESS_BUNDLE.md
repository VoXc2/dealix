# Dealix — Business Bundle
**AI revenue, growth, and compliance engine for Saudi B2B — PDPL-native, ZATCA-aware, approval-first.**
**محرّك إيرادات ونمو وامتثال بـ AI للشركات السعودية — PDPL أصلاً، ZATCA-aware، والموافقة أولاً.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-Latest-black)](https://nextjs.org)
[![PDPL: native](https://img.shields.io/badge/PDPL-native-success)](integrations/pdpl.py)

> **One-page index for anyone landing on this repo.** Investors, partners, engineers, founders, and operators: jump to your section in 30 seconds.

---

## 🚀 What is Dealix?

Dealix is a **Saudi-first B2B revenue operating system** with three engines:

1. **Lead Engine** — Saudi B2B lead discovery, enrichment, ICP scoring, duplicate suppression, and PDPL-aware usage controls.
2. **Service Engine** — Productized AI services: diagnostics, sales assistance, decision packs, customer health, proof curation, growth signals, executive command.
3. **Trust Engine** — Approval-first execution, audit trails, evidence packs, policy checks, and compliance registers for Saudi operating requirements.

**Operating rule:** *AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.*

It is **not** a generic CRM, chatbot, or blind sales automation tool. It is a sovereign revenue OS purpose-built for Saudi operating requirements (PDPL, ZATCA, CITC, Saudi commerce flows).

---

## 👥 Pick your starting point

| You are… | Start here | Time |
|---|---|---|
| 🤵 **Investor / Board member** | [`docs/investment/INVESTOR_BUNDLE.md`](docs/investment/INVESTOR_BUNDLE.md) · [live landing](landing/investor.html) | 10 min |
| 🤝 **Channel / Agency partner** | [`docs/AGENCY_PARTNER_PROGRAM.md`](docs/AGENCY_PARTNER_PROGRAM.md) · [live landing](landing/agency-partner.html) | 10 min |
| 🛒 **Customer (procurement / ops)** | [`landing/pricing.html`](landing/pricing.html) · [`landing/case-study.html`](landing/case-study.html) | 5 min |
| 👨‍💻 **Engineer (new to repo)** | [`README.md`](README.md) · [`AGENTS.md`](AGENTS.md) · [`docs/architecture/REPO_GAP_AUDIT.md`](docs/architecture/REPO_GAP_AUDIT.md) | 15 min |
| 🧑‍💼 **Founder / operator** | [`docs/FOUNDER_START_HERE_AR.md`](docs/FOUNDER_START_HERE_AR.md) · [`docs/DAILY_OPERATING_GUIDE_AR.md`](docs/DAILY_OPERATING_GUIDE_AR.md) | 20 min |
| 🤖 **AI coding agent** | [`AGENTS.md`](AGENTS.md) | 5 min |
| 🛡️ **Compliance / Security** | [`SECURITY.md`](SECURITY.md) · [`docs/SECURITY_RUNBOOK.md`](docs/SECURITY_RUNBOOK.md) · [`docs/PRIVACY_PDPL_READINESS.md`](docs/PRIVACY_PDPL_READINESS.md) | 15 min |

---

## 🧱 What's in this repo (high-level map)

| Area | Where | What |
|---|---|---|
| **Backend** | `api/` | FastAPI app, 120+ routers, SQLAlchemy async, Alembic migrations, multi-tenant |
| **Frontend** | `apps/web/`, `frontend/` | Next.js dashboard + public landing experience |
| **AI / Agents** | `dealix/`, `core/`, `intelligence_os/`, `self_evolving_os/` | AI agents, intelligence layer, autonomous workflows |
| **Trust / Compliance** | `integrations/pdpl.py`, `docs/compliance/` | PDPL-native, ZATCA-aware, audit, evidence |
| **Commercial** | `dealix/commercial/`, `docs/commercial/`, `landing/` | 13-step commercial chain, pricing, GTM, sales ops |
| **Growth** | `auto_client_acquisition/`, `autonomous_growth/`, `learning_flywheel/` | Lead gen, growth loops, learning system |
| **Integrations** | `integrations/`, `mcp_server/` | HubSpot, Calendly, WhatsApp, Moyasar, ZATCA, MCP |
| **Operations** | `docs/ops/`, `scripts/`, `ops/` | Launch runbooks, SLO, on-call, production gates |
| **Marketing site** | `landing/` | 77 static HTML pages (bilingual AR/EN) |
| **Tests / Evals** | `tests/`, `evals/`, `simulations/` | pytest + agent evals + business simulations |
| **Demos** | `demos/` | 3 working demo projects (ai_quick_win, company_brain, lead_intelligence) |
| **Templates** | `data/templates/`, `templates/` | AR/EN content templates, contracts, proposals |

**Totals (this repo):** 2,703 docs · 77 landing pages · 392 ops scripts · 39 top-level modules.

---

## 🧭 The Operating System, in 8 layers

```
              ┌─────────────────────────────────────────────┐
   L8         │  Founder OS  (CEO playbook, weekly cadence) │
              ├─────────────────────────────────────────────┤
   L7         │  Trust OS  (PDPL, ZATCA, evidence, audit)  │
              ├─────────────────────────────────────────────┤
   L6         │  Capital OS  (pricing, unit econ, runway)  │
              ├─────────────────────────────────────────────┤
   L5         │  Sales OS  (pipeline, ABM, enablement)     │
              ├─────────────────────────────────────────────┤
   L4         │  Service OS  (delivery, CS, proof packs)   │
              ├─────────────────────────────────────────────┤
   L3         │  Growth OS  (lead engine, outreach)        │
              ├─────────────────────────────────────────────┤
   L2         │  Intelligence OS  (AI agents, evals)        │
              ├─────────────────────────────────────────────┤
   L1         │  Data + Workflow OS  (Postgres, pipelines)  │
              └─────────────────────────────────────────────┘
```

Read [`docs/DEALIX_COMPANY_OS_MAP_AR.md`](docs/DEALIX_COMPANY_OS_MAP_AR.md) for the full map.

---

## 🔁 Founder's daily loop (5 commands)

```bash
# 1. Verify company is ready
bash scripts/company_ready_verify.sh

# 2. Verify commercial is ready to launch
bash scripts/verify_dealix_commercial_go_live.sh
# Expect: DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS

# 3. Daily ops status (5 min)
python scripts/run_dealix_daily_ops.py --api-only

# 4. Five founder metrics
python scripts/founder_daily_five_metrics.py

# 5. Comprehensive plan status (138 tasks)
python scripts/founder_comprehensive_plan_status.py
```

For the canonical "one command" routine: [`docs/FOUNDER_START_HERE_AR.md`](docs/FOUNDER_START_HERE_AR.md).

---

## 📊 Trust, security, and compliance posture

| Area | Status | Doc |
|---|---|---|
| **PDPL** (Personal Data Protection Law) | Native, designed-in | [`docs/PRIVACY_PDPL_READINESS.md`](docs/PRIVACY_PDPL_READINESS.md) |
| **ZATCA** (e-invoicing) | Aware, integration-ready | [`docs/INVOICING_ZATCA_READINESS.md`](docs/INVOICING_ZATCA_READINESS.md) |
| **Moyasar** (payments) | Integrated, sandbox default | [`docs/BILLING_MOYASAR_RUNBOOK.md`](docs/BILLING_MOYASAR_RUNBOOK.md) |
| **DPA / Contracts** | Full template + pilot template | [`docs/DPA_DEALIX_FULL.md`](docs/DPA_DEALIX_FULL.md) · [`docs/DPA_PILOT_TEMPLATE.md`](docs/DPA_PILOT_TEMPLATE.md) |
| **Incident response** | Documented + drillable | [`docs/SECURITY_RUNBOOK.md`](docs/SECURITY_RUNBOOK.md) · [`docs/PDPL_BREACH_RESPONSE_PLAN.md`](docs/PDPL_BREACH_RESPONSE_PLAN.md) |
| **SLOs** | Defined + measured | [`docs/SLO.md`](docs/SLO.md) |
| **On-call** | Rotating | [`docs/ON_CALL.md`](docs/ON_CALL.md) |
| **Hardening** | Server + frontend production | [`docs/ops/SERVER_HARDENING_CHECKLIST.md`](docs/ops/SERVER_HARDENING_CHECKLIST.md) |

**Approval-first principle:** AI explores, analyzes, recommends. **Humans approve critical external commitments.** See [`docs/AGENTS.md`](docs/AGENTS.md) and `dealix/governance/`.

---

## 🧪 Try it

```bash
# Clone + setup
git clone https://github.com/VoXc2/dealix.git
cd dealix
make setup
cp .env.example .env
# edit .env, then:
make run
# API docs: http://localhost:8000/docs
```

Full local stack (Postgres + Redis + API):
```bash
make docker-up
curl http://localhost:8000/health
```

Demos:
- [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/)
- [`demos/company_brain_demo/`](demos/company_brain_demo/)
- [`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/)

---

## 📡 Live production

| Domain | URL |
|---|---|
| Public site (AR/EN) | see [`docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md`](docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md) |
| API | `https://api.<domain>/docs` |
| Status | [`landing/system-status.html`](landing/system-status.html) |

---

## 🤝 How to engage

- **Buy:** See [`landing/pricing.html`](landing/pricing.html) or book via Calendly link in [`docs/DAILY_LEAD_PREP_SETUP_GUIDE.md`](docs/DAILY_LEAD_PREP_SETUP_GUIDE.md)
- **Partner:** [`docs/AGENCY_PARTNER_PROGRAM.md`](docs/AGENCY_PARTNER_PROGRAM.md)
- **Invest:** Reach out via the investor page
- **Contribute (engineers):** [`docs/contributing/`](docs/contributing/) (this is a private production repo — PRs by invitation)
- **Hire with us:** [`docs/HIRING_CSM_FIRST.md`](docs/HIRING_CSM_FIRST.md) (current open roles)

---

## 📜 License

**MIT** — see [`LICENSE`](LICENSE).

> Note: Operational runbooks, pricing, and commercial playbooks are public for transparency. Customer-specific data is never committed (enforced by `.gitignore` and PDPL policy).

---

## 🧭 Where to go next

- **Founder / operator** → [`docs/FOUNDER_START_HERE_AR.md`](docs/FOUNDER_START_HERE_AR.md)
- **Strategic context** → [`docs/STRATEGIC_MASTER_PLAN_2026.md`](docs/STRATEGIC_MASTER_PLAN_2026.md) · [`docs/DEALIX_OPERATING_CONSTITUTION.md`](docs/DEALIX_OPERATING_CONSTITUTION.md)
- **Engineer onboarding** → [`README.md`](README.md) → [`AGENTS.md`](AGENTS.md)
- **Architecture** → [`docs/architecture/REPO_GAP_AUDIT.md`](docs/architecture/REPO_GAP_AUDIT.md) · [`docs/ARCHITECTURE_LAYER_MAP.md`](docs/ARCHITECTURE_LAYER_MAP.md)
- **Everything (BEAST level)** → [`docs/BEAST_LEVEL_ARCHITECTURE.md`](docs/BEAST_LEVEL_ARCHITECTURE.md) · [`docs/DEALIX_MEGA_MASTER_FILE_AR.md`](docs/DEALIX_MEGA_MASTER_FILE_AR.md)

---

**Built in Saudi Arabia. For Saudi Arabia first. Then the GCC. Then the world.**
**صُنع في السعودية. للسعودية أولاً. ثم الخليج. ثم العالم.**
