# LaaS Invoicing SOP (Per-Reply + Per-Demo, Manual for First 5 Customers)

> **Scope:** how Dealix bills customers on R3 metered plans (`laas_per_reply`, `laas_per_demo`).
> **Phase 1 (customers 1–5):** founder reviews recorded events weekly and issues manual ZATCA invoices.
> **Phase 2 (customers 6+):** auto-invoice from accumulated events (build when justified by volume).

---

## Event Recording (already automated)

Every reply or booked-demo event POSTs to `/api/v1/pricing/usage`:

```http
POST /api/v1/pricing/usage
Content-Type: application/json
Authorization: Bearer <ADMIN_API_KEY>

{
  "plan": "laas_per_reply",
  "customer_handle": "acme_saas",
  "event_id": "wamsg_abc123_def",
  "lead_id": "lead_45",
  "metadata": {
    "channel": "whatsapp",
    "reply_text_hash": "...",
    "conversation_turns": 3
  }
}
```

Endpoint returns:
- `status: "recorded"` — first time this event_id is seen, billable
- `status: "duplicate"` — same event_id already counted, NOT billable

Idempotency window: 30 days. Same event_id outside that window WILL be counted (rare; investigate if it happens).

## Weekly Invoicing Cadence (Manual, Phase 1)

Every Sunday morning:

```bash
# 1. Pull billable events from last 7 days
redis-cli --scan --pattern "laas:laas_per_reply:*" | \
  xargs -I{} redis-cli GET {} | \
  jq -s 'map(select(.recorded_at > (now - 7*86400)))' > /tmp/week_events.json

redis-cli --scan --pattern "laas:laas_per_demo:*" | \
  xargs -I{} redis-cli GET {} | \
  jq -s 'map(select(.recorded_at > (now - 7*86400)))' >> /tmp/week_events.json

# 2. Group by customer_handle
jq 'group_by(.metadata.customer_handle) | map({
  handle: .[0].metadata.customer_handle,
  per_reply_count: map(select(.metadata.plan=="laas_per_reply")) | length,
  per_demo_count:  map(select(.metadata.plan=="laas_per_demo"))  | length
})' /tmp/week_events.json
```

For each customer:
- Replies × 25 SAR + Demos × 150 SAR = subtotal
- Add 15% VAT
- Issue ZATCA Phase 2 e-invoice (via `integrations/zatca.py:build_invoice_xml`)
- Charge via Moyasar (one-off) or include in next monthly subscription invoice
- Email customer ZATCA-compliant PDF receipt within 2 business days

## What to Tell the Customer at Intake

> "Our LaaS pricing is fully event-based: 25 SAR every time a lead engages back in Arabic conversation (≥ 2 message exchanges), or 150 SAR every time a lead books a demo on your calendar. We send you an itemized weekly summary on Sunday, then invoice via ZATCA-compliant e-invoice on the same day. You can audit every charge against the event log in your tenant dashboard."

## What Counts as a Billable Reply

A reply counts ONLY IF:
- Inbound message was in Arabic (detected by `core.lang.detect_arabic`)
- The lead exchanged ≥ 2 messages with Dealix's AI agent
- The lead is on Customer's ICP filter (not random spam)
- No duplicate `event_id` within 30 days

What does NOT count:
- Lead opened the message but didn't reply (read receipt only)
- Lead replied with "stop" / "remove me" / opt-out signal
- Test messages from the customer themselves (filtered by `WHATSAPP_TEST_ALLOWLIST`)
- Messages from numbers on customer's suppression list

## What Counts as a Billable Demo

A demo counts ONLY IF:
- Calendar event was created via Dealix-initiated link (Calendly UTM tag)
- The lead actually showed up (verified by customer post-meeting → "demo_held": true marked in tenant config)
- The demo is in Customer's currency = Saudi B2B target (not internal team practice meetings)

Customer marks demo_held=true via:
```http
POST /api/v1/pricing/usage
{
  "plan": "laas_per_demo",
  "event_id": "<calendly_event_id>",
  "customer_handle": "...",
  "metadata": {"demo_held": true, "attended_at": "..."}
}
```

If `demo_held` is never true within 7 days of scheduled time, the event is auto-marked no-show and NOT billed.

## Dispute Resolution

If customer disputes a charge:

1. Pull the event log: `redis-cli GET laas:laas_per_reply:<handle>:<event_id>`
2. Show the original WhatsApp/email thread (PDPL-compliant export, no PII to third parties)
3. If valid dispute → refund via Moyasar partial refund button + remove event from billable pool
4. If invalid dispute → explain calmly with evidence; offer "good faith" 1-event credit if customer is high-value

Refund rate target: < 2% of billable events. Higher = pipeline quality problem to investigate.

## Migration to Automated Billing (Phase 2)

Activate when ANY of:
- Total weekly events across all customers > 500 (founder time > 4 hours/week)
- Customer #6 onboards
- Customer requests programmatic invoicing API

Implementation (deferred):
- Cron job runs every Sunday 09:00 AST
- Aggregates events per customer
- Generates ZATCA invoice via existing builder
- Charges via Moyasar Recurring API (subscription with line items)
- Emails PDF receipt
- Updates customer dashboard with billing history

## Monthly Reconciliation

Last day of each month, founder reviews:

- [ ] Total billable replies vs total replies in tenant dashboard (sanity check)
- [ ] Total billable demos vs Calendly event count
- [ ] Sum invoiced vs sum collected (any payment gaps?)
- [ ] Average per-customer revenue trending up or down
- [ ] Per-customer reply/demo ratio (target: 5–10% of replies become demos)

Append findings to `docs/ops/laas_monthly_reconciliation/YYYY-MM.md` for trend analysis.
