# WhatsApp Business Integration — Canonical Setup & Transition Guide

**Canonical production target:** Meta WhatsApp Business Platform / Cloud API  
**Current transition transport:** GREEN-API, bounded and reversible  
**Current send posture:** fail-closed; `WHATSAPP_ALLOW_LIVE_SEND=false` until durable consent/suppression and exact cutover authority are proven  
**Canonical inbound owner:** `api/routers/webhooks.py`  
**Canonical Meta client:** `integrations/whatsapp.py`  
**Transition adapter:** `integrations/green_api.py`  
**Governed outbound adapter:** `auto_client_acquisition/email/whatsapp_multi_provider.py`

> Transport is not authority. A configured number, API token, public phone, or
> successful webhook never proves consent, buyer intent, commercial authority,
> or permission to send.

---

## 1. Architecture law

Dealix keeps one WhatsApp business pipeline regardless of transport:

```text
WhatsApp user
    |
    +-- GREEN-API webhook (transition) --> /api/v1/webhooks/green-api
    |
    +-- Meta Cloud webhook (canonical) --> /api/v1/webhooks/whatsapp
                                           |
                                           v
                                 canonical Dealix intake
                                           |
                           Company Brain / Opportunity Graph
                                           |
                            consent + suppression + policy
                                           |
                              approval / response drafting
                                           |
                            governed outbound transport
```

GREEN-API is **not** a second CRM, second conversation truth store, second
Company Brain, or second consent authority.

---

## 2. Phase A — GREEN-API transition

Use this only to establish inbound continuity and prove the end-to-end Dealix
conversation path while Meta activation is being completed.

### A1. Authorize the existing instance

Current known instance:

```text
7107600008
```

In GREEN-API Console:

1. Open the instance.
2. Open **QR / Authorize**.
3. On the phone: WhatsApp or WhatsApp Business → **Linked devices**.
4. Scan the QR shown by GREEN-API.
5. Wait until instance state is authorized/connected.

Do not paste the instance token into chat, GitHub, tickets, or documentation.

### A2. Deploy the Dealix webhook code first

The transition webhook endpoint is:

```text
POST https://api.dealix.me/api/v1/webhooks/green-api
```

The endpoint is intentionally fail-closed in staging/production unless
`GREEN_API_WEBHOOK_TOKEN` is present.

### A3. Configure GREEN-API webhook security

Generate an **independent** random webhook token. Do not reuse the GREEN-API API
token.

Set in the Dealix runtime secret store:

```text
GREEN_API_INSTANCE_ID
GREEN_API_TOKEN
GREEN_API_WEBHOOK_TOKEN
WHATSAPP_PROVIDER_PREFERENCE=green_api
```

Keep:

```text
WHATSAPP_ALLOW_LIVE_SEND=false
```

In GREEN-API instance settings configure:

```text
webhookUrl=https://api.dealix.me/api/v1/webhooks/green-api
webhookUrlToken=<same independent webhook token>
incomingWebhook=yes
stateWebhook=yes
```

Use Bearer authorization for the Webhook URL Token. Dealix also binds incoming
payloads to the configured `GREEN_API_INSTANCE_ID` and ignores group chats for
customer intake.

### A4. Transition acceptance

Prove, without enabling outbound:

```text
instance connected
webhook authenticated
wrong token -> 403
wrong instance -> 403
state event -> accepted but no lead
individual inbound text -> exactly one canonical intake path
provider metadata retained as intake metadata
group message -> ignored
WHATSAPP_ALLOW_LIVE_SEND=false
```

Webhook retries can happen. Provider message IDs are captured in intake
metadata; durable provider-event idempotency remains a separate hardening item
and must not be falsely claimed as proven until persisted.

---

## 3. Phase B — Meta WhatsApp Business Platform activation

Meta is the long-term official production transport.

### B1. Business identity

Use the legal Saudi business identity for verification and keep the public
Dealix brand/display identity evidence-backed. Do not invent or alter legal
information to match the brand.

Prepare in Meta Business settings:

- business portfolio / legal business details;
- required business verification evidence when requested;
- WhatsApp Business Account (WABA);
- a **dedicated Dealix business number** as the preferred production sender.

Do not migrate the founder's personal number merely to simplify setup. If Meta
explicitly offers a supported coexistence path for the exact number/account in
the live UI, treat that as a separate migration decision with rollback proof.

### B2. Meta application and WhatsApp assets

Create or use the Meta business application that owns the WhatsApp product and
record these values directly in the secret store, never in GitHub or chat:

```text
WHATSAPP_PHONE_NUMBER_ID
WHATSAPP_BUSINESS_ACCOUNT_ID
WHATSAPP_ACCESS_TOKEN
WHATSAPP_APP_SECRET
WHATSAPP_VERIFY_TOKEN
```

`WHATSAPP_VERIFY_TOKEN` should be independently generated by Dealix. The app
secret is used for `X-Hub-Signature-256` verification on production webhooks.

### B3. Canonical Meta webhook

Configure Meta callback URL:

```text
https://api.dealix.me/api/v1/webhooks/whatsapp
```

Use the same value as `WHATSAPP_VERIFY_TOKEN` for verification and subscribe to
message events required by the production flow.

Acceptance must prove both:

1. GET verification challenge succeeds only with the correct verify token.
2. POST webhook signature verification rejects invalid/missing signatures in
   production and accepts a valid Meta signature.

