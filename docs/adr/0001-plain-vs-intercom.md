# ADR 0001 — Customer support: Plain over Intercom / Crisp

- **Status**: Accepted
- **Date**: 2026-05-12
- **Owner**: Founder
- **Reviewers**: Platform

## Context

T0 commercial-readiness requires a real customer-support surface; "email
us at support@..." is amateur-grade for a paid Saudi enterprise SaaS.
Three vendors realistically fit our 2026 stack:

- **Intercom** — incumbent, full-featured, but expensive (≥ $74/seat/mo)
  and skewed toward consumer SaaS.
- **Crisp** — cheaper, multilingual (incl. Arabic), but limited B2B
  workflow (no MTTR SLAs, weak GraphQL, dated UI).
- **Plain** — modern (2022+), GraphQL-native, B2B-first, free tier
  covers our first ~100 customers, multilingual, integrates with
  Slack/Linear out of the box.

Constraints:

- Must support Arabic + English.
- Must integrate with our existing Resend email path so the migration
  is reversible.
- Must not bind the platform to a single vendor: a Plain ticket today
  should be a Linear issue tomorrow without a rewrite.

## Decision

Adopt **Plain** as the primary support ticketing system. Implement a
thin adapter (`dealix/integrations/plain_client.py`) that:

1. Uses GraphQL via httpx (no SDK pull).
2. Falls back to Resend email when `PLAIN_API_KEY` is unset *or* when
   the Plain API errors at runtime.
3. Surfaces a single API: `POST /api/v1/support/tickets`.

The fallback path is deliberate — it makes vendor swaps cheap (next
vendor implements the same adapter signature; the surface API never
changes).

## Alternatives considered

| Option | Why we rejected it |
| --- | --- |
| Intercom | Cost; consumer-skewed UX; vendor lock-in via their messenger SDK. |
| Crisp | Workflow depth insufficient for B2B SLA; weaker API surface. |
| Build our own (using AuditLog table) | Founder time better spent elsewhere; ignores existing customer-channel preferences. |

## Consequences

- **Positive**:
  - Free tier through ~100 paying customers.
  - GraphQL allows queries that would be REST page-walks elsewhere.
  - Arabic + English UI for our DPO and our customers.
  - Reversible — Resend fallback is always live.
- **Negative**:
  - Plain is younger than Intercom; some integrations (Salesforce,
    HubSpot) lag.
  - GraphQL learning curve for anyone unfamiliar.
- **Mitigations**:
  - Adapter pattern means we are never more than a day from swapping.
  - Linear sync covers our internal tracking via Plain's native
    integration.

## Links

- Code: `dealix/integrations/plain_client.py`, `api/routers/support.py`
- Vendor: https://www.plain.com/docs/api-reference
- Sub-processor record: `docs/sla.md` §8
