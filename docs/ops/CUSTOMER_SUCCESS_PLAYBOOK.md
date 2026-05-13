# Customer Success Playbook — Proactive Churn Prevention (W13.20)

> **Audience:** founder (until customer #10), then first CS hire (~customer #10-15).
> **Mission:** ensure ≥ 90% Month-to-Month retention through W4, ≥ 95% steady-state.
> **Source-of-truth:** [Customer Health Score](../../api/routers/customer_success_os.py) (W2.1) + [NPS data](../../api/routers/nps.py) (W13.4).

---

## The Iron Law of Customer Success

> **First 90 days = 80% of churn risk.** Invest heavily there, savings compound across years.

Forrester 2024 data: customers who reach 90-day Health Score ≥ 70 have 85% probability of 12-month retention. Customers stuck at < 50 at day 90 have 60% churn rate.

---

## The 5-Stage Customer Lifecycle

```
1. Onboard    →  2. Adopt   →  3. Expand  →  4. Renew  →  5. Advocate
   (Day 1-30)     (Month 2-3)    (Mo 4-9)      (Mo 10-12)   (Year 2+)
```

Each stage has explicit:
- Health-score signals to monitor
- Touchpoints to schedule
- Risks to watch for
- Success metrics to hit

---

## Stage 1 — Onboard (Day 1-30)

### Founder/CS Touchpoints

| Day | Touchpoint | Channel | Outcome |
|-----|-----------|---------|---------|
| 1 | Welcome call (30 min) | Zoom | Setup + expectations |
| 2-3 | Tech onboarding checklist | WhatsApp + email | DNS + WhatsApp + tenant ready |
| 5 | Mid-pilot check-in (15 min) | WhatsApp call | Issues surfaced early |
| 7 | Day-7 NPS survey | Email link to /api/v1/nps | Score captured |
| 14 | First reply quality review | Loom screen-share | AI-reply quality tuned |
| 21 | Decision Passport audit walkthrough | Zoom 30 min | Trust built |
| 30 | First-month QBR (Quarterly Business Review) | Zoom 60 min | Renewal commitment OR detractor intervention |

### Day 30 Success Criteria

- [ ] Customer Health Score ≥ 60 (`GET /api/v1/customer-success-os/{handle}/health`)
- [ ] Day-7 NPS ≥ 7 (passive or promoter)
- [ ] AI replies ≥ 80% approved as-is (low edit rate)
- [ ] Decision Passport entries flowing daily
- [ ] Customer's first inbound resolved in < 5 min average
- [ ] First payment cleared (Moyasar webhook → `payments` table)

### Day 30 Red Flags (intervene immediately)

| Signal | Trigger | Founder action |
|--------|---------|----------------|
| Health Score < 40 | Day 14 | WhatsApp call same day |
| NPS detractor (0-6) | Day 7 survey | 24-hour intervention call |
| AI replies < 50% approved | Day 14 | System prompt re-calibration session |
| Customer login activity = 0 for 5 days | Day 14 | Wellness check WhatsApp |
| Decision Passport empty | Day 7 | Verify webhook + onboarding completeness |

---

## Stage 2 — Adopt (Month 2-3)

### Founder/CS Touchpoints

| Frequency | Touchpoint | Outcome |
|-----------|-----------|---------|
| Bi-weekly | 30-min Friday call | Pulse check + roadmap input |
| Day 60 | NPS milestone survey | Retention prediction signal (Forrester: 70% accuracy) |
| Day 90 | Quarterly review + expansion conversation | Upsell or renewal commit |

### Month 2-3 Success Criteria

- [ ] Health Score ≥ 70
- [ ] Day-60 NPS ≥ 7
- [ ] AI replies ≥ 90% approved
- [ ] Customer's lead volume meets plan cap (utilization > 50%)
- [ ] Customer is using ≥ 4 of 7 AI services (S1-S7)

### Month 2-3 Red Flags

- Utilization < 30% of plan cap → DOWNGRADE risk (revenue at risk)
- AI replies < 80% approved → product fit issue
- Customer's primary champion leaves company → relationship rebuild
- Reply latency drift > 15 min → SLA violation, investigate

---

## Stage 3 — Expand (Month 4-9)

### Expansion Pathways (mapped to v4 §3 revenue streams)

| Trigger | Upsell Path | Revenue Impact |
|---------|-------------|----------------|
| Lead volume > 80% of cap | Starter → Growth | +2,000 SAR/mo |
| Customer asks "can you also..." | R5 Bespoke AI Setup | +5K-25K SAR one-off |
| Customer mentions complex compliance need | Add S4 Decision Passport standalone | +999 SAR/mo |
| Customer wants weekly sector intel | R4 Sector Reports | +1.5K-5K SAR/month |
| Customer references peer founder | Referral program activation | +5K SAR credit |

### Expansion Touchpoints

| Month | Touchpoint | Outcome |
|-------|-----------|---------|
| 4 | Usage review + plan fit | Right-size plan |
| 6 | "What would you love Dealix to do?" interview | Roadmap input + R5 lead |
| 9 | Renewal conversation (90 days before contract end) | Multi-year discount offer |

### Month 4-9 Red Flags

- Customer hasn't logged in > 30 days → urgent re-engagement
- Customer requests downgrade → 1:1 root-cause call before processing
- Decision Passport entries dropping → reduced engagement signal
- Customer asking about competitors → trust intervention

---

## Stage 4 — Renew (Month 10-12)

### The 90-Day Renewal Sequence

| Day before renewal | Touchpoint | Goal |
|--------------------|-----------|------|
| -90 | "Looking ahead" conversation | Surface concerns early |
| -60 | Annual review meeting | Demonstrate Year 1 value |
| -45 | Multi-year discount offer (W13.1 page) | Lock 2-year @ 20% off |
| -30 | Renewal contract sent | Signature window |
| -14 | Follow-up if not signed | Address blockers |
| -7 | Personal founder WhatsApp | Final push |
| -1 | Renewal expiration alert | Last chance |

### Renewal Success Criteria

- [ ] ≥ 90% monthly logo retention rate
- [ ] ≥ 110% NRR (Net Revenue Retention) — counts expansions
- [ ] Multi-year contract attach rate ≥ 25%
- [ ] Mid-renewal NPS ≥ 8 (otherwise high churn risk)

### Renewal Red Flags

- Customer goes silent in -30 to -14 window → likely churn
- Customer requests downgrade at renewal → revenue stable, fight to keep
- Customer wants to switch to month-to-month → 2× churn probability
- Customer's champion left → relationship rebuild required

---

## Stage 5 — Advocate (Year 2+)

### Advocacy Programs

1. **Referrals (W13.13):** 5,000 SAR credit per closed deal
2. **Case Studies:** offer to co-publish (gives customer brand boost)
3. **Conference Speaking:** invite customer to Dealix annual event
4. **Beta Access:** early access to R5/R7 features
5. **Board Seat Considerations:** for first 5 enterprise customers (advisory)

### Year 2+ Touchpoints

| Frequency | Touchpoint |
|-----------|-----------|
| Quarterly | Executive sync (60 min) |
| Semi-annual | Roadmap input session |
| Annual | Customer Advisory Board meeting |
| Ad-hoc | Founder personal WhatsApp (preserved) |

---

## Churn Prevention Playbook

### When a Detractor Submits NPS 0-6

**Within 24 hours** (intervention SLA per W13.4):

1. **Founder personally** WhatsApp the contact ("noticed your NPS, can we talk?")
2. **Schedule 30-min call** within 72 hours
3. **Listen 80% / Talk 20%** — let them vent first
4. **Identify root cause** — categorize:
   - Product gap (we don't do what they need)
   - Operational issue (slow response, missed SLA)
   - Compliance concern (PDPL/ZATCA question unresolved)
   - Relationship issue (champion changed, missed touchpoints)
   - Pricing concern (value-perception gap)
5. **Commit to specific fix** within 7 days
6. **Follow-up call** at day 7 to confirm fix landed
7. **Re-survey at day 30** to confirm sentiment shift

### Industry Benchmark (Wave 13 deep research)

24-hour response to detractor → **60% rescue rate** (the customer stays).
72-hour response → 25% rescue rate.
Over 1 week → < 10% rescue rate.

---

## Customer Success Metrics Dashboard

### Tracked Daily (via `GET /api/v1/revenue-metrics/dashboard`)

- MRR + ARR
- Active customer count
- Churn this period
- NRR
- ARPA

### Tracked Per-Customer (via `GET /api/v1/customer-usage/{handle}` + `/customer-success-os/{handle}/health`)

- Health Score (0-100)
- Plan utilization (leads_used / leads_cap)
- Last login recency
- Latest NPS score + milestone
- Days since last touchpoint
- Decision Passport entry count (engagement signal)

### Tracked Per-Cohort (via `GET /api/v1/revenue-metrics/cohort`)

- Month +1, +3, +6, +12 retention
- Cohort lifetime value
- Expansion revenue per cohort

---

## CS Hire Trigger + Job Description

### When to Hire First CS

After customer **#10** (or 6 months in, whichever first).

### CS Lead Job Description (preview for hiring time)

- **Location:** Riyadh or remote-Saudi
- **Reports to:** Founder
- **Comp:** 10-15K SAR/mo + 2% commission on expansion revenue
- **Goal:** ≥ 95% net retention, ≥ 110% NRR by month 6
- **Required:** Arabic + English fluency, B2B SaaS background, customer-empathy demonstrated
- **Bonus:** Saudi enterprise relationships, PDPL/ZATCA familiarity

### First-30-Days Plan for CS Hire

| Week | Focus |
|------|-------|
| 1 | Shadow founder on every customer call |
| 2 | Take over Day 14 + Day 21 touchpoints |
| 3 | Own NPS detractor intervention |
| 4 | Own renewal conversations -90 to -60 |

---

## Anti-Patterns to Avoid

❌ **"Customer Success = Helpdesk"** — CS is proactive expansion + retention, not reactive support tickets.

❌ **"Wait for renewal to talk price"** — Multi-year conversations start at month 4 (W13.1 page).

❌ **"Score is the truth"** — Health Score is *signal*, not gospel. Always verify with human conversation.

❌ **"Same playbook for SMB and enterprise"** — Enterprise (R7) gets bespoke briefings, weekly executive sync. SMB gets templated touchpoints.

❌ **"Save every customer at any cost"** — Bad-fit customer churn is GOOD churn. Don't burn margin on a customer who can't retain.

---

## Verification (the only test that matters)

| Stage | Done when |
|-------|-----------|
| Onboard | Customer #1 hits Day 30 Health Score ≥ 60 |
| Adopt | Customer #1 utilizes ≥ 50% plan cap by Month 3 |
| Expand | First R3/R4/R5 upsell closed by Month 6 |
| Renew | First Y1 renewal achieved at ≥ 100% original ARR |
| Advocate | First customer-referred deal closed |

The Customer Success Playbook isn't a document. It's a discipline.
The discipline begins when customer #1 pays 499 SAR.
