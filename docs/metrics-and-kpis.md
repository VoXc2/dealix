# Dealix — Metrics & KPIs

**Purpose:** one spec for every number the team looks at. If a metric is not here, it is not an official metric yet.
**Cadence:** daily standup (ops), weekly review (pipeline + product + AI), monthly (strategy).
**Owner:** founder until first full-time hire.

All monetary metrics in **SAR**. All times in **Asia/Riyadh**.

---

## 1. North Star Metric

**Active Pilot Revenue (APR)** — the sum of paid pilot subscriptions active on the last day of the week.

- Why this one: it captures demand, pricing, and retention in a single number.
- Target during Days 0–90: **APR ≥ SAR 6,000 by Day 45, ≥ SAR 15,000 by Day 90**.
- Pitfall: does not reward unpaid trials, POCs, or "we'll start next month" conversations.

---

## 2. Funnel metrics (weekly)

| Stage | Definition | Target wk 1–4 | Target wk 5–12 |
|---|---|---|---|
| Prospects identified | New Saudi SMBs added to outreach list this week | 15 | 30 |
| First-touch sent | Personalised first message sent | 15 | 30 |
| Replies | Any human reply (positive or negative) | 5 | 10 |
| Discovery calls booked | Call on calendar | 3 | 6 |
| Discovery calls held | Actually happened | 3 | 5 |
| Demos delivered | Demo completed per §5 of sales kit | 2 | 4 |
| Pilots signed | Contract signed + invoice issued | 1 | 2 |
| Pilots paid | Money received | 1 | 2 |
| Pilots activated | First real lead processed in-system within 48 h of signature | 1 | 2 |

Compute conversion rates between each pair. Any rate < 20% for two consecutive weeks → investigate that stage.

---

## 3. Product usage metrics (per tenant, daily)

Track in a simple daily `metrics_rollup` table. Minimum viable:

- **Active users:** users with ≥ 1 session that day.
- **Leads created:** rows inserted in `leads`.
- **Leads enriched:** rows where enrichment status moved to `complete`.
- **AI replies drafted:** rows in `ai_conversations` with `type=draft`.
- **AI replies sent** (only after human approval if Class-B).
- **Deals moved forward:** stage transitions in `deals`.
- **Dashboard opens:** `/dashboard` page loads.

Tenant is **healthy** if, on a rolling 7-day window:
- active users ≥ 2 on ≥ 5 of 7 days
- leads created ≥ 10 in the week
- ≥ 1 deal stage change in the week

Tenants that fall below any line for two consecutive weeks are flagged and get a founder check-in within 48 h.

---

## 4. AI quality metrics

Measure weekly on a sample of **50 real interactions** per tenant (or all, if fewer than 50).

| Metric | How measured | Threshold |
|---|---|---|
| Arabic fidelity | % of AR prompts answered in AR (no latinisation) | ≥ 98% |
| Intent-classification accuracy | % matching human label on sample | ≥ 85% |
| Summarisation usefulness (1–5) | Founder or admin rating | avg ≥ 4.0 |
| Hallucination rate | % outputs referencing facts not in input | ≤ 2% |
| Refusal / safety block | % blocked by policy when appropriate | > 95% when tested, with 0 false allows on prohibited flows |
| Fallback rate | % calls that had to fall back Ollama → Groq → OpenAI | track trend |
| p95 latency (Groq path) | `/api/v1/ai-agents/*` end-to-end | ≤ 2 s |
| p95 latency (local path) | `/api/v1/local-ai/chat` on small tier | ≤ 10 s |
| Cost per 1k AI calls (cloud) | Groq + OpenAI spend ÷ calls × 1000 | track trend |
| Cost per 1k AI calls (local) | always 0 API cost; record electricity note only | — |

Log raw samples to `docs/reality_reviews/ai-quality-YYYY-MM-DD.md` with anonymised snippets (customer-level data stripped).

---

## 5. Sales & revenue metrics (weekly)

- **New MRR** (pilot tier prices count at pilot rate until Day 30, then standard).
- **Expansion MRR** (upgrades from Starter → Growth, etc.).
- **Churned MRR** (cancelled or not renewed at Day 30).
- **Net MRR** = new + expansion − churned.
- **Pipeline SAR** (open pilots in discovery/demo) — weighted by stage:
  - Discovery: ×0.15
  - Demo done: ×0.35
  - Pilot verbal yes: ×0.65
  - Contract sent: ×0.85
