# Integration Overview — Dealix (AR)

---

## 1. Integration Categories

| Category | Integrations | Direction | Required? |
|----------|--------------|-----------|-----------|
| Communication | WhatsApp (Twilio), Email (Resend) | Outbound (gated) | Optional |
| CRM | HubSpot | Bi-directional | Optional |
| Calendar | Calendly | Inbound (webhook) | Optional |
| Payment | Moyasar | Outbound (link gen) | Required for billing |
| AI Models | MiniMax, OpenAI, DeepSeek, Ollama | Outbound (per Agent 19 policy) | Configurable |
| Hosting | Railway | N/A (managed) | Required |
| Database | PostgreSQL 16 | N/A (managed) | Required |
| Cache | Redis 7 | N/A (managed) | Required |

## 2. Integration Model

- **API-first:** كل integration له wrapper في `integrations/` أو `dealix/`
- **Degrade gracefully:** إذا الـ integration غير موفر، الميزة تُعطّل، النظام يستمر
- **Allowlist side effects:** الـ integration لا يعمل إلا مع approval بشري

## 3. Webhook Intake

| Webhook | Endpoint | Validation |
|---------|----------|------------|
| Calendly | `POST /api/v1/webhooks/calendly` | Signature header |
| (HubSpot) | `POST /api/v1/webhooks/hubspot/*` | Signature + replay protection |
| (Moyasar) | `POST /api/v1/webhooks/moyasar` | Signature + amount verify |

**راجع:** `docs/governance/INCIDENT_RESPONSE.md` لمشاكل webhook.

## 4. Outbound Approval Workflow

```
[Agent Draft] → [Quality Check] → [Founder Approve] → [API Call] → [Log] → [Notify]
```

**Default:** لا outbound بدون approval.

## 5. Onboarding an Integration

1. Business case (volume, value, risk)
2. Security review (DPA, data flow)
3. Schema + tests
4. Allowlist entry
5. Pilot client
6. Production rollout

## 6. Failover

- كل integration عنده **fallback** (مثل: Email fallback لو WhatsApp فشل)
- الـ founder يُخطر عند أي integration failure
- Audit row لكل attempt

## 7. ما لا ندمجه حالياً

- ❌ Slack/Teams (post-scale)
- ❌ Zapier/Make (لا حاجة، المنصة بديل)
- ❌ Public social posting (LinkedIn auto-post) — خارج scope حالياً
- ❌ Voice/phone calls (مُخطط)

---

> **Owner:** Founder + Tech Lead
