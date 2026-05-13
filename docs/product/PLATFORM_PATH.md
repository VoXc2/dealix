---
doc_id: product.platform_path
title: Platform Path — From Internal Tools to Service-Assisted SaaS
owner: CTO
status: approved
last_reviewed: 2026-05-13
audience: [internal, board]
---

# Platform Path

> Dealix is **not a SaaS company yet** and will not pretend to be.
> The platform graduates through 5 stages, each gated by paid
> evidence. Skipping a stage produces a SaaS that no Saudi enterprise
> buys.

## The 5 stages

| Stage | Name | What customers see | What we ship | Gate to next stage |
|------:|------|--------------------|--------------|---------------------|
| 1 | Internal tools | Nothing | Internal scripts, agents, ledgers, QA, reporting code | Same scripts run 5+ deliveries identically |
| 2 | Client-visible reports | Executive reports, Proof Packs, Capability Roadmap | Outputs that look standardized across all customers | 10 customers see the same report style; QA ≥ 85 floor holds |
| 3 | Client workspace | A workspace with their data, reports, capability roadmap | Read-mostly portal: dashboards + Proof Packs + ledgers | 10+ paid Sprints + 3+ retainers with the portal in active use |
| 4 | Self-serve modules | Ability for the customer to trigger limited workflows themselves | Selected agent runs gated by approval matrix | 15+ retainers; LLM cost per customer < 30% of revenue per customer |
| 5 | SaaS | Sign up, pay, use, mostly without Dealix humans | Productized self-serve platform | All of Stage 4 + 25+ customers paying for Stage 4 with NRR ≥ 110% |

## Where Dealix is today

Stage 1 → Stage 2 transition. Per `12_MONTH_ROADMAP.md`, 2026 ships
Stage 3 to first cohort.

## Hard rule (binding)

**No move to SaaS (Stage 5) before service-assisted SaaS (Stage 4) is
proven across 15+ retainers.** This is the single most common failure
mode for AI Operations companies in 2025–2026: they jump from
internal tools to SaaS without a base of operating customers, and the
product is rejected by Saudi procurement because it does not include
the operating model the buyer is actually paying for.

## What "service-assisted SaaS" means concretely

At Stage 4 the customer logs in and can run gated workflows; Dealix
CSM still attends the monthly review, files the Proof Pack (now
mostly auto-generated), and owns governance posture. The customer
never feels alone with software, never feels dependent on a single
person.

## Architecture commitments per stage

| Stage | Required architectural property |
|------:|--------------------------------|
| 1 | Append-only event store (`event_store.py`) |
| 2 | Schema-bound agent outputs + 100-point QA in code |
| 3 | Multi-tenant isolation (per `docs/adr/0003-multi-tenant-isolation.md`); RBAC designed |
| 4 | Customer-managed approval matrix; in-Kingdom residency; per-tenant cost cap |
| 5 | SSO + BYOK + audit-log export + Enterprise Controls Matrix passing |

## Anti-patterns (auto-reject)

- Building Stage 5 features before Stage 4 retainers exist.
- Letting "the portal" become the value proposition (the value is the
  capability, the portal is the surface).
- Releasing self-serve modules without the approval matrix in place
  (governance regression).
- Hiding Dealix humans behind the portal to look more SaaS-like (the
  buyer can tell).

## Why this matters commercially

| Stage | Revenue mix expected |
|------:|----------------------|
| 1 | 100% service revenue |
| 2 | 95% service / 5% productized |
| 3 | 70% service / 30% productized |
| 4 | 40% service / 60% productized |
| 5 | 10% service / 90% SaaS |

The Stage 4 mix is where Dealix's margin and category leadership
both peak. Stage 5 is opportunistic, not aspirational.

## Saudi context

Saudi enterprise procurement attaches strongly to the operating
model behind the platform (audit trail, governance, in-Kingdom
residency, sovereign options). A Stage 5 SaaS without the operating
model behind it is uncompetitive against Stage 4 with the operating
model. This is Dealix's positioning advantage.

## Cross-links

- `docs/strategy/FROM_SERVICE_TO_STANDARD.md` — company-level 5-stage arc (parallel)
- `docs/product/PRODUCT_ROADMAP.md` — feature-level roadmap
- `docs/product/ARCHITECTURE.md` — system architecture
- `docs/product/internal_os_modules.md` — 9 OS modules
- `docs/product/AI_AGENT_INVENTORY.md` — 10 agents
- `docs/adr/0003-multi-tenant-isolation.md` — Stage 3 enabler
- `docs/enterprise/CONTROLS_MATRIX.md` — Stage 5 gate
- `docs/company/SCALE_DECISION.md` — when to scale platform
- `docs/strategy/12_MONTH_ROADMAP.md` — near-term milestones
