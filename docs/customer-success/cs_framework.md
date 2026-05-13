---
title: Customer Success Framework — Segmentation, Health, Playbooks
doc_id: W5.T10.cs-framework
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W1.T05, W1.T31, W3.T07, W4.T14, W5.T18, W5.T19]
kpi:
  metric: net_revenue_retention
  target: 120
  window: 90d
rice:
  reach: 80
  impact: 2.5
  confidence: 0.85
  effort: 4
  score: 42
---

# Customer Success Framework

## 1. Context

Dealix sells a revenue-producing system, not a tool. Customer Success (CS) is therefore not a "support" function — it is the operating arm that converts a signed contract into measurable revenue inside the customer's funnel, then compounds that outcome into expansion, advocacy, and multi-year commitment. This framework defines how the CS organization is segmented, staffed, instrumented, and operated across the Saudi GTM motion.

The framework is the canonical reference for: (a) how a new logo is routed at signature, (b) which CSM owns it, (c) what cadence and playbooks apply, (d) how health is computed and acted on, (e) when and how risk is escalated to the CRO. It complements `CUSTOMER_SUCCESS_PLAYBOOK.md` (the day-to-day SOP) and `CUSTOMER_SUCCESS_SOP.md` (the procedural manual) by providing the **structural and strategic backbone** that those documents instantiate.

The northstar metric for this framework is Net Revenue Retention (NRR) at 120% within 90 days of GA cohort and 130% within 12 months. Logo retention is a floor (≥95% annualized), not a target. The mechanism for NRR is utilization-driven expansion at QBR cadence — not contract renegotiation under duress.

## 2. Audience

- **HoCS** — owns the framework end-to-end; updates segmentation and playbooks quarterly.
- **CSMs (pooled + named)** — operate within the framework; do not deviate without HoCS sign-off.
- **CRO** — receives escalations from the matrix in §3.7 and owns commercial recovery.
- **HoP / CTO** — receives product-driven health alerts and rescue tickets via the adoption rescue playbook.
- **Finance** — uses health score and segmentation for revenue forecasting and churn provisioning.

## 3. Decisions / Content

### 3.1 Segmentation

Four segments, defined by annual contract value (ACV) and strategic weight. Segment is set at contract signature and re-evaluated at every renewal.

| Segment | ACV band (SAR) | Strategic weight | Staffing model | Touch cadence |
|---------|----------------|------------------|----------------|---------------|
| **Starter** | < 120k | Volume, learning loop | Pooled CSM (1:40) | Digital + monthly group office hours |
| **Growth** | 120k – 480k | Mid-market, expansion engine | Pooled CSM (1:15) | Bi-weekly named touchpoint |
| **Enterprise** | 480k – 1.5M | Named logo, advocacy potential | Named CSM (1:5) | Weekly sync, QBR every 90 days |
| **Sovereign** | > 1.5M or Vision-2030-aligned entity | Strategic, board-visible | Named CSM + Exec Sponsor (1:2) | Weekly sync, monthly steering, QBR every 60 days |

Sovereign is a designation, not just a band: any account where the buyer is a ministry, a PIF portfolio company, or a Vision-2030 program owner is auto-routed to Sovereign regardless of ACV — the strategic value outweighs the contract value.

### 3.2 Pooled vs Named CSM

- **Pooled CSM** owns a queue, not relationships. Inbound tickets, scheduled touchpoints, and triggered alerts (health drop, ticket spike, billing anomaly) are worked off the queue. KPIs: queue SLA, NPS, expansion-qualified leads per quarter. Tooling: shared inbox, Linear queue, automated digital tour cadence.
- **Named CSM** owns relationships and outcomes. They run the QBR, the adoption plan, the expansion conversation, and the renewal. KPIs: NRR, logo retention, QBR completion rate, executive sponsor engagement. Tooling: customer plan in HubSpot, weekly account brief in Notion, QBR deck template.

The split is non-negotiable: a CSM is either pooled OR named in a given quarter, never both. Hybrid models collapse under load and we have seen this in prior iterations.

