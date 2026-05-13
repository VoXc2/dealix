# Delivery Checklist — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Revenue
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [delivery_checklist_AR.md](./delivery_checklist_AR.md)

## Context
This document is the **day-by-day operational script** for delivering the Lead Intelligence Sprint. It is the single source of truth that Delivery Leads, Analysts, and Copy Leads work from. It exists because every Dealix Sprint must be reproducible and auditable, per `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the quality regime in `docs/quality/QUALITY_STANDARD_V1.md`. Every checkbox below maps to a row in the proof pack events log.

## Roles
- **Delivery Lead (DL)** — owns the sprint end-to-end. Single accountable person.
- **Analyst (AN)** — owns data work, scoring, deduplication.
- **Copy Lead (CL)** — owns the outreach draft pack.
- **QA Reviewer (QA)** — independent reviewer, signs off before client preview.
- **Client Sponsor (CS)** — accepts final delivery.
- **Client Reviewer (CR)** — daily client point of contact during sprint.

## Day-by-Day Plan

### T-5 to T-1 — Pre-kickoff
- [ ] Welcome email sent with SFTP creds, intake summary, and Day 1 agenda. (Owner: DL)
- [ ] Internal sprint board created in Notion. (Owner: DL)
- [ ] Risk premium re-validated against intake. (Owner: DL + Margin Controller)
- [ ] Proof pack initialized with event `sprint_initialized`. (Owner: DL)

### Day 1 — Import & Preview
- [ ] Kickoff call (30 min) with CS and CR. (Owner: DL)
- [ ] Client uploads primary export. (Owner: CR)
- [ ] Integrity check: row count, encoding, required columns present. (Owner: AN)
- [ ] First-look report sent to client: `rows imported`, `columns detected`, `obvious gaps`. (Owner: AN)
- [ ] Proof event: `rows_imported = N`. (Owner: AN)

### Day 2 — Quality Score & Dedupe
- [ ] Run completeness scoring per row. (Owner: AN)
- [ ] Deterministic dedupe (email, domain, phone hash). (Owner: AN)
- [ ] Fuzzy-match queue created for manual review. (Owner: AN)
- [ ] DL reviews queue, makes merge/keep calls. (Owner: DL)
- [ ] ICP confirmation call with Client Head of Sales (30 min). (Owner: DL)
- [ ] Scoring rubric finalized and signed off internally. (Owner: DL + AN)
- [ ] Proof event: `duplicates_removed = N`. (Owner: AN)

### Day 3 — Scoring (Pass 1)
- [ ] Apply scoring rubric to full cleaned set. (Owner: AN)
- [ ] Generate `fit_score`, `intent_score`, `recency_score`, `reachability_score`. (Owner: AN)
- [ ] Each score must carry a one-line explanation. (Owner: AN)
- [ ] Internal review of distribution: no single-score cliffs. (Owner: DL)
- [ ] Proof event: `accounts_scored = N`. (Owner: AN)

### Day 4 — Scoring (Pass 2) & Top 50
- [ ] Re-run with adjusted weights if Day 3 review flagged issues. (Owner: AN)
- [ ] Lock top 50 list. (Owner: DL)
- [ ] Compose top-10 action plan (named owner, channel, first touch, fallback). (Owner: DL + AN)
- [ ] Send brief preview to CR for sanity check. (Owner: DL)

### Day 5 — Outreach Draft Pack
- [ ] CL drafts 4 sequences × Arabic + English. (Owner: CL)
- [ ] All drafts labeled `draft_only`. (Owner: CL)
- [ ] Tone check against client's prior outreach sample. (Owner: CL)
- [ ] No cold WhatsApp drafts produced. (Owner: CL + QA)
- [ ] No guaranteed claims used. (Owner: CL)
- [ ] Proof event: `drafts_generated = N`. (Owner: CL)

### Day 6 — Mini CRM Board
- [ ] Notion or Sheets workspace provisioned (client choice). (Owner: DL)
- [ ] Stage definitions documented: New → Contacted → Replied → Meeting → Closed-Won/Lost. (Owner: DL)
- [ ] Top 50 imported with score columns. (Owner: AN)
- [ ] Top 10 highlighted with action plan. (Owner: DL)
- [ ] Up to 5 named client users invited. (Owner: DL)

### Day 7 — Internal QA (Round 1)
- [ ] QA runs the QA checklist (see `qa_checklist.md`). (Owner: QA)
- [ ] Any failed gate creates a fix ticket with same-day SLA. (Owner: DL)
- [ ] Re-run any failed gate the same day. (Owner: AN/CL/DL)
- [ ] Proof event: `qa_round_1_complete`. (Owner: QA)

### Day 8 — Internal Review & Polish
- [ ] DL walks through deliverables with QA. (Owner: DL + QA)
- [ ] Executive proof report drafted. (Owner: DL)
- [ ] Sensitive-field anonymization verified per intake flags. (Owner: QA)
- [ ] Proof pack draft assembled. (Owner: DL)

### Day 9 — Client Preview
- [ ] 60-min preview call with CS and CR. (Owner: DL)
- [ ] Walk through: top 50, top 10 action plan, draft pack, mini CRM, proof report. (Owner: DL)
- [ ] Capture client revisions on a single revision log. (Owner: DL)
- [ ] Apply revisions if within scope; otherwise propose change order. (Owner: DL)

### Day 10 — Final Delivery
- [ ] Apply final revisions. (Owner: AN/CL/DL)
- [ ] Final QA pass (round 2). (Owner: QA)
- [ ] Send final deliverables package: list, top 50, top 10, drafts, mini CRM link, proof report, proof pack. (Owner: DL)
- [ ] Schedule optional Day 11 review session. (Owner: DL)
- [ ] CS signs handoff note. (Owner: CS + DL)
- [ ] Proof event: `sprint_delivered`. (Owner: DL)
- [ ] Trigger upsell motion per `upsell.md`. (Owner: DL + CSM)

## Cross-Cutting Controls
- Every deliverable change is tracked in the sprint board.
- No deliverable ships without QA sign-off.
- Sensitive client data is never moved out of the agreed jurisdiction.
- The proof pack is updated in real time, not at the end.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + intake summary | Sprint board initialized | DL | T-5 days |
| Daily standup notes | Sprint board updated | DL | Daily 10:00 AM |
| QA gate results | Fix tickets or signoff | QA + DL | Day 7, Day 10 |
| Final deliverables | Handoff note + proof pack | DL + CS | Day 10 |

## Metrics
- **On-time delivery** — `% sprints delivered on Day 10`. Target ≥ 95%.
- **QA pass rate first time** — `% sprints clearing QA round 1 without rework`. Target ≥ 70%.
- **Checklist adherence** — `% checklist items completed`. Target = 100%.

## Related
- `docs/capabilities/revenue_capability.md` — parent capability
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue playbook
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/V14_FOUNDER_DAILY_OPS.md` — operating loop
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
