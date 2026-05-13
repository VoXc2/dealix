---
title: Dealix Internal OS Modules — Architecture and Module Catalog
doc_id: W6.T34.os-modules
owner: CTO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W6.T32, W6.T33, W1.T31, W4.T14, W4.T22, W4.T25]
kpi:
  metric: module_reuse_index
  target: 80%
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 4
  score: engineering
---

# Dealix Internal OS Modules

## 1. Context

The 30+ customer-facing offerings in the service portfolio (W6.T33) are built from **eight reusable internal modules**. Engineering capacity is allocated against modules, not against bespoke per-customer features. This document is the canonical module catalog: scope, code location, interfaces, dependencies, and module-level KPIs.

The rule: a new offering must reuse existing modules. A new module is justified only when an offering's needs cannot be expressed as a composition of existing modules — and requires CTO + HoP sign-off.

## 2. Audience

CTO, engineering managers, product. Used in roadmap planning (W1.T11) to size capacity per module.

## 3. The eight modules

### 3.1 Intake OS

- **Scope**: collects company info, goals, files, channels, data, problems from new customers.
- **Surfaces**: web onboarding form, CSV import, CRM integration, partner API.
- **Code location** (current/target): `api/routers/onboarding.py`, planned `dealix/intake/`.
- **Outputs**: normalized customer profile + initial data inventory + use-case backlog.
- **Powers**: all pillars.
- **Module SLA**: complete intake in < 60 minutes for SME, < 1 business day for Enterprise.

### 3.2 Data Quality OS

- **Scope**: validation, dedupe, normalization, source attribution, PII detection, quality scoring.
- **Surfaces**: `POST /api/v1/data-quality/check`, async batch jobs.
- **Code location**: `auto_client_acquisition/revenue_os/dedupe.py`, `auto_client_acquisition/revenue_os/enrichment_waterfall.py`, planned `dealix/data_quality/`.
- **Outputs**: cleaned dataset + quality report + repair recommendations.
- **Powers**: Grow Revenue, Serve Customers, Automate Operations, Build Company Brain.
- **Quality gates**: see W4.T25.

### 3.3 Scoring OS

- **Scope**: feature-based scoring, model registry, explainability, calibration.
- **Surfaces**: `POST /api/v1/scoring/score`, model versioning API.
- **Code location**: `auto_client_acquisition/revenue_os/signal_normalizer.py`, `auto_client_acquisition/revenue_os/scoring.py`.
- **Outputs**: scored entities (leads / tickets / risks / opportunities) with explanations.
- **Powers**: Grow Revenue (lead ranking), Automate Operations (risk scoring), Forecasting.

### 3.4 Workflow OS

- **Scope**: durable workflows, retries, approvals, handoffs, audit trails.
- **Surfaces**: `POST /api/v1/workflows/{flow_id}/run`, webhooks, CLI.
- **Code location**: `auto_client_acquisition/orchestrator/runtime.py`, planned `dealix/workflows/`.
- **Outputs**: completed workflow run with full event trail.
- **Powers**: Automate Operations, Serve Customers.

### 3.5 Knowledge OS (RAG)

- **Scope**: document ingestion, citation-based answers, permissions, freshness tracking.
- **Surfaces**: `POST /api/v1/knowledge/query`, document management API.
- **Code location**: planned `dealix/knowledge/`; current spike: `auto_client_acquisition/knowledge/`.
- **Outputs**: cited answers, document indexes, freshness reports.
- **Powers**: Build Company Brain, Serve Customers, HR Assistant.

### 3.6 Outreach OS

- **Scope**: drafts, templates, tone control, AR/EN switching, prohibited claim filters, send orchestration.
- **Surfaces**: `POST /api/v1/outreach/draft`, `POST /api/v1/outreach/send`.
- **Code location**: `auto_client_acquisition/revenue_os/action_catalog.py`, planned `dealix/outreach/`.
- **Outputs**: drafted messages + approval requests + send results + delivery telemetry.
- **Powers**: Grow Revenue, Serve Customers, Content Engine.
- **Policy gates**: PDPL Art. 13/14 enforced via W4.T14 policy rules.

### 3.7 Reporting OS

- **Scope**: dashboards, scheduled reports, ad-hoc queries, exports.
- **Surfaces**: `GET /api/v1/reports/{report_id}`, dashboard UI.
- **Code location**: `api/routers/reports.py`, `frontend/components/dashboards/`.
- **Outputs**: executive reports, KPI dashboards, proof packs.
- **Powers**: all pillars; canonical KPI source is W4.T13.

### 3.8 Governance OS

- **Scope**: PDPL controls, approval matrix, PII redaction, audit logs, forbidden-action enforcement.
- **Surfaces**: `POST /api/v1/policy/check`, `GET /api/v1/audit/events`, Decision Passport stamping.
- **Code location**: `dealix/trust/policy.py`, `api/routers/decision_passport.py`, `auto_client_acquisition/revenue_memory/event_store.py`.
- **Outputs**: policy decisions, audit events, compliance reports.
- **Powers**: every pillar (mandatory — no action runs without a passport-stamped policy check).

## 4. Module dependency graph

```
Intake → Data Quality → Scoring → Workflow → Outreach
                        ↓           ↓
                     Reporting ← Knowledge
                        ↑
                  Governance (gates every other module's outputs)
```

Governance OS is the universal gate. Reporting OS is the universal sink. Intake OS is the universal entry.

## 5. Module-level KPIs

| Module | KPI | Target |
|---|---|---|
| Intake | Time-to-onboarded (SME / Enterprise) | < 1h / < 1bd |
| Data Quality | Quality gate pass rate (W4.T25) | ≥ 98% |
| Scoring | Calibration error (per cohort) | < 5% |
| Workflow | Durable run success rate | ≥ 99.5% |
| Knowledge | Citation-grounded answer rate | ≥ 95% |
| Outreach | Policy-gated rejection rate (caught before send) | 100% of violations |
| Reporting | Dashboard freshness (T13) | < 24h |
| Governance | Audit log completeness | 100% of policy-relevant events |

## 6. Module governance rules

1. **No customer-bespoke features**: customer-specific logic lives in configuration, not code.
2. **One owner per module**: each module has a named engineering owner who approves PRs touching it.
3. **API versioning**: per ADR 0005, modules expose versioned APIs; breaking changes have a 12-month deprecation window.
4. **Cost accountability**: each module reports monthly LLM/compute cost (W4.T24 FinOps).
5. **SLO ownership**: each module has its own SLO (W4.T23).
6. **Policy by default**: every module call passes through Governance OS — exceptions require explicit, audited bypass tokens.

## 7. Cross-links

- Positioning: `docs/strategy/dealix_operating_partner_positioning.md`
- Portfolio: `docs/strategy/service_portfolio_catalog.md`
- Lead Engine (flagship Grow Revenue offering): `docs/product/saudi_lead_engine.md`
- Policy rules: `docs/policy/revenue_os_policy_rules.md`
- Data quality: `docs/data/data_quality_gates.md`
- SLO: `docs/sre/slo_framework.md`
- ADRs: `docs/adr/`

## 8. Owner & Review Cadence

- **Owner**: CTO. Each module has a named engineering owner.
- **Review**: quarterly module health review; monthly cross-module dependency review.

## 9. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial 8-module catalog: scope, code locations, KPIs, governance rules |
