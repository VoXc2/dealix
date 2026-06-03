# Dealix Monitoring Matrix

This matrix defines what should be monitored now that Dealix is attached to a live domain.

## Availability

| Signal | Target | Alert when | Owner | First response |
|---|---|---|---|---|
| API health | `https://api.dealix.me/health` | Non-2xx or timeout | Operations | Check hosting deployment, logs, database connectivity. |
| Public website | `https://dealix.me` | Non-2xx, broken redirect, or TLS failure | Operations | Check frontend host, DNS, certificate, recent deploy. |
| Production smoke | GitHub `Production Smoke` workflow | Required smoke check fails | Engineering | Read artifact, identify endpoint, rollback if user-facing. |
| DNS resolution | Apex and API subdomain | Wrong target or no resolution | Operations | Compare DNS provider records with hosting target. |
| TLS expiry | Public and API hosts | Less than 14 days remaining | Operations | Check certificate auto-renew and hosting TLS settings. |

## Application behavior

| Signal | Target | Alert when | Owner | First response |
|---|---|---|---|---|
| API 5xx rate | Backend logs/APM | Sustained increase | Backend | Inspect recent deploy, route logs, external dependency failures. |
| Demo request flow | Public form/API | Requests fail or no CRM/email handoff | GTM + Backend | Check API route, webhook, email/CRM integration, keys. |
| Checkout flow | Pricing/checkout API | Payment creation or callback fails | Backend + Ops | Check Moyasar keys, webhook signature, callback URL. |
| Admin route auth | Admin endpoints | Missing auth accepted or valid auth rejected | Security | Treat missing auth as incident. Check middleware/config. |
| Webhook verification | Webhook routes | Signature verification disabled or failing unexpectedly | Security + Backend | Validate provider secret and payload format. |

## Trust and compliance

| Signal | Target | Alert when | Owner | First response |
|---|---|---|---|---|
| No-overclaim register | `dealix/registers/no_overclaim.yaml` | Public copy changed without register update | Product + Compliance | Update evidence/status or roll back claim. |
| Approval gates | Trust/execution flows | High-stakes action bypasses approval | Security + Product | Treat as incident and disable offending flow. |
| Data suppression | Lead/customer data workflows | Opt-out/suppression not respected | Compliance | Stop affected automation and investigate data lineage. |
| Audit trail | Trust/execution logs | Missing audit for external commitment | Engineering | Patch instrumentation and review impact. |

## Cost and provider reliability

| Signal | Target | Alert when | Owner | First response |
|---|---|---|---|---|
| LLM provider errors | Provider calls | Sustained timeout/rate limit/auth errors | AI Engineering | Fail over provider or disable affected feature. |
| LLM spend | Cost tracker/provider dashboards | Spend exceeds budget or sudden spike | Founder/Ops | Rate-limit, cache, or disable non-critical automations. |
| Email/WhatsApp limits | Channel providers | Near daily quota or throttling | GTM + Ops | Pause campaigns or reduce batch size. |

## Minimum dashboard

A minimum production dashboard should show:

- API health and latency.
- Public website uptime.
- Production smoke status.
- Error rate by route.
- Payment/demo request success rate.
- LLM spend and provider error rate.
- Last successful deployment and commit SHA.

## Arabic summary

المراقبة لازم تغطي: توفر الموقع والـ API، الدومين وTLS، أخطاء التطبيق، تدفقات الديمو والدفع، بوابات الموافقة، احترام opt-out، وتكلفة مزودي الـ AI.
