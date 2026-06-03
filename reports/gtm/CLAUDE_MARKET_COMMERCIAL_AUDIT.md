# Dealix — Market + Commercial Production Audit

> **Agent:** Claude Code Agent #1 — Market + Commercial Production OS
> **Date:** 2026-06-03
> **Branch:** `claude/practical-lamport-B9zHq`
> **Mode:** Inspect → Audit → Plan → Implement (safe, non-destructive, approval-first)
> **Status:** Inspection complete. No source files modified at audit time.

This audit is the mandatory pre-build inspection. It records exactly what exists
in the repository today, what is missing, what must not be overwritten, and the
safe order of implementation. Nothing in the existing app, API, database, or
governance layer was edited to produce this report.

---

## 0. Repository shape (ground truth)

Dealix is **not** a Python-first monorepo. It is:

- A **TypeScript / Vite / React 19** web app (`src/`, `index.html`, `vite.config.ts`).
- A **Hono + tRPC + Drizzle (MySQL)** backend (`api/`, `db/`, `contracts/`).
- A **content / operations layer** under `company_os/` (markdown, JSON, CSV).
- A small set of **Python automation scripts** under `scripts/` (governance, war room, scorecard, outreach queue, proof pack).

Tooling actually present:

| Tool | Version | Notes |
|------|---------|-------|
| Node | 22.22.2 | `npm test` → `vitest run` (config includes `api/**/*.test.ts` only) |
| Python | 3.11.15 | default interpreter has `pyyaml` 6.0.1, **no** `pytest` |
| pytest | 9.0.2 | installed in an isolated `uv` tool venv (`/root/.local/share/uv/tools/pytest`) |
| uv | 0.8.17 | available; PyPI reachable (provisioned `pyyaml` into the pytest venv) |

**Implication:** the task brief assumed directories (`dealix/`, `auto_client_acquisition/`,
`autonomous_growth/`, `core/agents/`, `mcp_server/`, `token-optimizer/`, `apps/`,
`frontend/`, `docs/gtm/`, `schemas/`, `reports/`, `data/`, `tests/`) that **do not exist**.
This is a greenfield build for the Market + Commercial layer, laid on top of an
existing safety/governance core. Most new files are therefore additive (no overwrite risk).

---

## 1. Existing Market Production OS files

| Path | Type | Role |
|------|------|------|
| `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md` | md | Daily revenue war-room view (closest existing thing to a GTM command room) |
| `company_os/war_room/WEEKLY_CEO_BRIEF.md` | md | Weekly executive brief |
| `company_os/war_room/RISKS.md` | md | Risk log |
| `company_os/war_room/SCORECARD_REPORT.md` | md | Scorecard output |
| `scripts/generate_war_room.py` | py | Generates the war-room markdown from revenue data |
| `scripts/revenue_scorecard.py` | py | Computes revenue scorecard |
| `scripts/generate_outreach_queue.py` | py | Builds outreach queue from prospects |
| `scripts/generate_proof_pack.py` | py | Builds proof-pack scaffold |
| `scripts/governance_check.py` | py | **Compliance gate** (approval / PII / pricing rules) |

There is a **daily/weekly rhythm in spirit** (war room + CEO brief) but no formal
Market Production OS definition, boundaries, file map, naming convention, metrics
spec, or founder command-center doc.

## 2. Existing commercial files

| Path | Type | Role |
|------|------|------|
| `company_os/revenue/pipeline.json` | json | Pipeline stages + counts + value (10 stages: Target→Referral) |
| `company_os/revenue/proposals.json` | json | Proposal records |
| `company_os/revenue/objections.json` | json | Objection bank (Arabic, 7 objections w/ responses) |
| `company_os/revenue/outreach_queue.json` | json | Outreach queue |
| `company_os/revenue/followups.json` | json | Follow-ups |
| `company_os/revenue/prospects.csv` | csv | Prospects (cols: company, segment, website, decision_maker, pain, status, next_action, next_date, offer, last_touch, score) |
| `company_os/finance/unit_economics.md` | md | Unit economics |
| `company_os/finance/revenue_scorecard.csv` | csv | Scorecard data |
| `company_os/delivery/*.md` | md | Delivery SOP, intake, success plan, proof-pack template |
| `package.json` → `commercial:*` scripts | json | **Broken** — see §10 |

