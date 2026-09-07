# Dealix — PDPL Direct-Marketing Control Map

Date: 2026-09-06
Scope: Dealix outbound email / WhatsApp / SMS controlled-live eligibility.
North Star: `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

This is an engineering control map, not legal advice. It intentionally keeps
live outbound **blocked** where evidence is not yet durable.

## Authority reviewed

Saudi Personal Data Protection Law Implementing Regulation / SDAIA guidance:

- consent must be documented in a way that allows future verification;
- separate consent should be obtained for separate processing purposes;
- data subjects must be able to withdraw consent;
- processing based on consent must stop without undue delay after withdrawal;
- direct marketing requires sender identification and a simple mechanism to
  stop receiving marketing materials;
- marketing must stop without undue delay after withdrawal/objection.

Official portal:
https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL

## Dealix engineering mapping

| Requirement | Current source control | Current verdict |
| --- | --- | --- |
| Recipient/channel eligibility | `app.outbound.consent.has_consent` + contact flags | Draft-policy only |
| Durable consent evidence | `persistent_consent_ready()` | **HOLD — memory only** |
| Independent do-not-contact | `app.outbound.suppression` | Memory default; Postgres candidate in #1529 |
| Durable suppression | `persistent_suppression_ready()` | **HOLD until Postgres table + privileges proven** |
| Withdrawal / opt-out | contact opt-out flags + suppression authority | Fail-closed; durable consent migration pending |
| Unsubscribe/halt wording | email/SMS policy gate | Enforced |
| WhatsApp explicit opt-in | WhatsApp policy gate | Enforced |
| Approved WhatsApp template | WhatsApp policy gate | Enforced |
| Sender/action authority | `EXTERNAL_SEND_ENABLED`, controlled-live mode, channel flags | Fail-closed default |
| Message approval | `message.status == approved` | Enforced |
| Rate limiting | `app.outbound.rate_limiter` | Enforced |
| Truth/claims safety | blocked-claims gate | Enforced |

## New hard invariant in PR #1529

A recipient-level flag is not the same thing as durable consent evidence.
Therefore controlled-live now requires **both**:

```text
persistent_suppression_ready() == true
AND
persistent_consent_ready() == true
```

Even if every other channel flag is enabled, `safe_to_send` remains false while
either durability gate is unproven.

## Durable consent model required by #1533

The future canonical consent store must preserve at minimum:

- normalized recipient identifier;
- channel;
- processing/marketing purpose;
- granted / withdrawn state;
- grant timestamp;
- source and evidence reference;
- withdrawal timestamp and source;
- tenant/account/contact linkage where applicable;
- created/updated timestamps.

It must also guarantee:

1. consent for one purpose does not silently authorize another;
2. withdrawal immediately blocks eligibility;
3. withdrawal evidence is retained rather than deleted;
4. re-consent does **not** automatically remove an independent suppression
   record;
5. production readiness is read-only-verifiable before live activation.

## Channel posture

### Email

Dealix may use `verification_status=approved_to_send` as a **draft eligibility
signal** today. It is not treated as durable marketing-consent proof for
controlled-live. A future consent authority must record the appropriate lawful
basis/consent evidence before the live gate is eligible.

### WhatsApp

Keep official Business Platform, permissioned/inbound-first posture. Explicit
opt-in and approved template remain required for controlled outbound. Publicly
found phone numbers are not consent.

### SMS

Explicit consent + durable evidence + opt-out mechanism are required before
controlled-live eligibility.

## What this does not authorize

This document and PR #1529 do **not** authorize:

- cold WhatsApp;
- mass LinkedIn automation;
- scraping private data;
- external send activation;
- Production DB migration;
- unsuppression;
- public publishing;
- payment/spend;
- contract/legal commitment.

The Company Machine can continue high-volume research, qualification, evidence
refresh, drafting, and internal prioritization while these live-effect gates
remain closed.
