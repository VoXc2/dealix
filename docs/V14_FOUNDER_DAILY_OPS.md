# Dealix — Founder Daily Ops Playbook

**Date:** 2026-05-06
**Audience:** Sami (founder, sole operator) — Wave 2 / Wave 2.5
**Companion docs:** `docs/V14_TURNKEY_PACKAGE.md` · `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` · `docs/V14_7_DAY_REVENUE_PLAN.md`
**Status:** active until Day 30 customer signal synthesis

> One-liner: _"Same plays every day. Same plays every customer. Predictable rhythm so the founder can hold 3 active customers without burning out."_

---

## 1. The two hard caps

| Window | Max active customers | Rationale |
|---|---|---|
| Days 1–30 (Wave 2) | **3** | 40h/customer in first month → 120h/month is the redline |
| Days 31–90 (Wave 4) | **6** | After Article 13 trigger, system + processes absorb load |

If a 4th customer wants in during Days 1–30 → say "I can take you Day 31" + book the call. **Never break the cap. Burnout = product death.**

---

## 2. Daily rhythm (every business day)

### 2.1 Morning ritual — ≤45 min
1. **Check `/founder-leads.html?access=dealix-founder-2026`** — new leads since yesterday
2. **Respond to overnight WhatsApp** — 30-min response SLA in business hours, 4h after
3. **Open `/decisions.html`** — review yesterday's pending decisions, approve/reject
4. **Send 1–2 personal warm WhatsApp** to named warm-intros (no automation, no template — Saudi-dialect, signed)
5. **Check `/pilot-tracker.html`** — confirm today's per-customer deliverable is queued

### 2.2 Per-customer execution windows
- **Sprint customer block:** ~2h (see §3 day-by-day table)
- **Partner customer block:** ~1h (see §4 weekly cadence)
- **Stack blocks consecutively** — don't context-switch between customers more than once/day

### 2.3 Evening shutdown — ≤15 min
1. **Mark today's decisions complete** on `/decisions.html`
2. **Queue tomorrow's voice note** for each active customer (drafted, not sent)
3. **Update `/pilot-tracker.html`** — log today's actual time spent (truth-tracking for founder hours model in §8.3 of strategic plan)
4. **Close laptop.** No customer work after Maghrib unless explicit emergency.

---

## 3. Per-Sprint-customer rhythm (14-day contract)

The Sprint is the same 14 plays every time — closed, predictable, scriptable. See `docs/V14_TURNKEY_PACKAGE.md` §3 for full delivery contract.

| Day | Founder action (~time) | Customer touchpoint | Endpoint(s) used |
|---|---|---|---|
| **D0** | WhatsApp voice note + Day-0 link + Calendly + agreement (30 min) | `/pilot-day-0.html` | — |
| **D1** | Sales Agent qualifies 3 named prospects (90 min) | Approve 3 outputs on `/decisions.html` | `/api/v1/sales-os/qualify` |
| **D2** | Growth Agent drafts 3 warm-route messages (60 min) | Approve drafts | `/api/v1/growth-beast/warm-route/draft` |
| **D3** | Support Agent builds first FAQ from customer's leads (60 min) | Review FAQ | `/api/v1/support-os/draft-response` |
| **D4** | Ops Agent: 7-step delivery checklist for one service line (60 min) | Pick the line | `/api/v1/full-ops/today` |
| **D5** | Executive Agent: weekly brief (30 min) | Read brief | `/api/v1/role-command-v125/today/ceo` |
| **D6** | Pipeline Audit deliverable v1 drafted (90 min) | Customer reviews | `/api/v1/sales-os/qualify` (rollup) |
| **D7** | Mid-Sprint check-in WhatsApp call (20 min) | Customer reflects | — |
| **D8–D10** | Lead Quality + Broker Brief deliverables (90 min/day) | Review per-deliverable | `/api/v1/qualification/*` |
| **D11–D12** | Sector Benchmark + 30-Day Action Plan deliverables (90 min/day) | Review | (synthesis from above) |
| **D13** | First Proof Pack snippet drafted (60 min) | Customer approves | `/api/v1/proof-to-market/snippet` |
| **D14** | 30-min final call → Partner upsell or 100% refund (60 min incl. prep) | Decision call | — |

**Total founder hours per Sprint:** ~40h spread over 14 days (≈3h/day).

---

## 4. Per-Partner-customer rhythm (monthly cadence)

After Sprint→Partner conversion. See `docs/V14_TURNKEY_PACKAGE.md` §4.

| Cadence | Action | Endpoint(s) |
|---|---|---|
| **Daily** | 5–10 Daily Decisions in customer's `/decisions.html` queue (founder approves/edits drafts) | `/api/v1/sales-os/qualify` · `/api/v1/growth-beast/warm-route/draft` · `/api/v1/support-os/draft-response` |
| **Weekly** | 1 founder call (30 min) + Pipeline Audit refresh + WhatsApp summary | `/api/v1/sales-os/qualify` (rollup) |
| **Monthly** | Executive Brief PDF + KPI lift report vs commitment | `/api/v1/role-command-v125/today/ceo` |
| **Quarterly** | Proof Pack publication + sector benchmark refresh | `/api/v1/proof-to-market/snippet` |

