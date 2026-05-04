# Dealix WhatsApp Architecture & Policy

> Three modes. One default. No exceptions.

## Default

`WHATSAPP_ALLOW_LIVE_SEND=false` → all outbound is **blocked**.
Verified live on prod: `POST /api/v1/os/test-send` returns
`{"status":"blocked","error":"whatsapp_allow_live_send_false"}`.

## Mode 1 — Internal daily brief preview

| Endpoint | Roles served | Status |
| --- | --- | --- |
| `GET /api/v1/whatsapp/brief?role=*` | growth_manager, ceo, revops, customer_success, finance, compliance | PROVEN_LIVE for `growth_manager` (the rest depend on `deals.hubspot_deal_id` schema fix) |
| `POST /api/v1/whatsapp/brief/send-internal` | staff allowlist | CODE_EXISTS_NOT_PROVEN — must require `WHATSAPP_ALLOW_INTERNAL_SEND=true` AND a phone allowlist before firing |

## Mode 2 — Customer inbound

Pipeline (verified locally):

1. Meta WhatsApp Cloud API webhook → `POST /api/v1/webhooks/whatsapp`
2. Signature verified (`WHATSAPP_APP_SECRET` HMAC).
3. `POST /api/v1/prospect/inbound/whatsapp` records the message.
4. `POST /api/v1/prospect/route` classifies (rule-based, deterministic).
5. `POST /api/v1/personal-operator/messages/draft` produces an Arabic
   reply DRAFT (never auto-sent).
6. Founder approves and sends the reply manually OR via the (future)
   approved-template path.

## Mode 3 — Approved templates (BACKLOG)

Out-of-24h-window template-send pipeline. Required pre-conditions before
this turns on:

1. Template catalog registered with Meta (`proof_ready`, `meeting_reminder`,
   `diagnostic_ready`, `pilot_followup`).
2. Per-customer opt-in record in `ConsentRecord` table.
3. 24h-window check at send time.
4. Last-send debounce.
5. `WHATSAPP_ALLOW_LIVE_SEND=true` flag.
6. Audit log of every send event.

Until all 6 are wired AND tested, **the flag stays false**.

## Hard policy (PDPL + Meta)

| Rule | Enforcement |
| --- | --- |
| No cold WhatsApp to purchased numbers | classifier blocks intent + `compliance/check-outreach` blocks per-row |
| No bulk send | classifier + channel gate |
| No bot replies without human approval | inbound webhook produces drafts only |
| 24h-window respected | template required outside window (BACKLOG) |
| Opt-out honored | `SuppressionRecord` checked on every send |
| Verify-token gate | `webhooks/whatsapp` GET requires token (verified 422 without) |
| HMAC sig gate | `webhooks/whatsapp` POST verifies `WHATSAPP_APP_SECRET` |

## What WhatsApp will NEVER do (in Dealix)

- send unsolicited messages to purchased numbers
- ignore opt-out
- run automated drip campaigns to cold lists
- bypass the 24h-window template rule
- pretend to be a human

## What WhatsApp CAN do safely today

- receive inbound and store in `ConversationRecord`
- generate Arabic-Saudi reply DRAFT
- escalate to a human (founder) for approval
- run risk classification on each inbound message
- track conversation state

## Test commands

```bash
# verify-token gate
curl -sf -o /dev/null -w "%{http_code}\n" https://api.dealix.me/api/v1/webhooks/whatsapp
# expected: 422

# outbound gate
curl -X POST 'https://api.dealix.me/api/v1/os/test-send?phone=%2B966500000000&body=hi'
# expected: blocked

# unsigned webhook gate
curl -X POST -H "Content-Type: application/json" -d '{}' \
  https://api.dealix.me/api/v1/webhooks/moyasar -o /dev/null -s -w "%{http_code}\n"
# expected: 401
```
