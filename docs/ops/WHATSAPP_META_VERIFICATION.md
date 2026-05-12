# WhatsApp Business — Meta Verification & Live-Send Activation

> Until verification completes, Dealix uses the multi-provider fallback chain (Green API → Ultramsg → Fonnte) in `WHATSAPP_MOCK_MODE=staging`. This document moves us to **Meta Cloud API in production**.

## Owner: Ops + Founder. Window: 2–4 weeks (Meta is slower than Moyasar).

---

## Phase 1 — Pre-requisites (T-28 → T-21)

- [ ] **1.1** Facebook Business Manager account: https://business.facebook.com
  - Owner: founder business account
  - Business name: matches CR exactly
  - Tax ID: same VAT number as Moyasar
- [ ] **1.2** Meta Business Verification submitted:
  - Upload CR (Saudi commercial registration)
  - Upload utility bill / national address
  - Upload bank statement < 90 days old
  - Time: 1–7 business days for Meta review
- [ ] **1.3** WhatsApp Business Account (WABA) created inside Business Manager
- [ ] **1.4** Phone number selected (must NOT have an active personal WhatsApp on it). Recommended: dedicated business number.

## Phase 2 — App + token setup (T-21 → T-14)

- [ ] **2.1** Create Meta App: https://developers.facebook.com/apps → WhatsApp Business
- [ ] **2.2** From App Dashboard, copy:
  - `WHATSAPP_VERIFY_TOKEN` — invent a random string (used by Meta to verify webhook URL ownership)
  - `WHATSAPP_APP_SECRET` — from App Settings → Basic
  - `WHATSAPP_ACCESS_TOKEN` — System User permanent token from Business Manager → System Users
  - `WHATSAPP_PHONE_NUMBER_ID` — from WhatsApp → API Setup
- [ ] **2.3** Store all four in 1Password and push to Railway env:
  ```env
  WHATSAPP_VERIFY_TOKEN=<random>
  WHATSAPP_APP_SECRET=<from-meta>
  WHATSAPP_ACCESS_TOKEN=<permanent-token>
  WHATSAPP_PHONE_NUMBER_ID=<numeric-id>
  META_APP_SECRET=<same-as-WHATSAPP_APP_SECRET>
  ```

## Phase 3 — Webhook registration (T-14 → T-10)

- [ ] **3.1** In Meta App Dashboard → WhatsApp → Configuration:
  - Callback URL: `https://api.dealix.me/api/v1/webhooks/whatsapp`
  - Verify Token: paste `WHATSAPP_VERIFY_TOKEN` exactly
  - Click **Verify and Save** — Meta calls our endpoint with `hub.mode=subscribe` and expects 200 + echo of `hub.challenge`
- [ ] **3.2** Subscribe to events:
  - `messages` (inbound)
  - `message_deliveries` (delivery receipts)
  - `message_reads` (read receipts)
- [ ] **3.3** Test inbound: from a personal WhatsApp, send a message to the business number → expect 200 in our logs + `webhook_received source=whatsapp signature_valid=true`.

## Phase 4 — Message templates (T-10 → T-7)

WhatsApp blocks free-form outbound messages to numbers that haven't opted in within 24 hours. For initial outreach we **must** use approved templates.

Submit these templates via Meta dashboard (Arabic + English; turnaround 24h–7d):

- [ ] **4.1** `dealix_intro_ar` — initial cold reach (Arabic). Limit: ≤ 1024 chars. Variables: `{{1}} = اسم العميل`, `{{2}} = اسم الشركة`.
- [ ] **4.2** `dealix_demo_followup_ar` — after demo. Variables: `{{1}} = أول اسم`, `{{2}} = موعد المتابعة`.
- [ ] **4.3** `dealix_pilot_invite_ar` — pilot offer (1 SAR). Variables: `{{1}} = أول اسم`, `{{2}} = checkout URL`.
- [ ] **4.4** `dealix_pilot_confirmation_ar` — post-payment. Variables: `{{1}} = أول اسم`, `{{2}} = onboarding URL`.
- [ ] **4.5** `dealix_intro_en` — English fallback.
- [ ] **4.6** `dealix_alert_oncall` — internal alerting from monitoring. Variables: `{{1}} = monitor`, `{{2}} = url`.

All templates must comply with Meta's Business Policy and Saudi PDPL (no false urgency, clear opt-out, no medical/financial claims without licensing).

## Phase 5 — Internal policy sign-off (T-7 → T-5)

- [ ] **5.1** Internal WhatsApp Outbound Policy written (`docs/ops/WHATSAPP_OUTBOUND_POLICY.md` — separate doc):
  - Sender identification ("Dealix")
  - Opt-out instructions in every message ("رد بـ ALGI لإيقاف")
  - PDPL consent recorded in DB before any outbound
  - Quiet hours: 09:00–21:00 AST only
  - Daily limit per number: 250 in initial 30 days (Meta will throttle)
- [ ] **5.2** Founder signs the policy (signature recorded in `docs/ops/POLICY_SIGNATURES.md`).
- [ ] **5.3** Set Railway env:
  ```env
  WHATSAPP_ALLOW_LIVE_SEND=true
  WHATSAPP_PROVIDER=meta_cloud
  WHATSAPP_MOCK_MODE=false
  ```

## Phase 6 — End-to-end live test (T-5 → T-3)

- [ ] **6.1** Send `dealix_intro_ar` template to a friendly test number. Verify:
  - Message delivered (Meta dashboard + delivery webhook)
  - PostHog event `whatsapp_sent { template, recipient_hash }` fires
- [ ] **6.2** Have the recipient reply → verify inbound webhook delivers to `/api/v1/webhooks/whatsapp` with `signature_valid=true`.
- [ ] **6.3** Recipient sends `ALGI` → verify our opt-out handler adds them to `data_suppression_list`.
- [ ] **6.4** Attempt a second send → should be **blocked** by the suppression list (test the safety).

## Phase 7 — GA cutover

- [ ] **7.1** Confirm `WHATSAPP_ALLOW_LIVE_SEND=true` in Railway production.
- [ ] **7.2** Update `docs/ops/POST_LAUNCH_BACKLOG.md` — strike WhatsApp items.
- [ ] **7.3** Schedule daily 09:00 batch via `dealix_whatsapp_morning_brief.py` (existing script).
- [ ] **7.4** Set Sentry alerts:
  - `whatsapp_send_failed` rate > 5% in 10 minutes → SEV-2
  - `webhook_received source=whatsapp signature_valid=false` (>3 in 5 min) → SEV-2

## Phase 8 — Ongoing

- [ ] **8.1** Weekly: review delivery + opt-out rates in PostHog. Opt-out rate > 5% = template needs rework.
- [ ] **8.2** Monthly: confirm Meta business verification still active.
- [ ] **8.3** Quarterly: rotate `WHATSAPP_APP_SECRET` (per `docs/security/KEY_ROTATION.md`).
- [ ] **8.4** Annual: review template content for PDPL + Meta policy drift.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Webhook verify keeps failing on save | Mismatched `WHATSAPP_VERIFY_TOKEN` | Re-paste the exact value from Railway into Meta dashboard |
| Inbound webhook returns 200 but signature invalid | `WHATSAPP_APP_SECRET` mismatch | Re-copy from Meta App Settings → Basic → Show |
| Template send returns 400 `pair_not_found` | Template not yet approved | Wait; or use a non-template message to a 24h-opted-in number |
| Send returns 131056 (limit reached) | Meta throttle for new business | Backoff + reduce daily volume; ramp up over 30 days |
| Mass opt-outs | Bad copy or list quality | Pause sends; review template + segmentation |
