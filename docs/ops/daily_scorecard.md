# 📊 Dealix — Daily Scorecard

**Update at end of each working day (17:00 Saudi time).**

---

## Day 2 — Execution Day 1

**Date:** 2026-04-24 (continued session)
**Production:** ✅ Green (healthz 200, pricing 200, landing 200 — verified this session)
**Custom Domain:** ✅ **https://dealix.me LIVE** with Let's Encrypt SSL (valid until 2026-07-23, auto-renew). GitHub Pages DNS check successful. www + all subpages serving 200 with proper cert.
**API Custom Domain:** 🟡 api.dealix.me DNS + TXT verify in place; awaiting Sami click "Update" in Railway → Networking dialog to finalize SSL + routing.
**Moyasar:** ✅ Webhook secret live (401 bad_signature on test confirms secret read). sk_live_ KYC-activated but key in Railway still returning 502 — likely paste whitespace; manual path unaffected.
**Lead Intelligence Router v1:** ✅ Shipped — Prospector agent upgraded with 9 opportunity types + 100-pt scoring + risk levels + next-action enum. 5 specs in `docs/ops/lead_machine/`. Top-10 direct + Top-5 partner leads scored. Live UI on dealix.me.
**Operating docs shipped today:** objection_library_ar · sector_playbooks · agency_partner_kit · reply_handling_log · manual_payment_log · partner_send_queue.

### Inputs (target → actual)
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| DMs sent | 5 | 0 | Message 1 delivered to Sami, awaiting SENT |
| Agency DMs sent | 2 | 0 | Partner Msg 1 prepared, not released |
| Follow-ups sent | 0 | 0 | Nothing to follow up yet |
| Content posts | 1 | 0 | Founder Launch Post queued for Sami |
| New leads added | 0 | 0 | Pipeline at 50, no need |

### Responses
| Metric | Target | Actual |
|--------|--------|--------|
| Positive replies | 0-1 | 0 |
| Demos booked | 0-1 | 0 |
| Demos completed | 0 | 0 |

### Revenue
| Metric | Target | Actual |
|--------|--------|--------|
| Pilots started | 0 | 0 |
| Payments requested | 0 | 0 |
| Payments received | 0 SAR | 0 SAR |
| Cumulative MRR | 0 SAR | 0 SAR |

### Blockers / Status
- ✅ Production OK (backend + landing + pricing all 200)
- 🟡 Moyasar live blocked on KYC — `/api/v1/checkout` returns `payment_provider_error` (502)
- 🟡 No `sk_test_` key provided to session — sandbox round-trip cannot be proven until Sami sends one
- ✅ Manual payment path (`MANUAL_PAYMENT_SOP.md` + `FIRST_REVENUE_ATTEMPT.md`) fully operational — no prospect will be lost if they say yes
- ⏸️ LinkedIn access is Sami-side — all DMs gated on `SENT` confirmations

### Next Single Action
**Sami sends Message 1 to Abdullah Al-Assiri → replies `SENT`.** Everything else waits on that one event.

---

## Day 1 — Launch Day

**Date:** 2026-04-24
**Production:** ✅ Green (backend + landing + healthcheck all 200)

### Inputs (target → actual)
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| New leads added | 10 | 50 | Pipeline tracker seeded |
| DMs sent | 5 | 0 | 10 queued as GitHub Issues #99-108 |
| Agency DMs sent | 2 | 0 | Queued in issues |
| Follow-ups sent | 0 | 0 | N/A — Day 1 |
| Content posts | 1 | 0 | Queued as Issue #109 |

### Responses (target → actual)
| Metric | Target | Actual |
|--------|--------|--------|
| Positive replies | 0-1 | 0 |
| Demos booked | 0-1 | 0 |
| Demos completed | 0 | 0 |

### Revenue
| Metric | Target | Actual |
|--------|--------|--------|
| Pilots started | 0 | 0 |
| Payments requested | 0 | 0 |
| Payments received | 0 SAR | 0 SAR |
| Cumulative MRR | 0 SAR | 0 SAR |

### Blockers
- 🔴 Moyasar KYC (Sami → Issue #110)
- 🔴 First DM not sent (Sami → Issues #99-108)
- 🟡 Sentry DSN empty (Sami → Issue #111)

### Tomorrow's Top 5 Actions
1. Send 5 Tier-A direct DMs (Issues #99-103)
2. Send 5 agency partner DMs (Issues #104-108)
3. Publish Founder Launch post (Issue #109)
4. Complete Moyasar KYC OR send test key (Issue #110)
5. Set up Sentry DSN (Issue #111)

---

## Template — Day N

Copy this block each day:

```
## Day N — YYYY-MM-DD

**Production:** ✅ / ❌ [explain if red]

### Inputs
| Metric            | Target | Actual |
|-------------------|--------|--------|
| New leads added   | 10     | __     |
| DMs sent          | 5      | __     |
| Agency DMs sent   | 2      | __     |
| Follow-ups sent   | 5      | __     |
| Content posts     | 1      | __     |

### Responses
| Metric            | Target | Actual |
|-------------------|--------|--------|
| Positive replies  | 1-2    | __     |
| Demos booked      | 0-1    | __     |
| Demos completed   | 0-1    | __     |

### Revenue
| Metric             | Target | Actual     |
|--------------------|--------|------------|
| Pilots started     | 0-1    | __         |
| Payments requested | 0-1    | __         |
| Payments received  | 0 SAR  | __ SAR     |
| Cumulative MRR     | 0 SAR  | __ SAR     |

### Blockers
- [list open blockers]

### Tomorrow's Top 5 Actions
1. 
2. 
3. 
4. 
5. 

### Learning
- Best channel today: __
- Biggest blocker: __
- Change for tomorrow: __
```

---

## Weekly Review Template (fill every Friday 17:00)

```
## Week N Review — YYYY-MM-DD

### Funnel Conversion
- Touches: __
- Reply rate: __% (target 5%)
- Demo booking rate: __% (target 40% of replies)
- Demo show rate: __% (target 70%)
- Close rate: __% (target 20%)
- Payment completion: __% (target 80%)

### Revenue
- New MRR this week: __ SAR
- Churn this week: __ SAR
- Net new MRR: __ SAR
- Cumulative MRR: __ SAR

### Best / Worst
- Best-converting segment: __
- Worst-performing segment: __
- Kill this segment: __
- Double down on: __

### Experiment for next week
- Hypothesis: __
- Metric: __
- Outcome target: __
```

---

## 30-Day Cumulative Dashboard

Update this section on 30-day mark:

```
## 30-Day Dashboard — YYYY-MM-DD

Leads:          __ contacted  / 250 target
Demos:          __ completed  / 20 target
Pilots:         __ started    / 5 target
Paid:           __ customers  / 2 target
MRR:            __ SAR        / 4,000 SAR target

Partners:       __ signed     / 1 target
Referrals:      __ received   / 0 target
Case studies:   __ published  / 0 target
```

---

**This file is the single scorecard for Dealix company operations.**
