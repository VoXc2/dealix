# Technical Architecture Overview — Dealix (AR)

> **Audience:** Enterprise architects, security reviewers, technical procurement.
> **Companion to:** `docs/architecture/`, `docs/36_architecture/`.

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CLIENTS                                                    │
│  Portal · WhatsApp · Email · CRM (HubSpot) · Calendar       │
└────────────────────────┬────────────────────────────────────┘
                         │ (TLS)
┌────────────────────────▼────────────────────────────────────┐
│  EDGE: Caddy / Proxy · WAF (E3+) · Rate Limit               │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  API: FastAPI · 120+ routers · Pydantic validation          │
│  ├─ /api/v1/leads (governed intake)                          │
│  ├─ /api/v1/commercial/* (commercial chain)                 │
│  ├─ /api/v1/ops-autopilot/* (founder cockpit)               │
│  ├─ /api/v1/decision-passport/* (audit)                     │
│  └─ /api/v1/webhooks/calendly (inbound)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Postgres 16  │ │ Redis 7      │ │ Object Store │
│ (primary)    │ │ (cache/queue)│ │ (uploads E3) │
└──────────────┘ └──────────────┘ └──────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  AI OPS LAYER (Agent 19)                                    │
│  Model Router · Eval Suite · Cost Governor · PII Guard      │
│  Models: MiniMax / OpenAI / DeepSeek / Ollama (per policy)  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  AGENTS (Wave 1–3)                                          │
│  Market · Commercial · Ops · Security · Frontend · ...     │
│  Each: allowlist · audit · no-auto-execute                  │
└─────────────────────────────────────────────────────────────┘
```

## 2. Component Inventory

| Component | Tech | Purpose |
|-----------|------|---------|
| API | FastAPI 0.115+ | HTTP API |
| DB | PostgreSQL 16 | Primary data |
| Cache | Redis 7 | Sessions, queue |
| Frontend | Next.js | Dashboard + public |
| LLM Router | Custom (in `dealix/llm/`) | Multi-model routing |
| Audit | JSONL append-only | Event log |
| Frontend proxy | `/api/dealix-proxy/[...path]` | Admin API key isolation |

## 3. Data Flow Patterns

| Flow | Description | Security |
|------|-------------|----------|
| Lead intake | Public → validated → DB → CRM sync | PII redaction, opt-in |
| Approval-gated send | Draft → review → approval → API call | Human-in-loop, audit |
| Webhook intake | External → validate → queue → process | Signature, replay protection |
| AI inference | Prompt + data → model → response | Allowlist, no secrets, eval |
| Audit emit | Action → JSONL → immutable | Append-only, signed |

## 4. Reliability

- **SLO target (E3+):** 99.5% monthly availability
- **Backups:** provider-managed، tested restore شهري في E3+
- **Health checks:** `/healthz` endpoint، synthetic monitoring
- **Rate limit:** per-IP, per-tenant
- **Graceful degradation:** features تُعطّل بدل أن ينهار النظام (e.g., CRM sync skips when no token)

## 5. Scalability

- **Stateless API** → horizontal scaling
- **Connection pool:** مفصول للـ revenue memory (dedicated worker)
- **Async I/O** throughout
- **Bottlenecks مُراقبة** في `/metrics`

## 6. Security Architecture

راجع `docs/enterprise/SECURITY_OVERVIEW_AR.md` للتفاصيل.

Highlights:
- **Network:** TLS only, egress allowlist (مُخطط E3+)
- **Identity:** API keys + admin key + portal sessions
- **Authorization:** Pydantic schemas + business logic checks
- **Audit:** كل privileged action

## 7. Integration Architecture

راجع `docs/enterprise/INTEGRATION_OVERVIEW_AR.md`.

## 8. Deployment

- **Primary:** Railway (production)
- **CI:** GitHub Actions
- **Migrations:** Alembic، single head enforced
- **Smoke tests:** `scripts/founder_production_smoke.sh`
- **Env matrix:** `python3 scripts/railway_launch_env_check.py`

## 9. Observability

- **Logs:** structured JSON to stdout
- **Metrics:** Prometheus-compatible (مُخطط)
- **Tracing:** (مُخطط E4)
- **Alerts:** rate limit, auth fail, schema fail

## 10. Limitations & Honest Disclosures

- ❌ لا multi-region active-active (single region E3، HA مُخطط E4)
- ❌ لا read replicas (post-scale)
- ❌ لا cross-cloud DR (single cloud E3، مُخطط E5)
- ❌ لا chaos engineering drills (مُخطط E4)

---

> **Owner:** Founder + Tech Lead · **Review:** كل 90 يوم
