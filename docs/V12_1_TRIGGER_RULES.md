# V12.1 Trigger Rules — gate the next iteration on real customer evidence

> The next iteration is V12.1, NOT V13.
> V12.1 can ship ONLY after at least one of the trigger conditions
> below is met with verifiable evidence.

## Trigger conditions (any one is enough)

| # | Trigger | Required evidence |
|---|---|---|
| 1 | `payment_received` | Moyasar dashboard screenshot OR bank statement showing the customer's funds landed |
| 2 | `written_commitment_received` | Email from customer with explicit commitment text + amount + date |
| 3 | `delivery_session_started` | `POST /api/v1/delivery-os/create-session` returned status `in_progress` AND ≥ 1 day-output sent |
| 4 | `proof_event_logged_from_real_customer` | A real `docs/proof-events/<slot>.json` file with a verified event (NOT placeholder, NOT empty template) |

## V12.1 scope (allowed when triggered)

Each item is a *patch* on existing V12, NOT a new layer:

- Real customer lifecycle records (in-memory → simple persistence)
- Manual payment confirmation record (Moyasar webhook → audit event)
- Support ticket evidence (real tickets → ledger)
- Delivery session evidence (per-customer outputs)
- Proof event ledger persistence (JSONL → DB-backed if customer count > 3)
- Customer approval snapshot (signed publish-permission)
- First case study template (only with signed permission)
- Founder weekly report from real data (replaces V12 stub)

## V12.1 forbidden (regardless of trigger)

- ❌ V13 naming
- ❌ Live WhatsApp / Gmail / LinkedIn / Moyasar live charge
- ❌ Scraping / cold WhatsApp / fake proof
- ❌ New pricing tier without ≥ 3 paid pilots
- ❌ White-label without ≥ 3 paid pilots
- ❌ Revenue-share automation without referral data
- ❌ Removing any V11/V12 hard gate
- ❌ Adding any heavy dependency (Sentry, Datadog, Langfuse) without explicit founder decision
- ❌ Self-modifying code in Self-Improvement OS

## What does NOT count as a trigger

- ❌ A diagnostic delivered (work, not revenue)
- ❌ A pilot OFFERED but not accepted (work, not revenue)
- ❌ A draft Moyasar invoice that hasn't been paid
- ❌ A verbal "yes" on a call without written follow-up
- ❌ A LinkedIn reply expressing "interest" without a meeting
- ❌ A customer testing the live demo without signing intake
- ❌ A partner introduction without the partner's customer paying

## How to check if V12.1 is allowed

```bash
# Check 1 — payment evidence
ls docs/proof-events/*.json 2>/dev/null
# (Real proof event JSONs would live here; empty = no trigger)

# Check 2 — commitment evidence (founder's manual record, NOT in repo)
echo "Check your private vault for signed-commitment emails"

# Check 3 — delivery session
curl -s https://api.dealix.me/api/v1/delivery-os/status

# Check 4 — pipeline truth
curl -s https://api.dealix.me/api/v1/revenue-pipeline/status
```

If at least one of the 4 checks shows real evidence → V12.1 is unblocked.
If all 4 show empty → **stay in execution mode**, run another 14-day cycle.

## Decision rule (founder, weekly)

Every Sunday, the founder asks one question:

> "Has anyone paid me OR signed a written commitment in the last 7 days?"

- **Yes** → V12.1 candidate, but only the patches that map to the real customer's path.
- **No** → No new code this week. Repeat the 14-day playbook.

The trap to avoid: building "V12.1 customer success enhancements" or
"V12.1 better support classifier" without a real customer to inform
what's missing. Code without customer signal is **imagination tax**.

## Dealix doctrine, re-asserted

```
DEALIX_DOCTRINE = {
  "build_only_what_real_customers_force_you_to_build": true,
  "never_invent_proof": true,
  "never_invent_revenue": true,
  "never_open_a_live_gate_without_evidence": true,
  "approval_first_always": true,
  "Arabic_primary": true,
  "first_paid_pilot_unblocks_v12_1": true,
  "no_v13_until_at_least_3_paid_pilots": true
}
```
