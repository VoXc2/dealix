# 14-Day First-Revenue Playbook

> One operating manual the founder follows daily for the next 14
> days. Every day cites the exact command + the exact V11/V12
> endpoint. No new code; pure execution.

## Day 0 — Merge + Deploy + Verify (60 min)

```bash
git push origin claude/service-activation-console-IA2JK
# Open PR via GitHub UI:
#   base: main, head: claude/service-activation-console-IA2JK
#   title: feat(v11-v12-rx): launch full-ops + revenue execution layer
# Merge → Railway redeploys (~5 min)
curl -s https://api.dealix.me/health
bash scripts/v11_customer_closure_verify.sh
bash scripts/v12_full_ops_verify.sh
bash scripts/revenue_execution_verify.sh   # NEW
python scripts/dealix_first10_warm_intros.py    # NEW — empty board
python scripts/dealix_phase_e_today.py
```

**Done condition:** all 3 verifiers PASS, `/health.git_sha` matches the merged commit.
**No-go:** any verifier FAIL → fix in same day, do not start outreach.

## Day 1 — Pick + draft 10 warm intros (90 min)

- Pick 10 warm contacts from your network (private notes, NOT in repo)
- Run `python scripts/dealix_phase_e_today.py` — see today's checklist
- Draft 5 messages using `docs/phase-e/02_FIRST_10_WARM_MESSAGES_AR_EN.md`
- Send 5 via LinkedIn / WhatsApp / Email **manually** (no auto-send)
- Update `docs/phase-e/live/FIRST_10_CUSTOMER_BOARD.md` (gitignored)

**Goal:** 5 messages sent.
**Founder rule:** if you can't pick 10 warm intros from your network, go back to the segment-radar in `docs/phase-e/01_FIRST_3_WARM_INTROS_BOARD.md`.

## Day 2 — Send remaining 5 + first replies (90 min)

- Send other 5 warm intros
- For replies received, schedule 30-min calls
- Log replies in `docs/phase-e/live/` (gitignored)

**Goal:** 2 replies, 1 scheduled call.

## Day 3 — Run first 2 mini diagnostics (90 min)

```bash
python scripts/dealix_diagnostic.py \
  --company "Slot-A" --sector b2b_services --region riyadh \
  --pipeline-state "(your customer's actual state, in placeholder form)"
```

- Generate 2 bilingual diagnostics (1-page each)
- Send manually via the original channel
- Log `diagnostic_delivered` in the board

**Goal:** 2 diagnostics in customer hands.
**Forbidden:** sending a diagnostic with `نضمن` / `guaranteed` / specific revenue numbers.

## Day 4 — Offer 499 SAR pilot to best fit (60 min)

```bash
python scripts/dealix_invoice.py \
  --email customer@example.sa \
  --amount-sar 499 \
  --description "Dealix 7-Day Growth Proof Sprint (Slot-A)" \
  --dry-run
```

- Use the dry-run output to draft the customer-facing offer (per `docs/phase-e/05_PILOT_499_OFFER.md`)
- Send manually
- Wait for written commitment OR Moyasar test-mode payment confirmation

**Goal:** 1 pilot offer sent, 1 verbal "yes" + path to written commitment.
**Forbidden:** Moyasar live-charge (`sk_live_*` is rejected by the CLI without `--allow-live`).

## Day 5 — Commitment / payment + open delivery session

- Wait for written commitment (email screenshot kept in your vault) OR test-mode payment confirmation
- Open delivery session:

```bash
curl -X POST https://api.dealix.me/api/v1/delivery-os/create-session \
  -H "Content-Type: application/json" \
  -d '{"customer_handle":"Slot-A","service_id":"growth_starter"}'
```

- Note the `session_id` in your private vault (NEVER in repo with real customer name)

**Goal:** 1 delivery session in `in_progress`.
**No-go:** if customer ghosts → mark slot `closed_lost`, refill from second-best fit.

## Day 6 — Day-1 of the 7-day delivery (60 min)

- Use V12 Growth OS to draft 10 ranked opportunities:

```bash
curl -X POST https://api.dealix.me/api/v1/growth-os/daily-plan \
  -H "Content-Type: application/json" \
  -d '{"sector":"b2b_services","region":"riyadh"}'
```

- Send the 10 to the customer for review
- Log `proof_event` for "10 opportunities sent for review"

**Goal:** customer picks ≤5 opportunities to act on.

## Day 7 — Day-2 message drafts (60 min)

- Draft 1 message per chosen opportunity (Arabic + English where relevant)

```bash
curl -X POST https://api.dealix.me/api/v1/growth-os/outreach-draft \
  -H "Content-Type: application/json" \
  -d '{"sector":"b2b_services","audience":"warm_intro","language":"ar"}'
```

