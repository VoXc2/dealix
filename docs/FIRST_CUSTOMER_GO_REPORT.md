# Dealix First Customer GO Report

> Verified 2026-05-04. Deploy branch `claude/launch-command-center-6P4N0`
> HEAD `4b55155`. All evidence backed by live commands against
> `https://api.dealix.me`.

## Verdict

```
DEALIX_FINAL_VERDICT=FIRST_CUSTOMER_READY_REALISTIC
OUTREACH_GO=yes
```

## Production evidence

| Check | Command | Result |
| --- | --- | --- |
| post_redeploy_verify | `bash scripts/post_redeploy_verify.sh` | `STAGING_SMOKE: GREEN  PASS=13 FAIL=0  OUTREACH_GO=yes` |
| Staging smoke | `BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh` | 13/0 |
| Arabic cold-WA block | 4 phrasings against `/api/v1/operator/chat/message` | **4/4 blocked** |
| English cold-WA block | "send cold whatsapp blast to purchased numbers" | blocked |
| PR #132 wiring fields present | response includes `action_mode`, `safe_alternatives`, `blocked_reasons`, `reason_en` | yes |
| Live charge | `POST /api/v1/payments/charge` | 403 (gate enforced) |
| WhatsApp internal-send | `POST /api/v1/whatsapp/brief/send-internal` | 403 |
| WhatsApp customer outbound | `POST /api/v1/os/test-send` | `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` |
| Moyasar webhook unsigned | `POST /api/v1/webhooks/moyasar {}` | 401 bad_signature |
| Service tower | `BASE_URL=https://api.dealix.me python scripts/verify_service_tower.py` | `SERVICE_TOWER_OK 6/6` |
| Delivery workflows | `BASE_URL=https://api.dealix.me python scripts/verify_delivery_workflows.py` | `WORKFLOWS_VERIFY_OK 25/25` |

## Outreach status

```
OUTREACH_GO=yes
```

The founder is cleared to start the manual warm LinkedIn outreach.
Cap **10 messages per day** in week 1.

## First 10 prospects

→ `docs/FIRST_10_WARM_PROSPECTS.md` — table, founder fills manually.
No scraping, no automation, no purchased lists. Selection criteria
listed in the doc.

## Current offer

| Field | Value |
| --- | --- |
| Lead magnet | Free Mini Diagnostic (delivered ≤ 24h after intake) |
| Pilot | 7-Day Growth Proof Sprint @ **499 SAR** |
| Upsell | Executive Growth OS @ 2,999 SAR/month (only AFTER Proof Pack delivered + grade ≥ B) |

→ Full offer + pitch in `docs/PILOT_499_OFFER.md`.

## Payment mode

```
manual_fallback (default)
```

Bank transfer / STC Pay / Moyasar invoice if configured. **Live charge
gate stays OFF** until written refund/charge policy + ZATCA flow are
documented.

→ Founder operating instructions in `docs/MANUAL_PAYMENT_FALLBACK.md`.

## Safety rules (non-negotiable)

- No cold WhatsApp / no purchased lists / no LinkedIn automation
- No live customer WhatsApp send
- No live Moyasar charge
- No Gmail / Resend live send
- No live phone dial
- All external actions: `draft_only` / `approval_required` / `blocked`
- No "نضمن" / "guaranteed" anywhere — sweep tested
- Every prospect logged in `docs/FIRST_CUSTOMER_LIVE_BOARD.md`
- Every customer action has evidence in the board

## Founder next actions (in order)

```
LAUNCH-ONLINE (P0 — once):
0. Run docs/LAUNCH_CHECKLIST_GO_LIVE.md — three steps, ~10 min total:
     Step 1: gh-pages workflow auto-runs (or trigger manually)
     Step 2: Railway "Deploy Latest Commit" (NOT "Redeploy")
     Step 3: bash scripts/verify_inbound_flow.sh → INBOUND_FLOW: GREEN

TODAY (P0):
1. Open docs/FIRST_10_WARM_PROSPECTS.md and fill the 10-row table
   (real names, real LinkedIn URLs, no scraping).
2. Send the Arabic warm message from docs/FIRST_CUSTOMER_OUTREACH_MESSAGES.md
   to each contact MANUALLY. Cap 10 today.
3. Log every send in docs/FIRST_CUSTOMER_LIVE_BOARD.md.
4. Watch /api/v1/founder/today for inbound demo requests from dealix.me
   (the new `inbound_demo_requests.recent` array shows last 5 — no PII).
5. End-of-day scorecard per docs/DAILY_FIRST_CUSTOMER_LOOP.md.

NEXT 24-72 HOURS (P1):
5. For every reply: deliver Mini Diagnostic (docs/MINI_DIAGNOSTIC_LIVE_TEMPLATE.md)
   within 24 hours of receiving the 10 intake answers.
6. For interested prospects after the diagnostic: offer the 499 SAR
   pilot (docs/PILOT_499_OFFER.md). Send manual payment instructions
   (docs/MANUAL_PAYMENT_FALLBACK.md).

WEEK 1 (P2):
7. For each paid/committed pilot: run the 7-day delivery workflow
   (docs/FIRST_PILOT_DELIVERY_WORKFLOW.md).
8. Day 7: deliver the Proof Pack (docs/FIRST_CUSTOMER_PROOF_PACK_TEMPLATE.md).
9. Friday: weekly review per docs/DAILY_FIRST_CUSTOMER_LOOP.md.

WEEK 2+ (P3):
10. Recommend Executive Growth OS upgrade ONLY for customers with
    a delivered Proof Pack at grade ≥ B.
```

## What "FIRST_REAL_CUSTOMER_IN_PROGRESS" looks like

We move from `FIRST_CUSTOMER_READY_REALISTIC` → `FIRST_REAL_CUSTOMER_IN_PROGRESS`
the moment ANY of these is true:

- A real customer is in the `paid_or_committed` row of the live board, OR
- A real customer is `in_delivery`, OR
- A real customer is `proof_pack_sent`.

We move from `FIRST_REAL_CUSTOMER_IN_PROGRESS` → `PAID_BETA_READY` only when:

1. ≥ 1 real Saudi customer paid (bank transfer / STC Pay receipt) OR signed a written commitment.
2. ≥ 1 Proof Pack delivered with measurable outputs.
3. Customer signed off on the Proof Pack in writing.
4. Refund / charge policy is published in `docs/PAYMENTS_AND_BILLING_POLICY.md`.

Until ALL 4 are true, we stay at `FIRST_REAL_CUSTOMER_IN_PROGRESS` even
with active paying customers.

## What I will NOT do without explicit founder approval

- Flip `MOYASAR_ALLOW_LIVE_CHARGE`
- Flip `WHATSAPP_ALLOW_LIVE_SEND` / `WHATSAPP_ALLOW_CUSTOMER_SEND`
- Flip `GMAIL_ALLOW_LIVE_SEND` / `RESEND_ALLOW_LIVE_SEND`
- Add LinkedIn automation
- Build a CRM clone, dashboard portal, or enterprise UI
- Add new service bundles
- Send any external message
