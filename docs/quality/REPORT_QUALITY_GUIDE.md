---
title: Executive Report Quality Guide — Acceptance Criteria
doc_id: W6.T36.exec-report-quality
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W4.T13]
kpi:
  metric: customer_artifact_first_pass_acceptance
  target: 90
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 0.5
  score: quality-operating
---

# Executive Report Quality Guide

## 1. Context

The executive report is the single customer-facing artifact that most
influences whether a customer renews. If the exec sponsor cannot understand
it in five minutes, the project loses its narrative — regardless of how good
the underlying build was. This guide is the acceptance rubric Dealix applies
to every executive report it ships.

## 2. Audience

CSMs producing executive reports, engineers producing the underlying data,
HoCS approving release, reviewers in the QA Delivery gate.

## 3. The Acceptance Criteria

An executive report ships only when ALL six conditions are true:

| # | Criterion | What to check |
|---|-----------|---------------|
| 1 | **Clarity for a non-technical reader** | Sponsor reads it once, can answer "what changed?" and "what's next?" without help |
| 2 | **Numeric KPIs** | At least 3 dated, signed-at-kickoff KPIs reported with before/after |
| 3 | **One-page Executive Summary first** | TL;DR, KPI block, decision asked-for, all on page 1 |
| 4 | **Source attribution** | Every claim links to a data source, audit log row, or proof artifact |
| 5 | **Next actions** | Three or fewer concrete next actions, each with an owner and a date |
| 6 | **Bilingual where required** | AR + EN side-by-side or stapled; AR primary for Saudi customers |

Artifacts failing any criterion fail the Delivery gate (see
[`QUALITY_STANDARD.md`](QUALITY_STANDARD.md)).

## 4. Standard Sections

In order, every customer-facing executive report contains:

1. **Executive Summary** (≤ 1 page) — TL;DR, KPI block, decision.
2. **Context** (≤ ½ page) — what we set out to do; who signed the metrics.
3. **What we did** (≤ 1 page) — the build in plain language.
4. **Results** — the KPI table with before/after; supporting charts on
   facing pages.
5. **Risks observed** — what the data revealed (data gaps, PDPL surfaces,
   adoption concerns).
6. **Next actions** — 1–3 actions with owners and dates.
7. **Appendix** — audit log link, proof pack link, SOP / runbook link,
   sub-processor list link.

## 5. Style Rules

- **No jargon unsourced**: any technical term used has a one-line plain
  definition the first time.
- **Charts over tables** for >10 data points; tables for ≤10.
- **One claim per sentence**: long compound claims hide hedges.
- **No forbidden phrases**: scan with `forbidden_claims.scan_text` before
  release. See [`ARABIC_QUALITY_GUIDE.md`](ARABIC_QUALITY_GUIDE.md).
- **PII absent**: PII never appears in customer-facing artifacts — verified by
  `pii_detector.decide_for_record` on every record cited.

## 6. The "Sponsor 5-Minute Test"

Before HoCS sign-off, the CSM hands the artifact to someone who is *not*
on the project (another CSM works) and gives them 5 minutes. The reader
must, unprompted, be able to state:

1. What did Dealix do?
2. What is the headline KPI move?
3. What is the customer being asked to decide / do next?

If any answer is unclear, the artifact returns for a rewrite.

## 7. Anti-Patterns

- **Build log dressed as an executive artifact**: a list of features
  delivered is not an executive artifact. Communicate *outcomes*.
- **Dashboard screenshot dump**: dashboards are inputs, not the artifact.
  The narrative tells the story.
- **Hedge-stack**: "may have potentially contributed to..." — pick a
  claim or omit it.
- **No decision asked**: an artifact without a "decide on X" is a
  newsletter. Always frame a next step.

## 8. Cross-links

- Quality Standard: [`QUALITY_STANDARD.md`](QUALITY_STANDARD.md)
- Handoff: [`../delivery/HANDOFF_PROCESS.md`](../delivery/HANDOFF_PROCESS.md)
- Arabic quality: [`ARABIC_QUALITY_GUIDE.md`](ARABIC_QUALITY_GUIDE.md)
- Executive KPI spec: [`../analytics/executive_kpi_spec.md`](../analytics/executive_kpi_spec.md)
- Reporting OS module: see `docs/product/internal_os_modules.md` §3.7

## 9. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: refresh quarterly with retro on which artifacts converted to renewal.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial acceptance rubric for customer-facing executive reports |
