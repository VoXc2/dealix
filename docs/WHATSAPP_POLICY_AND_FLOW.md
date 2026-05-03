# Dealix WhatsApp Policy & Flow

> Source: live verification on `https://api.dealix.me` and code inspection
> in `auto_client_acquisition/whatsapp/` and `api/routers/webhooks.py`.

## TL;DR

Dealix supports three WhatsApp surfaces:

1. **Internal daily brief (preview only)** — staff-only Arabic preview text
   per role. **Live for `growth_manager` only** today; `sales_manager`
   and `ceo` return 500 (DB schema bug — see Truth Report §4).
2. **Customer inbound webhook** — Meta WhatsApp Cloud API → Dealix records
   the message, runs intent classification, drafts an Arabic reply for
   human approval. **Outbound is NOT auto-sent.**
3. **Approved templates (post-launch)** — out-of-24h-window template sends
   for proof-ready / meeting-reminder / diagnostic-ready / pilot-followup.
   **Currently BACKLOG** — the template catalog and opt-in registry are not
   wired into the live `os/test-send` path.

## Hard rules (enforced today)

| Rule | Enforcement | Status |
| --- | --- | --- |
| No cold WhatsApp to purchased numbers | `compliance/check-outreach` rejects opt-out / no-consent rows; `compliance/campaign-risk` flags purchased lists | PROVEN_LIVE |
| No live customer outbound by default | `WHATSAPP_ALLOW_LIVE_SEND=false` (settings.py:106) → `os/test-send` returns `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` | PROVEN_LIVE |
| No bot replies to customers without human approval | inbound webhook records the conversation; outbound is draft-only | PROVEN_LIVE |
| Webhook signature verified | `webhooks/whatsapp` GET requires `WHATSAPP_VERIFY_TOKEN`; POST requires `WHATSAPP_APP_SECRET` HMAC | PROVEN_LIVE (422 on bad GET) |
| 24-hour window respected | template-send code path requires approved template id; not auto-sent | CODE_EXISTS_NOT_PROVEN |
| Opt-out honored | `SuppressionRecord` checked in `compliance/check-outreach` | PROVEN_LOCAL |

## Mode 1 — Internal Daily Brief Preview

Endpoint: `GET /api/v1/whatsapp/brief?role=<role>` (deploy branch only)

Tested roles:

| Role | Status | Notes |
| --- | --- | --- |
| `ceo` | **500 BLOCKER** | schema mismatch downstream of `deals.hubspot_deal_id` |
| `sales_manager` | **500 BLOCKER** | same root cause |
| `growth_manager` | **PROVEN_LIVE** | clean Arabic brief returned |
| `revops` | live (200) — depends on data | PROVEN_LIVE |
| `customer_success` | live | PROVEN_LIVE |
| `agency_partner` | not exercised | CODE_EXISTS_NOT_PROVEN |
| `finance` | live | PROVEN_LIVE |
| `compliance` | live | PROVEN_LIVE |

There is also `POST /api/v1/whatsapp/brief/send-internal` for staff-only
delivery — not exercised here, but the ALLOW_LIVE_SEND gate must apply.

## Mode 2 — Customer Inbound

Endpoint: `POST /api/v1/webhooks/whatsapp` (Meta inbound)

Pipeline (verified locally):

1. Webhook payload arrives, signature verified.
2. `prospect/inbound/whatsapp` records the message.
3. `prospect/route` classifies (rule-based deterministic, no LLM call needed).
4. `personal-operator/messages/draft` produces an Arabic-Saudi reply draft.
5. Reply is **not auto-sent** — human approval required before outbound.

A user can also start the conversation via `wa.me/<sales-number>` link from
the landing pages. Dealix never initiates a cold conversation.

## Mode 3 — Approved Templates (BACKLOG)

What's needed before turning this on:

- Approved template catalog (`proof_ready`, `meeting_reminder`,
  `diagnostic_ready`, `pilot_followup`) registered with Meta.
- Per-customer opt-in record in `ConsentRecord` table.
- Template-render endpoint that fills variables and sends ONLY when:
  - `WHATSAPP_ALLOW_LIVE_SEND=true`, AND
  - opt-in present, AND
  - 24h-window check passed (or template is approved for outside the
    window), AND
  - last-send-debounce passed.

Until all four conditions are wired and tested, **leave
`WHATSAPP_ALLOW_LIVE_SEND=false`**.

## What customer WhatsApp WILL NEVER do

- send unsolicited messages to purchased numbers
- ignore opt-out
- run automated drip campaigns to cold lists
- bypass the 24h-window template rule
- pretend to be a human

## What customer WhatsApp CAN do (today, safely)

- receive inbound messages and store them
- generate an Arabic-Saudi reply DRAFT
- escalate to a human (Sami / sales) for approval
- track conversation state in `ConversationRecord`
- run risk classification on each inbound (`prospect/route`)

## Test commands

```bash
# Verify the inbound webhook verify-token gate (must fail without token):
curl -i https://api.dealix.me/api/v1/webhooks/whatsapp
# expected: 422

# Verify outbound test-send is blocked by policy gate:
curl -X POST 'https://api.dealix.me/api/v1/os/test-send?phone=%2B966500000000&body=hi'
# expected: {"status":"blocked","error":"whatsapp_allow_live_send_false"}

# Verify cold-list compliance check:
curl -X POST https://api.dealix.me/api/v1/compliance/check-outreach \
  -H "Content-Type: application/json" \
  -d '{"to_email":"x@y.sa","contact_opt_out":true,"allowed_use":"cold_purchased"}'
# expected: {"allowed":false,"blocked_reasons":["contact_opt_out_true"],...}
# NOTE: this endpoint currently 500s on prod (DB session bug fix is on this
# branch but not yet deployed). Locally PROVEN.
```
