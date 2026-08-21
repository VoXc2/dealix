# Dealix — Commercial Chain Context (On-Demand Skill)

## Overview

السلطة التجارية الحالية:

**Dealix — Saudi-first AI Business Operating System**

أول wedge:

**Revenue + Proof + Command**

المسار الحالي:

```text
Free Mini Diagnostic
→ qualified discovery
→ customer-specific quote after approval
→ 30-day Revenue Command Pilot
→ weekly + final Proof
→ STOP / EXPAND / REDESIGN
```

هذا الملف **لا يعرّف Price ladder أو Payment authority أو External-send authority**. أي Modules/Enums/Templates تاريخية تحمل أسعارًا أو Sprint/Retainer قديمًا تعتبر compatibility/legacy حتى يثبت أنها تطابق `COMMERCIAL_IDENTITY.md` و`dealix/config/first_launch_offer_gate.yaml`.

## Current Authority Sources

اقرأ بالترتيب:

1. `COMMERCIAL_IDENTITY.md`
2. `dealix/config/first_launch_offer_gate.yaml`
3. `docs/DEALIX_BUSINESS_MODEL.md`
4. `landing/trust-center.html`
5. `docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md` — اسم Legacy فقط؛ المحتوى الحالي هو first paid Revenue Command Pilot.

إذا تعارض معها Agent/Template/Enum/API قديم، لا تستخدم السعر/العرض القديم؛ Flag/Quarantine المصدر المتعارض.

## Active Commercial Composition

### Minimum-data entry

- Public `Free Mini Diagnostic` لا يحتاج اسم شخص/هاتف/بريد أو Lead persistence.
- المخرجات: credible leak hypothesis + written diagnosis + missing-evidence report + Pilot hypothesis.
- التشخيص ليس Quote أو Customer Value أو Revenue.

### Proposal / pricing artifacts

`auto_client_acquisition/designops/generators/proposal_page.py`

- normalizes legacy callers to **Revenue Command Pilot**;
- 30 days;
- `customer_specific_quote_after_qualified_discovery`;
- `safe_to_send=false`;
- no live charge;
- no guaranteed outcome.

`auto_client_acquisition/designops/generators/pricing_page.py`

- one product / one first-launch path;
- no public fixed price;
- no self-serve checkout;
- expansion only after Proof and a newly approved scope.

### Client pack

`dealix/commercial_ops/client_pack.py`

- minimum-data;
- one 30-day Pilot;
- no copied contact details;
- customer-specific quote only;
- legacy sales deck is quarantined until current-authority QA;
- no send authority.

### Proof

`data/templates/proof_pack_ar.md`

- weekly/final evidence format;
- baseline + source + method;
- `Activity ≠ Delivery ≠ Payment ≠ Revenue ≠ Customer Value ≠ Publication Permission`;
- no automatic upsell;
- no PDPL/residency/certification claim without exact evidence and approval.

## Guardrails

```text
NO_LIVE_SEND
NO_LIVE_CHARGE
NO_COLD_WHATSAPP
NO_LINKEDIN_AUTOMATION
NO_SCRAPING
NO_FAKE_PROOF
NO_FAKE_REVENUE
NO_UNAPPROVED_TESTIMONIAL
```

Additional rules:

- public contact data is not consent;
- draft approval cannot bypass a product-level block;
- invoice intent/payment link is not payment or revenue;
- synthetic/demo/internal/stale/unsynced evidence is not customer proof;
- customer result does not grant publication permission;
- no production/DNS/secret/payment mutation to unblock a draft;
- personal/sensitive data requires the exact privacy/tenant/security/data-flow gates before scope expansion.

## Legacy Commercial Modules

The repository may still contain historical or compatibility modules such as:

- service-tier enums;
- old Sprint/Managed Ops price tables;
- payment-link helpers;
- old 7-day Pilot templates;
- old 499/1500/2999/etc proposal templates;
- old case-study/social content.

**Do not treat their presence as launch authority.**

Before calling a legacy module from an agent or API:

1. verify it is needed by the current 30-day Pilot;
2. verify it does not emit retired price/package claims;
3. verify it does not send, charge, publish, or mutate production automatically;
4. verify customer/data/tenant scope;
5. fail closed or route to human approval if evidence/authority is missing.

## Payments

Current first-launch public path is `NO_LIVE_CHARGE`.

Do not advise turning on a live payment flag, creating a live payment link, rotating a payment secret, or charging a test/live card merely because a customer is interested.

A real payment path needs a named customer and approved:

- contracting/invoicing entity;
- amount/currency from the customer-specific quote;
- issuer/payment destination;
- payment terms;
- applicable tax/e-invoicing review;
- receipt/reconciliation evidence path;
- action-specific financial approval.

## Usage Pattern

For a new opportunity:

```text
1. classify source / warm / inbound context
2. qualify with evidence
3. prepare minimum-data diagnostic/discovery
4. prepare internal 30-day Pilot scope
5. prepare customer-specific quote draft
6. surface approval/privacy/tenant/payment/production blockers
7. do not send or charge
8. after approved delivery, build weekly/final Proof
9. decide STOP / EXPAND / REDESIGN from evidence
```

The goal is real paid customer value, not maximizing sends, tiers, or synthetic funnel activity.
