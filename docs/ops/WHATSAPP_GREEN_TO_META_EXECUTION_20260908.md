# Dealix WhatsApp — GREEN-API → Meta Canonical Execution Runbook

Date: 2026-09-08  
Timezone: Asia/Riyadh  
North Star: `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

## Executive objective

Establish a secure, governed WhatsApp inbound channel immediately through the
existing GREEN-API instance, then migrate to the official Meta WhatsApp
Business Platform without creating a second CRM, Brain, Opportunity Graph,
consent authority, or agent fleet.

Final topology:

```text
Meta WhatsApp Business Platform
        |
        v
api.dealix.me/api/v1/webhooks/whatsapp
        |
        v
Canonical Dealix WhatsApp Intake
        |
        +--> Company Brain / account context
        +--> Opportunity Graph / qualification
        +--> HubSpot mirror where canonical workflow already requires it
        +--> dealix-sales / dealix-delivery
        +--> diagnostic / proposal / proof preparation
        |
        v
Consent + Suppression + Approval + Audit
        |
        v
Meta Cloud API outbound
```

During transition only:

```text
WhatsApp App/Business App --Linked Device--> GREEN-API
                                      |
                                      v
                  /api/v1/webhooks/green-api
                                      |
                                      v
                         SAME canonical intake
```

## Non-negotiable laws

1. `research != relationship`
2. `public contact != consent`
3. `draft != sent`
4. `quote != invoice`
5. `invoice != payment`
6. GREEN-API or Meta connectivity never grants outbound authority.
7. No cold WhatsApp.
8. No dual-send across Green and Meta.
9. No raw secrets in GitHub, chat, proof receipts, or screenshots.
10. Exactly five permanent agents remain canonical.

---

# Wave 0 — Live truth and source readiness

## Current source owner

Branch created for this bounded transition:

```text
feat/whatsapp-green-to-meta-transition-20260908
```

The branch must remain Draft/isolated until exact-head source acceptance is
proven against the then-current `main`.

## Source changes in this lane

- secure GREEN-API inbound parser/adapter;
- authenticated `/api/v1/webhooks/green-api` endpoint;
- shared Meta/Green canonical intake path;
- Meta official-first outbound provider selection;
- canonical Meta env names with temporary legacy compatibility;
- no silent Meta → unofficial fallback;
- environment contract documentation;
- parser/provider regression tests;
- this execution runbook.

## Source acceptance

At minimum run on the exact PR integration candidate:

```text
git diff --check
pytest tests/unit/test_green_api_webhook.py
pytest tests/unit/test_full_os_smoke.py
existing WhatsApp/policy/controlled-live tests
scripts/ops/verify_controlled_live_readiness.py
```

Expected controlled-live result before #1533 closure:

```text
CONTROLLED_LIVE_READINESS=NOT_READY
```

That is correct while durable consent is not proven.

---

# Wave 1 — GREEN-API inbound continuity

## Human-required action: authorize instance

Known instance:

```text
7107600008
```

In GREEN-API Console:

1. open instance `7107600008`;
2. choose QR/Authorize;
3. on the phone open WhatsApp/WhatsApp Business → Linked devices;
4. scan QR;
5. wait for connected/authorized state.

This is a physical-account action and cannot be safely automated by Dealix.

## Deployment prerequisites

Do not point GREEN-API at the new endpoint until the accepted source is actually
deployed to the canonical API service.

L5 packet required for production mutation must bind:

```text
accepted source SHA
current main SHA
current API release SHA
rollback API deployment
exact new Railway secret names
exact provider preference
outbound remains OFF
```

## Production variables — transition

Values must be entered directly into the Railway/API secret store:

```text
GREEN_API_INSTANCE_ID=7107600008
GREEN_API_TOKEN=<secret>
GREEN_API_WEBHOOK_TOKEN=<new independent secret>
WHATSAPP_PROVIDER_PREFERENCE=green_api
WHATSAPP_ALLOW_LIVE_SEND=false
```

Never reuse `GREEN_API_TOKEN` as the webhook token.

## GREEN-API instance settings

After the new API release is healthy:

```text
webhookUrl=https://api.dealix.me/api/v1/webhooks/green-api
webhookUrlToken=<same independent webhook token>
incomingWebhook=yes
stateWebhook=yes
```

Recommended additional transition posture:

- keep outgoing API actions disabled by Dealix policy;
- keep group traffic out of canonical customer intake;
- keep the phone online/healthy while using the linked-device transport;
- use provider-side IP/network restrictions where available;
- avoid unnecessary linked devices.

## GREEN acceptance canaries

### Security canary

- request with no/incorrect Authorization → 403;
- request with correct Authorization but wrong instance ID → 403;
- production runtime without `GREEN_API_WEBHOOK_TOKEN` → 503.

### Event canary

- state/outgoing/status event → 200, zero leads;
- direct inbound text → one canonical intake path;
- direct extended text → one canonical intake path;
- group message → zero leads.

### Business canary

From a consented internal test number, send:

```text
اختبار Dealix WhatsApp inbound
```

Verify:

```text
webhook received
provider=green_api
canonical lead/intake created
no outbound generated automatically
no payment/quote/contract authority created
```

---

# Wave 2 — Canonical conversation processing

GREEN and Meta must converge before business logic.

Canonical normalization fields:

```text
phone
contact_name
text
provider
provider_message_id
```

Then the existing acquisition pipeline remains owner of normalization and
commercial intake.

## Required follow-on hardening

Webhook providers retry. Provider message ID is preserved now, but durable
exact-once/idempotency must be persisted before Dealix claims exactly-once
customer processing.

Required design:

```text
provider
provider_account_or_instance
provider_message_id
received_at
payload_fingerprint
processing_status
canonical_entity_id
```

with a durable uniqueness boundary on provider/account/message ID.

Do not create a new CRM to solve this; extend the existing durable event/audit
model under its canonical owner.

---

# Wave 3 — Consent and suppression (#1533)

This wave is mandatory before controlled-live outbound.

## Durable channel-purpose consent

Persist:

```text
normalized recipient
channel=whatsapp
purpose
state=granted|withdrawn
granted_at
granted_source
evidence_reference
withdrawn_at
withdrawn_source
tenant/account/contact linkage
created_at
updated_at
```

## Independent suppression

Suppression remains independent from consent.

```text
re-consent != suppression removal
```

## Required WhatsApp state

Each recipient should be able to resolve to:

```text
PHONE_FOUND
RELATIONSHIP_STATE
WHATSAPP_OPT_IN
OPT_IN_PURPOSE
OPT_IN_SOURCE
OPT_IN_TIMESTAMP
SUPPRESSED
OPT_OUT_TIMESTAMP
LAST_INBOUND
CUSTOMER_SERVICE_WINDOW_STATE
SEND_ELIGIBLE
```

A public phone discovery should resolve to:

```text
PHONE_FOUND=true
WHATSAPP_SEND_ELIGIBLE=false
```

until the actual consent/relationship evidence exists.

---

# Wave 4 — Meta business activation

## Preferred identity structure

Use a dedicated Dealix business number for the canonical Meta sender.

Founder/personal number:

```text
high-value human escalation / warm / inbound
```

Dealix Meta number:

```text
official business automation / scale / templates / governed conversations
```

Do not migrate a personal founder number solely for implementation convenience.

## Meta Business setup

In live Meta Business Settings / WhatsApp Manager:

1. verify/select the correct business portfolio;
2. ensure legal business details match the evidence being submitted;
3. create or attach the correct WhatsApp Business Account (WABA);
4. add the dedicated Dealix business phone number;
5. complete the phone verification flow;
6. complete business verification requirements shown by Meta when applicable;
7. create/use the Meta application that owns the WhatsApp product;
8. configure appropriate system-user/application access;
9. collect IDs/tokens directly into the secret store.

Required runtime names:

```text
WHATSAPP_PHONE_NUMBER_ID
WHATSAPP_BUSINESS_ACCOUNT_ID
WHATSAPP_ACCESS_TOKEN
WHATSAPP_APP_SECRET
WHATSAPP_VERIFY_TOKEN
```

## Meta webhook

Callback:

```text
https://api.dealix.me/api/v1/webhooks/whatsapp
```

Production acceptance:

```text
GET challenge correct token -> PASS
GET challenge wrong token -> 403
POST valid X-Hub-Signature-256 -> PASS
POST bad/missing signature -> 403
inbound text -> same canonical intake as GREEN
```

---

# Wave 5 — Templates, diagnostics, files, and Founder Office

## Template governance

Maintain a registry with:

```text
template_name
Meta category
language
defined business purpose
consent basis required
approved status
last reviewed
owner
```

Do not treat approved template as permission to contact a person.

## Conversation response architecture

For an eligible/inbound conversation:

```text
message
  -> identity/account resolution
  -> current conversation context
  -> intent/classification
  -> account dossier
  -> problem hypothesis
  -> commercial authority check
  -> response draft
  -> consent/suppression/policy gate
  -> approval rule
  -> selected transport
  -> delivery receipt
  -> conversation/proof update
