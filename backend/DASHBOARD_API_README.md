# Dealix Dashboard API

Production FastAPI backend for the Dealix sales intelligence dashboard. Replaces `mock.json` with a real SQLite-backed API.

## Quick Start

```bash
# 1. Install dependencies
cd dealix-clean/backend
pip install -r requirements.txt
pip install slowapi httpx-ws

# 2. Seed the database (30 Saudi leads, agents, playbooks)
python scripts/seed_dashboard.py

# 3. Start the unified server (webhook + dashboard API)
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

Default test credentials: **sami@dealix.sa** / **dealix2026**

---

## Architecture

```
main.py (Uvicorn entry point)
├── dashboard_api.py       — All dashboard endpoints + WebSocket + auth
└── whatsapp_webhook_v2.py — WhatsApp webhook + event bus integration
```

Both modules share:
- The same SQLite database (`dealix_leads.db`)  
- An `asyncio.Queue` event bus for real-time WS broadcasting

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DEALIX_DB` | `/home/user/workspace/dealix-clean/dealix_leads.db` | SQLite path |
| `JWT_SECRET` | `dealix-dev-secret-change-in-prod` | JWT signing key |
| `GROQ_API_KEY` | *(empty)* | Groq LLM key for AI suggestions |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model |
| `TWILIO_ACCOUNT_SID` | *(empty)* | Twilio SID for real WhatsApp sends |
| `TWILIO_AUTH_TOKEN` | *(empty)* | Twilio auth token |
| `TWILIO_WHATSAPP_FROM` | `whatsapp:+14155238886` | Twilio sandbox number |
| `CORS_ORIGINS` | `localhost:3000,5173,8080,5500` | Allowed CORS origins |

---

## Auth Flow

```
POST /api/v1/auth/login
  Body: {"email": "sami@dealix.sa", "password": "dealix2026"}
  → {"access_token": "<JWT>", "token_type": "bearer", "tenant_id": "...", ...}

# All other endpoints:
  Authorization: Bearer <JWT>
```

JWT payload:
```json
{"sub": "<user_id>", "tenant_id": "...", "email": "...", "role": "admin", "exp": ...}
```

All data is scoped by `tenant_id`. Attempting to read another tenant's data returns 404.

---

## Endpoints Table

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/health` | ✗ | Health check |
| POST | `/api/v1/auth/login` | ✗ | Get JWT |
| GET | `/api/v1/overview` | ✓ | KPI cards + funnel + activity + channel perf |
| GET | `/api/v1/leads` | ✓ | Paginated leads list (search, sector, stage, tier filters) |
| GET | `/api/v1/leads/{id}` | ✓ | Full lead detail with signals + contacts + timeline |
| PATCH | `/api/v1/leads/{id}` | ✓ | Update stage / assignee / value (logs activity) |
| POST | `/api/v1/leads/{id}/stage` | ✓ | Drag-drop stage move |
| GET | `/api/v1/conversations` | ✓ | Inbox list (filter by channel) |
| GET | `/api/v1/conversations/{phone}/messages` | ✓ | Full thread |
| POST | `/api/v1/conversations/{phone}/reply` | ✓ | Send real message via Twilio |
| POST | `/api/v1/conversations/{phone}/ai-suggest` | ✓ | 3 AI reply suggestions (Arabic/Gulf) |
| GET | `/api/v1/pipeline` | ✓ | Kanban columns by stage |
| GET | `/api/v1/agents` | ✓ | Agent fleet status |
| POST | `/api/v1/agents/{id}/toggle` | ✓ | Pause / resume agent |
| GET | `/api/v1/playbooks` | ✓ | Playbook list |
| GET | `/api/v1/sources` | ✓ | Data source health |
| POST | `/api/v1/sources/{name}/discover` | ✓ | Trigger discovery (background) |
| GET | `/api/v1/analytics/mrr?range=30d` | ✓ | MRR time series (7d/30d/90d) |
| GET | `/api/v1/analytics/conversion` | ✓ | Conversion rates per channel |
| GET | `/api/v1/analytics/agent-roi` | ✓ | Agent ROI table |
| GET | `/api/v1/settings/me` | ✓ | Current user + tenant + masked API keys |
| POST | `/api/v1/settings/api-keys` | ✓ | Update Groq/Twilio/SendGrid keys |
| WS | `/api/v1/ws` | optional | Real-time event stream |
| POST | `/webhook/whatsapp` | Twilio | Inbound WhatsApp (TwiML response) |

### Leads list query params
```
?search=<text>   Company name / contact name search
&sector=ecommerce
&stage=qualified
&tier=hot|warm|cool|cold
&limit=50        Default 50, max 500
&offset=0
```

### Reply endpoint body
```json
{"channel": "whatsapp", "body": "رسالة الرد هنا"}
```
If `TWILIO_ACCOUNT_SID` is set, the real Twilio API is called. Otherwise dry-run mode returns `provider_sid: "dry-run-<trace_id>"`.

---

## WebSocket

Connect: `ws://localhost:8002/api/v1/ws?tenant_id=<tid>&token=<jwt>`

