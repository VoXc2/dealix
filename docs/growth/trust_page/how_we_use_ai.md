# How We Use AI — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [how_we_use_ai_AR.md](./how_we_use_ai_AR.md)

## Context
This page tells prospects and clients, in plain language, how Dealix uses
AI on their behalf. It is the public counterpart of the AI Workforce
Operating Model and the runtime guarantees enforced by the constitution
in `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Plain-language commitments

- **AI inside governed workflows.** AI does not act alone. Every action
  flows through a controlled workflow with rules and approvals.
- **Outputs reviewed.** Client-facing AI outputs are reviewed by a human
  before delivery.
- **Cost and risk monitored.** We monitor cost, errors, and governance
  events in our AI Control Tower.
- **Provenance tracked.** Each output is traceable to its inputs, prompts,
  and the rules it passed.

## What this looks like in practice

- We do not deploy autonomous agents that take external action on behalf
  of clients.
- We do not produce knowledge answers without a source citation.
- We do not send messages from AI without human approval.
- We test our agents on eval suites and report results internally and to
  clients on request.

## Why this matters

- It keeps quality high.
- It keeps risk inside known bounds.
- It makes value claims provable in the Value Ledger.

## Linked operating documents

- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability and evals.
- `docs/EVALS_RUNBOOK.md` — eval execution.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating posture.
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — Arabic trust pack.

## Anti-patterns we refuse

- "AI that sends emails on your behalf without supervision."
- Hidden prompts that override governance.
- AI-generated proofs that cannot be traced to inputs.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement workflow | Governed AI runs | Workflow Agent | Per task |
| Run telemetry | Public trust evidence | Head of AI | On request |
| Eval results | Public eval summary | Head of AI | Quarterly |

## Metrics
- External AI Action Without Approval — must remain zero.
- Citation Coverage on External Answers — target 100%.
- Eval Threshold Adherence — % of agents above threshold.
- Trust Evidence Requests Fulfilled — % of client requests answered.

## Related
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — business trust pack
- `docs/DPA_DEALIX_FULL.md` — data processing agreement
- `docs/DATA_RETENTION_POLICY.md` — retention rules
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — Arabic trust pack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