### B4. Templates and conversation policy

Create only templates that map to a real, consented business purpose. Keep
marketing, utility, authentication, and customer-service semantics distinct.

A template approval is **not** consent. A phone number is **not** consent.

---

## 4. Phase C — Controlled cutover Green → Meta

Never dual-send the same message through both providers.

### C1. Pre-cutover

Require current evidence for:

```text
Meta WABA active
Meta phone number active
Meta webhook accepted
Meta signature verification PASS
Meta inbound canary PASS
required templates approved where applicable
durable consent backend PASS
durable suppression backend PASS
opt-out path PASS
audit path PASS
rate limits / quiet hours PASS
rollback reference captured
```

### C2. Provider selection

Outbound selection is explicit:

```text
WHATSAPP_PROVIDER_PREFERENCE=green_api   # transition
WHATSAPP_PROVIDER_PREFERENCE=meta_cloud  # canonical cutover
```

`auto` is official-first: if Meta credentials are configured, Meta is the only
automatic transport attempted. Dealix will **not** silently fall back from a
Meta error to GREEN-API because doing so could bypass official template/window
or policy semantics.

### C3. Live-send authority

Do not enable:

```text
WHATSAPP_ALLOW_LIVE_SEND=true
```

until the controlled-live verifier proves durable channel-purpose consent,
suppression/withdrawal, recipient eligibility, approval authority, and every
other required outbound gate. This remains independent from provider cutover.

### C4. Rollback

If Meta inbound fails after cutover:

- keep outbound fail-closed;
- restore the previously accepted provider preference only under an exact
  rollback action;
- never send the same queued message twice;
- reconcile provider delivery status before retrying.

Once Meta is stable and rollback evidence is no longer required, de-authorize or
retire the GREEN-API WhatsApp session rather than leaving an unnecessary linked
device active indefinitely.

---

## 5. Security requirements

- Never store API tokens in repository files, chat, screenshots, or proof logs.
- Use an independent `GREEN_API_WEBHOOK_TOKEN`; do not reuse `GREEN_API_TOKEN`.
- Meta production webhooks require valid `X-Hub-Signature-256` when app secret
  is configured.
- GREEN-API production webhooks require Bearer authorization and configured
  instance binding.
- Prefer provider-side IP/network restrictions where available, in addition to
  application authentication.
- Keep raw message content out of security receipts unless a customer-data
  purpose explicitly requires it.
- Treat webhook retries as normal; persistent idempotency must be independently
  proven before claiming exact-once processing.

---

## 6. Consent, PDPL, and opt-out hard gate

Canonical issue: **#1533 — durable channel-purpose consent evidence**.

Controlled-live is not ready while consent is process-memory only.

The durable authority must preserve at minimum:

```text
normalized recipient
channel
purpose
consent state
consent timestamp
source + evidence reference
withdrawal timestamp + source
tenant/account/contact linkage
created/updated timestamps
```

Invariants:

- consent for one purpose does not authorize another purpose;
- withdrawal blocks controlled-live eligibility without undue delay;
- re-consent never silently clears an independent suppression record;
- public business contact != WhatsApp opt-in;
- research != relationship;
- draft != sent;
- no cold WhatsApp.

---

## 7. Verification matrix

| Gate | GREEN transition | Meta canonical |
|---|---:|---:|
| Provider connected | required | required |
| Authenticated inbound webhook | required | required |
| Instance/app binding | instance ID | app signature |
| Canonical Dealix intake | same | same |
| Provider metadata | required | required |
| Durable consent | required before live outbound | required before live outbound |
| Suppression/opt-out | required | required |
| Live send flag | OFF during transition acceptance | OFF until controlled-live PASS |
| Exact send audit | required before controlled-live | required before controlled-live |
| Rollback | GREEN session | accepted prior state |

---

## 8. Troubleshooting

| Symptom | Likely cause | Correct action |
|---|---|---|
| GREEN instance `Not Authorized` | phone session not linked | authorize via Linked Devices / QR |
| GREEN webhook 403 | wrong Bearer token or instance ID | reconcile secret + instance settings; do not weaken endpoint |
| GREEN webhook 503 in production | webhook token missing | configure secret before enabling webhook |
| Meta GET verification 403 | verify token mismatch | reconcile `WHATSAPP_VERIFY_TOKEN` |
| Meta POST webhook 403 | missing/invalid app signature | reconcile app secret/signature; never bypass |
| Draft generated but send blocked | policy/consent/approval gate | inspect block reason; do not force transport |
| Meta send fails while Green works | Meta policy/template/window/config issue | surface Meta error; do not silently fall back |
| Duplicate inbound processing | provider retry + missing durable idempotency | preserve message ID and close durable idempotency gap before exact-once claim |

---

## 9. Definition of Done

WhatsApp is production-ready only when all are true:

```text
META_OFFICIAL_TRANSPORT=PASS
META_WEBHOOK_SIGNATURE=PASS
INBOUND_CANARY=PASS
DURABLE_CONSENT=PASS
DURABLE_SUPPRESSION=PASS
OPT_OUT=PASS
APPROVAL_AUTHORITY=PASS
AUDIT=PASS
RATE_LIMITS=PASS
NO_COLD_WHATSAPP=PASS
ROLLBACK=PASS
```

A connected GREEN-API instance, a verified Meta number, or an HTTP 200 alone is
not Production Green.
