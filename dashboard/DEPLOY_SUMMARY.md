# Dashboard v2 Real Data — Deploy Summary

**Deployed URL:** https://www.perplexity.ai/computer/a/dealix-dashboard-GrEh65zwRs.fNNLjU8AJ3Q
**Asset ID:** 1ab121eb-9cf0-46cf-9f34-d2e353c009dd
**Status:** LIVE (demo mode fallback active until backend boots)

---

## File Tree Diff vs v1

```
dashboard/
├── index.html              [REWRITTEN] 705 lines — login gate, banners, readiness/ws pills, cmdk, shortcuts, source-config modals, bottom tabs, footer, honesty widget
├── app.js                  [REWRITTEN] 1798 lines — all data loaders, renderers, drag-drop, WebSocket, CSV export, settings save
├── styles-v2.css           [NEW]       640 lines — auth gate, demo/offline banners, skeleton, modals, cmdk, pills, api-keys, honesty, segmented, bottom-tabs, dark mode
├── styles.css              [UNCHANGED] 1387 lines — original token system and component styles
├── js/
│   ├── api.js              [NEW]       283 lines — Auth, fetch w/ retry+backoff, mock.json fallback on 0/404/5xx
│   └── ws.js               [NEW]       74 lines — WebSocket client with reconnect backoff, dispatches window events
├── data/
│   └── mock.json           [UNCHANGED] — used as demo fallback; api.js normalizes field names to contract
└── assets/
    ├── v2-login.png        [NEW] login screenshot
    ├── v2-overview.png     [NEW] overview screenshot (post-login, demo mode, all KPIs + funnel + activity)
    └── ... (v1 screenshots kept as historical reference)
```

**Unchanged**: `styles.css`, `data/mock.json`, existing v1 screenshots.

---

## API Assumptions (for backend subagent)

The frontend codes defensively against this exact contract. Backend MUST emit these exact shapes:

### Auth
- `POST /api/v1/auth/login` body `{email, password}` → `{token: string, user: {id,email,name,role}, tenant: {id,name,plan}}`

### Overview
- `GET /api/v1/overview` → `{kpis: {active_leads, hot_leads, meetings_week, pipeline_value_sar}, funnel: [{stage,count}], recent_activity: [{id,type,title,ts,actor,channel}], channel_performance: [{channel,leads,conversion}]}`
- ⚠️ **Field name contract**: backend must emit `meetings_week` (NOT `meetings_this_week`) and `conversion` (NOT `conv_rate`). The api.js client translates legacy mock.json names but real backend should use contract names directly.

### Leads
- `GET /api/v1/leads?limit=200&q=&stage=&source=` → `{items: [...], total, page}`
- `GET /api/v1/leads/{id}` → lead object with full details
- `PATCH /api/v1/leads/{id}` body `{stage?, value_sar?, notes?, assignee?}` → updated lead
- `POST /api/v1/leads/{id}/stage` body `{stage}` → used by pipeline drag-drop

### Conversations (Inbox)
- `GET /api/v1/conversations` → `[{phone, name, channel, last_message, unread_count, ts}]`
- `phone` is the canonical ID (not UUID) — frontend uses `phone || id`
- `GET /api/v1/conversations/{phone}/messages` → `[{id, direction, text, ts, status}]`
- `POST /api/v1/conversations/{phone}/reply` body `{text}` → message echo
- `POST /api/v1/conversations/{phone}/ai-suggest` → `{suggestions: [string, string, string]}`

### Pipeline
- `GET /api/v1/pipeline` → `{columns: [{stage, leads: [...]}]}`

### Agents
- `GET /api/v1/agents` → `[{id, name, status, channel, last_action, metrics}]`
- `POST /api/v1/agents/{id}/toggle` → updated agent

### Sources
- `GET /api/v1/sources` → `[{name, enabled, status, leads_today, config}]`
- `POST /api/v1/sources/{name}/discover` → `{job_id, progress}` (frontend polls or uses WS)

### Analytics
- `GET /api/v1/analytics/mrr?range=7d|30d|90d|ytd` → `{series: [{date, value}], total, delta}`
- `GET /api/v1/analytics/conversion?range=...` → `{funnel, by_channel, by_source}`

### Settings
- `GET /api/v1/settings` → `{org, team, api_keys, compliance, notifications}`
- `PATCH /api/v1/settings` body with partial settings

### Readiness
- `GET /api/v1/readiness-matrix` → `{counts: {live, partial, pilot, target}, services: [{status, name, description}], last_updated}`
- Parse from `docs/registry/SERVICE_READINESS_MATRIX.yaml` server-side; return stub counts if file missing

### WebSocket
- `ws://host/api/v1/ws?token=<bearer>` → emits JSON events `{type, payload}` with types: `message.new`, `lead.scored`, `agent.status`, `activity.new`

---

## Sami's Test Instructions

**Login**: demo@dealix.sa / demo1234 — works instantly (demo mode, no backend).

1. **Login page**: gradient green bg left, 480px panel right. Hint at bottom shows demo credentials.
2. **After login**: yellow banner "وضع تجريبي — الداتا من مخزن مؤقت" appears at top.
3. **Overview**: 4 KPI cards (142 leads, 18 hot, 23 meetings, 42.8M SAR pipeline), funnel bars Prospect→Lost, activity feed with channel icons, readiness pill "Live 5/29" top-right.
4. **Leads** (nav): 30 rows, search box + stage/source filter chips. Click a row → drawer opens with editable stage/value/notes, Save works optimistically.
5. **Inbox الموحّد**: conversation list left, messages right. Click "إعادة توليد" for AI suggestions. Composer sends replies (demo mode shows optimistic echo).
6. **Pipeline**: Kanban columns. Drag a card between columns → toast confirms, reverts on error (demo: always succeeds against mock).
7. **Playbooks**: agent list with pause toggle + drawer.
8. **Sources**: list of LinkedIn/WhatsApp/Email sources; "تشغيل اكتشاف" runs a progress bar; ⚙ opens config modal.
9. **Analytics**: date range segmented (7d/30d/90d/YTD), MRR chart, conversion funnel, "تصدير CSV" button downloads file.
10. **Settings**: org form, team table, API keys section, compliance toggles; all PATCH on Save.
11. **Keyboard**: `⌘K` / `Ctrl+K` opens command palette (nav + actions + first 20 leads, arrow+Enter). `?` opens shortcuts overlay. `Esc` closes any modal.
12. **Dark mode**: moon icon in header top-right.
13. **Mobile** (<768px): bottom tab bar replaces side nav, drawers become full-screen sheets.
14. **Readiness pill**: click it → modal shows Live/Partial/Pilot/Target counts with per-service list.
15. **Demo banner retry**: click "إعادة المحاولة" — tries real API; if backend now up, banner disappears and data switches to live.

---

## Behavior When Real Backend Goes Live

No frontend changes needed. `api.js` auto-detects: if `/api/v1/*` returns 200, it uses real data; if 0/404/5xx, it falls back to mock.json with the yellow banner. The WebSocket client attempts connection post-login and silently backs off if unavailable.

To point at a different backend: `localStorage.setItem('dealix_api_base', 'https://api.dealix.sa')` in devtools, then reload.

---

## Screenshots

- `assets/v2-login.png` — login gate (gradient + panel)
- `assets/v2-overview.png` — post-login overview in demo mode with banner, KPIs, funnel, activity
