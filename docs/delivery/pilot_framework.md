---
title: Paid Pilot Framework — 90-Day Structure, Gates, Exit-to-Paid
doc_id: W5.T18.pilot-framework
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W1.T05, W1.T31, W2.T08, W3.T07, W4.T14, W5.T10, W5.T19]
kpi:
  metric: pilot_to_paid_conversion
  target: 70
  window: 90d
rice:
  reach: 60
  impact: 3.0
  confidence: 0.8
  effort: 5
  score: 36
---

# Paid Pilot Framework

## 1. Context

Dealix does not run free trials. The pilot is a paid, scoped, time-bound engagement designed to convert a hypothesis ("Dealix will materially change our pipeline economics") into a contractual outcome ("we are buying the annual"). The pilot framework is the operating contract between Sales, CS, Product, and the customer for the first 90 days of the relationship.

A paid pilot exists for one reason: to retire risk on both sides — for the customer, the risk that the system will not produce the promised pipeline; for Dealix, the risk that the customer is not operationally ready to consume the output. Free pilots invert this discipline because neither side has skin in the game and disposition slips. We have run this experiment in prior waves and the conversion math is roughly 3x in favor of paid.

This framework defines the structure (week-by-week milestones), the scope (one vertical, five seats, five thousand enriched leads), the pre-defined success criteria (three quantitative, two qualitative), the go/no-go gates at days 30, 60, and 90, the exit-to-paid handoff to the named CSM, and the commercial mechanic (SAR 60K pilot fee, 100% credited toward annual on conversion).

Cross-link: `PILOT_DELIVERY_SOP.md` is the day-to-day procedural manual; `docs/sales/PILOT_AGREEMENT_DRAFT.md` is the legal template; this document is the strategic and operational backbone that both instantiate.

## 2. Audience

- **HoCS** — framework owner; signs off on every pilot's success criteria before kickoff.
- **Pilot CSM** — named delivery owner during the 90 days; transitions to Account CSM at conversion.
- **AE (Sales)** — co-owns the commercial conversion; runs the exit-to-paid conversation from Day 75.
- **HoP** — product escalations during pilot; owns the product gap log produced from every pilot.
- **Customer's economic buyer + executive sponsor + day-to-day owner** — the three required roles on the customer side.

## 3. Decisions / Content

### 3.1 Paid Pilot Scope

The scope is fixed and non-negotiable. The bounded surface is what makes the 90 days predictable.

