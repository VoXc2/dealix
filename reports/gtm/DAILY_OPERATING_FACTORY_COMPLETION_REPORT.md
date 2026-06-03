# Daily Operating Factory — Completion Report
*Date: 2026-06-03*

> Turns Dealix from "an AI project" into a daily run-send-deliver factory.
> Governance principle preserved throughout: **AI drafts. Human approves. System logs.**

---

## 1. Files Created / Modified

### Config registry (new) — `company_os/commercial/`
- `systems.json` — canonical Focus-5 registry (names, pain signals, delivery readiness, partner fit, internal-module + banned-phrase lists)
- `draft_scoring_rubric.json` — 100-point rubric, status thresholds, Top-Queue rules, evidence levels
- `suppression_list.json` — do-not-contact (empty seed; no purchased lists)
- `website_leads.json` — intake stub (empty)
- `draft_scores.json`, `sales_board.json` — generated machine outputs

### Scripts (new) — `scripts/` (these fix previously-broken `package.json` references)
- `commercial-lib.js` — shared, dependency-free scoring + IO library
- `draft-quality-gate.js` → `npm run commercial:quality`
- `commercial-daily-plan.js` → `npm run commercial:plan`
- `commercial-daily-brief.js` → `npm run commercial:brief`
- `commercial-control-check.js` → `npm run commercial:check`
- **Modified** `package.json` — reordered `commercial:all` to generate-then-validate

### Docs (new, 15)
- Founder control: `DAILY_SUPER_COMMAND_SYSTEM_AR.md`, `FOUNDER_DAILY_OPERATING_RHYTHM_AR.md`, `FOUNDER_DECISION_GATES_AR.md`
- Sales ops: `SALES_OPS_BOARD_AR.md`, `OWNER_ASSIGNMENT_POLICY_AR.md`, `LEAD_STATUS_MODEL_AR.md`
- Quality: `EMAIL_QUALITY_GATE_AR.md`, `CALL_BRIEF_QUALITY_GATE_AR.md`, `MINI_PROPOSAL_QUALITY_GATE_AR.md`, `DELIVERY_READINESS_GATE_AR.md`
- Content / Partners: `FOCUS_5_CONTENT_ENGINE_AR.md`, `FOCUS_5_PARTNER_CHANNEL_AR.md`
- Security: `UNTRUSTED_COMPANY_DATA_POLICY.md`, `PROMPT_INJECTION_GATE.md`, `AGENT_TOOL_USE_BOUNDARIES.md`

### Reports (new, 8)
- `reports/founder/DAILY_SUPER_COMMAND.md` (generated), `reports/founder/WEEKLY_BOARD_REVIEW.md`
- `reports/sales_ops/SALES_OPS_BOARD_STATUS.md` (generated)
- `reports/quality/DAILY_QUALITY_GATE_REVIEW.md` (generated)
- `reports/content/FOCUS_5_CONTENT_QUEUE.md`, `reports/partners/FOCUS_5_PARTNER_PIPELINE.md`
- `reports/security/DAILY_AGENT_SECURITY_REVIEW.md` (generated)
- `reports/gtm/DAILY_OPERATING_FACTORY_COMPLETION_REPORT.md` (this file)

> Note on placement: the prompt's assumed paths (`docs/outreach/`, `AGENTS.md`, etc.) do not exist in this repo. The repo organizes its operating system under `company_os/`. New machine data was placed under `company_os/commercial/` to sit beside the existing `company_os/revenue/` and `company_os/governance/` data; human docs/reports follow the requested `docs/` + `reports/` paths. `docs/` is safe (build `outDir` is `dist/public`, not `docs/`).

---

## 2. Daily Operating Rhythm

| Time | Stage | Command / Output |
|------|-------|------------------|
| 06:00 | Research Batch | real sources only |
| 07:00 | Company Intelligence Packs | — |
| 08:00 | 400 Draft Email Factory | — |
| 09:00 | Quality Scoring | `commercial:quality` → `DAILY_QUALITY_GATE_REVIEW.md` |
| 10:00 | Top Approval Queue | `draft_scores.json` |
| 11:00 | Email/Call Handoff | Call Briefs |
| 13:00 | Call Follow-up Queue | `commercial:plan` → `SALES_OPS_BOARD_STATUS.md` |
| 15:00 | Mini Proposal Queue | pending founder approval |
| 17:00 | Delivery Pipeline Update | Delivery Readiness Gate |
| 19:00 | Founder Daily Super Command | `commercial:brief` → `DAILY_SUPER_COMMAND.md` |

One command runs it all: `npm run commercial:all`.

---

## 3. Founder Command System

`DAILY_SUPER_COMMAND.md` is generated with all **13 required sections**: critical decision, 400-draft status, top-queue summary, top-20 to send, top-30 calls, mini proposals waiting, delivery status, website leads, best system, best sector, biggest risk, cash/pricing, tomorrow's recommendation. The critical decision is derived from the day's data.

