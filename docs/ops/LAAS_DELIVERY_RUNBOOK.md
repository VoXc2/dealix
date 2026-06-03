# LaaS (Lead-as-a-Service) Delivery Runbook

> **Stream:** R3 in v4 §3 — activated after customer #3.
> **Pricing:** 25 SAR per Arabic-replied lead OR 150 SAR per booked demo OR 50 SAR/lead flat-rate.
> **Margin:** ~90% (lead cost ~5 SAR via Hunter+Maps+Firecrawl quotas; sale ~50 SAR).
> **Cross-refs:** `auto_client_acquisition/pipeline.py`, `docs/business/PRICING_AND_PACKAGES.md` Tier 5, `scripts/lead_pipeline_smoke.py` (W1.2).

---

## What Customer Buys

A weekly delivery of qualified Saudi B2B leads matching their ICP, with three pricing models the customer picks:

| Model | Trigger | Price |
|-------|---------|-------|
| **Per-Reply** | Lead engaged in Arabic conversation (≥ 2 messages exchanged) | 25 SAR |
| **Per-Demo** | Lead booked a demo on customer's calendar | 150 SAR |
| **Flat-Rate** | All discovered + enriched leads delivered (whether they reply or not) | 50 SAR/lead |

Customer chooses per-engagement model. Most pick Per-Reply (lower risk).

## How Dealix Delivers

**Tuesday of each week (founder time: ~2 hours):**

1. Pull customer's ICP filter from their tenant config:
   - Industry (Saudi SaaS / Real Estate / Logistics / Hospitality)
   - Company size (1-50 / 50-500 / 500+)
   - Decision-maker role (Founder / VP Sales / Head of Operations)
   - Location (Riyadh / Jeddah / Dammam / Saudi-wide)
   - Tech stack signals (uses Salla / uses Foodics / etc. via Wappalyzer)

2. Run pipeline:
   ```bash
   python scripts/run_laas_weekly.py --customer-handle <handle> --target-count 50
   ```

3. Pipeline executes in sequence:
   - **Discovery** (Google Search + Tavily) → 200-500 candidate accounts
   - **Enrichment** (Maps + Hunter + Firecrawl + Wappalyzer) → 100-200 with full data
   - **Suppression** (against customer's existing CRM + Dealix's global suppression list) → 50-100 net new
   - **Scoring** (ICP fit + buying signals) → top 50 ranked

4. Output: CSV + customer dashboard view + WhatsApp pings to those who opt-in to PDPL Art. 5 consent.

5. Wait for replies. Each Arabic-reply triggers metered billing in Moyasar (R3 pricing config from W1.3).

## Delivery SLA

| Stage | SLA |
|-------|-----|
| Customer ICP intake → first weekly batch | 5 business days |
| Weekly batches | Every Tuesday by 12:00 AST |
| Reply detection → invoicing | Within 24 hours |
| Customer questions/feedback | < 2 hours during business hours |

## What's NOT Included

