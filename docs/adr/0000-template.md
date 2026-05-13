---
title: ADR-0000 Template (Michael Nygard format)
doc_id: W4.T21.adr-0000-template
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0001, W4.T21.adr-0002, W4.T21.adr-0003, W4.T21.adr-0004, W4.T21.adr-0005]
kpi: { metric: adr_coverage_percent, target: 100, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.9, effort: 0.1pw, score: engineering }
---

# ADR-NNNN: <Short Decision Title>

> **Decision (one sentence, bold):** State the single architectural choice in 25 words or fewer. Example: **We will use PostgreSQL as the canonical event store and reserve in-memory storage for unit tests only.**

## Context

Describe the forces, constraints, and current state that motivate this decision. Numbers preferred over adjectives.

Required sub-items:

- **Problem statement** (2–4 sentences).
- **Current state** in the repo (file paths, e.g. `auto_client_acquisition/revenue_memory/event_store.py`).
- **Constraints** — regulatory (PDPL, ZATCA), latency budgets (e.g. p95 < 250 ms), tenancy model, cost envelope (USD/month or SAR/month), team capacity (person-weeks available).
- **Stakeholders** — CTO, Head of Data, SRE lead, Compliance owner, CEO sign-off if customer-facing.
- **Forcing function** — pricing tier launch, regulatory deadline, SLA contract, incident root-cause.

## Decision

Repeat the bolded one-sentence decision and elaborate in 100–200 words. Cover:

1. **What** exactly is adopted.
2. **Scope** — services, environments (dev/stage/prod), tenants (Starter/Growth/Sovereign).
3. **Boundary** — what is explicitly out of scope.
4. **Migration trigger** — version, date, or event that initiates rollout.
5. **Owner of record** — single named role accountable for runtime behavior.

## Status

One of:

- `Proposed` — drafted, under review.
- `Accepted` — approved by CTO + relevant domain owner; in effect.
- `Deprecated` — superseded; link to replacing ADR.
- `Superseded by ADR-NNNN` — explicit link.

Include date of last status change.

## Consequences

### Positive

- Bullet list of expected gains: latency win, cost reduction (% or SAR), reliability uplift (SLO points), compliance posture.
- Each bullet must be **measurable** within 90 days of acceptance.

### Negative

- Bullet list of costs: engineering effort (person-weeks), runtime overhead (CPU/RAM), operational complexity, training burden, vendor lock-in.
- Include rollback cost (person-weeks to revert).

### Neutral / Follow-ups

- Required downstream changes (docs, dashboards, runbooks).
- Open questions to resolve within 30 days.

## Alternatives Considered

Minimum 2 alternatives. For each:

- **Name** of the alternative.
- **Why rejected** in 2–3 sentences with at least one number (cost, latency, complexity).

Example layout:

| Alternative | Reason rejected |
|---|---|
| A: keep status quo | p95 latency 1.4s violates Sovereign 300ms target |
| B: third-party SaaS | 4,200 USD/month exceeds 1,500 USD ceiling for tier |

## References

- Code anchors: file paths in `auto_client_acquisition/...`, `dealix/...`, `api/...`.
- Linked ADRs: `[ADR-NNNN](./NNNN-slug.md)`.
- External: RFCs, vendor docs, regulator notices (PDPL articles, ZATCA bulletins).

## Review Cadence

Every accepted ADR is re-reviewed quarterly by the owner. Add `last_reviewed` date to frontmatter on each pass. Word budget target: 400 words for the template; production ADRs typically run 800–1,200 words.
