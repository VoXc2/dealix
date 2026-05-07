# Finance Dashboard — Dealix

**Status:** DRAFT — Google Sheet to be created by founder Day 1 of Wave 7
**Owner:** Sami (founder) · accountant reviews quarterly
**Last updated:** 2026-05-07
**Companion docs:** `docs/REFUND_SOP.md` · `docs/INVOICING_ZATCA_READINESS.md` · `docs/ops/MANUAL_PAYMENT_SOP.md` · `auto_client_acquisition/revenue_profitability/` · Plan §23.5.6

> **Why this doc exists:** Without a single financial dashboard, the founder cannot answer "how is the business doing this week?" honestly to himself, the lawyer, or a future investor. With it, every Friday becomes a 5-minute truth check.

---

## 1. The dashboard — Google Sheet structure

Create one Google Sheet titled **`Dealix — Finance Truth (live)`**. Six tabs:

| # | Tab name | Purpose | Update frequency |
|---|---|---|---|
| 1 | Customers | one row per customer (paid + pending) | weekly |
| 2 | Revenue | monthly MRR + cumulative | weekly |
| 3 | Costs | tools + founder time + transaction fees | monthly |
| 4 | Margin | Sprint vs Partner gross margin | monthly |
| 5 | Runway | cash on hand / monthly burn | monthly |
| 6 | Tax | Zakat + VAT estimates | quarterly |

**Storage:** founder's Google Drive, shared with accountant only. NEVER put bank account numbers, IBAN, or payment screenshots into the sheet. Reference them by ID.

---

## 2. Tab 1 — Customers

| Column | Type | Notes |
|---|---|---|
| customer_handle | string | Same as Wave 6 CLI handle |
| company_name | string | Display only |
| sector | enum | real_estate / agencies / services / consulting / training / etc |
| sku | enum | sprint_499 / partner_2999 / partner_4999 / partner_12000 / partner_15000 |
| invoice_intent_at | date | When founder sent Sprint Brief |
| payment_evidence_at | date | When evidence uploaded |
| payment_confirmed_at | date | Ground truth — only this counts as revenue |
| amount_sar | number | Confirmed amount only (0 if unpaid) |
| commitment_months | number | 1 (Sprint) · 4 (Partner) |
| status | enum | active / completed / refunded / churned |
| founder_hours_logged | number | Cumulative hours founder spent |
| nps_score | number | -1 to 10 (deployed at Day 14 + Month 3) |
| renewal_due_at | date | Trigger for upsell call |

---

## 3. Tab 2 — Revenue (the truth tab)

The only revenue rule: **`payment_confirmed_at` is filled = revenue counted. Everything else is intent, not revenue.**

| Month | Sprint count | Partner count | New MRR | Total MRR | Cumulative recognized | Refunds |
|---|---|---|---|---|---|---|
| 2026-05 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2026-06 | _filled_ | _filled_ | _filled_ | _filled_ | _filled_ | _filled_ |
| ... | | | | | | |

**Formula notes:**
- New MRR = sum of new Partner contracts × monthly amount; Sprint adds nothing to MRR (one-time)
- Total MRR = sum of all active Partner subscriptions (not Sprints)
- Cumulative recognized = sum of all `payment_confirmed_at` amounts to date
- Refunds = subtract from cumulative; never negative MRR (drop the customer instead)

**Cross-check rule:** at month-end, `confirmed_revenue_sar` from `/api/v1/revenue-profitability/revenue-summary` should equal Total MRR row. If not → reconcile in 1 hour.

---

## 4. Tab 3 — Costs

### Fixed monthly costs (forecasted)

| Item | Cost (SAR/mo) | Vendor | Notes |
|---|---|---|---|
| Railway hosting | ~150 | Railway | api.dealix.me |
| Cloudflare DNS | 0 | Cloudflare | free tier |
| GitHub Pages | 0 | GitHub | free for public repo |
| Hunter API (when activated) | ~185 | Hunter.io | $49/mo conv. |
| Anthropic API (founder usage) | variable | Anthropic | track via dashboard |
| Domain | ~10/mo amortized | Namecheap | dealix.me |
| **Total floor** | **~345 SAR/mo** | | |

### Variable monthly costs (per customer)

| Item | Cost | Notes |
|---|---|---|
| Moyasar transaction fee | 2.75% per charge | only after live |
| Anthropic API per Sprint | ~30-80 SAR | LLM-grounded narrative |
| Founder hours (opportunity cost) | 200 SAR/hr × 40h month 1, 20h month 3+ | not cash, but track |

### Year-1 cash budget ceiling

- Legal (initial): 15,000 SAR (per `LEGAL_ENGAGEMENT.md` §5)
- Tools: 4,200 SAR (350 × 12)
- Hosting + APIs: ~5,000-10,000 SAR depending on usage
- Cybersecurity insurance (month 4+): 2,500-5,000 SAR
- Conferences / community / PR: 5,000 SAR
- **Total year-1 cash ceiling:** **~35,000-50,000 SAR**

---