- **Win rate**: signed ÷ (signed + lost) trailing 6 weeks.
- **Avg time to close** from first-touch → signature (days).
- **CAC** = founder's monetary cost of acquisition / signed pilots (include ad spend, any paid intro, travel). Founder time is free during launch; revisit post-Phase Gate.

---

## 6. Retention metrics (monthly, once Day 30 reached on first pilots)

- **Day-30 renewal rate** = pilots that convert to paid monthly ÷ pilots completing 30 days.
- **Logo churn** = tenants that cancel ÷ active tenants start of month.
- **Revenue churn** = MRR lost ÷ MRR start of month.
- **NPS** — send 1 AR question ("ما مدى احتمال أن توصي بديلكس لزميل؟ من 0 إلى 10") on Day 21. Target ≥ 30 per `CLAUDE.md` Phase Gate.
- **Net Revenue Retention (NRR)** — too early during launch; start reporting after 10 paying tenants.

---

## 7. Reliability & operational metrics

- **Uptime** — external pinger (`/api/v1/health`), target ≥ 99.5% during launch.
- **p50 / p95 API latency** — from access log. Read endpoints < 500 ms p95.
- **5xx rate** — < 0.5% weekly. > 1% for > 15 min pages founder.
- **Deploy frequency** — expect daily during launch. Abnormal silence is itself a signal.
- **MTTR** — minutes from alert to resolution. Target < 30 min for Sev-1.
- **Backup freshness** — `age(max(backup_time))` must be ≤ 26 h; else red.
- **Local AI availability** — % of hours `/local-ai/status` returned `daemon_up: true`. Target ≥ 95% but not a pager metric (has a fallback).

---

## 8. Compliance & trust metrics

- **PDPL consent coverage** — % of outbound messages whose contact has a stored, non-expired consent. Target **100%**; deviation is an incident.
- **Approval center SLA** — % of Class-B actions resolved within 24 h. Target ≥ 90%.
- **Truth Registry SUPPORTED rate** — per V005. Target 100% at Phase Gate; track weekly.
- **Secrets hygiene** — `gitleaks` clean on main. 1+ finding is a Sev-2.
- **Data export requests** — count + SLA. Target: fulfilled within 7 days.

---

## 9. Dashboards

### 9.1 Founder weekly view (one page)
- APR (North Star)
- Funnel: prospects → pilots paid
- New MRR / Net MRR
- Pilot health: green / yellow / red per tenant
- AI quality: fidelity + hallucination + p95 latency
- Reliability: uptime + 5xx
- Compliance: PDPL consent coverage + approval center SLA

### 9.2 Daily ops view
- Uptime last 24 h
- 5xx count last 24 h
- Open incidents
- Backup freshness
- Local AI availability %
- Active users last 24 h per tenant

---

## 10. Weekly review cadence

**When:** Thursday 18:00–19:00 Asia/Riyadh.
**Who:** founder (engineer joins if incidents that week).
**Where:** `docs/reality_reviews/YYYY-MM-DD.md` (create the file beforehand).

**Agenda (60 min, strict):**

1. **10 min — Numbers.** Read §2, §5, §6 from this spec into the doc. No debate.
2. **15 min — Wins.** What moved? Which customer conversation was the best this week?
3. **15 min — Red flags.** Which tenant is yellow/red? Which metric broke threshold?
4. **10 min — One thing to change.** Exactly one. Write it as an action with owner + due date.
5. **10 min — Phase Gate delta.** For each of the 6 Phase Gate criteria, update status: further / same / closer.

**Exit artefact:** the `.md` file is committed. A one-paragraph Arabic summary is pinned to the founder's WhatsApp.

---

## 11. Monthly retrospective

First Thursday of each month, last 30 min of the weekly review.

Questions:
- Which metric best predicted whether a pilot would convert?
- Which metric turned out not to matter? (Delete it from §2–§8 if true.)
- Did we hit last month's "one thing to change"? If not, why?
- Any metric we stopped looking at? Either re-instrument or formally drop it.

Metrics are living. If after 90 days a metric is never used in a decision, remove it — don't carry dead dashboards.

---

## 12. Instrumentation backlog (not yet live — track progress)

- [ ] Daily `metrics_rollup` job in Celery, 01:00 Riyadh.
- [ ] Admin endpoint `GET /api/v1/admin/metrics/weekly` returning §9.1 JSON.
- [ ] Simple CSV export for founder to keep a personal weekly sheet.
- [ ] NPS survey job (Day 21 trigger).
- [ ] External uptime pinger configured in UptimeRobot / Healthchecks.io.
- [ ] Backup-freshness check exported to Prometheus/text file for monitoring.

Until these ship, fill the weekly review manually — the discipline is the metric.
