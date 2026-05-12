# ADR 0002 — Durable workflows: Inngest over Temporal

- **Status**: Accepted
- **Date**: 2026-05-12
- **Owner**: Platform
- **Reviewers**: Founder

## Context

T2 commercial-readiness needs a durable workflow runtime for LLM jobs
that survive process restarts (proposal draft, daily targeting, weekly
digest, renewal pre-flight). In-process LangGraph is fine for sub-second
flows but loses state on deploy. The candidate set:

- **Temporal Cloud** — most mature, heavyweight; needs a separate worker
  fleet; Python SDK is solid but the operational surface is large.
- **Inngest** — younger, simpler operator model, generous free tier
  (50k step executions / month), built-in retries + fan-out + sleep
  + cron. Step-memoization API is ergonomic for LLM flows.
- **Trigger.dev** — strong DX but TS-first; Python SDK is a translation.

Constraints:

- LLM workflows are the primary user — they need step memoization so a
  retry after a restart doesn't re-spend tokens.
- Our team is small; the operator burden of Temporal (worker fleets,
  visibility, history retention) is real.
- We want to stay open-source-leaning where possible.

## Decision

Adopt **Inngest** as the durable workflow runtime. Implement a thin
dispatcher (`dealix/workflows/inngest_app.py`) so the rest of the code
fires events without importing the SDK; ship one reference function
(`proposal_draft`) broken into three memoized steps so the migration
pattern is visible.

Temporal stays on the "if we hit Inngest limits" shelf. We do not
migrate the existing arq queue — arq remains for short async work.

## Alternatives considered

| Option | Why we rejected it |
| --- | --- |
| Temporal Cloud | Operator burden too high for a 1–2 engineer team; cost climbs fast at our volume. |
| Trigger.dev | TS-first; Python SDK lags. We'd be a second-class user. |
| arq + custom durability layer | Reinventing the wheel; no replay model. |
| LangGraph in-process | Already in use; the problem we're solving is durability *across* restarts. |

## Consequences

- **Positive**:
  - Free tier covers our first 50k step executions / month.
  - Step memoization means LLM tokens aren't re-spent on retry.
  - Built-in dashboard for inspecting stuck runs — the founder doesn't
    need to grep logs.
  - Self-hostable via the OSS Dev Server image if vendor lock becomes
    a concern.
- **Negative**:
  - Less mature than Temporal; smaller community.
  - Vendor-specific event naming convention; we abstract via the
    dispatcher to limit blast radius if we ever switch.
- **Mitigations**:
  - Dispatcher facade isolates the surface area to one module.
  - We migrate flows one at a time; existing LangGraph keeps working
    in parallel.

## Links

- Code: `dealix/workflows/inngest_app.py`
- Vendor: https://www.inngest.com/docs
- Related ADRs: future ADR will record any decision to migrate flows
  off LangGraph wholesale.