### Event types (server → client)

| Type | Payload |
|------|---------|
| `connected` | `{tenant_id}` |
| `heartbeat` | *(every 30s)* |
| `message.new` | `{message, phone, lead_id}` |
| `lead.updated` | `{lead_id, updates}` |
| `lead.scored` | `{lead_id, score}` |
| `agent.status` | `{agent_id, status}` |
| `source.discovered` | `{source}` |
| `activity.new` | `{activity}` |

### Client → server

```json
{"type": "ping"}
```
Server responds with `{"type": "pong"}`.

### JavaScript example

```javascript
const ws = new WebSocket(
  `ws://localhost:8002/api/v1/ws?tenant_id=${tenantId}&token=${jwt}`
);

ws.onmessage = (event) => {
  const { type, payload, ts } = JSON.parse(event.data);
  
  if (type === 'message.new') {
    appendMessage(payload.message);
  } else if (type === 'lead.scored') {
    updateLeadScore(payload.lead_id, payload.score);
  } else if (type === 'agent.status') {
    updateAgentStatus(payload.agent_id, payload.status);
  }
};

ws.onopen = () => ws.send(JSON.stringify({ type: 'ping' }));
```

---

## Database Schema

All tables have `tenant_id` for multi-tenant isolation.

| Table | Key Columns |
|-------|------------|
| `leads` | id (TEXT UUID), phone, company_name, sector, stage, score_total, score_breakdown (JSON), priority_tier, tenant_id |
| `messages` | id, phone, direction (in/out), body, channel, tenant_id |
| `conversations` | phone (UNIQUE), channel, last_message_preview, unread_count, sentiment, stage, tenant_id |
| `agents` | id, name, channel, status (active/paused), msgs_today, success_rate, cost_today, tenant_id |
| `playbooks` | id, name, sector, steps (JSON), active_count, tenant_id |
| `signals` | id, lead_id, category, text, score_impact, source, tenant_id |
| `activities` | id, lead_id, actor, channel, action, meta (JSON), trace_id, tenant_id |
| `sources_health` | source_name, status, records_imported, last_sync, error, tenant_id |
| `tenants` | id, name, created_at |
| `users` | id, tenant_id, email, password_hash, role, api_keys (JSON, encrypted-at-rest planned) |

---

## Running Tests

```bash
cd dealix-clean/backend/tests_dashboard_standalone
pytest . -v
```

Test coverage:
- Auth (login success/failure, protected endpoints, trace_id header)
- Leads CRUD (list, filter, detail, patch stage/value, search)
- Conversations (list, channel filter, messages, reply dry-run, reply persistence, AI suggest)
- Pipeline (kanban shape, stage move)
- Agents (list, toggle pause/resume)
- Playbooks, Sources, Analytics (MRR, conversion, agent ROI), Settings
- **Tenant isolation** — tenant A cannot read, patch, or enumerate tenant B's leads, agents, pipeline
- WebSocket (event bus, ws_manager connect/disconnect, queue draining)

**Result: 45/45 tests passing**

---

## Seeding

```bash
python scripts/seed_dashboard.py
```

Creates:
- Tenant: **Dealix Demo** (id: `00000000-0000-0000-0000-000000000001`)
- User: **sami@dealix.sa** / **dealix2026** (role: admin)
- **30 Saudi companies** as leads, scored via `LeadScorer`
- **7 AI agents** (WhatsApp, Email, LinkedIn, SMS, Qualification, Proposals, CS)
- **3 playbooks** (ecommerce, agency, real_estate)
- **10 conversations** with 3-8 messages each
- **6 data source** health records
- **50 activity** events

---

## Response Headers

Every response includes:
- `X-Trace-ID: <uuid4>` — correlates logs with requests
- `X-Service: dealix-dashboard-api`

Pass `X-Trace-ID` in requests to propagate your own trace ID.

---

## Error Shape

All errors follow:
```json
{
  "detail": "Human-readable message"
}
```
HTTP status codes: 200, 201, 207 (partial success with warning), 400, 401, 404, 422, 500.
