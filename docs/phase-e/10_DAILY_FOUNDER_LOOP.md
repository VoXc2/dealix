# Daily Founder Loop (KSA time)

The single founder routine that ties Dealix's daily operations to
revenue. NO automation of customer messages — every external action
passes through founder approval.

## The schedule (4–5 active touchpoints / day)

### 08:30 KSA — Health + dashboard

```bash
curl -s https://api.dealix.me/health
python scripts/dealix_status.py
python scripts/dealix_phase_e_today.py        # V11 — today's checklist
```

Look for:
- `/health` → 200 + `git_sha` matches the latest commit
- `dealix_status` → all hard gates `BLOCKED`
- `dealix_phase_e_today` → today's checklist + next-best action

If any of the above is wrong → fix that FIRST. No customer work
until the system is healthy.

### 10:00 KSA — Manual warm intros (if approved)

If the first-3 board has a slot in `next_action=ask_for_30m`:
1. Send the warm-intro message manually (template
   `02_FIRST_10_WARM_MESSAGES_AR_EN.md`)
2. Update slot status to `requested` if customer replied
3. NEVER send a cold WhatsApp / cold email

### 13:00 KSA — Diagnostic prep

For each `requested` slot:
1. Run `python scripts/dealix_diagnostic.py`
2. Save the output, send it manually
3. Update slot to `delivered`

### 16:00 KSA — Manual follow-up

For each `delivered` Diagnostic with no reply ≥ 7 days:
1. Send the bilingual follow-up (template #3 / #4 in
   `02_FIRST_10_WARM_MESSAGES_AR_EN.md`)
2. ONE follow-up max. After that, mark slot `declined` and pick
   another warm intro.

### 18:00 KSA — Update + log

- Update `docs/phase-e/live/FIRST_3_CUSTOMER_BOARD.md` (gitignored)
- Log key learnings in your private notes (NEVER in this repo
  unless redacted)
- For active pilots: update `docs/proof-events/<slot>.json` with
  events from today

## Weekly cadence (Sunday)

- Read the previous week's scorecard via
  `https://api.dealix.me/api/v1/founder/dashboard`
- Pick top 3 founder decisions from
  `docs/EXECUTIVE_DECISION_PACK.md` to act on this week
- Take 1 day OFF — protect founder energy

## Monthly cadence

- Run `python scripts/dealix_proof_pack.py` per active customer
- Open new pilot slots only if existing pilots have closed
  (`proof.customer_approved`)
- Review pricing — ONLY change 499 SAR if ≥ 3 archived proof events
  justify it

## Hard rules — re-asserted

- ❌ NO live send / NO live charge on any day
- ❌ NO scraping / NO cold WhatsApp / NO LinkedIn DM automation
- ❌ NO customer name in this repo without signed permission
- ❌ NO public revenue claim without ≥ 1 archived proof event +
  signed permission
- ✅ Every external action: drafted by Dealix → approved by
  founder → sent manually
- ✅ Arabic primary, English secondary

## Bilingual one-liner

**Arabic**: 4–5 لمسات يومياً، كل خطوة بموافقة المؤسس، لا تشغيل آلي.
**English**: 4–5 founder-approved touchpoints per day. No automated
sends, ever.
