---
doc_id: company.operating_intelligence
title: Operating Intelligence — Monthly Questions from the Ledgers
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
---

# Operating Intelligence

> The 8 ledgers (`OPERATING_LEDGER.md`) are useless if no one asks them
> the right questions. Operating Intelligence is the monthly close-out
> ritual that turns ledger rows into pricing, hiring, productization,
> and stop-doing decisions.

## When this runs

Last Monday of every month, 60 minutes, inside the Monday Operating
Review (`WEEKLY_OPERATING_REVIEW.md`). CEO leads. CRO + HoCS attend.
Output: 1 decision per question (or an explicit "no change"), filed to
`docs/ledgers/DECISION_LEDGER.md`.

## The 7 monthly questions

| # | Question | Source ledgers | Decision shape |
|---|----------|---------------|----------------|
| 1 | Which service generated the highest gross margin this month? | Delivery + Proof + Client | Raise price OR replicate scope |
| 2 | Which service has the highest Sprint-to-Retainer conversion rate over the trailing 90 days? | Client + Delivery | Make it the default Sprint offer |
| 3 | Which sectors produced ≥2 paid Sprints AND a Quality Score ≥ 85 average? | Client + Delivery | Promote the sector playbook; target similar accounts |
| 4 | Which QA gate failed most often this month? | Delivery (QA score breakdown) | Build a feature OR fix the template OR retrain the operator |
| 5 | Which risks / approval-denials repeated ≥3 times? | Governance | Publish a policy entry; tighten approval matrix |
| 6 | Which manual step repeated ≥3 times and saved ≥1 hour each time when automated? | Product (Feature Candidate) | Promote to product backlog (per `FEATURE_PRIORITIZATION.md`) |
| 7 | Which proof type generated the highest reply-rate when used in outbound? | Proof + Request | Make it the lead artifact in sales decks |

## The 7 decision types (only these are allowed)

1. **Raise price** (per `PRICING_DECISION.md`) — when Q1 / Q2 evidence supports it.
2. **Stop selling a service** (per `STOP_DOING.md`) — when QA score average < 80 over 3 deliveries or zero conversion to retainer over 5 sales calls.
3. **Build a product feature** (per `FEATURE_PRIORITIZATION.md`) — Q6 trigger only.
4. **Create / update a sector playbook** (per `docs/playbooks/`) — Q3 trigger.
5. **Publish content / case study** (per `MARKET_AND_PARTNER_STRATEGY.md`) — Q7 trigger.
6. **Target a sector in outbound** (per `DAILY_OUTREACH_PLAN.md`) — Q3 trigger.
7. **Hire a role** (per `CAPACITY_AND_HIRING.md`) — only when delivery capacity is the documented bottleneck across 3 consecutive weeks.

## What this prevents

- Pricing by gut feel.
- Building features no customer paid for.
- Selling services with no margin.
- Outbound to sectors that never close.
- Hiring before the ledgers show the bottleneck.

## What "no decision" means

If a question has no evidence (e.g., fewer than 2 paid Sprints in a
sector), the answer is **defer + collect more evidence**, not invent.
The Operating Intelligence ritual is anti-speculation.

## Saudi / PDPL note

Q5 (repeating risks) is the surface-area where PDPL incidents
accumulate. Any Governance Ledger entry tagged `pdpl` or `approval_gap`
that recurs ≥3× is escalated to HoLegal in the same review.

## Cross-links

- `docs/company/OPERATING_LEDGER.md` — the 8 ledgers
- `docs/company/WEEKLY_OPERATING_REVIEW.md` — host ritual
- `docs/company/DECISION_RULES.md` — binding CEO rules
- `docs/company/CONTROL_PLANE.md` — feeds these questions
- `docs/company/STOP_DOING.md` — service de-listing
- `docs/company/PRICING_DECISION.md` — pricing changes
- `docs/product/FEATURE_PRIORITIZATION.md` — feature promotion
- `docs/meetings/OPERATING_REVIEW_PACK.md` — meeting pack template
