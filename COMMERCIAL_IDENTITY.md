# Dealix Commercial Identity Standards

## Overview

This document defines the canonical commercial identity for Dealix as a **Saudi-first AI Business Operating System**. Use it to keep public-facing materials, code, scripts, proposals, pricing discussions, and documentation consistent.

Dealix is the company and platform identity. **Revenue + Proof + Command** is the first market wedge. Do not narrow the company identity to a revenue tool, and do not market the full long-term platform as already deployed for every company function.

---

## Commercial authority order

When commercial surfaces disagree, use the following order:

1. [`docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md`](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md) — company and platform positioning.
2. [`docs/DEALIX_BUSINESS_MODEL.md`](docs/DEALIX_BUSINESS_MODEL.md) — founder-governed canonical commercial truth for the active offers, first-five ICP, qualification exit criteria, 30-day Pilot delivery/proof cadence, and evidence-based expansion rule.
3. This document — canonical market language and a readable mirror of current first-launch boundaries. It cannot weaken the Business Model.
4. [`dealix/config/first_launch_offer_gate.yaml`](dealix/config/first_launch_offer_gate.yaml) together with decision issue [#917](https://github.com/Dealix-sa/dealix/issues/917) — the active first-launch progression gate. It must remain consistent with the canonical Business Model and controls founder approval, qualified-conversation requirements, the exact current Pilot scope and exclusions, runtime blocks, external-send eligibility, and invoice/payment-link readiness. It is not itself a price catalogue and cannot authorize checkout or a quote.
5. [`auto_client_acquisition/service_catalog/registry.py`](auto_client_acquisition/service_catalog/registry.py) — canonical **executable offering metadata** (service IDs, commercial modes, scope metadata, and hard gates). For `custom` / `quote_only` offerings, numeric placeholders such as `price_sar = 0.0` are **not** price authority and must never be interpreted as a free customer quote. Once the canonical commercial truth and active launch gate permit progression and named-customer commercial terms are explicitly approved, the **approved customer-specific quote is the price authority for that customer**.
6. [`auto_client_acquisition/finance_os/pricing_catalog.py`](auto_client_acquisition/finance_os/pricing_catalog.py) — internal pricing basis and experiments. Values such as `None` represent an unknown/custom price; this catalogue cannot by itself authorize a quote, invoice, checkout, public price, or external send.
7. [`dealix/registers/no_overclaim.yaml`](dealix/registers/no_overclaim.yaml) — evidence status and public-claim limits.
8. GitHub issue [#864](https://github.com/Dealix-sa/dealix/issues/864) — live design-partner and first-revenue evidence.

If two sources conflict, the **most restrictive current authority wins**. No document, generated proposal, numeric experiment, demo, or draft can authorize a quote, invoice, checkout, external send, revenue claim, or delivery claim without the required approval and evidence.

---

## Organization identity

| Item | Value |
|---|---|
| Company name | Dealix |
| Legal entity | Dealix Software LLC (planned; not a claim of current incorporation) |
| GitHub org | `Dealix-sa` |
| Repository | `Dealix-sa/dealix` |
| Website | `https://dealix.me` |
| GitHub Pages | `https://dealix-sa.github.io/dealix` |
| Contact | `hello@dealix.me` |

### Canonical GitHub URLs

- Repository: `https://github.com/Dealix-sa/dealix`
- Issues: `https://github.com/Dealix-sa/dealix/issues`
- Actions: `https://github.com/Dealix-sa/dealix/actions`
- Security: `https://github.com/Dealix-sa/dealix/security`

---

## Brand positioning

### One-liner

> Dealix is a Saudi-first AI Business Operating System.

### Tagline

> Revenue + Proof + Command for Saudi companies.

### Sub-line

> PDPL-native · ZATCA-aware · Approval-first

### Core promise

AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.

### Arabic positioning

> ديلكس هو نظام تشغيل أعمال بالذكاء الاصطناعي للشركات السعودية، يبدأ من الإيرادات والإثبات والقيادة، ويجمع الفرص والموافقات والمتابعة والنتائج في مسار تشغيلي واحد. قدرات التدقيق الشاملة ما زالت ضمن مرحلة Pilot وتُوصف فقط بحدود ما يثبته سجل الإثبات الحالي.

---

## What Dealix is

Dealix helps Saudi B2B companies turn commercial intent into governed execution. It combines company context, opportunity intelligence, decision support, approval-first action control, outcome evidence, and executive command so founders and revenue teams can operate with proof instead of guesswork.

It is **not** a generic CRM, chatbot, blind sales automation tool, guaranteed-revenue service, or a claim that AI replaces accountable human owners.

---

## First market wedge

### Entry path

```text
Free Mini Diagnostic (`free_mini_diagnostic`)
→ founder review
→ qualified discovery
→ first-launch gate and founder approval
→ Revenue Command Pilot — 30 days
→ verified delivery and Proof Pack
→ only then consider a recurring or expanded scope
```

The free entry offer uses the canonical service-registry ID/name `free_mini_diagnostic` / **Free Mini Diagnostic**, but the **higher-priority Business Model controls the minimum customer-facing deliverables**. The Diagnostic must include a short discovery and evidence intake, identify one credible operational/revenue leak, and return a written diagnosis, missing-evidence report, and pilot hypothesis. [`auto_client_acquisition/service_catalog/registry.py`](auto_client_acquisition/service_catalog/registry.py) remains executable offering metadata and hard-gate wiring; it must not narrow or replace the stricter deliverables in [`docs/DEALIX_BUSINESS_MODEL.md`](docs/DEALIX_BUSINESS_MODEL.md). Do not substitute the lower-priority internal `Free Growth Diagnostic` experiment or its different session scope in customer-facing materials.

### First paid motion

The authorized first paid motion is the **Revenue Command Pilot — 30 days**, but it may progress only when the canonical Business Model and active first-launch gate permit it and the named scope is approved.

The Pilot delivery contract must preserve the Business Model's explicit scope/baseline/owner/data-boundary/approval/acceptance/proof-cadence requirements, including a **weekly Proof Pack and final outcome review**. The active gate may add stricter deliverables such as a measured operating target, weekly executive readout, final Proof Pack, and stop/expand/redesign decision; it cannot silently remove a Business Model requirement. **Do not prepare or approve a named-customer quote from a copied scope list in this document.** Read both the canonical Business Model and active gate at quote time; the stricter requirement wins.

No live external send is implied by Pilot scope. While the active gate keeps `external_send_allowed: false`, **customer-facing external send is unconditionally disabled**. Action-specific approval does not override that product gate. If a later governed change explicitly enables external send, every individual send must still pass action-specific approval plus the applicable consent, suppression, policy, tenant, connector, and technical-safety controls.

### Pricing authority

- The 30-day Revenue Command Pilot is **quote-only after discovery**.
- For this quote-only Pilot, the **actual customer price authority is the founder-approved named-customer quote** created after discovery and only after the canonical Business Model and active launch gate permit progression. The service-registry `price_sar = 0.0` value is a quote-only placeholder, not a SAR 0 offer; the finance catalogue's `None` likewise means the price is not pre-authorized.
- Before any pricing experiment can become public authority, the operator must evaluate **every current `pricing_experiment` gate** in [`dealix/config/first_launch_offer_gate.yaml`](dealix/config/first_launch_offer_gate.yaml), not a copied subset in this document. The current gate requires: five qualified conversations, founder approval, margin-floor review, and tax/e-invoice review. If the Business Model or YAML adds or tightens a prerequisite, that newer/more restrictive requirement applies automatically.
- No public first-launch price or self-serve checkout is authorized yet.
- Numeric entries for other services are internal experiments or follow-on planning inputs; they cannot authorize a quote, invoice, checkout, or public price.
- A founder-approved named-customer scope and quote must identify deliverables, exclusions, acceptance criteria, evidence, payment terms, the agreed customer-specific price, and the customer, and must remain consistent with the canonical Business Model and active first-launch gate.

### Current launch blocks

The active first-launch gate remains authoritative for runtime progression. In particular:

- customer-facing external send is **blocked unconditionally while `external_send_allowed: false`**; founder/action approval alone cannot bypass this gate;
- real customer data remains blocked until the privacy/data gate permits the exact dataset;
- live checkout remains blocked until the payment/security gates close;
- invoice or payment-link progression remains blocked until a documented payment path is approved;
- production sales proof remains dependent on current production-trust evidence.

### Evidence gates by claim type

Use the evidence chain that matches the exact claim. Do not require payment to prove a free delivery, and do not use delivery alone to claim revenue.

**Paid-pilot / revenue claim** — require same-company evidence of:

1. approved named-customer scope and commercial terms;
2. authorized invoice or payment request actually issued;
3. payment-received evidence reconciled to that customer and obligation.

A proposal, invoice draft, verbal interest, or deal stage labelled `paid` is not revenue proof.

**Completed-delivery claim** — require same-company evidence of:

1. an approved or otherwise valid delivery obligation/scope;
2. tracked completion of the required delivery work;
3. delivery evidence, acceptance evidence when applicable, and the corresponding Proof Pack or delivery artifact.

Payment evidence is **not** required to prove completion of a free diagnostic or other no-charge deliverable. If the delivery is part of a paid pilot, revenue proof remains a separate requirement.

**Customer-value / outcome claim** — require same-company evidence of:

1. an agreed baseline or source-bound starting state;
2. the measured outcome and measurement window;
3. source-bound evidence connecting the outcome to the customer/workflow;
4. attribution caveats and confidence limits;
5. outcome/learning record and customer acceptance when the claim implies customer-confirmed value.

Synthetic demos, internal estimates, unverified attribution, and completed activity alone are not verified customer value.

A full paid-pilot lifecycle can link all three chains — commercial/payment evidence, delivery evidence, and outcome/value evidence — but each claim must stand on its own required proof.

---

## First-launch validation cohort

The **five qualified conversations required by the current pricing experiment count only when each conversation satisfies both**:

1. the canonical **first-five ICP** in [`docs/DEALIX_BUSINESS_MODEL.md`](docs/DEALIX_BUSINESS_MODEL.md) and mirrored in the active launch gate: Saudi B2B SaaS or business-service company, approximately 20–200 employees, direct founder/GM decision access, identifiable revenue-operations pain, usable lawful data, an accountable owner, willingness to run a measured 30-day Pilot, and acceptance of human approval gates; and
2. **all** canonical qualification exit criteria in [`docs/DEALIX_BUSINESS_MODEL.md`](docs/DEALIX_BUSINESS_MODEL.md): a painful and specific business problem; an accountable decision owner; relevant data that can be used lawfully; a measurable baseline and proof path; willingness to operate through approval gates; a completed budget/timing discussion; and no guarantee, compliance-bypass, or prohibited-data request.

An approximate sector fit or generic ICP match alone is **not** a qualified conversation. A conversation missing even one current first-five ICP or qualification exit criterion does not count. If the canonical Business Model later adds or tightens a criterion, that newer/more restrictive source contract automatically wins over this readable mirror.

Current first-five validation snapshot:

- company type: Saudi B2B SaaS or business-service;
- approximate employee range: 20–200;
- decision access: direct founder or general-manager access;
- pain/data/owner posture: identifiable revenue-operations pain, lawful usable data, accountable owner;
- pilot posture: willingness to run a measured 30-day Pilot and accept human approval gates;
- active operating signals may include opportunities without a verified owner/next action, inconsistent follow-up/response time, manually assembled executive reporting, or CRM activity without evidence governance;
- the conversation must also satisfy all seven current qualification exit criteria before it is counted;
- defer banks, government, heavily regulated enterprise transformation, anonymous mass outbound, and customers requesting guaranteed revenue.

This list is a readable mirror only. Qualification must read the canonical Business Model and active gate at conversation-count time; any future narrower or stricter requirement automatically wins.

Broader Saudi companies may remain research or future-market candidates, but they **must not be counted toward the first five validation conversations** unless the canonical first-five ICP is deliberately changed and every current canonical qualification exit criterion is still satisfied.

### Poor first-launch fit

- requests scraped or purchased personal data;
- requires cold WhatsApp blasts, LinkedIn automation, or unreviewed auto-send;
- expects guaranteed sales or government access;
- refuses baseline, data-governance, approval, or proof requirements;
- wants a company-wide transformation before one controlled workflow is proven.

---

## Key product language

Use these terms consistently across landing pages, decks, and documentation:

| Term | Meaning |
|---|---|
| Business OS | The broader company operating platform and long-term identity |
| Revenue OS | First commercial wedge: opportunity, pipeline, follow-up, and proof |
| Proof Engine | Source-bound outcomes, evidence packs, and before/after artifacts |
| Command Room | Executive surface for priorities, blockers, decisions, and next actions |
| Trust Gate | Approval-first control point before external commitments |
| Company Brain | Governed company context with provenance and tenant boundaries |
| Pilot | The 30-day Revenue Command Pilot; quote-only after qualified discovery and the active launch gate |
| Proof Pack | Evidence of approved work, delivery, outcomes, caveats, and next learning |

---

## External-action rules

- No cold WhatsApp automation.
- No LinkedIn automation or scraping.
- No customer-facing auto-send.
- No payment capture, production mutation, contract commitment, public claim, or customer communication without action-specific approval.
- No external send at all while the active first-launch gate keeps `external_send_allowed: false`; action-specific approval cannot bypass an active product-level block.
- No fake customer, outcome, revenue, ROI, security, compliance, or government-access claim.
- Missing consent, tenant, approval, suppression, configuration, launch-gate authority, or evidence must fail closed or remain draft-only.

---

## Visual identity

- **Primary color:** Deep Saudi green `#006C35` on white
- **Accent:** Warm gold `#C5A059`
- **Type:** Clean sans-serif (Inter / IBM Plex Sans / system)
- **Tone:** Professional, credible, restrained — never hype-driven
- **Icons:** Avoid emojis in production commercial materials

---

## Repository hygiene

### Never commit

- Real customer or prospect data
- API keys, secrets, credentials
- Large archives (`.zip`, `.tar.xz`, `.rar`, `.7z`)
- Session export artifacts (`*_EXPORT*`, `*_BUNDLE*`, `*_PATCH*`)
- Runtime state snapshots generated during agent sessions

### Always commit

- Canonical product data under `data/commercial/`
- Bilingual templates under `data/templates/`
- Documentation updates reflecting current identity and authority
- Tests and verification scripts

---

## Related authority

- [README](README.md)
- [Platform Source of Truth](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md)
- [Canonical Business Model](docs/DEALIX_BUSINESS_MODEL.md)
- [First Launch Offer Gate](dealix/config/first_launch_offer_gate.yaml)
- [Service Catalogue](auto_client_acquisition/service_catalog/registry.py)
- [Pricing Catalog](auto_client_acquisition/finance_os/pricing_catalog.py)
- [No-Overclaim Register](dealix/registers/no_overclaim.yaml)
- [Commercial Trust Gate — #917](https://github.com/Dealix-sa/dealix/issues/917)
- [Production Readiness Checklist](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)
- [Commercial Go-Live Gate](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)
- [Trust Engine](trust/)

---

*Last updated: 2026-08-16. Maintained as the canonical commercial identity and first-launch authority mirror for Dealix; `docs/DEALIX_BUSINESS_MODEL.md` remains canonical commercial truth.*
