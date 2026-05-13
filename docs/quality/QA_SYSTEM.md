# QA System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CTO + Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [QA_SYSTEM_AR.md](./QA_SYSTEM_AR.md)

## Context

QA at Dealix is not a final sweep — it is a five-layer review run on
every delivered artifact before it leaves the workspace. Without
it, Dealix cannot make the promises in
`docs/company/DEALIX_CEO_STRATEGY.md` (proof-led, governance-first,
Arabic-quality-first). This document is the canonical QA framework
and complements the eval automation in
`docs/AI_OBSERVABILITY_AND_EVALS.md` and the runbook in
`docs/EVALS_RUNBOOK.md`.

## The 5 QA Layers

| # | Layer | What it checks |
|---|---|---|
| 1 | **Business QA** | Does the artifact answer the stated business question? Outcome metric defined and measurable? Scope respected? Buyer language? |
| 2 | **Data QA** | Are the inputs cleaned, sourced, dated, owned? Are records linked to source rows? Are PDPL constraints respected? |
| 3 | **AI QA** | Did model output match the eval set? Hallucination risk checked? Source citations present? Prompt version captured? |
| 4 | **Language QA** | Arabic Business Quality score per `docs/quality/ARABIC_BUSINESS_QUALITY.md`. English clarity score. No forbidden phrasing. |
| 5 | **Governance QA** | Approvals captured for external actions? Audit log written? Forbidden actions absent? PDPL boxes ticked? |

Each layer is scored 0-100. The overall score is the **minimum**
across the five, not the average — a single failing layer fails the
artifact.

## Pass Rule

An artifact is approved for delivery only if all of the following:

- **Overall score ≥ 85** (i.e. all five layers ≥ 85).
- **Governance score = 100** (no partial credit; governance is binary).
- **Zero critical issues unresolved** (a critical issue is any one
  of: source error, PII leak, governance breach, hallucinated fact,
  Arabic register breach in client-visible text).

If pass rule fails, the artifact is returned with a Required Fixes
list and a re-review is triggered.

## QA Review JSON Schema

Every QA review is captured as a structured record:

```json
{
  "qa_review_id": "qa_2026_05_13_001",
  "engagement_id": "eng_acme_lead_intel",
  "artifact_id": "lead_list_v3",
  "reviewer": "qa@dealix",
  "scores": {
    "business": 92,
    "data": 88,
    "ai": 90,
    "language": 95,
    "governance": 100
  },
  "overall": 88,
  "critical_issues": [],
  "required_fixes": [
    "Add Hijri date column to header row.",
    "Re-cite source row IDs for rows 47-52."
  ],
  "approved_for_delivery": true,
  "reviewed_at": "2026-05-13T14:22:00+03:00"
}
```

Records are written to the QA ledger and linked to the Proof Pack
generated at engagement close.

## Reviewers

- **Business QA** — Account Lead (or CSM for retainers).
- **Data QA** — Delivery Engineer.
- **AI QA** — AI Lead (uses eval suite from
  `docs/AI_OBSERVABILITY_AND_EVALS.md`).
- **Language QA** — Arabic Quality Reviewer.
- **Governance QA** — Compliance Lead (or Legal contact).

No single reviewer can cover more than two layers on the same
artifact (separation-of-duties).

## Cadence

- **Per artifact** — full 5-layer review before delivery.
- **Weekly** — random spot-check of 10% of delivered artifacts (audit).
- **Monthly** — leadership review of critical-issue trends.
- **Quarterly** — eval refresh per `docs/EVALS_RUNBOOK.md`.

## Common Failure Patterns

- AI score high but Data score low → garbage-in fluent answers.
- Language score 100 but Business score low → polished irrelevance.
- Governance score 90 but missing one approval → still fails.
- "We approved over chat" → does not count; must be in the system.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Delivered artifacts, eval results, governance logs | QA review records, approval/return decisions | QA reviewers | Per artifact |
| Trend reports | Critical-issue heatmaps | CTO | Monthly |
| Updated evals | Refreshed AI scoring | AI Lead | Quarterly |

## Metrics

- **First-pass QA rate** — % of artifacts approved on first review (target ≥85%).
- **Critical issue rate** — # critical issues per 100 artifacts (target ≤2).
- **Governance score = 100 rate** — % artifacts (target 100%).
- **QA review latency** — median hours from submission to decision (target ≤24h).

## Related

- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval automation feeding AI QA.
- `docs/EVALS_RUNBOOK.md` — operating runbook for evals.
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — incident handling for QA failures.
- `docs/quality/QUALITY_STANDARD_V1.md` — sibling quality standard.
- `docs/quality/ARABIC_BUSINESS_QUALITY.md` — language QA detail.
- `docs/product/QUALITY_AS_CODE.md` — quality enforcement in code.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
