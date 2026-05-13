---
title: Module Map — OS Module Directory and Phase State
doc_id: W6.T37.module-map
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T34, W6.T37]
kpi:
  metric: phase1_modules_in_production
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: engineering-foundation
---

# Module Map

## 1. Context

Each OS module has a name, a directory, an owner, and a phase state.
This file is the single index. The canonical module catalog with scope,
KPIs, and dependencies is [`internal_os_modules.md`](internal_os_modules.md);
the phase plan is [`PRODUCT_ROADMAP.md`](PRODUCT_ROADMAP.md).

## 2. Audience

CTO, engineering managers, HoP, on-call engineers, new starters orienting
themselves.

## 3. The Map

| # | Module | Directory | Owner | Phase State |
|---|--------|-----------|-------|-------------|
| 1 | **Intake OS** | `api/routers/onboarding.py`, planned `dealix/intake/` | HoP | Phase 1 — done (gap-fills queued) |
| 2 | **Data Quality OS** | `auto_client_acquisition/revenue_os/{dedupe,enrichment_waterfall}.py`, `customer_data_plane/{validation_rules,data_quality_score}.py`, planned `dealix/data_quality/` | HoData | Phase 1 — done; Phase 2 hardening pending |
| 3 | **Scoring OS** | `auto_client_acquisition/revenue_os/{signal_normalizer,scoring}.py` | HoData | Phase 2 — pending production hardening |
| 4 | **Workflow OS** | `auto_client_acquisition/orchestrator/runtime.py`, planned `dealix/workflows/` | CTO | Phase 2 — pending productization |
| 5 | **Knowledge OS (RAG)** | `auto_client_acquisition/knowledge/`, planned `dealix/knowledge/` | HoP | Phase 2 — spike → production pending |
| 6 | **Outreach OS** | `auto_client_acquisition/revenue_os/action_catalog.py`, planned `dealix/outreach/` | HoP | Phase 2 — pending integration with Approval Matrix |
| 7 | **Reporting OS** | `api/routers/reports.py`, `frontend/components/dashboards/`, `dealix/reporting/` | HoP | Phase 1 — done |
| 8 | **Governance OS (Trust)** | `dealix/trust/{policy,approval,approval_matrix,pii_detector,forbidden_claims,audit}.py` | HoLegal + CTO | Phase 1 — done |
| 9 | **Delivery OS** | `auto_client_acquisition/delivery_factory/` (intake / scope_builder / delivery_checklist / qa_review / client_handoff / renewal_recommendation / stage_machine / event_writer) | HoCS + CTO | Phase 1 — done |

## 4. Phase State Legend

- **Phase 1 — done**: in production, used in customer delivery, audited.
- **Phase 1 — done (gap-fills queued)**: in production with declared
  smaller upgrades on the backlog.
- **Phase 2 — pending**: scoped for Phase 2; spike or partial production.
- **Phase 3 — productize**: pending customer-portal / console exposure.
- **Phase 4 — integrate**: pending external integrations (CRM / inbox /
  billing). See [`INTEGRATION_STRATEGY.md`](INTEGRATION_STRATEGY.md).

## 5. Dependency Graph

```
Intake → Data Quality → Scoring → Workflow → Outreach
                        ↓           ↓
                     Reporting ← Knowledge
                        ↑
                  Governance (gates every other module's outputs)
```

Per [`internal_os_modules.md`](internal_os_modules.md) §4. Governance is
the universal gate; Reporting is the universal sink; Intake is the
universal entry.

## 6. Module-Level KPIs

Each module has a KPI listed in [`internal_os_modules.md`](internal_os_modules.md)
§5. Top-line targets:

- Intake: time-to-onboarded < 1h (SME).
- Data Quality: pass rate ≥ 98%.
- Scoring: calibration error < 5%.
- Workflow: durable run success ≥ 99.5%.
- Knowledge: citation-grounded answer rate ≥ 95%.
- Outreach: policy-gated rejection 100% of violations.
- Reporting: dashboard freshness < 24h.
- Governance: audit log completeness 100%.
- Delivery: project intake → signed scope < 3 business days.

## 7. Cross-links

- Canonical module catalog: [`internal_os_modules.md`](internal_os_modules.md)
- Roadmap: [`PRODUCT_ROADMAP.md`](PRODUCT_ROADMAP.md)
- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- API spec: [`API_SPEC.md`](API_SPEC.md)
- Service readiness: [`../quality/SERVICE_READINESS_SCORE.md`](../quality/SERVICE_READINESS_SCORE.md)
- Integration strategy: [`INTEGRATION_STRATEGY.md`](INTEGRATION_STRATEGY.md)

## 8. Owner & Review Cadence

- **Owner**: CTO.
- **Review**: quarterly module health + phase-state refresh.

## 9. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial mapping of 9 modules to directories + phase state |
