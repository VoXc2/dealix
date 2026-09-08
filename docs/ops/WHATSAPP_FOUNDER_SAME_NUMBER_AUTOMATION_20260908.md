# Dealix Founder Same-Number WhatsApp Automation

Date: 2026-09-08
Owner: `dealix-engineer` + `dealix-sales`
Canonical transport owner: PR #1564
Canonical consent authority: merged PR #1565

## Executive decision

Launch Dealix WhatsApp using the founder's existing working number first, without creating a second CRM, inbox, consent system, scheduler, Company Brain, or agent fleet.

The founder number is treated as the **Founder Business Line**. The customer-facing identity remains founder-led while Dealix operates the research, triage, qualification, diagnostic, reply drafting, negotiation analysis, follow-up planning, handoff, proof, and learning layers internally.

## Launch mode

The immediate same-number path is:

```text
Founder WhatsApp Business App
        |
        | Linked Devices / QR
        v
GREEN-API bounded transition session
        |
        | authenticated webhook
        v
/api/v1/webhooks/green-api
        |
        v
canonical Dealix WhatsApp intake
        |
        +-> identity / company resolution
        +-> consent + suppression check
        +-> opportunity state
        +-> AI triage / qualification
        +-> diagnostic drafting
        +-> negotiation analysis
        +-> approval card / founder handoff
        +-> proof + learning
```

Meta WhatsApp Business Platform / Cloud API remains the canonical long-term API transport. If the actual Meta onboarding flow for this exact number explicitly offers an approved same-number coexistence path, Dealix may later cut over to that official path under a separate exact production action. Do not assume coexistence support from documentation or another provider; prove it in the actual Meta account flow before changing the number registration.

## Important provider constraint

Do not migrate the founder number to Twilio if the requirement is to keep using the WhatsApp Business App with that same number. Twilio's current migration documentation says an app-registered number must be removed from the app before becoming a Twilio WhatsApp Business Platform sender, and the app can no longer continue using that same number.

Therefore:

- **same number + phone app now:** GREEN linked-device transition, inbound-first;
- **same number + official API later:** only if the actual Meta onboarding flow proves an eligible coexistence path;
- **Twilio migration:** not the launch path for this founder same-number requirement.

## Identity contract

No personal phone number is committed to Git.

Runtime identity is provided only through approved runtime configuration:

```text
DEALIX_FOUNDER_WHATSAPP_E164
DEALIX_WHATSAPP_IDENTITY_MODE=founder_same_number
```

The number value must never be printed in public logs, GitHub comments, screenshots, or model prompts unless the founder intentionally provides it for a specific action.

## Automation boundary

### Automatic after authenticated inbound

Dealix may automatically:

1. accept and normalize authenticated direct-message events;
2. ignore groups and broadcasts;
3. resolve existing contact/account context;
4. create or update internal conversation/opportunity context;
5. classify intent and urgency;
6. detect opt-out / suppression language;
7. evaluate tenant + recipient + channel + purpose consent state;
8. research the company from allowed sources;
9. build WHY THEM / WHY NOW / evidence / unknowns;
10. score the opportunity;
11. create a Free Execution Diagnostic draft;
12. draft Arabic/English replies in Founder Office voice;
13. prepare discovery questions;
14. prepare objection handling and negotiation options;
15. prepare meeting / proposal / catalog handoff;
16. create Approval Cards for material replies;
17. update proof and learning records.

### External effect boundary

The transport being connected does **not** create send authority.

The following remain fail-closed unless the exact action is authorized and the existing policy gate passes:

- first proactive WhatsApp message;
- commercial counteroffer;
- binding scope/price/timeline/payment term;
- template-initiated marketing message;
- cold contact;
- bulk/broadcast send;
- payment request;
- public claim/publication.

`WHATSAPP_ALLOW_LIVE_SEND=false` remains the default launch posture.

## Consent and suppression

PR #1565 is now the single durable authority. Required identity is:

```text
tenant_scope + normalized recipient + channel + purpose
```

Rules:

- `PUBLIC_PHONE != CONSENT`
- relationship does not imply purpose-specific consent;
- consent on email does not imply WhatsApp consent;
- opt-out / suppression overrides scoring, urgency, model advice, and commercial value;
- withdrawal fails closed;
- suppression remains independent from consent;
- provider configuration never creates consent.

