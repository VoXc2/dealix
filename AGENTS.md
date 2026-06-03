# Dealix — Agent & Contributor Guide

Dealix is an end-to-end acquisition → delivery operating machine for five launch
systems, presented through an Arabic (RTL) marketing site and driven by a set of
deterministic Node scripts over JSONL data.

## The five systems (canonical ids)

| id | الاسم | starts at | drafts/day |
|----|------|----------:|-----------:|
| `revenue-operating-system` | نظام تشغيل الإيرادات | 4,500 SAR | 100 |
| `executive-command-os` | نظام القيادة التنفيذية | 5,500 SAR | 70 |
| `follow-up-recovery-os` | نظام استعادة المتابعة | 3,500 SAR | 90 |
| `whatsapp-client-os` | نظام عملاء واتساب | 4,500 SAR | 70 |
| `proposal-proof-os` | نظام العروض والإثبات | 3,000 SAR | 70 |

Total = **400 drafts/day**.

## Single source of truth

- `data/systems.json` — canonical registry (customer copy + ops metadata). Consumed by the scripts.
- `src/data/systems.ts` — typed display registry for the website. Kept in sync with the JSON by `src/data/systems.test.ts`.

Change both together. The test fails if ids, names, or prices drift.

## Layout

```
data/systems.json            canonical 5-systems registry
schemas/*.json               JSON Schemas for every record type
data/outreach|acquisition|delivery/*.jsonl   operational data (sample seed today)
scripts/                     the commercial machine (Node ESM, zero deps)
  lib/commercial.js          shared helpers + draft scoring + guardrails
  seed-sample-data.js        emits sample data/**/*.jsonl
  commercial-control-check.js  enforces hard guardrails (non-zero exit on fail)
  commercial-daily-plan.js     400-draft plan vs staged drafts
  draft-quality-gate.js        scores drafts, gates >=75 into Top 100
  generate-reports.js          acquisition + delivery + founder weekly reports
  commercial-daily-brief.js    founder Daily Super Command
reports/                     generated Markdown (outreach/acquisition/delivery/founder)
docs/                        Arabic operating docs (acquisition/delivery/outreach/founder_control/site/whatsapp)
src/pages/marketing/         website pages (systems, pricing, diagnostic, start, contact, resources, partners)
src/components/site/         shared site chrome (nav, footer, layout, system card)
```

## Commands

```bash
npm run commercial:seed     # regenerate sample data/**/*.jsonl
npm run commercial:all      # control-check → plan → quality gate → reports → daily brief
npm run check               # tsc -b (typecheck)
npm run build               # vite build + api bundle
npx vitest run              # unit tests (incl. systems consistency)
npm run dev                 # local dev server
```

## Hard guardrails (enforced by `commercial:check`, exits non-zero on violation)

- 400 drafts/day is the target; **400 sends/day is NOT enabled**. No external send by default.
- Every email stays a **draft** until founder approval. `DEALIX_SEND`/`SEND_ENABLED=true` is rejected by the control check.
- Call briefs are for **human** callers only — no automated calling.
- No cold WhatsApp or LinkedIn automation. No purchased lists. No fake `Re:`/`Fwd:` subjects.
- No guaranteed-revenue claims anywhere (the literal tokens appear only in the guardrail definitions).
- Public or founder-provided data only. Respect `do_not_contact` / suppression list.
- Mini proposals require founder approval before sending.
- Delivery work cannot start before required inputs are received.
- Evidence levels L0–L4: L0/L1 (assumptions) must be phrased as *likely*, not certain.
- No secrets/PII in data, prompts, or logs.
