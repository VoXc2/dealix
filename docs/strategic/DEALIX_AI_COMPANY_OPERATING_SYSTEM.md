# Dealix — AI Company Operating System

## 1. Thesis

Dealix is not an AI app and not an AI service agency. It is an **AI
Company Operating System**: a company whose internal operations run as a
small set of named, governed, maturity-tracked systems, with AI in the
core of the operating model rather than bolted on as a feature.

The difference that matters is not "more technology". It is operating
leverage — a small human team orchestrating governed systems that
deliver repeatable quality, measurable value, and auditable trust.

Master principle:

> Do not build AI that answers. Build AI that operates.
> Do not build features. Build operating systems.
> Do not sell bots. Sell transformation.
> Do not measure usage. Measure business impact.
> Keep humans above the loop.

This document is the human-readable companion to the machine-readable
spine in `auto_client_acquisition/company_os/`. The registry there is
the source of truth; this document explains it.

## 2. The 7 Internal Systems

Each system maps to canonical modules that already exist in the repo.
Company OS names them, scores them, and gates them.

| System | Backing modules | Maturity | Home phase |
|---|---|---|---|
| Delivery System | `delivery_factory`, `diagnostic_workflow`, `service_catalog`, `workflow_os_v10` | Proven | Foundation |
| Agent Factory | `agent_factory`, `ai_workforce`, `ai_workforce_v10` | Working | Agentic Platform |
| Governance System | `governance_os`, `trust_os`, `responsible_ai_os` | Proven | Foundation |
| Knowledge OS | `knowledge_os`, `knowledge_v10`, `core.memory.revenue_memory` | Working | Foundation |
| Executive System | `executive_command_center`, `founder_v10`, `executive_reporting` | Proven | Foundation |
| Evaluation System | `eval_os`, `agent_observability` | Working | Foundation |
| Transformation System | `transformation_os`, `service_catalog` | Seed | Delivery Maturity |

Maturity bands: `seed` → `working` → `proven` → `scaled`. Scoring is
deterministic (`company_os/maturity.py`): backing modules wired,
doctrine gates declared, evidence present, API exposed, evals present.

### 2.1 Delivery System
Repeatable delivery: discovery, assessment, blueprint, playbook, QA,
ROI, handover, monthly optimization. Backed by the existing delivery
factory and the `workflow_os_v10` state machine.

### 2.2 Agent Factory
Design-time templates for governed AI agents. The Factory
(`auto_client_acquisition/agent_factory/`) defines 6 templates —
sales, support, ops, research, executive, governance — each with a
role, tools, permissions, memory policy, **bounded escalation rules**,
eval metrics, and a risk class. `validate_template` enforces
`no_unbounded_agents`: no escalation path, no risk class, or a
forbidden tool means the template never compiles. `to_agent_spec`
compiles a template into the runtime `AgentSpec` used by `ai_workforce`.

### 2.3 Governance System
The AI policy engine: risk classes, action modes, human approval rules.
AI recommends; humans approve external actions. Backed by
`governance_os` and `trust_os`.

### 2.4 Knowledge OS
Permission-aware, citation-grounded retrieval. `grounded_retrieval.py`
adds RBAC and tenant filtering on top of `answer_with_citations`: a
source above the caller's role or from another tenant is dropped before
an answer is composed; if nothing survives, the result is
`insufficient_evidence`, never a fabricated answer.

### 2.5 Executive System
The executive command center: revenue, operations, AI impact, risks,
and opportunities in one pane. Backed by `executive_command_center` and
`founder_v10`.

### 2.6 Evaluation System
Without evals you are blind. `eval_os` defines a 4-category taxonomy —
retrieval quality, response quality, workflow quality, business
quality — with 12 metrics, paired with declarative YAML packs in
`evals/`.

### 2.7 Transformation System
Dealix sells transformation, not tools. `transformation_os` is a
5-stage lifecycle — Assessment → Pilot → Workflow Redesign →
Operational Deployment → Governance & Scale — where each stage maps to
a rung of the offer ladder and every stage transition is gated by
**verified evidence** (`no_unverified_outcomes`).

## 3. The 4-Phase Roadmap

| Phase | Focus | Gate | Status |
|---|---|---|---|
| 1. Foundation | Company OS spine, 7 systems registered, read-only API | active now | Active |
| 2. Delivery Maturity | Repeatable playbooks, QA, ROI reports | 1 paid pilot delivered | Open |
| 3. Agentic Platform | Agent runtime, orchestration, human oversight | **3 paid pilots** | Deferred-gated |
| 4. Enterprise Readiness | SSO, advanced governance, compliance, SLA | **3 paid pilots** | Deferred-gated |

Phases 3 and 4 are `deferred_gated=True`. The Operating Constitution
(Article 13) forbids activating Build-Order Phase H "Scale" and Waves
2–5 before 3 paid pilots deliver proof. `roadmap.py` encodes this:
`is_phase_active` returns False for those phases until `paid_pilots`
reaches 3. The doctrine test
`tests/governance/test_company_os_doctrine.py` enforces it.

This is deliberate. The "full 4-phase build" is executed as a governed
sequence: Foundation ships now in full; Phases 2–4 are scaffolded,
tracked, and gated — not vaporware, and not activated ahead of proof.

## 4. Doctrine Map

`company_os/doctrine_map.py` maps each of the 11 non-negotiables to the
systems that enforce it; `doctrine_coverage()` proves every
non-negotiable has at least one enforcing system. The 11:
`no_live_send`, `no_live_charge`, `no_cold_whatsapp`, `no_scraping`,
`no_fake_proof`, `no_unconsented_data`, `no_unverified_outcomes`,
`no_hidden_pricing`, `no_silent_failures`, `no_unbounded_agents`,
`no_unaudited_changes`.

## 5. The Machine-Readable Spine

`auto_client_acquisition/company_os/` is the queryable spine. The
read-only API at `/api/v1/company-os` exposes it:

| Endpoint | Returns |
|---|---|
| `GET /api/v1/company-os/systems` | The 7 systems registry |
| `GET /api/v1/company-os/systems/{id}` | One system |
| `GET /api/v1/company-os/maturity` | Maturity scores for all 7 |
| `GET /api/v1/company-os/roadmap?paid_pilots=N` | 4-phase roadmap with live activation status |
| `GET /api/v1/company-os/doctrine` | 11 non-negotiables × systems |
| `GET /api/v1/company-os/agent-factory/templates` | Agent templates + validation status |
| `GET /api/v1/company-os/eval/metrics` | 4-category eval taxonomy |
| `GET /api/v1/company-os/transformation/stages` | 5 transformation stages |

Every endpoint is read-only and returns a `governance_decision` field.

## 6. Related Doctrine

- `docs/DEALIX_OPERATING_CONSTITUTION.md` — the 17 binding articles
- `docs/COMMERCIAL_WIRING_MAP.md` — the 11 non-negotiables
- `docs/strategic/DEALIX_EXECUTION_WAVES_AR.md` — the 5 execution waves
- `docs/OFFER_LADDER_AND_PRICING.md` — the offer ladder the
  Transformation System stages map onto
