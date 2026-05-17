# Pricing & Packaging v6 — التسعير والباقات

> **SUPERSEDED — 2026-05-17.** The Governed Revenue & AI Ops ladder (Decision Ledger D-003)
> is now canonical. For current offers and prices, see
> [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) and
> [`strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md`](strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md).
> The "When to flip pricing" process below remains useful as a price-governance reference.

**Date:** 2026-05-05 (original) · superseded 2026-05-17
**Owner:** Founder (Decision Pack §S1 covers the formal flip)

---

## Current ladder — Governed Revenue & AI Ops

Canonical source: [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md).

| Rung | Offer | Price | Why this rung exists |
|---|---|---|---|
| 0 | **Governed Revenue & AI Ops Risk Score + Sample Proof Pack** | 0 SAR | Door-opener; risk score + sample proof pack. |
| Entry | **7-Day Governed Revenue & AI Ops Diagnostic** | 4,999 / 9,999 / 15,000 / 25,000 SAR (4 tiers) | Evidenced diagnosis: workflow map, top 3 decisions, proof pack. |
| Sprint | **Revenue Intelligence Sprint** | 25,000 SAR+ (scoped) | Governed execution of the top decisions. |
| Retainer | **Governed Ops Retainer** | 4,999–35,000 SAR/month (scoped) | Monthly governed decision rhythm + proof. |
| Adjacent | **Board Decision Memo · AI Governance / Trust Pack Lite · CRM/Data Readiness for AI** | scoped | Specific board, governance, or data-readiness needs. |

---

## When to flip pricing

The founder may approve a pricing change ONLY when ALL of the
following are true:

1. **3+ paying Pilots completed** (real Moyasar invoices closed, not test-mode)
2. **3+ Proof Packs signed** (customer-attested, with explicit consent)
3. **Decision Pack §S1 signed** in `docs/EXECUTIVE_DECISION_PACK.md`
4. **No active customer complaint** about Pilot delivery

If any of these is missing, the price stays locked.

---

## Recommended post-proof pricing (NOT yet authorized)

After conditions above are met, the founder MAY change to:

| Tier | Today | After 5 customers |
|---|---|---|
| Free Diagnostic | 0 SAR | 0 SAR (stays free) |
| Growth Starter Pilot | 499 SAR | retire — replaced by Growth Starter Standard |
| **Growth Starter Standard** (new) | — | 990–1,500 SAR (no longer "introductory") |
| Data to Revenue | 1,500–3,000 SAR | 1,800–3,600 SAR (+20%) |
| Executive Growth OS | 2,999 SAR/mo | 3,499–4,499 SAR/mo |
| Partnership Growth | 3,000–7,500 SAR | 4,500–9,000 SAR (+50%) |
| **Compliance-tier premium** (new) | — | +30% on any tier for full PDPL audit pack |

Justification of each move is to be captured in Decision Pack §S1.

---

## Inclusions vs exclusions per tier

### Free Growth Diagnostic
- ✅ 30-min founder review
- ✅ 3 specific recommendations
- ✅ Best-first-offer recommendation
- ❌ NOT included: external outreach, data processing at scale,
  content publishing.

### Growth Starter Pilot (499 SAR)
- ✅ 10 qualified opportunities
- ✅ Arabic outreach drafts
- ✅ 72-hour follow-up plan
- ✅ Signed Proof Pack
- ❌ NOT included: live external send (the founder/customer sends
  manually), scraped data sources, ranking guarantee.

### Data to Revenue
- ✅ Customer's existing list/CRM cleaned + scored
- ✅ Priority queue
- ✅ Bilingual messaging suggestions
- ✅ Follow-up plan
- ✅ Proof Pack
- ❌ NOT included: data acquisition (customer brings the data).

### Executive Growth OS (2,999 SAR/month)
- ✅ Daily brief (7AM KSA)
- ✅ Weekly executive report
- ✅ Pipeline review
- ✅ Proof ledger access
- ✅ Growth experiments queue
- ✅ Role briefs (CEO / Sales / Growth / etc.)
- ❌ NOT included: live sends, agency-style operational delivery.

### Partnership Growth
- ✅ Partner candidate list
- ✅ Fit score per partner
- ✅ Warm intro drafts
- ✅ Co-branded proof pack
- ✅ Referral tracking
- ❌ NOT included: cold outreach to partners (warm only).

---

## SLA per tier

| Tier | First response SLA | Delivery SLA |
|---|---|---|
| Free Diagnostic | 24h to schedule | 48h to deliver brief after call |
| Growth Starter Pilot | 24h to invoice | 7 calendar days to Proof Pack |
| Data to Revenue | 48h to scope | 14 calendar days to delivery |
| Executive Growth OS | 24h to onboard | daily brief by 7AM KSA each weekday |
| Partnership Growth | 48h to scope | 21 calendar days to first 3 introductions |

SLAs are documented in `auto_client_acquisition/service_quality/sla_tracker.py`
where applicable.

---

## What pricing does NOT cover (regardless of tier)

- ❌ Scraping
- ❌ Cold WhatsApp / cold email
- ❌ LinkedIn DM automation
- ❌ Live charge automation
- ❌ Revenue / ranking guarantees
- ❌ Customer data exfiltration
- ❌ Auto-send anything to a customer's customers

These are platform-level forbidden tools (`agent_governance.FORBIDDEN_TOOLS`),
not pricing options.

---

## Why "no discount" is the policy

Discounts on the Pilot would dilute the test we're running:
*does this offer convert at 499 SAR for the target ICP?*

If the prospect won't pay 499, they won't pay 990 later. Better to
move them to free Diagnostic + nurture for 90 days than to discount.

The only "discount" is the Pilot itself — locked at the introductory
price for the first 5 customers — and that's a deliberate
loss-leader to seed proof, not a price ladder.

---

## Pricing review trigger

**At customer #5 paid Pilot:**
1. Founder reviews this doc + Decision Pack §S1
2. If GO: update `auto_client_acquisition/finance_os/pricing_catalog.py`
3. Update YAML matrix `service_id=growth_starter_pilot` → `growth_starter_standard`
4. Update `docs/PRICING_STRATEGY.md` with the new ladder
5. Run `python scripts/verify_service_readiness_matrix.py` to confirm
   no fake-`live` flips
6. Commit with message `chore(pricing): retire Pilot 499 → Standard 990 (Decision §S1)`
7. Open PR; founder reviews; merge

— Pricing & Packaging v6 v1.0 · 2026-05-05 · Dealix