- Send drafts to customer for approval
- NEVER auto-send

**Goal:** customer approves 3+ drafts.

## Day 8 — Day-3 approved manual sends + 1 follow-up + start 2nd diagnostic

- Customer sends approved drafts manually
- Log `proof_event` per approved send
- Run 1 follow-up on Day-1 outreach (no reply ≥ 5 days)
- Start 2nd diagnostic if a 2nd lead is warm

**Goal:** 3 sends, 1 follow-up, 1 new diagnostic in flight.

## Day 9 — Day-4 follow-up plan + Day-5 risk note (90 min)

- Build the 7-day follow-up calendar
- Run Compliance v12 `action-check` on every planned action:

```bash
curl -X POST https://api.dealix.me/api/v1/customer-data/action-check \
  -H "Content-Type: application/json" \
  -d '{"action_type":"send_message","channel":"warm_intro","consent_state":"granted"}'
```

- Build the 1-page risk note (≤ 3 risks)

**Goal:** customer has a follow-up plan + risk note.

## Day 10 — Day-6 Proof Pack draft (90 min)

```bash
python scripts/dealix_proof_pack.py \
  --customer-handle "Slot-A" \
  --period-from 2026-MM-DD --period-to 2026-MM-DD
# OR (if no events recorded yet):
python scripts/dealix_proof_pack.py --customer-handle "Slot-A" --allow-empty
```

- Pack is `decision: review_required` + `audience: internal_only`
- Send to customer for review

**Goal:** Proof Pack draft in customer hands.
**Forbidden:** ANY metric the customer didn't supply.

## Day 11 — Day-7 review call + upsell decision (60 min)

- 30-min review call (per `docs/phase-e/09_CUSTOMER_REVIEW_AND_UPSELL.md`)
- Get customer feedback per section
- Mark which events the customer approves to publish (default: NONE)
- Discuss next step (refund / pause / extend / custom)

**Goal:** customer signs which events are publishable + picks next step.

## Day 12 — Customer success health score + first referral ask

```bash
curl -X POST https://api.dealix.me/api/v1/customer-success-os/health-score \
  -H "Content-Type: application/json" -d '{...explicit signals...}'
curl -X POST https://api.dealix.me/api/v1/sales-os/objection-response \
  -H "Content-Type: application/json" \
  -d '{"objection_text":"<customer's objection if any>"}'
```

- If health ≥ 61 ("good"+), ask for 1 referral
- NEVER pressure manipulation

**Goal:** 1 referral name (placeholder in your vault).

## Day 13 — Weekly learning (45 min)

```bash
curl -s https://api.dealix.me/api/v1/self-improvement-os/weekly-learning
```

- Review the 3 suggestions
- Pick 1 to act on next week
- Log in your private vault

**Goal:** 1 prioritized improvement for next week.

## Day 14 — Decision day (60 min)

```bash
curl -s https://api.dealix.me/api/v1/full-ops/daily-command-center
curl -s https://api.dealix.me/api/v1/executive-os/weekly-pack
```

Decision matrix:

| Outcome at Day 14 | Action |
|---|---|
| 1+ paid pilot delivered + 1 proof event | ✅ Trigger V12.1 — see `docs/V12_1_TRIGGER_RULES.md` |
| 1+ written commitment but no payment | Continue execution; do NOT call it revenue |
| 0 commitments | **Investigate the segment, offer, or message — NOT the code.** Pick a different warm-intro segment for the next 14 days. |

**Forbidden at Day 14:**
- Building V13
- Adding a new pricing tier
- Switching to cold outreach
- Buying ads
- Public case study without signed permission
- Claiming revenue that hasn't landed in your bank/Moyasar dashboard

## The 14-day quality bar

| Metric | Day-14 target |
|---|---|
| Warm intros sent | 10 |
| Replies | 3 |
| Mini diagnostics delivered | 3 |
| Pilots offered | 2 |
| Paid OR committed pilots | 1 |
| Proof events logged | 5+ |
| Support tickets handled | 100% classified |
| Unsafe action attempts blocked | 100% |
| Fake claims | 0 |
| Manual approval logs | 100% |

## When to STOP and re-think

If by Day 14:
- 0 replies → segment is wrong; re-pick from a closer ring of relationships.
- replies but 0 diagnostic accepts → diagnostic offer copy is weak.
- diagnostics but 0 pilot offers → diagnostic is too long or doesn't bridge to offer.
- pilot offers but 0 commitments → 499 SAR is too high or the offer doesn't match the pain.

In each case: **the answer is NOT more code.** The answer is the next 14 days with a tighter offer.
