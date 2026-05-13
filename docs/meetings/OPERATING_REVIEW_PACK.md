---
doc_id: meetings.operating_review_pack
title: Operating Review Pack — The Monday Meeting Document
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
---

# Operating Review Pack

> The pack that walks into the Monday Operating Review. Mirrors
> `WEEKLY_OPERATING_REVIEW.md`, but in **pack form** — sections the
> attendees read on screen, in order, before the 3 decisions are
> made. Filed weekly to `docs/meetings/packs/<YYYY-MM-DD>.md` (copy
> from this template).

## Pack metadata

- **Week of**: YYYY-MM-DD
- **Held**: Monday 09:00
- **Attendees**: CEO, CTO, HoCS, CRO
- **Prep owner**: HoCS (numbers) + CEO (narrative)
- **Output**: 3 decisions filed to `DECISION_LEDGER.md`

## Section 1 — Revenue

| Metric | This week | Last week | Δ | Target (week) |
|--------|-----------|-----------|---|---------------|
| New leads (top of funnel) | | | | |
| Calls held | | | | |
| Proposals sent | | | | |
| Closed revenue (SAR) | | | | |
| Retainer opportunities surfaced | | | | |
| MRR end of week (SAR) | | | | per `12_MONTH_ROADMAP.md` |

**Narrative**: top 3 deals + biggest pipeline risk this week.

## Section 2 — Delivery

| Item | Count | Notes |
|------|-------|-------|
| Active projects | | |
| On track | | |
| At risk | | reason + owner |
| QA issues this week | | |
| Proof Packs due | | |
| Proof Packs delivered | | within 14d? |
| Capability levels advanced | | per `CAPABILITY_MATURITY_MODEL.md` |

**Narrative**: any project blocked by data / governance / approvals.

## Section 3 — Product

| Item | Value |
|------|-------|
| Manual steps logged (count) | |
| Feature candidates promoted | per `FEATURE_PRIORITIZATION.md` |
| Bugs / regressions | |
| LLM cost MTD | per `MODEL_PORTFOLIO.md` |
| Platform stage progress | per `PLATFORM_PATH.md` |

**Narrative**: 1 product decision needed this week.

## Section 4 — Governance

| Item | Count | Notes |
|------|-------|-------|
| Risk events | | from `GOVERNANCE_LEDGER.md` |
| PII issues | | |
| Approval gaps | | |
| Forbidden-action blocks | | |
| PDPL register updates | | |

**Narrative**: any incident requiring HoLegal escalation.

## Section 5 — Market

| Item | Value |
|------|-------|
| Content published | per `MARKET_AND_PARTNER_STRATEGY.md` |
| Partner activity | per `PARTNER_OUTREACH_PLAN.md` |
| Reference customer asks | |
| Case studies in flight | per `ASSET_GRADUATION_SYSTEM.md` |

**Narrative**: which sector is heating up this week.

## Section 6 — Decisions

CEO closes the meeting with exactly **3 decisions**, no more, drawn
from the 7 weekly questions in `WEEKLY_OPERATING_REVIEW.md`:

1. **Decision 1**: [name] · Owner: [name] · Deadline: [date] ·
   Evidence-of-done: [link]
2. **Decision 2**: [name] · Owner: [name] · Deadline: [date] ·
   Evidence-of-done: [link]
3. **Decision 3**: [name] · Owner: [name] · Deadline: [date] ·
   Evidence-of-done: [link]

Each decision is filed to `DECISION_LEDGER.md` before the meeting
ends.

## Monthly extension — Operating Intelligence

The last Monday of each month adds a 60-minute extension to walk the
7 monthly questions in `OPERATING_INTELLIGENCE.md`. The pack is
extended with one section per question, evidenced from the 8
ledgers. Output: up to 7 decisions (one per question, or explicit
"no change").

## Anti-patterns

- A pack with narrative but no numbers (defer the meeting).
- A pack with numbers but no decisions (the meeting failed).
- Adding sections beyond the 6 (scope creep — split the meeting).
- Reading the pack during the meeting instead of before.

## Rule

The pack is **published Monday 08:00** (one hour before the
meeting). Attendees who haven't read it lose voting rights on the 3
decisions.

## Saudi / PDPL context

Section 4 (Governance) is the binding section. Any PDPL-relevant
risk event surfaced here is escalated to HoLegal within 24h, before
the Wednesday standup.

## Cross-links

- `docs/company/WEEKLY_OPERATING_REVIEW.md` — the underlying review
- `docs/company/OPERATING_INTELLIGENCE.md` — monthly extension
- `docs/company/OPERATING_LEDGER.md` — the 8 ledgers feeding sections
- `docs/company/CONTROL_PLANE.md` — aggregation
- `docs/company/FOUNDER_COMMAND_CENTER.md` — founder dashboard
- `docs/company/DECISION_RULES.md` — binding rules
- `docs/operations/executive_operating_cadence.md` — cadence detail
- `docs/strategy/12_MONTH_ROADMAP.md` — targets