| Dimension | Pilot scope | Rationale |
|-----------|-------------|-----------|
| Verticals | 1 (customer's primary buyer vertical) | Single-vertical proof beats dilute multi-vertical noise |
| Seats | 5 active named users | Enough to test handoffs; small enough to coach |
| Enriched leads | 5,000 over 90 days | One vertical at our default depth model |
| Integrations | 1 CRM (HubSpot or Salesforce) + 1 channel (email or WhatsApp Business) | Two-system pilot, not five |
| Geography | Saudi only | Defer GCC expansion to post-conversion expansion play |
| Languages | Arabic + English (bilingual artifacts mandatory) | Saudi-first stance |
| Custom development | None | Out-of-the-box product, configuration only |

Anything beyond this scope is a paid scope extension (statement of work, separate fee). Saying no to scope creep during a pilot is the single most important discipline.

### 3.2 Commercial Mechanic

- **Pilot fee**: SAR 60,000, invoiced at kickoff, payable Net-15.
- **Credit on conversion**: 100% of pilot fee credited toward Year-1 annual contract value if conversion occurs within 30 days of Day 90.
- **No-conversion outcome**: pilot fee retained by Dealix; customer keeps any data exported during pilot; orderly off-boarding within 30 days (data deletion certificate issued).
- **Annual minimum on conversion**: SAR 240K Year-1 ACV (Growth segment floor); higher for Enterprise / Sovereign segments per pricing schedule.
- **Multi-year incentive**: 2-year commitment at conversion → additional 10% credit applied to Year-1; 3-year commitment → 15%.

The credit mechanic aligns incentives without making the pilot free. The customer is making a paid bet that the system will deliver; we are making a paid bet that we can prove it.

### 3.3 Pre-Defined Success Criteria

Five criteria written before kickoff, signed by customer's executive sponsor and Dealix HoCS. No criteria → no kickoff. Criteria do not change during the pilot except by joint written agreement.

**Three quantitative** (must all be Green at Day 90 for go decision):
1. **Pipeline generated** — ≥ SAR 2.5M qualified pipeline attributable to Dealix-sourced leads (3-5x the pilot fee at a minimum).
2. **Enriched-lead conversion** — ≥ 8% of delivered leads reach Stage-2 (qualified) in customer CRM.
3. **Cycle-time delta** — ≥ 25% reduction in lead-to-meeting cycle vs. customer's prior 90-day baseline.

**Two qualitative** (must both be Green at Day 90):
1. **Executive sponsor sentiment** — written endorsement from economic buyer that Dealix should continue; captured in QBR minutes.
2. **Team adoption** — 4 of 5 seats are weekly active power-users at Day 75; team self-reports willingness to continue.

If a customer cannot articulate plausible success criteria during pre-pilot scoping, the pilot does not happen. We have walked away from pilots over this. The discipline is preserved.

### 3.4 Week-by-Week Milestones

#### Phase 1 — Foundation (Weeks 1–4)

- **Week 1**: Kickoff. Stakeholder map signed. Success criteria signed. Data-source intake completed. First 100 enriched leads delivered as a sample (calibration).
- **Week 2**: CRM integration live. Channel integration live. Bilingual artifacts produced. First 500-lead batch delivered.
- **Week 3**: First weekly outcome review with day-to-day owner. Calibration loop applied (ICP refinement, exclusion rules tuned).
- **Week 4**: Day 30 gate (see §3.5). 1,500 cumulative leads delivered. ≥ 3 seats active.

#### Phase 2 — Adoption (Weeks 5–8)

- **Week 5**: Power-user training session. Playbook customization. Decision Passport tour with executive sponsor.
- **Week 6**: Pipeline-attribution session with customer's RevOps. First attributable revenue / qualified opportunities documented.
- **Week 7**: Mid-pilot health review. Adoption rescue triggered if needed (see `cs_framework.md` §3.4).
- **Week 8**: Day 60 gate (see §3.5). 3,500 cumulative leads delivered. ≥ 4 seats active.

#### Phase 3 — Conversion (Weeks 9–13)

- **Week 9**: Outcome verification session with customer's CFO/Head of Revenue. Pipeline attribution signed off.
- **Week 10**: AE re-engages. Exit-to-paid conversation opened. Annual contract structure proposed.
- **Week 11**: Multi-year framing if Enterprise / Sovereign. Procurement / legal track started in parallel.
- **Week 12**: QBR with executive sponsor — outcome review, success criteria status, decision conversation.
- **Week 13 (Day 90)**: Day 90 gate (see §3.5). Conversion decision. Hand-off to Account CSM or off-boarding.

### 3.5 Go/No-Go Gates

Gates are decision events, not status updates. Each gate ends with a written disposition: Go, Conditional Go, or No-Go. Disposition is logged and shared with the customer within 24 hours.

#### Day 30 Gate

- **Owner**: Pilot CSM, reviewed by HoCS.
- **Criteria**: foundations live (integrations, data sources, seats), ≥ 1,500 leads delivered, success criteria still active and unchanged, customer's three required roles still engaged.
- **No-Go outcomes**: pause and rescue (extend Phase 1 by 2 weeks, no Day 90 extension) OR terminate with refund of unused-period fraction.

#### Day 60 Gate

- **Owner**: Pilot CSM + AE, reviewed by HoCS + CRO.
- **Criteria**: ≥ 3,500 leads delivered, ≥ 4 seats active, first attributable revenue or qualified opportunities documented, executive-sponsor pulse Green.
- **No-Go outcomes**: adoption rescue (formal, written, signed by exec sponsor) OR termination (rare — only on executive-sponsor turnover or scope failure).

#### Day 90 Gate

- **Owner**: HoCS + CRO + customer's economic buyer.
- **Criteria**: all three quantitative + both qualitative criteria Green (see §3.3).
- **Outcomes**: Go → conversion conversation + annual contract within 30 days; Conditional Go → 30-day extension at no additional fee with binding success criteria; No-Go → orderly off-boarding, post-mortem, learning logged.

The Day 90 gate is not a sales-driven decision. It is an outcome-driven decision. The AE participates but does not override.

### 3.6 Exit-to-Paid Handoff

Conversion is not a closing event — it is a handoff. The 30 days after Day 90 are structured:

1. **Day 91–95**: Annual contract draft circulated; commercial terms (seats, leads, integrations, multi-year, AR partner co-sell if applicable) finalized.
2. **Day 96–105**: Procurement / legal closure. Account CSM (different from Pilot CSM in most cases) shadowed onto weekly calls.
3. **Day 106–115**: Contract signature. Pilot fee credit applied. First annual invoice.
4. **Day 116–120**: Formal hand-off ceremony. Account CSM owns. Pilot CSM exits. Customer-facing handoff memo issued.

The Pilot CSM and Account CSM are usually different individuals. This is deliberate: the Pilot CSM's job ends when the pilot ends; the Account CSM's job is to own the multi-year arc. The hand-off memo captures everything material about the customer that the Account CSM needs to know.

### 3.7 Product Gap Log

Every pilot produces a product gap log — three categories: (a) blockers (the pilot would have failed without a workaround), (b) friction (slowed time-to-value), (c) wishlist (customer-requested but non-essential). The log is delivered to HoP at the Day 90 gate and is an input into the next quarterly product planning.

This is the second-order value of the pilot system: it is the single best mechanism we have for getting real customer feedback into the product roadmap, because the pilot incentives align the customer to be candid.

## 4. KPIs / Acceptance

| Metric | Target | Window |
|--------|--------|--------|
| Pilot-to-paid conversion | ≥ 70% | annualized cohort |
| Time-to-first-outcome (within pilot) | ≤ 60 days | per pilot |
| Day 90 gate Go rate | ≥ 75% | annualized |
| Multi-year attach on conversion | ≥ 40% | annualized |
| Average days from Day 90 to signed annual | ≤ 25 days | per cohort |
| Net Promoter Score at conversion | ≥ 50 | per pilot |
| Pilot fee invoice → paid latency | ≤ 15 days | per pilot |

## 5. Dependencies

- Legal: `docs/sales/PILOT_AGREEMENT_DRAFT.md` (template), `DPA_PILOT_TEMPLATE.md` (data processing addendum).
- Docs: W1.T05 (ICP — pilot ICP fit gate), W1.T31 (lead engine — output that drives quantitative criteria), W2.T08 (pricing — annual contract floor), W3.T07 (trust pack — used in pre-pilot scoping), W4.T14 (policy gates), W5.T10 (CS framework — pilot inherits its discipline), W5.T19 (expansion — multi-year framing originates at Day 90).
- Code: `auto_client_acquisition/revenue_memory/event_store.py`; pilot dashboards in `dashboard/`.
- People: Pilot CSM (named), AE (co-owner), HoCS (gate authority), HoP (product gap log consumer).

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Lead engine: `docs/product/saudi_lead_engine.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Day-to-day SOP: `PILOT_DELIVERY_SOP.md`
- Legal template: `docs/sales/PILOT_AGREEMENT_DRAFT.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
- Dashboards: `BUSINESS_KPI_DASHBOARD_SPEC.md`

## 7. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: monthly during ramp (first three pilots post-GA); quarterly thereafter.
- **Escalation**: any deviation request from scope or commercial mechanic → HoCS within 24 hours; structural framework changes → quarterly review only.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial framework: scope, SAR 60K paid mechanic, success criteria, 90-day milestones, Day 30/60/90 gates, exit-to-paid handoff, product gap log |
