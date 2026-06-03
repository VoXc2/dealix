# Dealix — Integration Roadmap & Vendor Matrix

## الهدف

اختيار integrations التي تزيد الإيراد أو الثقة فقط، مع fallback واضح لكل مزود.

## Integration principles

- لا تضف integration بدون owner وmetric.
- كل integration له env vars، health signal، failure mode، وfallback.
- كل secret يبقى في Railway/GitHub Secrets فقط.
- أي provider customer-facing يحتاج logging وrate limits.

## Priority matrix

| Area | Provider examples | Priority | Why |
|---|---|---:|---|
| LLM | Anthropic, OpenAI, Groq, Google | P0 | core reasoning/generation |
| Search | Google CSE, Tavily | P0 | lead discovery |
| Local discovery | Google Maps, SerpAPI | P1 | Saudi account discovery |
| Email | Gmail OAuth, SendGrid | P1 | outreach and follow-up |
| WhatsApp | Meta, Green API, Ultramsg | P1 | Saudi channel fit |
| CRM | HubSpot | P2 | customer adoption |
| Payments | Moyasar | P2 | paid step and checkout |
| Observability | Sentry, OTEL | P0 | reliability |
| Analytics | PostHog | P2 | product usage |

## Integration checklist

- [ ] Env vars documented.
- [ ] Timeout configured.
- [ ] Retry policy configured.
- [ ] Rate limit or budget exists.
- [ ] Error redaction exists.
- [ ] Health/deep health signal exists if critical.
- [ ] Fallback behavior documented.
- [ ] Tests cover success and failure.
- [ ] Runbook updated.

## Rollout phases

### Phase 1 — reliable core

- LLM provider fallback.
- Search provider fallback.
- Sentry/health deep checks.
- Manual approval for outbound.

### Phase 2 — revenue execution

- Email/WhatsApp channel execution.
- CRM sync.
- proposal and diagnostic delivery.

### Phase 3 — scale

- analytics loops.
- customer health scoring.
- automated expansion signals.
- workflow cost optimization.

## Kill switch rule

Any integration that can contact a customer, spend money, or mutate external state must have a kill switch or approval gate.
