---
title: Scope Control — What Counts as Creep and How We Hold the Line
doc_id: W6.T36.scope-control
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W5.T18, W5.T10]
kpi:
  metric: in_scope_delivery_rate
  target: 95
  window: per_project
rice:
  reach: 0
  impact: 2
  confidence: 0.85
  effort: 0.5
  score: delivery-operating
---

# Scope Control

## 1. Context

The single biggest threat to a fixed-fee Sprint or Pilot is silent scope
creep. Engineering capacity disappears into requests that were never
budgeted, margin evaporates, and the project misses its timebox. Holding
scope discipline is therefore a productization discipline — Dealix does not
deliver bespoke consulting at sprint prices.

## 2. Audience

CSM (project owner), assigned engineer, AE, day-to-day owner on the customer
side. Anyone who can receive a customer request — Slack, email, kickoff
side-comment — needs to apply the same filter.

## 3. What Counts as Scope Creep

Anything **not** explicitly listed in the signed SOW or design doc is creep.
Canonical patterns:

| Pattern | Example | Why it's creep |
|---------|---------|----------------|
| Extra workflow | "Can you also classify support tickets?" on a Lead Engine Sprint | Different OS module, different QA gates |
| Extra vertical | "Add construction sector while you're at it" | Different ICP, different scoring rules |
| Extra integration | "Push results into our PowerBI too" | New connector, new auth, new schema |
| Extra users | "Add 8 more seats to the pilot" | Pricing tier shift; training overhead |
| Extra geography | "Run this for UAE too" | New regulatory perimeter (no PDPL ≠ no compliance) |
| Custom UI | "Can we get a custom dashboard skin?" | Bespoke front-end — not productized |
| Bespoke logic | "Hard-code these 12 exception rules in code" | Config vs code (see `internal_os_modules.md` §6) |

## 4. The Three-Question Filter

Before saying yes to ANY new request mid-flight, the CSM asks:

1. Is this listed in the signed SOW or design doc? → **Yes** = do it.
2. Can it be deferred to Stage 8 (Expand) without missing this project's KPIs? → **Yes** = log as expansion opportunity in CRM.
3. Is it small (< 4 engineer-hours) AND unblock-critical for current scope? → **Yes** = absorb but log in change ledger; warn customer if it recurs.

Everything else routes to the **Change Request Process** —
see [`CHANGE_REQUEST_PROCESS.md`](CHANGE_REQUEST_PROCESS.md).

## 5. How to Say No (Examples)

- *"That's a great fit for Stage 8 expansion — let's scope it after handoff. I'll add it to the proposal."*
- *"To add that mid-flight, we'd need a short scope amendment (price + 5 days). Want me to send it?"*
- *"Outside this Sprint's scope, but we have a Workflow Automation Sprint that's the right shape for it. I'll send the offer."*

Saying no protects the customer's timebox as much as ours.

## 6. Anti-Patterns

- **Quiet absorption**: the engineer just builds the extra thing because "it's small". Margin gone, future requests calibrated to "free".
- **Verbal yeses**: a "we'll see" in a meeting becomes a contractual expectation. Always write it down — yes, no, or change request.
- **Sponsor bypass**: day-to-day owner adds scope; exec sponsor never sees it. Always loop the sponsor for scope shifts.

## 7. Cross-links

- Change request: [`CHANGE_REQUEST_PROCESS.md`](CHANGE_REQUEST_PROCESS.md)
- Lifecycle: [`DELIVERY_LIFECYCLE.md`](DELIVERY_LIFECYCLE.md)
- Pilot framework (pilots have stricter scope): [`pilot_framework.md`](pilot_framework.md)
- Expansion playbook: [`../customer-success/expansion_playbook.md`](../customer-success/expansion_playbook.md)
- OS modules (config vs code): [`../product/internal_os_modules.md`](../product/internal_os_modules.md)

## 8. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: after every 5 closed projects — refresh the canonical creep
  patterns table with what was actually seen.

## 9. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial scope-creep patterns + three-question filter |