**Total founder hours per Partner customer:** ~20h/month after Sprint (≈45 min/business day).

---

## 5. Capacity math (so you don't overbook)

| Configuration | Sprint h/day | Partner h/day | Total h/day | Headroom |
|---|---|---|---|---|
| 1 active Sprint, 0 Partners | 3.0 | 0.0 | 3.0 | 5h |
| 1 Sprint + 1 Partner | 3.0 | 0.75 | 3.75 | 4h |
| 2 Sprints + 1 Partner | 6.0 | 0.75 | 6.75 | 1h ← **caution zone** |
| 3 Partners (post-Wave-4) | 0.0 | 2.25 | 2.25 | 6h |
| 1 Sprint + 3 Partners | 3.0 | 2.25 | 5.25 | 3h |

**Rule of thumb:** if today's customer-block math exceeds 6h, decline new commitments today and re-baseline tomorrow morning.

---

## 6. Escalation rules

### 6.1 Escalate to CTO (me) within 24h
- Customer hits a bug in any LIVE endpoint
- Customer asks for a feature that maps to a TARGET service in `docs/registry/SERVICE_READINESS_MATRIX.yaml` → trigger condition fired
- CI red on `claude/service-activation-console-IA2JK` or `main`
- Any test in `tests/test_landing_*` or `tests/test_smoke_*` fails

### 6.2 Escalate to lawyer within 7 days
- Any data-subject request (export/delete/correct) — first one triggers Wave 4 PDPL services
- Any complaint citing PDPL Articles 6, 7, 9, 12, or 19
- Any contract redline beyond the standard Sprint/Partner template

### 6.3 Decline politely
- Cold-outreach automation requests ("can you message my whole list?") → "We don't do that — that's Article 4 of our contract"
- Custom integrations not on the closed package → "Closed package, founding-partner price-lock — Sprint or Partner, those are the two doors"
- Discounts beyond founding-partner price-pin → "First 3 customers got the price-lock; price is what it is now"

---

## 7. Weekly review (every Sunday — 30 min)

1. **Pull `/founder-leads.html` summary** — leads this week vs last week
2. **Pull `/pilot-tracker.html` summary** — actual founder hours per customer vs model
3. **Read the `/decisions.html` activity log** — which decisions did each customer engage with most
4. **Update `docs/V14_CUSTOMER_SIGNAL_SYNTHESIS.md`** if any new signal landed (interview snippet, refund request, expansion ask)
5. **Pick next week's 1–2 warm-intro targets** — write the names down

---

## 8. The forbidden list (what you NEVER do, even when tired)

- ❌ Send live WhatsApp without `/decisions.html` approval (NO_LIVE_SEND gate exists in code; don't try to bypass)
- ❌ Promise "guaranteed revenue" or "نضمن عوائد" — Article 8, immediate breach
- ❌ Run cold WhatsApp campaigns or LinkedIn scraping (NO_COLD_WHATSAPP, NO_SCRAPING gates)
- ❌ Take a 4th active customer in Days 1–30 (cap rule, §1)
- ❌ Negotiate price below the founding-partner pin for first 3 customers, or below the standard rate after
- ❌ Customize the Sprint deliverables outside the 5-PDF closed scope (each deviation = 30% delivery cost overrun)
- ❌ Reply to a customer after Maghrib unless they explicitly flag urgent
- ❌ Skip the evening shutdown ritual — that's how decisions get lost

---

## 9. The single number that matters

> **Today's question:** _"Did I send 1 personal warm WhatsApp to a named real-estate office owner today?"_

If yes → tomorrow can take care of itself. If no for 3 days running → break glass, talk to CTO, reset the rhythm.

---

## 10. Files this playbook references

- `landing/launchpad.html` — what you point new prospects at
- `landing/diagnostic-real-estate.html` — the sector intake link in your warm-WhatsApp message
- `landing/founder-leads.html?access=dealix-founder-2026` — Lead Inbox (founder-tier)
- `landing/decisions.html` — Daily Decisions inbox (per-customer approval queue)
- `landing/pilot-tracker.html` — 7/14-day pilot tracker
- `landing/founder.html` + `landing/founder-dashboard.html` — Founder Beast Command Center
- `docs/V14_TURNKEY_PACKAGE.md` — closed package master spec
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` — 8 LIVE / 24 TARGET (trigger conditions)

---

## 11. One-line founder commitment

> _"3 customers max in 30 days. Same plays every day. WhatsApp before Maghrib. Closed package, no negotiation. This is the rhythm that gets to 3 paid pilots without burning out — anything else is imagination tax."_