No formal product catalog, offer ladder, pricing guardrails, ICP matrix, persona
library, pain→offer matrix, sales-process doc, objection-bank doc, or pipeline-stage spec.

## 3. Existing brand files

| Path | Type | Role |
|------|------|------|
| `company_os/marketing/one_pagers/one_pager_arabic.md` | md | **Strong existing Arabic brand voice + positioning + pricing** |
| `company_os/marketing/linkedin_posts/post_01..04.md` | md | Content samples |
| `company_os/marketing/pitch_deck/` | mixed | Pitch deck (outline, design, 11 pages) |

No `docs/BRAND_PRESS_KIT.md`, no `docs/brand/` system (identity, messaging house,
voice, claims policy, visual direction, outbound system, content rules, asset checklist).
The one-pager already encodes voice and an approval-first governance loop — this is the
canonical seed for Brand OS.

## 4. Existing product catalog / offer files

- **None formal.** Pricing is embedded inline in `one_pager_arabic.md`:
  - P1 — Revenue Intelligence Sprint — from **2,500 SAR / 5 days**
  - P2 — AI Sales Ops Retainer — from **3,000 SAR / month**
- `company_os/finance/unit_economics.md` holds cost assumptions.
- No `schemas/product_offer.schema.json`, no `data/commercial/product_catalog.yaml`,
  no offer ladder, packaging, scope/out-of-scope, deliverables library, pricing
  guardrails, discount policy, payment terms, or quote-approval policy.

**Reconciliation note:** the task's 7-tier ladder (Readiness Scan → Custom Company OS)
must be reconciled with the existing P1/P2 naming. Plan: keep P1/P2 as the *live, sold*
offers and map them onto the fuller ladder so nothing already in-market is contradicted.

## 5. Existing sector files

- **None formal.** Sectors appear only as free-text in `prospects.csv` /
  `REVENUE_WAR_ROOM_TODAY.md`: *Marketing Agency, Training Company, B2B Services*.
- No `docs/sectors/`, no `data/sectors/sectors.yaml`, no sector playbooks.

## 6. Existing outreach / draft files

| Path | Type | Role |
|------|------|------|
| `company_os/governance/approval_queue.json` | json | **Approval queue** — drafts w/ `requires_approval`, `approved`, `risk` (the canonical approval shape) |
| `company_os/revenue/outreach_queue.json` | json | Outreach queue |
| `scripts/generate_outreach_queue.py` | py | Queue generator |

Drafts today are ad-hoc (5 sample items). No draft schema, no 250/day factory spec,
no personalization tiers, no sequence library, no risk gates doc, no rejection-reason taxonomy.

## 7. Existing signal detection files

- **None.** No `docs/signals/`, no signal schemas, no `data/signals/*`, no prospect
  research OS, no suppression list. Prospect "scores" exist as a single integer in
  `prospects.csv` with no documented rubric.

## 8. Existing content / press / partnership files

- **Content:** `company_os/marketing/linkedin_posts/*` (samples only, no engine/calendar).
- **Press:** none.
- **Partnerships:** none.

## 9. Existing tests and gates

| Item | Status |
|------|--------|
| `vitest` (`npm test`) | Configured for `api/**/*.test.ts` only; **no api tests exist yet** |
| `scripts/governance_check.py` | A real compliance gate (approval/PII/pricing). Exit-code based. |
| `tests/` directory | **Missing** |
| Commercial/GTM tests | **None** |
| pytest | Available (uv venv); pyyaml provisioned into it during inspection |

The governance gate is the strongest existing safety asset and aligns exactly with the
task's non-negotiables (no send without approval, no AI pricing, no PII in public tools).

## 10. Duplicate or conflicting files

1. **Nested duplicate tree:** `company_os/company_os/` is a **stale, divergent copy**
   of `company_os/`. Every shared file *differs* (older content). The outer
   `company_os/` is the newer canonical tree (more files: full pitch-deck pages,
   `SCORECARD_REPORT.md`, `one_pager_arabic.md`, `post_01..04`). The inner tree holds
   older scaffolding (`launch_post.md`, `p1_one_pager.md`, `p1_intake_template.md`,
   `company_os/company_os/scripts/`). → **Flag for founder cleanup; do NOT auto-delete.**
2. **Duplicated Python scripts:** `scripts/*.py` (canonical) also exist under
   `company_os/company_os/scripts/*.py` with different content. Canonical = top-level `scripts/`.
