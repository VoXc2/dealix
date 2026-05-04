# Dealix — Founder Action Plan
> Generated: 2026-05-03 — after PROVEN_LOCAL gate passed.
> Audience: founder (Sami) — solo, Arabic-first, post-launch hour 0.

## What Dealix already does for you (do not redo)

Don't reimplement these — they exist, are tested, and run safely:
- 14-stage Prospect Tracker (forward-only, blocked-channel enforcement)
- Service Tower with 6 bundles + Service Contracts (8 fields each)
- Auto-creates `CustomerRecord` + Company Brain on `closed_won`
- 7-day Sprint Engine (Days 1–7, LLM-enhanced where Brain present)
- Approval Queue + auto-executor (gate-aware, never sends without env flag)
- Forbidden-claims scanner (draft-time + audit) — `نضمن`/`guaranteed` blocked
- Role Action Guard (PDPL): 9 roles × allowed actions matrix
- Proof Pack HTML + HMAC signature → emit on every customer
- Founder Daily Digest, Forecast, Sector Benchmarks (light)
- 9 internal Role Briefs + WhatsApp render-only briefs
- Dealix Self-Ops (eats own dogfood) + 3 cron jobs ready for Railway

## What only the founder can do (4 manual actions, in order)

### 1. Send LinkedIn DMs (today, ≤30 min)
Dealix drafts the message; **you** copy-paste from the Founder Digest:

```bash
DEALIX_BASE_URL=http://127.0.0.1:8000 python scripts/dealix_cli.py smart-launch
```

This prints:
- 3 LLM-personalized warm intros (or template fallback)
- The recommended channel for each prospect (Brain-aware)
- The exact Arabic copy to send

**Why manual:** LinkedIn ToS forbids automated DMs. Dealix codifies this
as a hard refusal — `linkedin_auto_dm` is in the blocked_channels list.

### 2. Take the discovery call (today, ≤25 min)
Dealix prepares the call brief. Open `landing/client.html?customer_id=...`
or:

```bash
curl -s "http://127.0.0.1:8000/api/v1/sprints/{sprint_id}/day/4" | jq .
```

You get:
- 8-point script
- 30-min agenda
- 5 deterministic discovery questions + 2 LLM-personalized ones
- Brain-aware risks-to-avoid

### 3. Send the contract + invoice (after the call wins)

```bash
# After verbal commitment, generate invoice (no live charge needed):
curl -X POST http://127.0.0.1:8000/api/v1/payments/invoice \
  -H 'Content-Type: application/json' \
  -d '{"amount_sar":499,"customer_id":"cus_<id>","description_ar":"Pilot Dealix — 7 أيام"}'
```

If `MOYASAR_SECRET_KEY` is set in Railway env → real Moyasar invoice.
Otherwise → manual-fallback URL pointing to `api.dealix.me/manual-pay`.
Either way you paste the URL into WhatsApp — customer pays via Mada/Visa.

### 4. Confirm the payment (when received)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/payments/confirm \
  -H 'Content-Type: application/json' \
  -d '{"invoice_id":"pay_<id>"}'
```

This:
- Marks invoice `paid`
- Emits proof event
- Triggers `closed_won` advance which auto-creates the Company Brain
- Kicks off the 7-day Sprint Engine
- Enables the customer to receive their Proof Pack on Day 7

## What you should NOT do this week

- ❌ Do **not** flip `MOYASAR_ALLOW_LIVE_CHARGE` to true — invoice path
  works; flip only after merchant onboarding + DPA
- ❌ Do **not** flip `WHATSAPP_ALLOW_*` flags — render-only is sufficient;
  flip only after Meta Business KYB
- ❌ Do **not** flip `RESEND_ALLOW_LIVE_SEND` — drafts work; flip only
  after DMARC-validated `noreply@dealix.me`
- ❌ Do **not** add new product features. Run the loop above 5×
  before changing anything.

## Daily ritual (10 min, Arabic)

```bash
# Every morning at 9 AM:
DEALIX_BASE_URL=http://127.0.0.1:8000 python scripts/dealix_cli.py smart-launch
```

Outputs:
- Standup queue (today's prospects to message)
- Pending approvals count
- Active sprints + days remaining
- Best channel pick (Brain-aware)
- 3 LLM-drafted LinkedIn intros
- Live-action gate snapshot (must remain all False)
- LLM provider status

This replaces "what should I do today?" — Dealix already knows.

## Weekly ritual (Sunday, 30 min)

```bash
# Generate the weekly proof for all live customers:
python scripts/cron_dealix_self_ops.py
curl -s http://127.0.0.1:8000/api/v1/intelligence/forecast?horizon_days=30 | jq .
curl -s http://127.0.0.1:8000/api/v1/intelligence/benchmarks | jq .
```

Then for each active customer:
```bash
curl -sL "http://127.0.0.1:8000/api/v1/proof-ledger/customer/{cid}/pack.html" -o /tmp/pack.html
# Open in browser — share with customer + post anonymized stats on LinkedIn
```

## The 4 launch-decision toggles (in priority order)

| Toggle | When to flip | Why wait |
|---|---|---|
| `MOYASAR_SECRET_KEY` (set, not flip) | After merchant onboarding | Need test→live key transition |
| `RESEND_API_KEY` + `_ALLOW_LIVE_SEND=true` | After DMARC verified for `dealix.me` | Avoid spam-folder reputation hit |
| `ANTHROPIC_API_KEY` (or any of 5 providers) | Before first 5 customer Sprint Day 1 generations | LLM-enhanced output > template; template still works |
| `MOYASAR_ALLOW_LIVE_CHARGE=true` | After 3+ pilots paid via invoice + DPA signed | Server-side charge is higher trust burden than invoice link |

## When you are stuck (escalation)

```bash
# Re-run all 4 audits — every one of these is a hard truth gate:
bash scripts/full_acceptance.sh
python scripts/forbidden_claims_audit.py
python scripts/repo_architecture_audit.py
python scripts/launch_readiness_check.py
```

If any returns red → fix the failing check before doing anything customer-facing.

## The North Star metric

**Day 7 Proof Pack delivery rate.** If you onboard 1 customer this week
and they receive their Proof Pack on Day 7 with ≥6 RWUs and a real
revenue_impact_sar number, Dealix has earned its first month of subscription.
That is the *only* metric that matters until customer #5.