## 5. Tab 4 — Gross margin

Per `auto_client_acquisition/revenue_profitability/gross_margin.py` patterns.

### Sprint customer (one-time)

| Item | Value |
|---|---|
| Revenue | 499 SAR |
| Direct cost (Anthropic API) | ~50 SAR |
| Founder hours (40h × 200 opportunity cost) | 8,000 SAR (NOT cash) |
| **Cash margin** | **~449 SAR positive** |
| **Opportunity-adjusted margin** | **~-7,551 SAR (loss-leader by design)** |

### Partner customer (4-month commit)

| Item | Value (4 months) |
|---|---|
| Revenue | 48,000 SAR (12,000 × 4) |
| Direct cost (Anthropic + Moyasar fees) | ~1,500 SAR |
| Founder hours (~80h × 200) | 16,000 SAR (NOT cash) |
| Tools allocation | ~1,400 SAR |
| **Cash margin** | **~46,500 SAR (97%)** |
| **Opportunity-adjusted margin** | **~30,500 SAR (63%)** |

**Net per Sprint→Partner pair:** -7,551 + 30,500 = **+22,949 SAR over 4 months** (60% margin opportunity-adjusted).

> **Hard rule:** every margin number is `is_estimate=True` (per `revenue_truth.py`). No "guaranteed margin" claims to investors.

---

## 6. Tab 5 — Runway

Simple monthly burn-rate calc:

```
Cash on hand:           [founder fills, e.g., 150,000 SAR personal runway]
Fixed monthly burn:     ~350 SAR (tools)
+ One-time legal:       15,000 SAR (month 1)
+ Founder living wage:  [founder's actual SAR/mo from personal funds — NOT counted as Dealix burn but tracked]

Effective burn during Wave 7: ~350-500 SAR/mo
Runway: cash / effective_burn months
```

**Trigger conditions:**
- Runway drops below 6 months → pause Wave 7, evaluate angel-round timing
- Runway drops below 3 months → emergency cash mode (sell more Sprints aggressively, defer hiring, freeze tools)

---

## 7. Tab 6 — Tax (Zakat + VAT)

> **Disclaimer:** Saudi tax law is complex. Use this section only as a planning estimate. File via certified accountant.

### VAT (15%)

- All Dealix invoices in Wave 7 should include VAT line
- Sprint 499 SAR = 433.91 ex-VAT + 65.09 VAT
- Partner 12,000 SAR = 10,434.78 ex-VAT + 1,565.22 VAT/month
- Filed quarterly via ZATCA portal
- E-invoicing (Phase 2 of ZATCA) deferred — manual invoicing OK until ZATCA notifies (per `INVOICING_ZATCA_READINESS.md`)

### Zakat (~2.5%)

- Applied to net Zakat-eligible base (working capital + receivables - liabilities)
- For Wave 7 founder-only entity with minimal balance sheet, expected Zakat = small (≤500 SAR for first year)
- File annually with ZATCA

### Provision rate to set aside

For every payment_confirmed:
- Set aside **15%** for VAT (already collected from customer; pay-through to ZATCA)
- Set aside **3%** as Zakat reserve (estimate, accountant adjusts)
- **Net retained: 82%** — this is the actual cash margin to allocate to costs / runway / founder

---

## 8. Friday review — 5 minutes

Every Friday, founder opens the sheet and verifies:

1. New `payment_confirmed_at` rows match Wave 6 CLI ledger? (cross-check with `docs/wave6/live/payment_state.json`)
2. Total MRR matches `/api/v1/revenue-profitability/revenue-summary`?
3. Refunds in past week recorded in Tab 1 + revenue subtracted in Tab 2?
4. Runway calc still ≥6 months?

If any answer is NO → 30-minute deep dive same day.

---

## 9. Investor-readiness checkpoint (when MRR ≥ 50K SAR/month)

Per Plan §8.4, when MRR hits ~50K SAR/month, prepare for friendly angel round:

1. Export this dashboard as a 1-page PDF
2. Cross-reference with `confirmed_revenue_sar` from API (the ground truth)
3. Add NRR (from `CUSTOMER_SUCCESS_SOP.md` §3)
4. Add CAC payback per cohort
5. Schedule first investor coffee — only when 3+ Partners signed

**Investor truth rules:**
- Show only `payment_confirmed` revenue, not invoice intent
- Mark every projection with "estimate, not commitment"
- Provide source for every benchmark cited

---

## 10. Hard rules

- ❌ Never report MRR including invoiced-but-unpaid contracts
- ❌ Never include refunded customers in active count
- ❌ Never include opportunity-cost margin in cash margin
- ❌ Never share dashboard publicly or with prospects ("we have N customers" can be said only when N ≥ 3 paid)
- ❌ Never mix personal and Dealix bank accounts (founder uses separate sub-account or new account)
- ✅ Always update on Friday — even if zero changes
- ✅ Always cross-check API ground truth weekly
- ✅ Always set aside VAT immediately on receipt
- ✅ Always file Zakat + VAT on time (quarterly VAT, annual Zakat)
