# Board Memo Automation

## Cadence

Monthly (or pre-board meeting) memo generated from internal signals + scorecards. v1 is **template + deterministic sections**; later: pull from Revenue Memory / proof ledger.

## Required sections (Markdown)

1. Executive Summary
2. Revenue Quality
3. Proof & Value
4. Retainer Opportunities
5. Governance & Risk
6. Productization Queue
7. Client Health
8. Market Intelligence
9. Business Unit Maturity
10. Stop / Kill List
11. Capital Allocation
12. Next Strategic Bets

## Why it matters

Even for a solo founder, the memo forces **CEO cognition** (bets, kill list, capital). Over time it becomes diligence-ready evidence that Dealix is operated as a system, not ad-hoc execution.

## API

`GET /api/v1/board-decision-os/board-memo-template` returns section headings + placeholder guidance.

`POST /api/v1/board-decision-os/board-memo` accepts structured metrics JSON and returns filled Markdown (deterministic).
