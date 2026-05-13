---
title: Dealix Architecture — 5-Layer Summary
doc_id: W6.T37.architecture
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T34, W6.T37]
kpi:
  metric: modules_correctly_placed_in_layer
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: engineering-foundation
---

# Dealix Architecture — 5-Layer Summary

## 1. Context

Dealix's architecture stacks into exactly five layers. Every module, every
service, every document belongs to exactly one of these layers. The layered
view is the canonical answer to "where does this thing live?" and prevents
the architecture drift that haunts service companies that have not
productized their stack.

The canonical statement is
[`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
§12. This document is the operator-friendly summary.

## 2. Audience

CTO, engineering managers, HoP, new engineers (read on Day 1), architecture
reviewers.

## 3. The 5 Layers

```
┌────────────────────────────────────────────────────┐
│ 1. Service Catalog                                 │  Offers, prices, scopes, outcomes
│    docs/strategy/service_portfolio_catalog.md      │
├────────────────────────────────────────────────────┤
│ 2. Delivery OS                                     │  Intake, checklist, QA, report,
│    auto_client_acquisition/delivery_factory/       │  proof, handoff, renewal
├────────────────────────────────────────────────────┤
│ 3. Product OS                                      │  Data / Revenue / Customer /
│    auto_client_acquisition/{revenue_os,            │  Operations / Knowledge OS
│      customer_data_plane, orchestrator,            │
│      knowledge_v10, ...}                           │
├────────────────────────────────────────────────────┤
│ 4. Trust OS                                        │  Governance, approvals,
│    dealix/trust/                                   │  redaction, audit, event
│                                                    │  store, decision passport
├────────────────────────────────────────────────────┤
│ 5. AI Platform                                     │  LLM gateway, agents,
│    dealix/llm_gateway/, ai_workforce/              │  evals, observability
└────────────────────────────────────────────────────┘
```

## 4. Layer Roles

### 4.1 Service Catalog (Layer 1)
The customer-facing surface. Offers, prices, scopes, outcomes. The catalog
sells; the layers below deliver.

### 4.2 Delivery OS (Layer 2)
Productizes Layer 1. Takes a sold offering and runs it through the 8-stage
Delivery Standard. Owns intake, scope, QA, handoff, renewal. Without this
layer, services drift into bespoke consulting.

### 4.3 Product OS (Layer 3)
The capability stack — Data Quality, Scoring, Workflow, Outreach,
Knowledge, Reporting. Layer 2 composes these to deliver Layer 1's
offerings.

### 4.4 Trust OS (Layer 4)
Universal gate. Every action in Layer 3 passes through Trust before
egressing. Governance, approvals, PII, audit, decision passport. No
exceptions.

### 4.5 AI Platform (Layer 5)
The AI substrate beneath everything. LLM routing, evals, agents,
observability. Provides the models that Layers 3 uses; Layer 4 gates the
calls.

## 5. Dependency Rules

- **Layers depend downward only**: Layer 2 depends on 3, 4, 5; Layer 4
  may depend on 5; Layer 1 depends on 2.
- **No cross-layer skipping**: a customer-facing surface never bypasses
  Trust to talk directly to the AI Platform.
- **Governance is universal**: every Layer 3 call routes through Layer 4
  pre-action checks.

## 6. Where to Put New Code

| New thing | Goes in layer |
|-----------|---------------|
| A new customer offer page | 1 |
| A new QA gate question | 2 |
| A new scoring model | 3 |
| A new approval action kind | 4 |
| A new model integration | 5 |

If a new piece of code does not fit one of these layers, the layer model
is incomplete — escalate to CTO. Do not create a sixth layer informally.

## 7. Cross-links

- Canonical statement: [`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md) §12
- OS modules: [`internal_os_modules.md`](internal_os_modules.md)
- Module map: [`MODULE_MAP.md`](MODULE_MAP.md)
- API spec: [`API_SPEC.md`](API_SPEC.md)
- Data model: [`DATA_MODEL.md`](DATA_MODEL.md)
- ADRs: [`../adr/`](../adr/)

## 8. Owner & Review Cadence

- **Owner**: CTO.
- **Review**: quarterly; immediate on any architecture change discussion.

## 9. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial 5-layer summary (Service Catalog / Delivery / Product / Trust / AI) |
