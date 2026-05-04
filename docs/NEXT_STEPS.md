# Dealix — Next Steps (Comprehensive Operational Plan)

> Generated after PR-OS-FOUNDATION + PR-PHASES-2-3-4 ship.
> The single source of truth for "what does Dealix do now, and what do
> I (the founder) do next?"

---

## What's now live (state as of this PR)

### Backend — 14 systems × 4 layers × 12 loops

| Layer | What's wired |
|---|---|
| **Decision Layer** | 9 role briefs (CEO/Sales/Growth/RevOps/CS/Finance/Compliance/Agency/Meeting) + Card Priority Ranker |
| **Execution Layer** | Stage Machine v2 (14 stages) + 10 sprint endpoints + Approval Queue + Moyasar invoice (manual fallback) |
| **Proof Layer** | 14 RWUs + Proof Ledger + HMAC-signed Proof Pack (HTML + optional PDF) |
| **Learning Layer** | Self-Growth weekly + /learning/playbook (objection library + message experiments + channel performance) |
| **Governance Layer** | 8 live-action gates default-False + Role Action Guard middleware + Forbidden Claims at draft level |

**Endpoint count:** 371+ (was 361)

### Phase 2 — 7-Day Growth Proof Sprint Engine (NEW this PR)

Complete delivery automation. Once a customer pays Pilot 499:

```
POST /api/v1/sprints/start                      → creates SprintRecord with contract snapshot
POST /api/v1/sprints/{id}/diagnostic/generate    (Day 1) → diagnostic_delivered RWU
POST /api/v1/sprints/{id}/opportunities/generate (Day 2) → 10 opportunity_created RWUs
POST /api/v1/sprints/{id}/messages/generate      (Day 3) → 6 draft_created RWUs
POST /api/v1/sprints/{id}/meeting-prep           (Day 4) → meeting_drafted RWU
GET  /api/v1/sprints/{id}/review                 (Day 5) → pipeline review
POST /api/v1/sprints/{id}/proof/draft            (Day 6) → proof_generated RWU
POST /api/v1/sprints/{id}/close-out              (Day 7) → final Proof Pack + Growth OS upsell
```

Every output is deterministic (no LLM cost). Each day:
- Pulls Company Brain (offer / ICP / tone / channels)
- Runs the day's template generator
- Persists output to `SprintRecord.day_outputs_json`
- Emits matching RWU into Proof Ledger
- Surfaces in Customer Workspace + Daily Role Briefs

### Phase 3 — Learning Engine Skeleton (NEW this PR)

```
GET /api/v1/learning/today           → today's deterministic plan
GET /api/v1/learning/weekly?days=7   → weekly learning report
GET /api/v1/learning/playbook        → channel performance + message experiments + objection library
```

Phase 3 modules in `auto_client_acquisition/learning/`:
- `objection_library.py` — mines ObjectionEventRecord, scores response variants
- `message_experiments.py` — A/B scores by segment + channel
- `channel_performance.py` — funnel conversion per channel

**Honest limitation:** modules return small-sample warnings until ≥30 events
per dimension. Full Phase 3 (Bayesian A/B, statistical significance) lands at
3 paid pilots + 30 conversations.

### Phase 4 — 6 Product Brands (NEW this PR)

```
landing/products/command.html   → Dealix Command (CEO)
landing/products/sell.html      → Dealix Sell (Sales)
landing/products/grow.html      → Dealix Grow (Growth)
landing/products/serve.html     → Dealix Serve (CS)
landing/products/partner.html   → Dealix Partner (Agencies)
landing/products/proof.html     → Dealix Proof (the deliverable)
```

Each page: 60-second pitch + 3 sample decisions live-fetched from the
underlying role brief + CTA → onboarding wizard.

### Phase 5 — Revenue Intelligence (deferred — needs 90 days of data)

NOT built. Trigger: **5 retainers + 90-day revenue data**. Includes:
forecasting, sector benchmarks, NRR tracking, sector playbooks. Don't
build until the data exists.

---

## The 17-checkpoint Definition of Done — all green

```
bash scripts/full_acceptance.sh
```

returns: **61/61 checks pass · 6/6 layers · 4 gates green**

| Gate | What | Result |
|---|---|---|
| Backend | 21 endpoints HTTP 200 | ✅ |
| Frontend | 17 landing pages + 6 product pages | ✅ |
| Safety | 8 gates FALSE + draft-level blocks + 128/128 audit | ✅ |
| Business E2E | Lead → Pilot → Sprint × 7 days → Proof Pack → Upsell | ✅ |

---

## YOUR daily routine — 60 minutes

### 9:00 AM KSA — Morning Standup (5 minutes)

```bash
DEALIX_BASE_URL=https://api.dealix.me dealix standup
```

Shows:
- 6 prospects due today
- Stale (>3 days no reply)
- Yesterday's wins
- Funnel snapshot

### 9:05 — Send 6 LinkedIn DMs (30 minutes)

Open `docs/WARM_INTRO_TEMPLATES.md` § "Warm-1" → polish 6 personalized
messages → send manually from your LinkedIn (no automation, ever).

For each sent:
```bash
dealix prospects advance <id> --target messaged
```

### 11:30 — Check approvals (5 minutes)

```bash
dealix approvals
```

Interactive — approve / reject / skip pending RWUs.

### 12:30 KSA — Midday cron auto-runs

You don't do anything. Dealix's `daily-ops-midday` cron generates:
- Sales follow-up cards for stale prospects
- Growth experiment for the day

### 4:00 PM — Hold any booked meetings (variable)

After each meeting:
```bash
curl -X POST https://api.dealix.me/api/v1/meetings/log \
  -d '{"customer_id":"...","outcome":"held","notes_ar":"...","next_action_ar":"..."}'
```

