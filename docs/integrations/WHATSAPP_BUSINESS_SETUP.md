# WhatsApp Business Integration — Setup Guide

**Status:** PRODUCTION_READY when credentials set · DEMO_FALLBACK without
**Audience:** Dealix paying customers + Sami (founder)
**Companion:** `auto_client_acquisition/whatsapp_safe_send.py` · `auto_client_acquisition/safe_send_gateway/` · `integrations/whatsapp.py`
**Wave:** 7.5 §24.4

> **What you get:** Inbound WhatsApp messages classified, draft replies prepared in Saudi-Arabic, every outbound message gates through 6 hard rules (approval / opt-out / quiet-hours / consent record). Founder presses Approve to send.

---

## Prerequisites

- Saudi commercial registration (CR number)
- Verified Facebook Business account
- WhatsApp Business app installed on a real phone (not Personal account)
- Phone number that's NOT used in Personal WhatsApp
- DPA lawyer-signed (per `docs/LEGAL_ENGAGEMENT.md` deliverable L1)

**Fallback if not yet ready:** Sami uses his personal WhatsApp number for first 3 customers. Drafts still generate; he taps the WhatsApp share button manually.

---

## Step-by-step (Meta Business verification — 2-5 days)

### 1. Create Facebook Business account

- Go to `business.facebook.com` → Create Account
- Fill: Saudi business name, CR number, owner contact

### 2. Create WhatsApp Business app

- In Business Manager → Settings → WhatsApp Accounts → Add
- Verify business domain (DNS TXT record check)
- Submit business verification (KYC documents, takes 2-5 business days)

### 3. Generate System User token

- Business Manager → System Users → Add
- Name: `dealix_whatsapp_system_user`
- Assign to your WhatsApp Business app
- Generate Access Token (long-lived, 60 days+)

### 4. Get phone number ID

- WhatsApp Business → Phone Numbers tab
- Click your number → Copy Phone Number ID (15-digit)

### 5. Approve `dealix_daily_decisions` template

- WhatsApp Manager → Message Templates → Create
- Name: `dealix_daily_decisions`
- Category: UTILITY (not Marketing — required for daily-use)
- Body (Saudi-Arabic): «صباح الخير، عندك ٣ قرارات اليوم: ...»
- Wait for Meta approval (~24h)

### 6. Hand tokens to Sami

Tokens sent via 1Password / signed PDF (NEVER plaintext WhatsApp):

```
WHATSAPP_PHONE_NUMBER_ID=<15-digit>
WHATSAPP_ACCESS_TOKEN=<long-token>
WHATSAPP_APP_SECRET=<from Meta App Settings>
WHATSAPP_BUSINESS_ACCOUNT_ID=<from Manager>
```

Sami pastes into Railway dashboard → service env vars.

### 7. Webhook URL (for inbound messages)

- WhatsApp Manager → Configuration → Webhook
- Callback URL: `https://api.dealix.me/api/v1/webhooks/whatsapp`
- Verify token: agreed value (same as `WHATSAPP_VERIFY_TOKEN` env var)
- Subscribe to: `messages`, `message_template_status_update`

---

## Verification

After Sami sets env vars + Railway redeploys:

```bash
# 1. Production health
curl -s https://api.dealix.me/health | jq '.providers'
# Should include "whatsapp" if env vars set

# 2. Send test inbound (from Meta tester tools)
# Webhook should return 200, lead record appears in /founder-leads.html

# 3. Approve a draft
# /decisions.html → click Approve on a pending draft
# Outbound message sends through 6 gates, audit log entry written
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "WhatsApp Cloud API rate limit hit" | New account low quota | Wait 24h, gradually warm up |
| Webhook returns 403 | `WHATSAPP_VERIFY_TOKEN` mismatch | Double-check Railway env var matches Meta config |
| Drafts generate but don't send | `safe_send_gateway` blocking | Check `consent_record_id` exists in approvals table; review block reason in audit log |
| Customer phone receives "blocked" notification | Quiet-hours gate triggered | KSA 21:00-08:00 outbound paused — message will queue until next active window |

---

## What's automated vs manual

| Action | Automated? |
|---|---|
| Inbound message classification (Saudi-Arabic intent detection) | ✅ Automated |
| Draft reply generation | ✅ Automated |
| Founder approval | ❌ Manual (per NO_LIVE_SEND) |
| Outbound send (after approval) | ✅ Automated |
| Opt-out detection (customer sends "STOP" or "ايقاف") | ✅ Automated |
| Quiet-hours queue | ✅ Automated |

---

## Hard rules (immutable in code)

- ❌ NO_COLD_WHATSAPP: zero outbound to numbers without consent_record_id on file
- ❌ NO_LIVE_SEND in test env: production-only outbound
- ❌ NO_BLAST: no bulk 1-to-many sends; each conversation is 1-to-1 with explicit approval
- ✅ Every send has audit_log entry with correlation_id
- ✅ Opt-out is permanent (PDPL — cannot be re-enabled by customer accident)

---

## What's deferred to Wave 8

- Customer self-service WhatsApp number setup wizard (currently Sami-led)
- Template approval pre-flight checker
- WhatsApp Decision Bot for non-founder roles (currently founder-only via `/decisions.html`)
