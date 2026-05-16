# Pricing & Packaging v6 — التسعير والباقات

> **Single source of truth for the offer set:** [`docs/COMPANY_SERVICE_LADDER.md`](COMPANY_SERVICE_LADDER.md).
> This doc details pricing rationale and SLAs; the rung names and prices
> below must match the canonical 5-rung ladder.

> **Hard rule:** This doc does NOT change live pricing in code.
> This doc is the **founder's reference** for when + why + how to change it later.

**Owner:** Founder (Decision Pack §S1 covers the formal flip)
**Hard invariant:** Rung 1 Sprint price 499 SAR locked until 3 paid pilots are delivered.
**Stage:** Dealix is pre-revenue with zero customers.

---

## Today (locked) — the canonical 5-rung ladder

| Rung | Offer | Price (SAR) | Pricing basis | Trigger to unlock next rung |
|---|---|---|---|---|
| 0 | **Free AI Ops Diagnostic** | 0 | free | 3 diagnostics delivered |
| 1 | **7-Day Revenue Intelligence Sprint** | 499 | one-shot | 1 paid pilot fully delivered |
| 2 | **Data-to-Revenue Pack** | 1,500 | project | 3 pilots in the same sector |
| 3 | **Managed Revenue Ops** | 2,999–4,999 / month | recurring | 3 consecutive months of paid retainer |
| 4 | **Custom AI Service Setup** | 5,000–25,000 | scoped | 3 pilots delivered + signed publish permission |

**Locked / future — not active offers:** "Executive Command Center",
"Support OS Add-on", and "Agency Partner OS" are not standalone offers. They
may become components of Rung 3 or Rung 4 only after that rung's unlock
trigger is met. Do not quote or sell them.

---

## When to flip pricing

The founder may approve a pricing change ONLY when ALL of the
following are true:

1. **3+ paying pilots completed** (real Moyasar invoices closed, not test-mode)
2. **3+ Proof Packs signed** (customer-attested, with explicit consent)
3. **Decision Pack §S1 signed** in `docs/EXECUTIVE_DECISION_PACK.md`
4. **No active customer complaint** about pilot delivery

If any of these is missing, the price stays locked.

---

## Recommended post-proof pricing (NOT yet authorized)

After conditions above are met, the founder MAY review Rung prices. Any change
keeps the 5-rung structure; only the numbers move, and only with Decision
Pack §S1 justification. Rung 0 stays free.

---

## Inclusions vs exclusions per rung

### Rung 0 — Free AI Ops Diagnostic
- ✅ 1-page bilingual diagnostic in 24-48 hours
- ✅ 3 prioritized opportunities + 1 message draft + 1 risk
- ✅ Next-step recommendation
- ❌ NOT included: external outreach, data processing at scale,
  content publishing.

### Rung 1 — 7-Day Revenue Intelligence Sprint (499 SAR)
- ✅ 10 qualified opportunities
- ✅ Arabic + English outreach drafts
- ✅ 30-day follow-up plan
- ✅ Signed Proof Pack draft
- ❌ NOT included: live external send (the founder/customer sends
  manually), scraped data sources, ranking guarantee.

### Rung 2 — Data-to-Revenue Pack (1,500 SAR)
- ✅ Customer's existing list/CRM cleaned + scored
- ✅ Ranked opportunity map
- ✅ 10 bilingual targeting drafts
- ✅ Sector playbook
- ❌ NOT included: data acquisition (customer brings the data).

### Rung 3 — Managed Revenue Ops (2,999–4,999 SAR/month)
- ✅ Weekly executive brief
- ✅ Monthly approval-ready drafts
- ✅ Monthly Proof Pack + KPI report
- ✅ Monthly strategy session
- ❌ NOT included: live sends, agency-style operational delivery.

### Rung 4 — Custom AI Service Setup (5,000–25,000 SAR)
- ✅ Scoped, customer-specific AI service build
- ✅ Built on top of an existing retainer relationship
- ❌ NOT included: any Custom Enterprise tier without 6+ months retainer history.

---

## SLA per rung

| Rung | Offer | First response SLA | Delivery SLA |
|---|---|---|---|
| 0 | Free AI Ops Diagnostic | 24h to schedule | 24-48h to deliver brief |
| 1 | 7-Day Revenue Intelligence Sprint | 24h to invoice | 7 calendar days to Proof Pack |
| 2 | Data-to-Revenue Pack | 48h to scope | 14 calendar days to delivery |
| 3 | Managed Revenue Ops | 24h to onboard | weekly executive brief each week |
| 4 | Custom AI Service Setup | 48h to scope | scoped per engagement |

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

Discounts on the Rung 1 Sprint would dilute the test we're running:
*does this offer convert at 499 SAR for the target ICP?*

If the prospect won't pay 499, a later, higher price won't convert them either.
Better to move them to the free Rung 0 Diagnostic + nurture than to discount.

---

## Pricing review trigger

**After 3 paid pilots are delivered:**
1. Founder reviews this doc + Decision Pack §S1
2. If GO: update the pricing catalog in code to match the reviewed numbers
3. Keep the 5-rung structure; update [`docs/COMPANY_SERVICE_LADDER.md`](COMPANY_SERVICE_LADDER.md) first, then this doc
4. Run the service readiness check to confirm no fake-`live` flips
5. Open PR; founder reviews; merge

— Pricing & Packaging v6 · Aligned to docs/COMPANY_SERVICE_LADDER.md · Dealix

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
