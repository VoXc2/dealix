# Retainer Operating System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CSM Lead + CTO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [RETAINER_OPERATING_SYSTEM_AR.md](./RETAINER_OPERATING_SYSTEM_AR.md)

## Context

A retainer at Dealix is **not** ongoing support. It is a monthly
operating cadence around a business capability we have already
proven (via a Sprint and Proof Pack). This system defines the
retainer types, the monthly deliverables, and the JSON monthly
report schema. It is the destination of every successful sprint
graduated through `docs/client/CLIENT_HEALTH_SCORE.md` and the
delivery counterpart of `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md`.

## What A Retainer Is

A retainer = **monthly operating cadence around a business
capability**. Components, all monthly:

- **Capability backlog** — what we will operate next, ranked.
- **Weekly or bi-weekly review** — stakeholder sync on backlog +
  outputs.
- **Data refresh** — pull, clean, verify; QA per
  `docs/quality/QA_SYSTEM.md`.
- **AI output QA** — 5-layer review on all client-visible AI work.
- **Governance monitoring** — approvals, audit log, PDPL checks.
- **Proof updates** — Proof Pack refreshed with new metrics.
- **Executive report** — single monthly artifact summarizing impact.
- **Next improvement recommendation** — what to add next month.

If any of these is missing for two consecutive months, the retainer
is downgraded to a service review meeting.

## The 5 Retainer Types

| Type | Capability | Anchor offer that earned it |
|---|---|---|
| **RevOps Retainer** | Continuous lead intelligence, scoring, opportunity ranking | Lead Intelligence Sprint |
| **AI Ops Retainer** | Operating governed AI workflows for repetitive ops | AI Quick Win Sprint |
| **Company Brain Retainer** | Maintaining the knowledge layer, vocabulary, FAQ accuracy | Company Brain Sprint |
| **Support AI Retainer** | Running governed Arabic support agents with QA | Support pilot |
| **Governance Retainer** | Approvals, audit, PDPL operating layer for AI initiatives | Enterprise governance sprint |

A retainer cannot be sold without the matching anchor sprint
already delivered.

## Monthly Deliverables List

Every retainer month produces, at minimum:

1. Refreshed dataset / index / configuration.
2. AI output run logs.
3. QA review records (per artifact reviewed).
4. Governance log with named approvals.
5. Updated Proof Pack section for the month.
6. Executive monthly report (JSON + PDF).
7. Next-month backlog with at least 3 ranked items.

## JSON Monthly Report Schema

```json
{
  "report_id": "ret_acme_2026_05",
  "retainer_id": "ret_acme",
  "client": "Acme Bank",
  "type": "RevOps",
  "period_start": "2026-05-01",
  "period_end": "2026-05-31",
  "outputs_delivered": 142,
  "qa_pass_rate": 0.94,
  "governance_breaches": 0,
  "impact": {
    "primary_metric": "qualified_opportunities_per_week",
    "baseline": 22,
    "current": 31,
    "delta_pct": 0.41
  },
  "proof_pack_link": "/proof/acme/2026-05",
  "backlog_next_month": [
    "Add wealth-management segment",
    "Refresh objection bank",
    "Integrate KYC-cleared list"
  ],
  "recommendations": [
    "Promote 2 reps to coached calls based on top-ranked leads",
    "Add Hijri-month scoring weight"
  ],
  "stakeholder_signoff": {
    "sponsor": "L. Al-Mansouri",
    "signed_at": "2026-06-02T09:14:00+03:00"
  }
}
```

## Cadence

- **Day 1-5** — data refresh + AI runs.
- **Weekly** — stakeholder sync (15-30 min).
- **Mid-month** — QA spot-check + governance log review.
- **Last week** — Proof Pack update + executive monthly report.
- **Month +2 days** — stakeholder sign-off.

## Pricing

Retainers are priced via `docs/company/PRICING_ENGINE.md` retainer
rules. Margin floor 65% per `docs/company/MARGIN_GUARD.md`.

## Exit Rules

A retainer ends or is downgraded if any of the following:

- 2 consecutive months of missing deliverables.
- Client Health drops below 50 for two consecutive months.
- Governance breach + missing recovery plan.
- Sponsor turnover with no replacement aligned within 60 days.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sprint proof + client signal | Retainer proposal | CSM + Sales | Per opportunity |
| Monthly deliverables checklist | Monthly report, Proof Pack update | CSM + Delivery | Monthly |
| Governance log | PDPL/audit attestations | CTO + Legal | Monthly |

## Metrics

- **Sprint-to-retainer conversion rate** — target ≥40%.
- **Retainer NRR** — target ≥110% annual.
- **Retainer gross margin** — target ≥65%.
- **% retainers producing Proof Pack update monthly** — target 100%.
- **Sponsor sign-off rate** — target 100%.

## Related

- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CSM playbook.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot offer feeding retainers.
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue playbook.
- `docs/V7_REVENUE_FACTORY_LAUNCH_BOARD.md` — revenue factory.
- `docs/client/CLIENT_HEALTH_SCORE.md` — expansion gate.
- `docs/company/PRICING_ENGINE.md` — retainer pricing.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
