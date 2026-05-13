# Reporting Agent — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [reporting_agent_AR.md](./reporting_agent_AR.md)

## Context
The Reporting Agent generates the executive and operational documents that
turn engagement work into proof packs and ledger entries. It is the
production face of the Value Realization System and writes both English
and Arabic outputs consistent with
`docs/localization/ARABIC_TONE_LIBRARY.md`.

## Agent Card

- **Role:** Generates executive and operational documents from project outputs.
- **Allowed Inputs:** project outputs, KPIs, capability scores, ledger
  rows, sector context.
- **Allowed Outputs:** bilingual executive document; operational summary;
  proof pack export.
- **Forbidden:** fabricated numbers; un-versioned data; un-cited claims;
  publishing without owner sign-off.
- **Required Checks:**
  - all numbers map to a versioned source;
  - executive summary + next action are present;
  - Arabic output passes tone library check;
  - sensitivity labels honored.
- **Output Schema:** `ExecDoc { title, period, summary, kpis[],
  next_actions[], proof_links[] }`.
- **Approval:** owner sign-off before external delivery.

## Document types

- **Engagement Executive Document** — per project; bilingual.
- **Monthly Operating Review Section** — feeds
  `docs/meetings/OPERATING_REVIEW_PACK.md`.
- **Proof Pack** — packaged delivery artifact.
- **Capability Snapshot** — capability strength view.

## Anti-patterns

- "AI-generated charts" without provenance.
- Numbers without a versioned dataset reference.
- Arabic translated by template instead of native tone.
- Missing "next action" — incomplete document.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Project outputs | ExecDoc | Reporting Agent | Per engagement |
| Ledger snapshot | Capability snapshot | Reporting Agent | Monthly |
| Tone library | Arabic compliant text | Reporting Agent | Per output |

## Metrics
- Citation Integrity — % of numbers traceable to a versioned source.
- Tone Pass Rate — % of Arabic outputs passing tone review.
- Time-to-Delivery — minutes from data freeze to delivery.
- Owner Sign-off Rate — % of documents signed first-pass.

## Related
- `docs/AI_STACK_DECISIONS.md` — model selection
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval suite
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — governance rules
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
