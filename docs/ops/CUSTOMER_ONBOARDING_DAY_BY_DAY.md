# Customer Onboarding — 7-Day Managed Pilot (Day-by-Day)

> **Owner:** Founder (Sami). White-glove for first 10 customers; productized after.
> **Scope:** This document covers the **R1 Managed Pilot (499 SAR)** onboarding.
> **Goal:** convert pilot → Growth (2,999 SAR/mo) by Day 7.
> **Refund trigger:** Dealix replied to <50% of incoming Arabic leads OR avg response >5 min for 3+ days.

---

## Pre-Day-1 (the moment they say "yes")

Within 60 minutes of verbal/written commitment:

- [ ] Send 499 SAR Moyasar checkout link via WhatsApp
  - Plan: `pilot` (after W1.3 adds metered options, may swap to `pilot_managed`)
  - Currency: SAR, 1× one-off
- [ ] Once paid: log via `python scripts/pipeline_tracker_update.py paid --id N --plan pilot --revenue 499`
- [ ] Send welcome WhatsApp (template: `templates/first_customer_welcome.txt`)
- [ ] Send welcome email (template: `templates/first_customer_welcome.eml`)
- [ ] Add to `docs/ops/active_pilots.md` (create if doesn't exist; one section per customer)
- [ ] Schedule Day-1 discovery call (30 min, founder-led)
- [ ] Send PDPL consent form for data processing (`landing/pdpl-consent.html` deep-link)

---

## Day 1 — Discovery + Setup (4 hours founder time)

**Morning (Discovery Call, 30 min):**
- [ ] Run S1 Diagnostic intake live with customer (`/api/v1/diagnostic`)
- [ ] Capture: top 3 pain points, current inbound volume, existing tools, decision-makers, success criteria
- [ ] Set expectation: "We'll auto-reply with your approval first 3 days, then mixed-mode"

**Afternoon (Technical Setup, 3.5 hours):**
- [ ] Create customer tenant: `python scripts/create_tenant.py --handle {handle} --name "{Company}"`
- [ ] Provision WhatsApp Business number (via existing Meta integration or Green API)
- [ ] Configure inbound webhook routing to tenant
- [ ] Email DNS records sent for SPF/DKIM (15 min customer task)
- [ ] Pre-seed first 20 prospects from customer's existing data (CSV import)
- [ ] Test inbound: customer sends 1 test message → Dealix replies → customer approves → message goes out

**End-of-day:** Send "Day 1 recap" WhatsApp with key results + Day 2 plan.

---

## Day 2 — First Live Inbound Day

**Founder time:** 2 hours (monitoring + approvals)

- [ ] Monitor approval queue every 2 hours during business hours
- [ ] Aim: 80%+ of AI drafts approved as-is, <20% edited
- [ ] Track: number of inbound leads, avg response time, customer satisfaction signals
- [ ] Capture 1–2 great replies for Day 7 case study
- [ ] EOD WhatsApp: "Today's metrics — X inbound, Y replied, Z still pending"

**If <50% of inbound was Arabic-replied:** flag immediately, root cause, fix overnight.

---

## Day 3 — Calibration

**Founder time:** 1.5 hours

- [ ] Review past 2 days of approvals — identify pattern of edits the customer makes
- [ ] Tune system prompt for that customer (`api/routers/ai_workforce.py` tenant config)
- [ ] Add customer's preferred phrasing to local glossary
- [ ] Mid-day customer check-in (15-min call): "What's working? What's annoying?"

---

## Day 4 — Mixed-Mode Activation

**Founder time:** 1 hour

- [ ] Move 50% of low-risk replies to auto-send (high-confidence, FAQ-like)
- [ ] Keep 50% in approval queue (high-stakes: pricing, custom requests, escalations)
- [ ] Verify Decision Passport entries for every external commitment
- [ ] Customer trains on the approval UI themselves (Loom screen-share)

---

## Day 5 — Customer Health Score Calibration (B1 in v5)

**Founder time:** 1 hour

- [ ] Run `/api/v1/customer-success-os/{handle}/health` — review score components
- [ ] Adjust signals based on real intake events (this is the B1 work in §17)
- [ ] Customer sees their own health dashboard for the first time

---

## Day 6 — Decision Passport Review Session

**Founder time:** 1 hour

- [ ] 30-min call: walk customer through every external commitment Dealix made on their behalf this week
- [ ] Show audit log (`/api/v1/decision-passport/{handle}/log`)
- [ ] Demonstrate PDPL compliance: consent recorded, data retention policy applied
- [ ] Demonstrate ZATCA invoice (if any billable services delivered to their customers)

---

## Day 7 — Decision Day

**Founder time:** 2 hours

**Morning (90 min): Pilot wrap-up call**
- [ ] Read out final 7-day metrics:
  - Total inbound leads handled: X
  - Arabic-reply percentage: Y% (target: >70%)
  - Avg response time: Z minutes (target: <5)
  - Demos booked from inbound: N
  - Customer-rated reply quality (1–5): R
- [ ] Show top-3 best replies (customer's own words: "I would've sent this")
- [ ] Show 1–2 misfires + how they were caught by approval gate
- [ ] **Compute pilot success:** Did Dealix handle 50%+ inbound? Avg <5 min response?
  - YES → present Growth plan (2,999 SAR/mo); offer 14-day commit window with 7-day money-back
  - NO → refund 499 SAR, capture lessons, log churn reason

**Afternoon (30 min): Contract or Exit**
- [ ] Growth signed: Moyasar subscription link → first month charged → tenant moved from `pilot` to `growth`
- [ ] Refund: Moyasar refund button → customer data export emailed (PDPL Art. 14) → tenant archived
- [ ] In either case: 5-min retro call within 48 hours ("what did we learn?")

**EOD:**
- [ ] Update tracker: `python scripts/pipeline_tracker_update.py paid --id N --plan growth --revenue 2999`
- [ ] Draft case study: `docs/case-studies/{handle}.md` (real one — replaces hypothetical from W1.1)

---

## Common Pitfalls (and how to avoid)

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Customer expects 100% AI autonomy day-1 | "Why do I have to approve everything?" | Set expectation pre-Day-1: "Mixed-mode by Day 4" |
| Founder over-edits replies | Approval queue piles up | Tune system prompt aggressively Day 2-3 |
| Customer's inbound is too low | <5 messages/day | Suggest LaaS add-on (R3) for warm pipeline |
| Refund attempt outside criteria | "I want my money back, I'm bored" | Refund anyway. Trust > 499 SAR. |
| Customer trying to use Dealix outbound | "Can you send cold messages?" | Politely decline. Dealix is inbound + approval-first. |

---

## After Day 7 (Growth signed)

- [ ] Schedule weekly check-in for first month (founder calls 15 min every Friday)
- [ ] Set up health-score alert: notify founder if score drops below 70
- [ ] Ask for 1 referral by Day 14 ("Who else has the same pain?")
- [ ] Ask for testimonial by Day 30 (recorded 60-sec video or written quote)

---

## Refund SOP (if pilot fails)

1. Verify trigger (response rate or latency from logs)
2. Apologize directly, no excuses
3. Initiate Moyasar refund (full 499 SAR)
4. Generate PDPL Art. 14 data export → email customer
5. Schedule 30-min lessons-learned call within 48h
6. Update tracker: `--status declined --note "{reason}"`
7. Add anonymized failure pattern to `docs/ops/pilot_failure_patterns.md` (create if needed)