## Founder same-number workflow

```text
WA_F01_AUTHENTICATED_INBOUND
-> WA_F02_IDENTITY_RESOLUTION
-> WA_F03_CONSENT_SUPPRESSION_STATE
-> WA_F04_INTENT_AND_OPPORTUNITY
-> WA_F05_ACCOUNT_RESEARCH
-> WA_F06_DIAGNOSTIC_DRAFT
-> WA_F07_FOUNDER_REPLY_DRAFT
-> WA_F08_NEGOTIATION_ANALYSIS
-> WA_F09_APPROVAL_OR_HANDOFF
-> WA_F10_CONTROLLED_SEND_IF_EXACTLY_AUTHORIZED
-> WA_F11_DELIVERY_REPLY_RECEIPT
-> WA_F12_PROOF_LEARNING
```

These are workflow labels only; they do not create new truth stores.

## One-time activation sequence

### A. Phone / GREEN linked-device action

Founder action on the actual phone:

1. Ensure the working number is active in WhatsApp Business App.
2. Open **Settings -> Linked Devices -> Link a Device**.
3. In GREEN-API for the existing Dealix instance, open the authorization QR.
4. Scan the QR from the founder phone.
5. Confirm the GREEN instance reports authorized/connected.

This phone/QR action cannot be performed from the repository or VPS.

### B. Secret configuration

Store values only in the approved production secret store; never paste values into Git:

```text
GREEN_API_INSTANCE_ID
GREEN_API_TOKEN
GREEN_API_WEBHOOK_TOKEN
DEALIX_FOUNDER_WHATSAPP_E164
WHATSAPP_PROVIDER_PREFERENCE
WHATSAPP_ALLOW_LIVE_SEND
```

Initial posture:

```text
DEALIX_WHATSAPP_IDENTITY_MODE=founder_same_number
WHATSAPP_PROVIDER_PREFERENCE=green_api
WHATSAPP_ALLOW_LIVE_SEND=false
```

### C. Inbound acceptance

Before outbound is considered:

- authenticated direct inbound accepted;
- wrong webhook token rejected;
- wrong GREEN instance rejected;
- group/broadcast rejected;
- inbound reaches canonical Dealix intake;
- opportunity/contact context is updated internally;
- response is drafted, not silently sent;
- opt-out becomes durable suppression;
- no duplicate send path exists.

### D. Controlled external pilot

Only after exact authority for the concrete test action:

- use founder/controlled consenting recipient;
- one message only;
- prove policy gate decision;
- prove provider receipt;
- prove reply ingestion;
- prove suppression on opt-out;
- record proof.

## Meta cutover later

When the actual Meta account is ready:

1. reconcile existing Meta Business Portfolio/WABA/app assets;
2. inspect whether the exact founder number is offered an official coexistence onboarding path;
3. if coexistence is offered, complete official onboarding and signed webhook acceptance;
4. if not offered, do **not** delete or migrate the founder app account merely to force API activation;
5. keep the founder line on the current transition path until a dedicated API number or explicitly acceptable migration decision exists;
6. cut `WHATSAPP_PROVIDER_PREFERENCE=meta_cloud` only after exact production acceptance;
7. retire GREEN after the rollback window.

## Definition of Done for launch phase

```text
FOUNDER_NUMBER_REMAINS_ON_PHONE=true
AUTHENTICATED_INBOUND_AUTOMATION=PASS
CANONICAL_DEALIX_INTAKE=PASS
DURABLE_CONSENT_AUTHORITY=MERGED
DURABLE_SUPPRESSION=PASS
AI_TRIAGE=READY
DIAGNOSTIC_DRAFTING=READY
FOUNDER_REPLY_DRAFTING=READY
NEGOTIATION_ANALYSIS=READY
APPROVAL_HANDOFF=READY
COLD_WHATSAPP=BLOCKED
BULK_WHATSAPP=BLOCKED
LIVE_SEND_DEFAULT=false
```

## Truth firewall

`research != relationship`

`public contact != consent`

`provider connected != send authority`

`draft != sent`

`quote != invoice`

`invoice != payment`

`HTTP 200 != Production Green`

`technical automation != customer permission`
