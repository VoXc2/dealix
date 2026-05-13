# Value Flywheel — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO + Head of Dealix Services
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [VALUE_FLYWHEEL_AR.md](./VALUE_FLYWHEEL_AR.md)

## Context
The Value Flywheel is the **10-step compounding loop** that every Dealix engagement runs through. It is how the Cash Engine and the Compound Engine of [`DUAL_ENGINE_MODEL.md`](./DUAL_ENGINE_MODEL.md) actually mesh in practice. Each turn of the flywheel should produce more proof, more reusable assets, more margin, and a stronger ICP than the previous turn. The flywheel is the operational backbone behind `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`.

## The 10 steps

```
                       ┌────────────────────────────────┐
                       │                                ▼
   1. Sell focused Sprint     2. Deliver governed workflow
                                                ▼
   10. Repeat with higher    3. Produce Proof Pack
       margin & better ICP                       ▼
       ▲                     4. Convert Sprint → Retainer
       │                                         ▼
   9. Improve Core OS        5. Extract reusable assets
       ▲                                         ▼
   8. Attract better clients 6. Productize repeated work
   & partners                                    ▼
       ▲                     7. Publish market-safe insights
       └─────────────────────────────────────────┘
```

| Step | Verb | Owner | Output | Compound contribution |
|---|---|---|---|---|
| 1 | Sell | Sales | Signed Sprint SoW | Pipeline data, ICP signals |
| 2 | Deliver | Delivery + BU | Working governed workflow in client tenant | Workflow templates |
| 3 | Produce | BU + Proof Ledger owner | Proof Pack (ROI + evidence) | Case study, proof event |
| 4 | Convert | CSM | Signed retainer SoW | MRR, retention cohort |
| 5 | Extract | BU + Head of Core | Capital assets logged | Prompts, datasets, evals, agents |
| 6 | Productize | Product Council | New Core OS feature or module | Platform IP |
| 7 | Publish | Brand / Content | Market-safe insight (article, talk, sample) | Inbound demand |
| 8 | Attract | Sales + Growth | Higher-quality inbound / partner intros | Pipeline ↑, better fit |
| 9 | Improve | Head of Core | Core OS upgrade | Lower delivery cost |
| 10 | Repeat | BU GM | Next engagement at better terms | Margin ↑, win-rate ↑ |

## What makes it a flywheel

A flywheel is **a loop where each turn makes the next turn cheaper and faster**. The Dealix flywheel hits that property because:

- Step 5 (Extract) **lowers the cost** of step 2 (Deliver) next time.
- Step 6 (Productize) **raises the margin** of step 1 (Sell) next time.
- Step 7 (Publish) **lowers the cost of acquisition** for step 1 next time.
- Step 9 (Improve) **lowers the cost of delivery** across all BUs next time.

A project that fails to complete steps 5–9 is **a one-shot project**, not a flywheel turn. That is why the [`SUCCESS_ASSURANCE_SYSTEM`](./SUCCESS_ASSURANCE_SYSTEM.md) tracks Proof, Capital, and Product separately.

## Common breakages

| Breakage | Symptom | Fix |
|---|---|---|
| Step 3 skipped | Project closed without Proof Pack | QA gate: no invoice until Proof Pack uploaded |
| Step 4 skipped | Retainer conversion < 20% | CSM playbook & retainer offer pre-built |
| Step 5 skipped | No capital assets per project | BU GM compensation tied to Capital Ledger |
| Step 6 skipped | Same work done 3+ times manually | Product Council backlog auto-prioritization |
| Step 7 skipped | No inbound from market | Content calendar shared with BU output |

## Cadence

| Action | Cadence | Owner |
|---|---|---|
| Flywheel health review per BU | Monthly | BU GM + CSM |
| Group flywheel review | Quarterly | CEO |
| Productization council | Bi-weekly | Head of Core |
| Content publish | Weekly | Brand |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sprint SoWs | Step 1 metric | Sales | Per project |
| Delivery sign-off | Step 2 metric | Delivery | Per project |
| Proof Pack | Step 3 metric | BU + Proof owner | Per project |
| Retainer SoWs | Step 4 metric | CSM | Per project |
| Capital Ledger entries | Step 5 metric | BU | Per project |
| Productization Ledger | Step 6 metric | Product Council | Bi-weekly |
| Publishing calendar | Step 7 metric | Brand | Weekly |

## Metrics
- **Flywheel completion rate** — % of projects that complete steps 1–7.
- **Margin lift per turn** — gross margin delta between consecutive engagements with the same ICP.
- **Win-rate lift per turn** — win-rate delta after Publish events tied to the segment.
- **Asset reuse per project** — average capital assets reused per new project.
- **Time-to-retainer** — median days from step 1 sign to step 4 sign.

## Related
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — sell + convert plays.
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — retainer conversion plays.
- `docs/growth/GROWTH_MACHINE.md` — distribution flywheel side.
- `docs/PROOF_PACK_V6_STANDARD.md` — Proof Pack standard.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
