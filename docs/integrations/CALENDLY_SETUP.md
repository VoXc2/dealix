# Calendly Integration — Setup Guide

**Status:** PARTIAL — Calendly link can be embedded; webhook handler NOT_BUILT (Wave 8 trigger)
**Audience:** Dealix paying customers + Sami (founder)
**Companion:** `integrations/calendar.py` · Plan §23.5.1 P0.4
**Wave:** 7.5 §24.4

> **Honest disclosure:** Calendly link sharing works (just paste URL); automated webhook capture of bookings → Dealix Lead Inbox is NOT built (deferred to Wave 8).

---

## What works today

### Customer-facing demo booking

1. Customer creates Calendly account (Standard plan recommended — $10/mo for webhook access)
2. Sets up a booking type: "Dealix Demo — 30 min" or "Dealix Day-7 Review — 30 min"
3. Customer shares the link in:
   - Their email signature
   - WhatsApp Business away-message
   - Their existing website CTA

### Sami-facing for first 5 warm intros

Per `SALES_OPS_SOP.md` §6 close cadence:

1. Sami's Calendly: `calendly.com/sami-dealix` (or whatever domain Sami picks)
2. After diagnostic call, Sami sends Calendly link to prospect via WhatsApp
3. Prospect books → Sami's Calendly emails confirmation
4. Sami manually copies booking details to `dealix_demo_outcome.py` (per Wave 6 CLI):

```bash
python3 scripts/dealix_demo_outcome.py \
  --prospect-handle <handle> --sector <sector> \
  --outcome interested --next-action "Demo booked Calendly $<date>"
```

---

## What activates in Wave 8 (`calendly_webhook` TARGET)

When triggered (3rd customer asks for "did the prospect book?" auto-update):

### Webhook setup (future state)

1. Sami creates Calendly Personal Access Token (P0.4 in `docs/SAMI_ACTION_ITEMS.md`):
   - `developer.calendly.com` → API key generation

2. Configure Calendly webhook:
   - URL: `https://api.dealix.me/api/v1/webhooks/calendly`
   - Events: `invitee.created`, `invitee.canceled`, `routing_form_submission.created`

3. Each booking → automatic:
   - Lead Inbox entry (if new prospect)
   - Demo Outcome record (if known prospect)
   - Calendar block on Sami's calendar
   - Pre-meeting brief generated

### Endpoint (when activated)

```bash
POST https://api.dealix.me/api/v1/webhooks/calendly
{
  "event": "invitee.created",
  "payload": {
    "scheduled_event": {...},
    "invitee": {"name": "...", "email": "...", "questions_and_answers": [...]}
  }
}
```

Webhook handler validates Calendly signature (`Calendly-Webhook-Signature` header), parses payload, creates Lead/Demo records with `source=calendly`.

---

## Setup environment variables (when Wave 8 activates)

```bash
# Railway dashboard → service envs
CALENDLY_API_KEY=<personal-access-token>
CALENDLY_WEBHOOK_SIGNING_KEY=<from webhook config>
CALENDLY_OWNER_URI=https://api.calendly.com/users/<sami-uuid>
```

---

## Verification (current state — manual)

After customer books a demo:

```bash
# Sami logs the outcome (Wave 6 CLI)
python3 scripts/dealix_demo_outcome.py \
  --prospect-handle <handle> --sector <sector> \
  --outcome interested --next-action "..."

# Check Lead Inbox
curl -s "https://api.dealix.me/api/v1/customer-portal/<handle>?access=<token>" | jq '.sections.lead_inbox'
```

---

## Verification (Wave 8 — when webhook activates)

```bash
# Trigger test booking from Calendly's webhook tester
# Should appear within 30 seconds in Lead Inbox

curl -s "https://api.dealix.me/api/v1/customer-portal/<handle>?access=<token>" \
  | jq '.sections.lead_inbox.recent_leads[] | select(.source=="calendly")'
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Booking confirmed, but no Lead Inbox entry | Webhook not configured (Wave 7.5 — manual) | Sami runs `dealix_demo_outcome.py` manually |
| Webhook returns 403 (Wave 8) | Signing key mismatch | Verify `CALENDLY_WEBHOOK_SIGNING_KEY` matches Calendly dashboard |
| Saudi timezone offset wrong | Calendly default UTC | Set Sami's Calendly profile to `Asia/Riyadh` |
| Quiet-hours conflict | Booking 21:00-08:00 KSA | Calendly availability rules → exclude quiet hours |

---

## Hard rules

- ❌ NO_BLAST: Calendly is for 1-to-1 demos, never group booking blast
- ❌ NO_SCRAPING: Dealix never scrapes Calendly URLs from prospects' websites
- ✅ Customer's bookings respect their own Calendly availability rules
- ✅ Saudi quiet-hours (21:00-08:00) honored on Sami's profile

---

## Pricing notes

- Calendly Free: shareable link, NO webhook
- Calendly Standard ($10/mo): webhooks + multiple booking types — recommended
- Calendly Teams ($16/seat/mo): not needed until 2nd CSM hired

---

## What's deferred to Wave 8

- Webhook handler at `/api/v1/webhooks/calendly`
- Auto-create Lead Inbox entry on booking
- Auto-create pre-meeting brief
- Calendly API two-way sync (cancel/reschedule from Dealix)
- Multi-Calendar support (Cal.com, Google Calendar native, etc.)