### 3.3 Health Score Formula

Health is a composite, computed daily, range 0–100. Three bands: Green (≥70), Yellow (40–69), Red (<40). Formula:

```
health = 0.35 * usage + 0.25 * engagement + 0.20 * sentiment + 0.20 * outcome
```

Where each component is normalized to 0–100:

- **Usage (0.35)** — weighted blend of value-metric utilization (enriched leads consumed / contracted), seat activation rate, and weekly active power-users. The single most predictive component; weighted highest.
- **Engagement (0.25)** — meeting attendance rate, response latency on shared channels, completion of onboarding milestones (30/60/90).
- **Sentiment (0.20)** — last-NPS score, support-ticket sentiment (auto-scored), exec-sponsor pulse survey.
- **Outcome (0.20)** — customer-reported pipeline generated / revenue closed attributable to Dealix, captured at QBR and verified at renewal.

A Red flag on any one component for two consecutive weeks triggers the adoption rescue playbook (§3.4) regardless of overall score. Conversely a Green overall score does not exempt an account from the churn-risk playbook if the renewal window is < 60 days and outcome is unverified.

### 3.4 Playbooks

#### Onboarding 30/60/90

- **Day 0 (signature)** — handoff call with Sales; CS plan drafted within 48 hours; kickoff scheduled within 7 days.
- **Day 30 — Foundation milestone**: seats provisioned, source integrations live, first 500 enriched leads delivered, Decision Passport tour completed, success criteria written and signed by customer's executive sponsor.
- **Day 60 — Adoption milestone**: ≥3 weekly active power-users, ≥50% of contracted value-metric consumed, first pipeline outcome reported.
- **Day 90 — Outcome milestone**: contracted value-metric on pace, first attributable revenue or qualified opportunities documented, expansion conversation opened if utilization >70%.

Missed milestone at any gate → rescue playbook. Missed two consecutive gates → escalation to CRO (see §3.7).

#### Adoption Rescue

Triggered by: health score Red on usage component, missed onboarding milestone, ticket spike, or executive-sponsor disengagement. Steps:

