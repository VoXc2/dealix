# Dealix

Dealix is a Saudi B2B revenue-operations workspace: a full-stack app plus a
file-based **Company OS** that helps a founder run outbound, pipeline, delivery,
finance, and governance — **draft-first and approval-first**, never as a spam or
auto-send tool.

> Dealix produces drafts and plans. A human approves before anything leaves the
> building. There are no guaranteed-revenue claims and no autonomous external
> sends.

## Architecture

| Layer | Path | Stack |
| --- | --- | --- |
| Frontend | `src/` | React + Vite + Tailwind (shadcn UI) |
| API | `api/` | Node/ESM routers (auth, prospect, followup, proposal, finance, governance, war room) |
| Database | `db/`, `drizzle.config.ts` | Drizzle ORM |
| Shared contracts | `contracts/` | TypeScript types / constants / errors |
| Company OS (data + ops) | `company_os/` | JSON / CSV / JSONL + Markdown |
| Automation scripts | `scripts/` | Python (war room, scorecard, governance) + Node (commercial gates) |

### Company OS layout

```
company_os/
  revenue/      prospects.csv, pipeline.json, outreach_queue.json,
                proposals.json, objections.json, followups.json
  governance/   approval_queue.json, ai_action_ledger.jsonl,
                suppression_list.json, agent_permissions.md, *_checklist.md
  delivery/     P1 intake/SOP, client success plan, proof pack template
  finance/      invoices_tracker.csv, revenue_scorecard.csv, unit_economics.md
  war_room/     generated daily briefs and reports
  marketing/    LinkedIn posts, pitch deck, one-pagers
```

## Safety model

These invariants are enforced by the commercial scripts and the governance
check, and are verified by tests:

- **No external sending by default.** Sending stays disabled unless
  `DEALIX_SEND_ENABLED=true` is set deliberately; everything runs dry-run.
- **Approval-first.** Every outbound item is approval-gated; nothing is
  auto-sent. High-risk items (pricing, data handling) surface for founder review.
- **Suppression is honored.** Recipients on `governance/suppression_list.json`
  can never become send-ready.
- **No guaranteed claims.** Overclaim / guaranteed-revenue language (Arabic and
  English, e.g. `نضمن`, `مضمون`, `10x revenue`, `risk-free`) fails the gate.
- **No deceptive subjects.** Fake `Re:` / `Fwd:` / `رد:` subjects fail the gate.
- **Offer mapping.** Drafts must map to an offer in the product catalog.
- **PII / PDPL aware.** Recipient PII is kept out of templates; governance checks
  flag potential leaks.

## Commercial scripts

The `commercial:*` npm scripts read the Company OS data and are read-only except
for the plan/brief, which write generated reports into `company_os/war_room/`.

```bash
npm run commercial:test     # safety-gate unit tests (no deps; node --test)
npm run commercial:check    # control-room safety gate → READY / BLOCKED
npm run commercial:quality  # draft quality gate → pass/fail per draft
npm run commercial:plan     # today's prioritized action plan (drafts only)
npm run commercial:brief    # one-screen founder daily brief
npm run commercial:all      # all of the above in sequence
```

`commercial:check` and `commercial:quality` exit non-zero when an invariant is
violated, so they double as CI / pre-send gates.

### Python automation (`scripts/`)

```bash
python3 scripts/governance_check.py        # PDPL / governance rules (G001–G007)
python3 scripts/generate_war_room.py       # daily war-room brief
python3 scripts/revenue_scorecard.py       # revenue scorecard
python3 scripts/generate_outreach_queue.py # build the outreach queue
python3 scripts/generate_proof_pack.py     # delivery proof pack
```

## App development

```bash
npm install        # install dependencies
npm run dev        # Vite dev server
npm run build      # build frontend + bundle API (dist/)
npm run check      # tsc type-check
npm run lint       # eslint
npm run test       # vitest (api/**/*.test.ts)
```

Environment variables are documented in `.env.example`. Never commit real
secrets; the API reads configuration from the environment.

## Notes / housekeeping

- A nested `company_os/company_os/` directory exists with slightly different
  copies of some files (and an extra `payments.csv`). It is intentionally left
  untouched here so no data is lost — it should be reconciled with the
  top-level `company_os/` and removed once confirmed redundant.
