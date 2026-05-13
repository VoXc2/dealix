# Customer Capability — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Head of Customer Success
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [customer_capability_AR.md](./customer_capability_AR.md)

## Context

The Customer capability exists so a client company can respond to its
customers faster, more consistently, and in the correct language and
tone. It targets the WhatsApp / email / form-overload reality of Saudi
SMBs and is anchored to `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` and the
KPI baselines in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`. Maturity is
scored using
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Business Purpose

Respond to customers faster, more consistently, and in the correct
language and tone — without sacrificing safety.

## Typical Problems

- WhatsApp overload — replies stall after-hours.
- Scattered FAQs — every agent answers differently.
- Slow response — first reply hours late.
- Inconsistent answers — agent-by-agent variance.

## Required Inputs

- Support history (chats, tickets, emails).
- Knowledge base (FAQs, policies, product info).
- Channels in use (WhatsApp, email, web).
- Escalation rules and on-call coverage.

## AI Functions

- Classify incoming messages by intent and urgency.
- Draft a response from KB with citation to source.
- Escalate to a human when rules require.
- Summarize long threads for handoff.
- Propose new KB additions from repeated questions.

## Governance Controls

- No auto-send without human approval (MVP rule).
- Sensitive cases (legal, payments, complaints) routed to humans.
- Every drafted answer cites a KB source.
- Audit log of every classification, draft, and send.

## KPIs

- Response time — minutes to first reply.
- Resolution time — minutes from inbound to resolved.
- Reply quality — QA score on tone, accuracy, citation.
- Escalation rate — % of conversations escalated to humans.

## Services

- AI Support Desk — first capability build.
- Monthly Support AI — recurring operating retainer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Inbound message | Classification + draft | Delivery (agent) | Real-time |
| Draft + approval | Sent reply | Client agent | Real-time |
| Resolved tickets | Quality + escalation report | Delivery | Weekly |
| Repeated questions | KB proposals | Delivery | Monthly |

## Metrics

- Response time and resolution time (see KPIs).
- Reply QA score 0–100.
- Escalation rate per category.
- KB freshness — days since last review.

## Related

- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — playbook this capability operationalizes.
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI definitions and dashboard hooks.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan framing CS.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity anchor (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