3. **Broken npm scripts (real bug):** `package.json` defines
   `commercial:check|plan|quality|brief|all` pointing at
   `scripts/commercial-control-check.js`, `scripts/commercial-daily-plan.js`,
   `scripts/draft-quality-gate.js`, `scripts/commercial-daily-brief.js` — **none of which exist.**
   `npm run commercial:all` fails today. This is a concrete, safe gap to fill.

## 11. Missing files (the build surface)

Effectively the entire Market + Commercial layer is missing and must be created:
`docs/gtm/`, `docs/brand/`, `docs/commercial/`, `docs/outreach/`, `docs/sectors/`,
`docs/signals/`, `docs/content/`, `docs/press/`, `docs/partnerships/`, `docs/privacy/`,
`docs/evals/`, `schemas/`, `data/commercial/`, `data/sectors/`, `data/signals/`,
`data/prospects/`, `data/outreach/`, `data/content/`, `data/partners/`, `data/evals/`,
`reports/gtm/`, `reports/commercial/`, `reports/sectors/`, `reports/signals/`,
`reports/outreach/`, `reports/privacy/`, `reports/content/`, `reports/press/`,
`reports/partnerships/`, and `tests/`. Full file-by-file targets are tracked in
`reports/gtm/MARKET_PRODUCTION_GAP_MATRIX.md`.

## 12. Files that MUST NOT be overwritten (protected)

| Path / area | Reason |
|-------------|--------|
| `company_os/governance/agent_permissions.md` | Canonical safety/approval matrix — extend by reference only |
| `company_os/governance/pdpl_checklist.md` | Canonical PDPL checklist — extend by reference only |
| `company_os/governance/approval_queue.json`, `ai_action_ledger.jsonl` | Live governance state |
| `company_os/company_os/**` | Stale duplicate — leave untouched; founder decides cleanup |
| `company_os/revenue/*.json`, `prospects.csv` | Live revenue state; new data goes in `data/` |
| `src/**`, `api/**`, `db/**`, `contracts/**` | Application & backend — out of scope for this layer |
| `package-lock.json`, `package.json` deps | No dependency changes without approval |
| `scripts/*.py` (existing 5) | Working automation — extend alongside, don't rewrite |

## 13. Safe extension points

- **New top-level dirs** `docs/`, `data/`, `schemas/`, `reports/`, `tests/` — additive, zero overwrite risk.
- **Satisfy the broken `commercial:*` npm scripts** by *creating* the 4 missing Node
  scripts (control-check, daily-plan, draft-quality-gate, daily-brief). This fixes a real
  bug and gives the founder a working `npm run commercial:all` command room.
- **Reuse existing data shapes:** approval-queue object shape, `prospects.csv` columns,
  `pipeline.json` stage list, `objections.json` structure — extend, don't fork.
- **Reuse the Arabic voice** already established in `one_pager_arabic.md` and `objections.json`.
- **Reuse the governance gate** (`governance_check.py`) as the upstream compliance authority.

## 14. Recommended implementation order

1. **Scaffold + conventions** — directory tree, file map, naming conventions, system boundaries.
2. **Brand OS** (voice/claims first — every later draft depends on the claims policy).
3. **Product Catalog + Offer OS** (the commercial spine; reconcile P1/P2 with the ladder).
4. **ICP / Personas / Pain→Offer** (the targeting + matching brain).
5. **Sector Intelligence** (10 playbooks built on ICP + catalog).
6. **Signals + Prospect Research** (input to the draft factory).
7. **Cold Email Draft Factory (250/day)** (consumes catalog + ICP + signals + brand).
8. **Deliverability / Compliance / Privacy** (gates that decide draft → send readiness).
9. **Content / Press / Partnerships.**
10. **Commercial Pipeline / Sales / Objections.**
11. **Executable gates (Node) + Tests (pytest)** — wire the rules into runnable checks.
12. **Final report + verification.**

### Guardrails honored throughout
`dry_run=true`, `approval_required=true`, `send_enabled=false` by default. No external
sending, no cold WhatsApp/LinkedIn automation, no scraping, no secrets, no PII in
logs/reports, no guaranteed-revenue or "10x" claims, no fake `Re:/Fwd:` subjects, no
fabricated clients/case studies, no weakening of existing trust/security/approval gates,
no test deletion.

---

*Audit produced by inspection only. Build proceeds per §14.*
