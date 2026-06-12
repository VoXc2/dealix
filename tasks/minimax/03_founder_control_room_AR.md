# MiniMax Sub-prompt 03 — Founder Super Control Room (status binding, no rebuild)

> **Scope:** Map every existing Founder Control surface into a single status doc. Do not rebuild the UI.
> **Do not break:** `make cockpit`, `make v10-verify`, the `/[locale]/ops/founder` route, the `founder_one_command.sh` script.
> **Branch:** `feature/minimax-factory-p0-hardening`

---

## 1. Objective

A "Founder Super Control Room" already exists as:
- CLI: `make cockpit` → `scripts/dealix_founder_daily_brief.py`
- One-command: `bash scripts/founder_one_command.sh`
- UI: `frontend/src/app/[locale]/ops/founder/page.tsx`
- Cadence scripts: `founder_cadence.sh`, `founder_weekly_loop.sh`, `run_founder_commercial_day.sh`
- CEO master plan: `scripts/run_ceo_master_plan_status.py`
- Daily 5 metrics: `scripts/founder_daily_five_metrics.py`
- Strongest plan: `scripts/founder_strongest_plan_status.py`
- Backed by API: `GET /api/v1/ops-autopilot/founder/ceo-master-plan`

**This sub-prompt does NOT build a new control room.** It produces **one map** that tells the founder which command, route, or script to use for which decision — and a one-line status of each.

---

## 2. Files to Create

### 2.1 `docs/ops/FOUNDER_SUPER_CONTROL_ROOM_MAP_AR.md`

A 12-tab map (GTM, Prospects, Drafts, Approvals, Replies, WhatsApp, Portal, Proposals, Proof Packs, Payments, Delivery, Renewals, Finance, Privacy, Security, Agents, Risks). For each tab, list:

| Tab | CLI | UI | API | Daily / Weekly |
| --- | --- | --- | --- | --- |
| GTM | `make cockpit` | `/[locale]/ops` | `GET /api/v1/business-now/snapshot` | daily |
| Prospects | `python scripts/warm_list_outreach.py --print` | `/ops/sales` | `POST /api/v1/leads/batch` | daily |
| Drafts | `make minimax-status` | `/ops/marketing` | `GET /api/v1/ops-autopilot/marketing/social-today` | daily |
| Approvals | — | `/ops/approvals` | `POST /api/v1/ops-autopilot/marketing/queue-approval` | daily |
| Replies | `make cockpit` | `/ops/founder` | `GET /api/v1/ops-autopilot/war-room/today-pack` | daily |
| WhatsApp | (consent-only) | `/ops/...` | consent gate | on demand |
| Proposals | `python scripts/render_diagnostic_proposal.py` | `/ops/sales` | `POST /api/v1/commercial/diagnostic` | on demand |
| Proof Packs | `make v5-proof-pack HANDLE=<client>` | `/ops/evidence` | `GET /api/v1/commercial/proof-pack/{handle}` | weekly |
| Payments | — | `/ops/sales` | `POST /api/v1/payments/moyasar/link` (admin) | on demand |
| Delivery | `python scripts/customer_success_playbook.py` | `/ops/...` | `GET /api/v1/customer-success/{handle}/health` | weekly |
| Renewals | `python scripts/customer_success_playbook.py --renewals` | `/ops/...` | `GET /api/v1/customer-success/renewals/queue` | weekly |
| Finance | `python scripts/founder_daily_five_metrics.py` | `/ops/founder` | `GET /api/v1/finance/gtm/daily` | daily |
| Privacy | `make privacy-guard` | `/ops/...` | DSR via `docs/wave8/DSR_REQUEST_TEMPLATE.md` | on demand |
| Security | `make security-audit` | `/ops/...` | `GET /api/v1/security/redteam/latest` | weekly |
| Agents | `make trust-gates` | `/ops/...` | `GET /api/v1/agents/permissions/matrix` | weekly |
| Risks | `make prod-verify` | `/ops/founder` | `GET /api/v1/ops-autopilot/risks/today` | daily |

Keep it under 250 lines. This is a **map**, not a tutorial.

---

## 3. Constraints

- Do not edit any existing script. This is a doc-only sub-prompt.
- Do not create new files in `frontend/`. The UI already exists.
- Do not add new API endpoints. They already exist.
- The map must be readable on mobile. No wide tables.

---

## 4. Acceptance

```bash
test -f docs/ops/FOUNDER_SUPER_CONTROL_ROOM_MAP_AR.md
wc -l docs/ops/FOUNDER_SUPER_CONTROL_ROOM_MAP_AR.md   # must be <= 250
```