1. CSM diagnostic call within 48 hours with customer's day-to-day owner.
2. Root-cause categorization: data fit (engine outputs don't match ICP), workflow fit (CRM/process gaps), team fit (under-staffed on customer side), product gap.
3. Rescue plan written within 5 business days, signed by customer's executive sponsor, with explicit 30-day exit criteria.
4. Weekly checkpoint until Green for 4 consecutive weeks or escalation triggered.

#### Churn Risk

Triggered by: health Red overall for 3 consecutive weeks, executive-sponsor turnover, M&A event, or competitive RFP detected. Steps:

1. CSM brief to HoCS within 24 hours.
2. CRO-led save call within 7 days with the customer's economic buyer.
3. Save plan: usually a combination of (a) success-criteria reset, (b) commercial concession capped at 10% with multi-year tradeoff, (c) executive co-sponsorship from Dealix CEO if Sovereign segment.
4. Outcome logged in the renewal forecast and the post-mortem regardless of save success.

#### Advocacy

Triggered by: NRR > 110% sustained for 6 months, NPS ≥ 9 from executive sponsor, or outcome event ≥ SAR 1M closed-won attributable. Steps:

1. Case-study production (writer + customer review within 30 days).
2. Reference enrollment (logo + spoken reference + RFP reference).
3. Co-marketing motion: joint webinar, joint press, conference panel slot.
4. Expansion-into-network: warm intros to peer accounts; advocacy bonus to CSM.

### 3.5 QBR Template

Quarterly Business Reviews are non-optional for Growth, Enterprise, and Sovereign segments. Standard agenda (60 minutes):

1. **Outcome review (15m)** — value-metric utilization vs contracted, pipeline/revenue attribution, success-criteria status.
2. **Adoption review (10m)** — seat activation, power-user count, integration health, ticket trends.
3. **Roadmap & feedback (15m)** — what's shipping next quarter, customer's top-3 wishlist, escalations.
4. **Expansion conversation (15m)** — new BU, new vertical, new use-case, multi-year framing.
5. **Action items & sign-off (5m)** — owner, due date, success criteria.

QBR deck is produced from a templated source-of-truth dashboard (cross-link: `BUSINESS_KPI_DASHBOARD_SPEC.md`). The CSM does not author from scratch — they curate and narrate.

### 3.6 Tooling & Instrumentation

- **CRM**: HubSpot for relationship, opportunity, and renewal. All CS notes live here.
- **Health & telemetry**: computed in-product, surfaced via the dashboard at `dashboard/`. Source events in `auto_client_acquisition/revenue_memory/event_store.py`.
- **Playbook automation**: triggered alerts route to Linear queues with SLA timers per segment.
- **Customer-facing surfaces**: shared workspace per account; bilingual (Arabic + English) artifacts mandatory for Sovereign.

### 3.7 Escalation Matrix to CRO

| Trigger | First responder | Escalation to CRO | Time-to-CRO |
|---------|-----------------|-------------------|-------------|
| Missed Day 60 milestone | CSM | HoCS, then CRO | 5 business days |
| Health Red 3 consecutive weeks | CSM | HoCS, then CRO | 7 days |
| Executive-sponsor churn | Named CSM | HoCS + CRO joint | 24 hours |
| Competitive RFP detected | Named CSM | CRO direct | Same day |
| Sovereign account billing dispute | Named CSM + Finance | CRO + CEO | Same day |
| M&A event at customer | Named CSM | CRO + CEO | 24 hours |
| Outcome-reported revenue < 50% of forecast at Day 90 | CSM | HoCS, then CRO | 5 business days |

The escalation matrix is exhaustive — CSMs do not invent new escalation paths; they map any new situation to the closest row and escalate through that path. New patterns get added at the quarterly framework review by HoCS.

## 4. KPIs / Acceptance

| Metric | Target | Window |
|--------|--------|--------|
| Net Revenue Retention | 120% | 90d (cohort) |
| Net Revenue Retention | 130% | 12 months |
| Logo retention | ≥ 95% | annualized |
| Onboarding 30/60/90 completion rate | ≥ 90% | cohort |
| Health score Green share | ≥ 70% of book | continuous |
| QBR completion rate (Growth+) | 100% | quarter |
| Time-to-first-outcome | ≤ 60 days | per logo |
| Advocacy enrollment | ≥ 20% of Enterprise+Sovereign | annualized |

## 5. Dependencies

- Code: `auto_client_acquisition/revenue_memory/event_store.py`; dashboard health rollups; HubSpot pipeline.
- Docs: W1.T05 (ICP), W1.T31 (lead engine outputs that drive utilization), W3.T07 (trust pack used in onboarding), W4.T14 (policy gates that affect health), W5.T18 (pilot framework — onboarding inherits its discipline), W5.T19 (expansion playbook — QBR feeds into it).
- People: HoCS (owner), CSM hires (cross-link `HIRING_CSM_FIRST.md`), CRO (escalations), Exec Sponsors.

## 6. Cross-links

- Day-to-day SOP: `CUSTOMER_SUCCESS_PLAYBOOK.md`, `CUSTOMER_SUCCESS_SOP.md`
- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Lead engine: `docs/product/saudi_lead_engine.md`
- Pricing & packaging: `docs/pricing/pricing_packages_sa.md`
- Hiring: `HIRING_CSM_FIRST.md`
- Dashboards: `BUSINESS_KPI_DASHBOARD_SPEC.md`
- Pilot framework: `docs/delivery/pilot_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`

## 7. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: monthly during ramp (first 90 days post-GA); quarterly thereafter.
- **Escalation**: any framework deviation request → HoCS within 48 hours; structural changes (segment redefinition, formula change) → quarterly framework review only.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial framework: 4 segments, pooled vs named, health formula, 4 playbooks, QBR template, CRO escalation matrix |
