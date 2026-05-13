# Internal Controls — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** COO + Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [INTERNAL_CONTROLS_AR.md](./INTERNAL_CONTROLS_AR.md)

## Context
A company that governs other companies' AI must first govern itself. Internal controls are the explicit "must not happen" list across Dealix's Sales, Delivery, Product, and Governance functions — the operational backbone behind the principles in `docs/DEALIX_OPERATING_CONSTITUTION.md` and the execution plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`. The discipline here is what allows incident response in `docs/ops/INCIDENT_RUNBOOK.md` to land into a healthy organization rather than a chaotic one.

## Sales controls
The Sales function operates under these non-negotiable controls.

- **No unsafe services promised.** Any service involving high-risk AI behavior (autonomous external action, regulated decisions, deep PII processing) requires Governance Council sign-off before the proposal is signed.
- **No guaranteed claims.** No revenue, ROI, or precision guarantees in client-facing materials. Outcome ranges and confidence statements only.
- **No enterprise promises before readiness.** Enterprise commitments (uptime, DPA terms, data residency) cannot be promised beyond what Dealix's current platform supports without an exception approved by the Governance Council and a documented mitigation plan.

## Delivery controls
The Delivery function operates under these non-negotiable controls.

- **No delivery without QA.** Every Class-B output is reviewed against the eval framework in `docs/AI_OBSERVABILITY_AND_EVALS.md` before going to the client.
- **No project close without proof pack.** A project does not close until a documented proof pack (value events, outputs, lessons) is delivered.
- **No out-of-scope work without change request.** No silent scope creep. Every change is logged, priced, and approved.

## Product controls
The Product function operates under these non-negotiable controls.

- **No feature without build decision.** Every shipped feature traces to a recorded build decision with owner, scope, and acceptance criteria.
- **No agent without inventory.** Every agent appears in the agent inventory before it produces any output.
- **No AI output without provenance.** Every client-facing output carries a complete provenance record per `docs/product/AI_RUN_PROVENANCE.md`.

## Governance controls
The Governance function operates under these non-negotiable controls.

- **No PII in logs.** Logs are redaction-tested; PII findings are an incident.
- **No external action without approval.** Any Class-D action requires explicit, recorded approval bound to a named human.
- **No source-less knowledge answer.** Internal knowledge answers carry source links; agents that produce knowledge outputs without sourcing are flagged in eval and demoted.

## Enforcement
- Each control has a named owner and a measurement.
- Breaches are logged as incidents and reviewed in the next Council session.
- The Internal Controls scorecard is included in the monthly Board Pack at `docs/company/BOARD_PACK.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sales proposals, delivery artifacts, product changes | Control checks per artifact | Function leads | Per artifact |
| Incident reports | Control improvement actions | COO + Governance | Per incident |
| Monthly review | Scorecard for Board Pack | Governance | Monthly |

## Metrics
- Control Breach Count — incidents per function per quarter (target: trending to 0).
- QA-Before-Delivery Rate — % of Class-B outputs that passed QA before delivery.
- Provenance Completeness — % of client-facing outputs with complete provenance.
- Approval-Bound-Action Rate — % of Class-D actions with an explicit named approver.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/ops/INCIDENT_RUNBOOK.md` — incident runbook
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