- ❌ **Outbound cold messaging** — LaaS is enrichment + warm intro setup, not cold spam. PDPL forbids.
- ❌ **LinkedIn data** — `NO_LINKEDIN_AUTO` flag. Use Apollo (post customer #3) instead.
- ❌ **Custom integrations to customer CRM** — that's R5 (Bespoke AI Setup) territory.
- ❌ **Reply quality guarantee** — we deliver the lead and the AI-assisted intro; customer's product/pitch determines reply rate.

## Cost Structure Per Lead Delivered

| Cost item | Per-lead amount | Notes |
|-----------|------------------|-------|
| Google Maps API | 0.50 SAR | $0.017 USD per 1K calls |
| Hunter.io email lookup | 1.20 SAR | 50/day free tier; over: $0.05/lookup |
| Firecrawl page extract | 1.50 SAR | $0.40 USD per 1K pages |
| Wappalyzer fingerprint | 0.30 SAR | $0.05 USD per 1K calls |
| Anthropic/OpenAI scoring | 1.50 SAR | per lead, ~2K tokens |
| **Total per lead delivered** | **~5 SAR** | |
| **Sale per Arabic-replied lead** | **25 SAR** | |
| **Gross margin** | **~80%** | |

## When to Refund

- Lead delivered but customer can prove the company doesn't exist (phantom data)
- Same lead delivered twice in one month (Dealix's suppression failed)
- Lead is on customer's "do not contact" list provided at intake

NOT a refund trigger: lead didn't reply, lead was already in customer's CRM (must be in pre-shared suppression list), customer's outreach was poor.

## Invoicing Cadence

- **Weekly** for Per-Reply and Per-Demo (charge after the trigger event)
- **Monthly** for Flat-Rate (Moyasar subscription, prepaid)
- All invoices ZATCA Phase 2 compliant (`integrations/zatca.py`)

## When to Decline LaaS Service

- Customer asks for non-Saudi geo → decline (this is the Saudi-sovereign moat, don't dilute)
- Customer wants > 500 leads/month → decline (founder bandwidth ≤ 200/customer until automation hardens)
- Customer wants real-time delivery → decline (weekly batches preserve quality)
- Customer's ICP is so narrow that fewer than 10 leads/week exist → decline + suggest broader filter

## Quality Metrics (track weekly)

| Metric | Target | Where measured |
|--------|--------|----------------|
| Leads delivered per customer | 50/week | Tracker dashboard |
| Reply rate | ≥ 15% | Triggered events in Moyasar |
| Demo booking rate | ≥ 3% of delivered | Calendar integration |
| Suppression hits (avoided dupes) | ≥ 90% accuracy | Dedupe pipeline logs |
| Customer NPS (monthly) | ≥ 50 | Manual survey |

## Escalation Triggers

If any of these for 2 consecutive weeks, pause LaaS for that customer until root-caused:

- Reply rate < 8%
- Customer complaints ≥ 3
- Customer's suppression list grew by > 20% (sign their CRM has dupes you're hitting)
- Lead cost exceeded 8 SAR/lead (margin compression — investigate provider quota burn)

## Customer Onboarding to LaaS (after they sign)

- [ ] Day 1: ICP intake interview (30 min) — populate tenant config
- [ ] Day 2: Customer uploads existing CRM CSV → seed suppression list
- [ ] Day 3: Customer chooses pricing model (Per-Reply / Per-Demo / Flat-Rate)
- [ ] Day 4: First weekly batch generated → delivered → customer reviews
- [ ] Day 5: Customer approves/rejects sample → ICP tuned
- [ ] Day 7: First WhatsApp pings sent → wait for replies
- [ ] Day 14: First invoice cycle complete; review metrics with customer

## Automation Roadmap (post customer #5)

Move from "founder runs pipeline weekly" to:
1. **Customer #5:** Cron job auto-generates batches; founder reviews + approves before send
2. **Customer #10:** Auto-send batches if customer's reply rate > 15% prior month; flag for review if < 15%
3. **Customer #15:** Fully autonomous (founder only intervenes on escalation triggers above)
4. **Customer #20:** Customer-self-serve UI for ICP tuning, eliminate weekly call entirely

---

## Validation This Service Is Ready

Before offering LaaS to customer #1 of this service:

- [ ] `scripts/lead_pipeline_smoke.py` passes against 10 real Saudi B2B targets (W1.2)
- [ ] All 7 lead adapter env vars set in production (`docs/ops/PRODUCTION_ENV_TEMPLATE.md` P3)
- [ ] Moyasar Per-Reply and Per-Demo plans configured (W1.3)
- [ ] ZATCA invoice template tested with 1-SAR sample charge
- [ ] PDPL consent flow tested end-to-end (customer-side opt-in works)
- [ ] Suppression list dedupe tested with 1000-row sample CSV
- [ ] First customer ICP intake interview script rehearsed
