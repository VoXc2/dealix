# Dealix First Customer — Realistic Playbook

> Sales-led, no live external action, no live charge, no automation.
> Follow this exact script for the first 3 paying customers.

## STOP gate (P0) — do NOT start outreach until ALL pass

| # | Gate | How to verify |
| - | --- | --- |
| 1 | Operator Arabic cold-WA safety tests pass | `python -m pytest tests/test_operator_saudi_safety.py -q` → 28/28 |
| 2 | AsyncSession fix is on the deploy branch | this PR is merged into `claude/launch-command-center-6P4N0` |
| 3 | Railway redeploy is done | Railway dashboard → deployments → most recent commit matches HEAD |
| 4 | Staging smoke passes after redeploy | `BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh` → `PASS=36 FAIL=0` |

If any of the 4 fails, the verdict stays at `PROVEN_STAGING_READ_ONLY` and outreach must wait.

---

## Step 1 — Warm sources only

Allowed sources for first prospects:

- LinkedIn 1st-degree contacts (people who already follow you)
- referrals from friends / former colleagues
- inbound form submission on `landing/index.html`
- inbound `wa.me` link (the prospect messages YOU first)
- existing customer list with a written consent record

Not allowed:

- purchased phone lists
- scraped numbers / emails
- cold WhatsApp to anyone you don't have consent from
- LinkedIn automation tools / bots

---

## Step 2 — First message (Arabic, no spam)

Use this template:

> السلام عليكم، أنا سامي مؤسس Dealix — نظام نمو ذكي للسوق السعودي.
> شفت ملفك ومهتم أعرف إذا تواجهون تحدّي في المبيعات أو سرعة الرد على leads.
>
> ما عندي طلب الآن، فقط أبي أعرض عليك Free Diagnostic لمدة 20 دقيقة.
> النتيجة: 3 فرص نمو + توصية بقناة آمنة + Proof Pack مختصر.
>
> إذا مهتم، رد على هذه الرسالة ونرتب موعد. شكراً لوقتك.

NO guarantees. NO blanket "نضمن لك مبيعات". NO mention of bulk WhatsApp.

---

## Step 3 — Mini Diagnostic intake (Free Diagnostic bundle)

API call after the prospect agrees:

```bash
curl -X POST https://api.dealix.me/api/v1/operator/service/start \
  -H "Content-Type: application/json" \
  -d '{
    "bundle_id":"free_diagnostic",
    "company_name":"<company>",
    "website":"<url>",
    "sector":"<sector>",
    "city":"<city>",
    "offer":"<one-line offer>",
    "ideal_customer":"<icp>",
    "goal":"<goal>",
    "current_channels":"<channels>",
    "consent_status":"warm_inbound|consent_recorded|none"
  }'
```

If the prospect mentions a list, REQUIRE them to state source and consent
status before any draft is created.

---

## Step 4 — Mini Diagnostic output (≤ 24 hours)

Deliver as a 1-page Arabic doc:

```
1. Best starting segment + why
2. 3 specific opportunities (by company name if possible)
3. 1 ready Arabic message they can send manually
4. Recommended safe channel (LinkedIn manual / inbound wa.me / opt-in form)
5. 1 risk to avoid (compliance + spam)
6. Next step: 7-Day Growth Proof Sprint (Pilot 499 SAR)
```

Send manually via WhatsApp/email — Dealix does NOT auto-send the
diagnostic.

---

## Step 5 — Pilot 499 SAR (manual fallback)

```bash
# 1. Record the prospect as a lead
curl -X POST https://api.dealix.me/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name":"<contact>", "email":"<email>", "company":"<co>", "phone":"<+966...>",
    "source":"website|referral|linkedin", "sector":"<sector>"
  }'

# 2. Create a deal at pilot_offered
curl -X POST https://api.dealix.me/api/v1/deals \
  -H "Content-Type: application/json" \
  -d '{"lead_id":"<lead_id>", "value_sar":499, "stage":"pilot_offered"}'

# 3. Manual invoice — bank transfer / STC Pay (NO live charge)
curl -X POST https://api.dealix.me/api/v1/payments/manual-request \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"<deal_id>", "amount_sar":499}'
# → returns instruction text + follow_up_task_id

# Optional: if Moyasar invoice key is configured, the same endpoint
# can be wired to call Moyasar's invoices API. Amount in halalah:
#   499 SAR = 49900   (1 SAR = 100 halalah, integer required).
# Live CHARGE remains OFF; an invoice link is hosted by Moyasar and
# the customer pays voluntarily.
```

When the bank transfer arrives:

```bash
curl -X POST https://api.dealix.me/api/v1/payments/mark-paid \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"<deal_id>", "reference":"<bank-transfer-ref>"}'
# → returns customer_id + onboarding_task_id
```

---

## Step 6 — 7-Day delivery (Growth Starter)

| Day | Action | Output |
| --- | --- | --- |
| 1 | Intake follow-up | confirmed ICP + segment |
| 2 | Generate 10 opportunities | list (manual or via `/api/v1/leads/discover/local`) |
| 3 | Draft 6 messages | `/api/v1/personal-operator/messages/draft` |
| 4 | Risk review | `/api/v1/compliance/check-outreach` per draft |
| 5 | Generate 3 follow-ups | `/api/v1/personal-operator/followups/draft` |
| 6 | Run safe send (manual approval) | only after the customer reviews |
| 7 | Proof Pack | `/api/v1/customers/{id}/proof-pack` + `/api/v1/command-center/proof-pack` |

---

## Step 7 — Proof Pack (day 7)

The Proof Pack must explicitly contain:

- what was created (10 opps, 6 drafts, 3 follow-ups)
- what was protected (compliance blocks count, opt-out respected, no cold WA)
- revenue impact estimate (label clearly as "تقدير" / "estimate")
- next 7-day plan
- upgrade recommendation (Executive Growth OS — only if grade ≥ B)

Do NOT promote `executive_growth_os` until you have a signed proof pack
with measurable outcomes.

---

## Hard rules during the playbook

1. Never enable `WHATSAPP_ALLOW_LIVE_SEND=true`.
2. Never set `MOYASAR_SECRET_KEY` to a live key.
3. Never set `GMAIL_ALLOW_LIVE_SEND=true`.
4. Never use a LinkedIn automation tool.
5. Always require written consent before any direct WhatsApp message.
6. Always store consent in `ConsentRecord` (or in your CRM with a date).
7. If a prospect goes cold, stop — do NOT escalate frequency.