---

## 4. Sales Ops Board

16-stage board (`researched … do_not_contact`) with five owner roles per company. Generated to `SALES_OPS_BOARD_STATUS.md` + `sales_board.json`. Today: 15 companies (10 researched, 5 draft_ready), 2 calls due, 0 mini proposals (no positive signal yet) — all honest, data-driven counts.

---

## 5. Quality Gates

Four gates, each declaring explicit fail conditions: Email, Call Brief, Mini Proposal, Delivery Readiness. The Email Gate is executable: drafts are scored 0–100 (Personalization 25 / Pain 20 / Fit 20 / CTA 15 / Risk 10 / Tone 10) with thresholds rejected `<65`, needs_rewrite `65–74`, approval_queue `75–84`, top_priority `85+`. The Top Queue admits only gate-pass + score ≥ 75 + non-high-risk drafts.

---

## 6. Content / Partner Engines

- Content engine: weekly pillar per system + 5 light daily posts; no fake case studies (illustrative samples only). Queue: `FOCUS_5_CONTENT_QUEUE.md`.
- Partner channel: 7 partner types mapped to best-fit systems; referral/margin model with founder-only pricing. Pipeline: `FOCUS_5_PARTNER_PIPELINE.md`.

---

## 7. Security Boundaries

- All company web/email/PDF content treated as **untrusted data**; never instructions.
- Prompt Injection Gate (with self-test) blocks "ignore previous instructions / reveal secret / execute command / change system prompt / …".
- Agent tool-use boundaries: Observe/Advise/Draft only. No external send, no automated calls, no cold WhatsApp, no purchased lists, no AI pricing, no secrets in prompts/logs.
- Consistent with existing `company_os/governance/agent_permissions.md` red lines.

---

## 8. Tests / Checks Run

`npm run commercial:check` — **11/11 passed, exit 0** (real harness, not faked):

| Result | Check |
|--------|-------|
| ✅ | Daily Super Command contains required sections |
| ✅ | Draft quality thresholds are documented |
| ✅ | Top Approval Queue excludes low-score drafts |
| ✅ | Sales ops statuses are complete (16) |
| ✅ | Quality gates include fail conditions |
| ✅ | Security policy treats company data as untrusted |
| ✅ | No guaranteed claims in customer-facing copy |
| ✅ | No internal module names in customer-facing copy |
| ✅ | Self-test: Email Gate rejects guaranteed/fake-thread/module/pain-as-fact drafts |
| ✅ | Self-test: Prompt Injection Gate flags injection, passes benign copy |
| ✅ | Governance: AI external send & autonomous action remain prohibited |

Generation runs verified: `commercial:quality` (5 scored, 0 gate fails), `commercial:plan` (15 board, 2 calls due), `commercial:brief` (13 sections), and full `commercial:all` chain green.

> Non-vacuous: the two self-tests construct malicious synthetic drafts and assert the gate blocks them; if the gate logic regressed, the check would exit non-zero.

---

## 9. Failed / Skipped Checks and Why

- No checks failed.
- **Skipped:** ESLint/TS typecheck over these `scripts/*.js` — they are standalone Node ESM utilities outside the Vite/TS app graph (`tsconfig` targets `src/`), run via `node` directly; linting them would require config changes out of scope here.
- **Not done (by design):** no real outbound sending, no live web scraping of 400 companies, no fabricated companies/case studies — all gated by policy and honesty rules.

---

## 10. Remaining Risks

1. **Capacity vs. reality:** "400/day" is factory capacity, not verified companies. Current seed pipeline is 15 prospects / 5 drafts. Scaling needs real research input (no purchased lists).
2. **CSV parser is minimal** (no embedded-comma/quote handling) — fine for current `prospects.csv`; revisit if the schema gains quoted fields.
3. **Heuristic scoring** is deterministic and conservative; it rewards well-formed templates (today all 5 score high). It is a quality floor, not a substitute for human judgement on nuance.
4. **Repo has a duplicated `company_os/company_os/` tree** (pre-existing) — left untouched; worth a cleanup later.
5. **`docs/` mixes built site assets with these new docs.** Safe today (build `outDir=dist/public`), but if a future deploy repurposes `docs/`, relocate the documentation.

---

## 11. Founder Next Actions

1. Run `npm run commercial:all` each morning (or wire to the 06:00–19:00 rhythm).
2. Review `reports/founder/DAILY_SUPER_COMMAND.md`; approve the Top Queue; send manually.
3. Make the 2 due calls using the briefs in `reports/sales_ops/SALES_OPS_BOARD_STATUS.md`.
4. Feed real researched companies into `company_os/revenue/prospects.csv` + drafts into `outreach_queue.json` to grow the batch.
5. Keep all pricing/sending/delivery decisions human — the gates assume it.

---

*Prepared: 2026-06-03 | Reproduce all: `npm run commercial:all` | Owner: Founder*
