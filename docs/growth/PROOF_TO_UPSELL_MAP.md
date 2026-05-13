---
doc_id: growth.proof_to_upsell_map
title: Proof to Upsell Map — Every Proof Pack Has a Next Sale
owner: CRO
status: approved
last_reviewed: 2026-05-13
audience: [internal, partner]
---

# Proof to Upsell Map

> **Binding rule** (per `DEALIX_STANDARD.md` #8): every project closes
> with a documented next step. This file is the lookup table — given
> what the Proof Pack found, here is the upsell. The CRO uses this
> table in the 14-day post-Sprint review with every paying customer.

## The map

| # | Proof Found (what the Sprint surfaced) | Meaning (what it tells the customer) | Upsell (what we offer next) |
|---|----------------------------------------|--------------------------------------|-----------------------------|
| 1 | Top-50 accounts identified + ranked + 10 next actions | Execution is the bottleneck, not knowledge | **Pilot Conversion Sprint** — 30–60 day supervised execution → Monthly RevOps |
| 2 | Data quality lifted + CRM still partially messy + lawful basis gaps | This is ongoing hygiene, not a one-time fix | **Monthly RevOps OS** — recurring data + revenue cadence |
| 3 | Support tickets categorized + repeat questions identified | An AI reply system is now a build, not a guess | **AI Support Desk Sprint** *(Phase 2)* — then Monthly Customer Support AI |
| 4 | Documents indexed + cited-answer assistant live | Documents change; the index must update too | **Monthly Brain retainer** — content audit + freshness + new section ingestion |
| 5 | One workflow automated; team identified 3 more recurring tasks | Workflow library, not one-offs | **Monthly AI Ops** — recurring automation cadence + run-history dashboards |
| 6 | Governance review surfaced PII or approval-matrix gaps | Policy is now a build, not a draft | **AI Governance Program** *(Phase 3)* — full audit + dashboard + approval matrix |
| 7 | Executive report shipped; decisions logged | Customer wants this every Monday | **Reporting retainer** — weekly executive pack ongoing |
| 8 | Capability moved L1 → L3 in one capability + adjacent capability still L1 | Next capability is the next sale | **Diagnostic-refresh + adjacent Sprint** (per `CAPABILITY_FACTORY_MAP.md`) |

## Mechanics — when the upsell is offered

| Stage | Timing | Who runs it |
|-------|--------|-------------|
| Stage 7 Prove | Day of Proof Pack delivery | CSM presents next-step proposal |
| Stage 8 Expand | 7–14 days after Proof Pack | CRO + founder review on call |
| 60-day check-in | 60 days post-Sprint | CSM revisits the unsold rows |
| Quarterly | Each quarter | CRO refreshes capability roadmap with customer |

## What an upsell proposal must include

1. The exact row from this map (referenced by # in the proposal).
2. The proof point from the Proof Pack (anonymized if needed).
3. The capability level before and target (per
   `CAPABILITY_MATURITY_MODEL.md`).
4. The KPI to be moved (per `SERVICE_KPI_MAP.md`).
5. Tier + price (per `IMPLEMENTATION_TIERS.md`).
6. Risk + governance posture (per `DEALIX_STANDARD.md`).

A proposal missing any of these 6 elements is rejected by CRO before
sending.

## Anti-patterns (auto-reject)

- Pitching a generic retainer with no proof point.
- Offering the same Sprint a customer just bought.
- Skipping the capability framing.
- Citing "best practice" instead of the Proof Pack.

## Why this works commercially

- The Proof Pack is the **buying trigger**, not the closer's pitch.
- Customers self-justify the upsell from their own evidence.
- Conversion from Sprint to Retainer (Metric 8 in
  `AI_OPS_CATEGORY_METRICS.md`) is driven by this discipline.
- Margin on upsells is higher because there is zero acquisition cost.

## Saudi context

Rows 2 and 6 (data hygiene + governance) are the upsells that most
often unlock the **enterprise contract** because Saudi procurement
attaches to data residency, PDPL compliance, and audit trail.

## Cross-links

- `docs/company/DEALIX_STANDARD.md` — #8 Expansion Planned
- `docs/company/CAPABILITY_FACTORY_MAP.md` — problem → service → expansion
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — level transitions
- `docs/company/IMPLEMENTATION_TIERS.md` — tier pricing
- `docs/company/SERVICE_KPI_MAP.md` — KPI alignment
- `docs/growth/CLIENT_JOURNEY.md` — journey cadence
- `docs/growth/RETAINER_DECISION.md` — retainer rules
- `docs/strategy/AI_OPS_CATEGORY_METRICS.md` — Sprint-to-Retainer metric
- `docs/PROOF_PACK_V6_STANDARD.md` — proof pack standard
