# Client Health Score — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CSM Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CLIENT_HEALTH_SCORE_AR.md](./CLIENT_HEALTH_SCORE_AR.md)

## Context

Client health is the single best leading indicator for renewal,
expansion, churn, and reference-ability. Without a structured
score, founders rely on vibes — which always overstates good
clients and understates risky ones. This document defines the
seven-factor health score used in CSM cadence and in the retainer
expansion gate. It complements
`docs/CUSTOMER_SUCCESS_PLAYBOOK.md` and the executive dashboard
spec in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`, and pairs with the
client journey in `docs/client/CLIENT_JOURNEY.md`.

## The 7 Factors and Weights

| # | Factor | Weight | What we score |
|---|---|---:|---|
| 1 | Value delivered | 25 | Has the agreed metric moved? |
| 2 | Proof clarity | 15 | Is there a current, signed-off Proof Pack? |
| 3 | Stakeholder engagement | 15 | Sponsor + operator regularly engaging? |
| 4 | Data cooperation | 10 | Is data access, refresh, and ownership on time? |
| 5 | Payment reliability | 10 | Invoices paid on standard terms? |
| 6 | Retainer fit | 15 | Could a retainer be sold here today? |
| 7 | Risk level | 10 | PDPL, governance, scope-creep, sponsor turnover risks |
| **Total** | | **100** | |

Each factor is scored 0, 50%, or 100% of its weight (no fractional
intermediate scores). Risk level is scored inverted (no risks = 100%
of weight; major risk present = 0%).

## Health Levels

| Score | Level | What CSM does |
|---|---|---|
| 85-100 | **Expansion-ready** | Pitch retainer; pitch second offer; ask for case study. |
| 70-84 | **Healthy** | Quarterly business review; small expansion when ready. |
| 50-69 | **Needs attention** | Weekly check-ins; recovery plan; escalate to CEO. |
| <50 | **Risky** | Stop expansion talks; recover or end gracefully. |

## Expansion Rule

> **Only Expansion-ready or Healthy clients receive retainer
> proposals.**

This is non-negotiable. Pitching a retainer to a Needs-attention or
Risky client extends the wrong relationship and damages the
retainer product (`docs/retainers/RETAINER_OPERATING_SYSTEM.md`).
A retainer pitch to a Risky client requires CEO override and a
written recovery plan.

## Scoring Cadence

- **Weekly** — CSM updates the score row for active clients.
- **Monthly** — CSM leadership reviews movement and triggers.
- **Quarterly** — Executive review for case-study candidates and
  churn risks.

## Example Score Snapshot

| Client | Value | Proof | Engage | Data | Pay | Retainer fit | Risk | Total | Level |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Acme Bank | 25 | 15 | 15 | 10 | 10 | 15 | 10 | **100** | Expansion-ready |
| Beta Retail | 12 | 7 | 15 | 10 | 10 | 7 | 10 | **71** | Healthy |
| Gamma Logistics | 12 | 0 | 7 | 5 | 10 | 7 | 5 | **46** | Risky |

## CSM Actions By Level

**Expansion-ready:**

- Schedule retainer pitch within 14 days.
- Confirm Proof Pack signed-off.
- Request a logo/case-study consent.
- Identify a second buying center inside the client.

**Healthy:**

- Schedule QBR within 30 days.
- Identify the one factor blocking 85+.
- Confirm next QA cycle and Proof Pack refresh.

**Needs attention:**

- Weekly CSM check-ins.
- Written 30-day recovery plan with named actions.
- CEO informed.

**Risky:**

- Pause expansion talks.
- Plan either recovery or graceful exit per
  `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`.
- Refund/credit only via CFO approval.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement metrics, payment logs, Proof Packs, CSM notes | Health score, level, action plan | CSM | Weekly |
| Trend reports | Quarterly executive review | CSM Lead + CEO | Quarterly |
| Score | Retainer pitch gate | CSM + Sales | Per opportunity |

## Metrics

- **Average health score across clients** — target ≥75.
- **% clients ≥85** — target ≥40% (expansion pool).
- **% clients <50** — target ≤10%.
- **Retainer conversion from Expansion-ready** — target ≥60%.
- **Time from "Needs attention" entry to recovery plan** — target
  ≤7 days.

## Related

- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CSM playbook.
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard for client KPIs.
- `docs/HIRING_CSM_FIRST.md` — CSM hiring plan.
- `docs/client/CLIENT_JOURNEY.md` — sibling client journey.
- `docs/retainers/RETAINER_OPERATING_SYSTEM.md` — expansion target.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — Trust capital tied to health.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