### 6:00 PM — Daily-ops closing window auto-runs

Generates tomorrow's plan + LinkedIn post draft for tomorrow.

### Total founder time: ~60 min/day, 5 days/week.

Everything else, the OS does.

---

## When a customer says "yes, I'll pay 499 SAR"

```bash
# 1. Create invoice
DEALIX_BASE_URL=https://api.dealix.me dealix invoice 499 cus_<id>

# 2. Paste Moyasar URL into WhatsApp / Email

# 3. After they pay (manual confirmation):
dealix prospects advance <prospect_id> --target closed_won
# (auto-creates CustomerRecord with Brain pre-populated)

# 4. Start the 7-day sprint:
curl -X POST https://api.dealix.me/api/v1/sprints/start \
  -H 'Content-Type: application/json' \
  -d '{"customer_id":"cus_<id>","service_id":"growth_starter"}'

# 5. Each day, run the day's generator (or wire to cron):
SPRINT_ID="spr_xxx"
curl -X POST .../sprints/$SPRINT_ID/diagnostic/generate     # Day 1
curl -X POST .../sprints/$SPRINT_ID/opportunities/generate  # Day 2
# ... through day 7
```

By Day 7: Proof Pack ready at `/api/v1/proof-ledger/customer/<id>/pack.html`,
Growth OS upsell card surfaced. **Total founder work: review + send 7 outputs
(~30 min/day × 7 = 3.5 hours).**

---

## When you have 3 paying customers (Phase 3 trigger)

You'll have ~30 outreach events + ~5 objection events accumulated. At that
point, `/api/v1/learning/playbook` returns statistically meaningful data.

Wire the weekly cron job:
```bash
curl https://api.dealix.me/api/v1/learning/playbook?days=30 | jq .
```

Use the output to:
- Pick the highest-reply-rate segment for next week's outbound
- Drop the worst-performing channel
- Use the best objection response variant verbatim

---

## When you have 1 retainer (Growth OS 2,999 SAR/month)

Go live with Phase 4 — the 6 product brands. Update `pricing.html` to
present the 6-product split:

```
Dealix Command — للمدير التنفيذي
Dealix Sell — لمدير المبيعات
Dealix Grow — لمدير النمو
Dealix Serve — لـ CS
Dealix Partner — للوكالات
Dealix Proof — الدليل
```

All 6 included in Executive Growth OS. Each has its own landing page
already built at `landing/products/*.html`.

---

## When you have 5 retainers + 90 days of data (Phase 5 trigger)

Build:
- `auto_client_acquisition/intelligence/forecasting.py` (linear projection
  from current pipeline + historical conversion per stage)
- `auto_client_acquisition/intelligence/sector_benchmarks.py` (anonymized
  averages across all paying customers)
- `auto_client_acquisition/intelligence/nrr_tracker.py` (per-customer
  expansion vs churn)
- `landing/playbooks/<sector>.html` (top 3 templates per sector,
  auto-published weekly)

---

## The 90-day money plan (unchanged from LAUNCH_90_DAY.md)

| Day | Pilots delivered | MRR | Cumulative cash | Phase action |
|---|---|---|---|---|
| 7 | 0 | 0 | 0 | Phase 1 + 2 ready, 30 warm intros sent |
| 14 | 1 | 0 | 425 SAR | First Pilot signed → Sprint Day 1 |
| 30 | 3 | 0 | 1,275 SAR | Phase 3 trigger fires (≥30 conversations) |
| 45 | 5 | 5,124 | 6,399 SAR | First Growth OS retainer (Phase 4 trigger) |
| 60 | 7 | 7,686 | 14,085 SAR | First case study published, inbound starts |
| 90 | 10 | 12,810 | 30,795 SAR | 5 Growth OS + 1 Partnership = ~154K ARR |

---

## What requires you (the founder) — the only human bottleneck

The OS does:
- Daily cron windows (4 × per day)
- Brief generation (9 roles)
- Sprint day-actions (deterministic)
- Proof Pack assembly (HMAC-signed)
- Approval queue (you only approve/reject)
- Forbidden claims blocking (per draft)
- Weekly learning report

The OS does NOT do:
- Pick prospects from your network (only you know)
- Send LinkedIn DMs (LinkedIn ToS forbids automation, period)
- Hold discovery calls (you do, with the script Dealix prepared)
- Approve outbound (you do, in the queue)
- Sign retainer contracts (you do, with the close plan Dealix prepared)

**Ratio:** ~95% OS, ~5% you. But the 5% is the irreducible part.

---

## When the OS breaks

| Symptom | First action |
|---|---|
| Endpoint 500 | `/api/v1/founder/today`'s `_errors` map shows what failed |
| New table missing | `POST /admin/recreate-tables -d '{"names":["sprints"]}'` |
| Forbidden claim at draft | `assert_safe()` raised → check `meta.draft_text` for unsafe phrase |
| Sprint stuck mid-day | `GET /sprints/{id}` shows current_day; re-POST the day's endpoint |
| Customer Brain empty | `PATCH /api/v1/companies/{id}/brain` — fill the 12 fields |

Or just run:
```bash
bash scripts/full_acceptance.sh
```

It tests all 4 gates in 60 seconds and shows exactly what failed.

---

## The one-line summary

**Dealix is a 4-layer Saudi Revenue OS that delivers a 7-day Proof Sprint to
every Pilot 499 customer, escalates them to a 2,999 SAR/month Growth OS
retainer with a Proof Pack the customer can forward to their CFO, and learns
weekly from the data — without ever sending a cold WhatsApp.**

Tomorrow morning at 9 AM KSA, send 6 LinkedIn DMs.
