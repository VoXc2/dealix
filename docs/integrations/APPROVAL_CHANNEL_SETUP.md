# Approval Channel — Setup Guide

**Status:** PRODUCTION_READY — `/decisions.html` browser + WhatsApp Decision Bot (founder-only)
**Audience:** Sami (founder)
**Companion:** `landing/decisions.html` · `api/routers/whatsapp_decision_bot.py` · `api/routers/approval_center.py`
**Wave:** 7.5 §24.4

> Every external action requires Sami's approval (NO_LIVE_SEND). Approvals route through `/decisions.html` (browser) by default. Optional WhatsApp Decision Bot (admin-only) lets Sami approve from his phone via voice/text commands.

---

## Default flow — `/decisions.html`

### URL

```
https://dealix.me/decisions.html?org=<handle>&access=<token>
```

The `access` parameter:
- Founder's master token: `dealix-founder-2026` (from `landing/assets/js/access-gate.js`)
- Per-customer token: from `data/customers/<handle>/customer_portal_token.txt`

### What Sami sees

1. **KPI strip:** pending count · approved today · rejected today
2. **Pending list:** each card shows:
   - Draft text (Saudi-Arabic + English)
   - Channel (whatsapp / email / sms)
   - Risk level (low / medium / high)
   - Source (which agent/workflow generated it)
   - Customer context
3. **Per-card buttons:** Approve · Reject · Edit (rare)

### Behavior on Approve

```bash
POST https://api.dealix.me/api/v1/approvals/<approval_id>/approve
```

- Approval state: `pending` → `approved`
- `safe_send_gateway.enforce_consent_or_block()` runs (per Fix 4)
- If gates pass → outbound send happens
- Audit log entry written with `correlation_id`

### Behavior on Reject

```bash
POST https://api.dealix.me/api/v1/approvals/<approval_id>/reject
```

- Approval state: `pending` → `rejected`
- No send happens
- Customer-facing UI shows "founder reviewed, declined" (no detail leak)

---

## Optional — WhatsApp Decision Bot (admin-only)

### Setup

The bot is FOUNDER-ONLY (per `_HARD_GATES.no_customer_outbound: True`). It listens on Sami's personal WhatsApp number (NOT a business number). Sami sends commands like:

```
وش الوضع اليوم؟        → returns top 3 decisions
وش أهم 3 قرارات؟       → returns priority decisions
جهز رد للعميل acme     → drafts reply (does NOT send)
اعتمد الرد <id>        → marks as approved
صعّد التذكرة <id>      → escalates with reason
```

### Endpoint

```bash
POST https://api.dealix.me/api/v1/whatsapp-decision/command
Authorization: Bearer <FOUNDER_TOKEN>
{"text": "وش أهم 3 قرارات؟", "from": "+966<sami>"}
```

Returns:
```json
{
  "command": "top_3_decisions",
  "decisions": [...],
  "ar_response": "...",
  "en_response": "..."
}
```

### Limitations

- Founder-only auth (Sami's phone only)
- NEVER sends customer-facing messages
- ALWAYS routes through `safe_send_gateway` for any approval action
- Verbose audit log (every command logged)

---

## Verification

```bash
# 1. Check pending decisions count
curl -s "https://api.dealix.me/api/v1/approvals/pending?customer_handle=acme-real-estate" \
  -H "Authorization: Bearer $FOUNDER_TOKEN" | jq 'length'

# 2. Approve one (test)
curl -s -X POST "https://api.dealix.me/api/v1/approvals/<id>/approve" \
  -H "Authorization: Bearer $FOUNDER_TOKEN" | jq

# 3. Verify it left pending
curl -s "https://api.dealix.me/api/v1/approvals/pending?customer_handle=acme-real-estate" \
  -H "Authorization: Bearer $FOUNDER_TOKEN" | jq 'length'  # should be N-1

# 4. Verify audit trail
curl -s "https://api.dealix.me/api/v1/audit/<correlation_id>" -H "Authorization: Bearer $FOUNDER_TOKEN" | jq
```

---

## Founder daily ritual (per `V14_FOUNDER_DAILY_OPS.md`)

Morning (≤45 min):
1. Open `/decisions.html?org=&access=<founder_token>` (master token sees all customers)
2. Approve / reject yesterday's queue
3. New decisions for today appear during the day

Evening (≤15 min):
1. Mark today's decisions complete
2. Queue tomorrow's voice notes for active customers

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `/decisions.html` shows nothing | Token wrong | Use master `dealix-founder-2026` to debug |
| Approval succeeds but message doesn't send | `safe_send_gateway` blocked | Check `audit_log` for block reason (likely consent_record_id missing) |
| WhatsApp Decision Bot returns "unauthorized" | Sender phone mismatch | Verify Sami's number matches `FOUNDER_PHONE` env var |
| Same approval shown 2x | DB race condition | Refresh page; check `approval_id` uniqueness |
| Approval expires before founder reviews | Default 7-day expiry | Sami runs `POST /api/v1/approvals/expire-sweep` to clear, then re-route work |

---

## Hard rules (immutable in code)

- ❌ Customer NEVER directly approves — only founder can
- ❌ NO_LIVE_SEND respected — `safe_send_gateway` blocks outbound on any gate failure
- ❌ NO bulk-approve (`bulk_approve` requires explicit founder confirmation per approval batch)
- ❌ NO automated re-approval — every approval is human-in-the-loop
- ✅ Every approve/reject has `correlation_id` in audit log
- ✅ Approval expiry sweeps run nightly (default 7-day max)
- ✅ Bilingual draft text (Saudi-Arabic primary, English secondary)

---

## Per-channel approval rules (Wave 4 §22.5.5)

| Channel | Approval requirement |
|---|---|
| WhatsApp | ALWAYS founder approval; never auto-send |
| Email (transactional) | Auto-approve if risk_level ≤ low; founder approves anything else |
| Email (marketing) | ALWAYS founder approval; consent_record_id required |
| LinkedIn | BLOCKED entirely (NO_LINKEDIN_AUTO) |
| SMS | ALWAYS founder approval (NEW channel — minimal volume) |
| Phone calls | NOT_AUTOMATED — founder makes calls personally |

---

## What's deferred to Wave 8

- Multi-approver workflows (founder + CSM both approve high-value actions)
- Approval delegation rules (when CSM hired)
- Approval analytics dashboard (rejection rate by source/agent)
- Slack / email digest of pending decisions (currently dashboard-only)
