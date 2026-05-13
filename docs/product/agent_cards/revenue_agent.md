# Revenue Agent — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [revenue_agent_AR.md](./revenue_agent_AR.md)

## Context
The Revenue Agent is the analytical heart of the Lead Intelligence and
RevOps services. It scores accounts and recommends actions inside a
governed workflow so that the human seller can focus on the highest-value
moves. It plugs into the workforce contract in
`docs/product/AI_WORKFORCE_OPERATING_MODEL.md` and the routing logic in
`docs/AI_MODEL_ROUTING_STRATEGY.md`.

## Agent Card

- **Role:** Scores accounts and recommends revenue actions.
- **Allowed Inputs:** client-approved datasets, ICP, service offer, sector
  playbook.
- **Allowed Outputs:** account score, score explanation, segment
  recommendation, next action.
- **Forbidden:** sending messages, scraping, guaranteed claims, unsourced
  personal data.
- **Required Checks:**
  - data source exists and is approved;
  - PII flagged where present;
  - score is explainable (top features cited);
  - compliance check passed.
- **Output Schema:** `AccountScore { account_id, score, reasons, risks,
  recommended_action }`.
- **Approval:** human review required before client delivery.

## Scoring model (summary)

- Inputs: firmographics, signal events, ICP fit, engagement history.
- Output: 0–100 score with top three contributing reasons.
- Risks: data-staleness, sector-mismatch, sensitive industry exposure.
- Recommended action: one of `enrich`, `engage`, `nurture`, `disqualify`.

## Anti-patterns

- Scoring on top of an unapproved dataset.
- Producing scores without explanations.
- Recommending an action that the Human-in-the-Loop matrix forbids.
- Producing a "guaranteed result" framing.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Approved dataset + ICP | AccountScore[] | Delivery owner | Per engagement |
| Score explanations | Reviewer summary | CSM | Per engagement |
| Action recommendations | Workflow queue items | Workflow Agent | Per task |

## Metrics
- Score Calibration — correlation between score and downstream conversion.
- Explanation Coverage — % of scores with top-3 contributing reasons.
- Action Acceptance — % of recommended actions accepted by reviewer.
- Forbidden Attempt Rate — blocked actions per 1k runs.

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
