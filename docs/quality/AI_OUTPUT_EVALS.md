---
title: AI Output Evals — Accuracy, Citation, Tone, Safety, Hallucination, PII
doc_id: W6.T36.ai-evals
owner: HoData
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W4.T26, W3.T07b]
kpi:
  metric: ai_eval_pass_rate
  target: 95
  window: rolling_28d
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 1
  score: quality-engineering
---

# AI Output Evals

## 1. Context

Every AI-generated output that reaches a customer must pass an eval. The eval
framework is the engineering complement to the AI gate in
[`QUALITY_STANDARD.md`](QUALITY_STANDARD.md). The gate asks "did we check?";
the evals are the checks — they run on every release, every model swap, every
prompt change, and on a rolling sample of production traffic.

## 2. Audience

HoData (framework owner), engineers building AI features, HoP (decisions on
shipping a model change), HoLegal (compliance evals).

## 3. The Six Eval Dimensions

| Dimension | What it measures | Pass threshold |
|-----------|------------------|----------------|
| **Accuracy** | Output matches a held-out truth set on a per-task basis | ≥ 95% on truth set; lower for open-ended tasks (defined per offering) |
| **Citation** | Every factual claim cites a source the model could see | ≥ 95% citation-grounded for RAG outputs; 100% for executive reports |
| **Tone (AR / EN)** | Bilingual outputs match the sector/buyer-level tone band | ≥ 90% reviewer agreement on a sampled 50/release |
| **Safety** | No banned content, no prompt-injection leakage, no policy-overrides | 100% — any miss is a release-blocker |
| **Hallucination** | Detectable invented facts, mis-statements, fabricated entities | ≤ 1% on sampled production traffic |
| **PII** | No leakage of PII into outputs, logs, or training pipelines | Zero tolerance — every detected PII leak triggers incident response |

## 4. Eval Datasets

- **Truth sets** per task: hand-labelled examples, refreshed quarterly.
  Stored in `evals/`. Each set carries provenance + lawful-basis notes.
- **Held-out splits**: 20% of every truth set is held out; only used at
  release time. Never used in prompt iteration.
- **Production sample**: rolling 1% sample of live traffic, anonymized
  before storage, retained for 30 days for eval purposes only (see
  [`../governance/PDPL_DATA_RULES.md`](../governance/PDPL_DATA_RULES.md)).

## 5. When Evals Run

| Trigger | Which dimensions |
|---------|------------------|
| Prompt change merged to main | All six |
| Model version swap | All six, with A/B per [`../experiments/ab_framework.md`](../experiments/ab_framework.md) |
| Weekly rolling | All six on production sample |
| Customer report generation | Accuracy + Citation + PII per generation (synchronous gate) |

## 6. The A/B Connection

A model or prompt change ships only after passing the AI eval *and* an A/B
that meets the framework in [`../experiments/ab_framework.md`](../experiments/ab_framework.md).
The eval guards quality; the A/B guards real-world impact. Neither alone is
sufficient.

## 7. Reporting

- Eval results land in `evals/results/<run_id>.json`.
- Weekly summary surfaces in the QA scoreboard meeting (see
  [`QA_REVIEW_PROCESS.md`](QA_REVIEW_PROCESS.md)).
- Any production drift (rolling pass rate falls below threshold for 3
  consecutive days) triggers a model-routing review.

## 8. Anti-Patterns

- **Test-set contamination**: training/prompt iteration on held-out sets.
  Banned. Held-out splits are sealed.
- **Tone eval by author**: the author of the prompt cannot be the tone
  reviewer. Mandatory second reviewer.
- **PII allowlists**: there is no "allowed PII" in outputs. Redaction is
  policy.

## 9. Cross-links

- Quality Standard: [`QUALITY_STANDARD.md`](QUALITY_STANDARD.md)
- A/B framework: [`../experiments/ab_framework.md`](../experiments/ab_framework.md)
- Arabic quality: [`ARABIC_QUALITY_GUIDE.md`](ARABIC_QUALITY_GUIDE.md)
- PII policy: [`../governance/PII_REDACTION_POLICY.md`](../governance/PII_REDACTION_POLICY.md)
- Code: `dealix/trust/pii_detector.py`, `dealix/trust/forbidden_claims.py`

## 10. Owner & Review Cadence

- **Owner**: HoData.
- **Review**: monthly thresholds review; quarterly truth-set refresh.

## 11. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoData | Initial 6-dimension eval framework |