```

## Diagnostic asset flow

The agent may prepare:

```text
customer-specific Mini Diagnostic PDF
Dealix Capability Catalog
technical brief
commercial proposal draft
proof plan
```

But an attachment is sent only when the recipient and conversation are eligible
under the canonical outbound policy.

---

# Wave 6 — Meta cutover

## Pre-cutover evidence packet

Require:

```text
META_PHONE_ACTIVE=PASS
META_WABA_ACTIVE=PASS
META_WEBHOOK_VERIFY=PASS
META_WEBHOOK_SIGNATURE=PASS
META_INBOUND_CANARY=PASS
TEMPLATE_REGISTRY=PASS
DURABLE_CONSENT=PASS
DURABLE_SUPPRESSION=PASS
OPT_OUT=PASS
AUDIT=PASS
RATE_LIMITS=PASS
QUIET_HOURS=PASS
ROLLBACK=PASS
```

## Exact provider switch

Transition state:

```text
WHATSAPP_PROVIDER_PREFERENCE=green_api
```

Cutover state:

```text
WHATSAPP_PROVIDER_PREFERENCE=meta_cloud
```

Do not use `auto` as an implicit production change packet. For production
cutover use explicit `meta_cloud` so the evidence and rollback are unambiguous.

## No automatic unofficial fallback

Once Meta is selected, a Meta error is surfaced as a Meta error. Dealix does
not retry through GREEN-API automatically.

This prevents an official policy/template/window rejection from being bypassed
through a linked-device transport.

---

# Wave 7 — Controlled-live activation

Provider cutover and controlled-live are separate approvals.

Only after `verify_controlled_live_readiness.py` is genuinely READY should an
exact action packet consider enabling WhatsApp live send.

The packet must bind:

```text
consent backend + migration proof
suppression backend + migration proof
recipient eligibility policy
approval policy
rate limits
quiet hours
template policy
current Meta sender identity
current source/release SHA
rollback
```

Then, and only then, the exact environment mutation may set:

```text
WHATSAPP_ALLOW_LIVE_SEND=true
```

for the authorized scope.

No global cold-outbound permission is implied.

---

# Wave 8 — Observability and operational proof

Measure without leaking customer message bodies into unnecessary telemetry.

Minimum metrics:

```text
whatsapp_webhook_received_total{provider}
whatsapp_webhook_rejected_total{provider,reason}
whatsapp_inbound_processed_total{provider,type}
whatsapp_inbound_duplicate_total{provider}
whatsapp_send_attempt_total{provider}
whatsapp_send_blocked_total{reason}
whatsapp_send_success_total{provider}
whatsapp_send_failure_total{provider,reason}
whatsapp_opt_out_total
whatsapp_consent_withdrawal_total
whatsapp_handoff_total
```

Executive/business metrics:

```text
real interactions
qualified problems
diagnostics requested
discovery booked
quotes prepared
verified payments
outcome sprints
customer-validated proof
founder minutes per paid cycle
```

Never upgrade engagement/response counts into revenue evidence.

---

# Wave 9 — GREEN retirement

After Meta has remained stable through the accepted observation window:

1. confirm no required messages/events exist only in GREEN;
2. remove GREEN from active outbound preference;
3. disable GREEN webhooks;
4. de-authorize/logout linked WhatsApp device/session;
5. remove GREEN secrets from production secret store under exact secret-mutation
   authority;
6. retain only non-secret proof/rollback receipts needed for audit;
7. close the transition lane.

Target final posture:

```text
CANONICAL_PROVIDER=meta_cloud
GREEN_ACTIVE=false
UNOFFICIAL_FALLBACK=false
DURABLE_CONSENT=true
DURABLE_SUPPRESSION=true
NO_COLD_WHATSAPP=true
```

---

# Founder-only actions

Founder involvement should be limited to account/identity material actions:

1. scan GREEN QR from the actual phone;
2. enter/verify Meta legal/business identity where Meta requires human proof;
3. verify the dedicated Meta phone number;
4. enter secrets directly into the provider secret store;
5. approve exact production deploy/provider switch/controlled-live packets when
   they become current and evidence-backed.

Everything else should remain L0-L4 automation/repo execution where safe.

---

# Definition of complete

```text
GREEN_TRANSITION_INBOUND=PROVEN_OR_RETIRED
META_OFFICIAL_TRANSPORT=PASS
META_WEBHOOK=PASS
META_INBOUND=PASS
DURABLE_IDEMPOTENCY=PASS
DURABLE_CONSENT=PASS
DURABLE_SUPPRESSION=PASS
OPT_OUT=PASS
APPROVAL=PASS
AUDIT=PASS
CONTROLLED_LIVE=PASS
GREEN_RETIRED=PASS
CUSTOMER_FLOW=INBOUND_TO_DIAGNOSTIC_TO_DISCOVERY_PROVEN
```

Until all required gates are current, report the missing gate explicitly rather
than claiming WhatsApp production readiness.
