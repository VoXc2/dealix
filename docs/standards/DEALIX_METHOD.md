# Dealix Method — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** Head of Dealix Services + Head of Dealix Core
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_METHOD_AR.md](./DEALIX_METHOD_AR.md)

## Context
The Dealix Method is the **public-facing methodology** that every Dealix Business Unit applies to every engagement. It is the verb sequence behind the brand: Diagnose → Design → Build → Govern → Validate → Deliver → Prove → Operate → Compound. The Method is the standard that the [`DEALIX_STANDARD_METRICS`](./DEALIX_STANDARD_METRICS.md) measures against. It is the operational expression of `docs/DEALIX_OPERATING_CONSTITUTION.md` and is mirrored in Arabic for the Saudi/MENA market via `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`.

## The nine phases

```
Diagnose → Design → Build → Govern → Validate → Deliver → Prove → Operate → Compound
```

### 1. Diagnose
- **Purpose:** Find the highest-leverage AI opportunity that is also safe and sellable.
- **Deliverables:** Opportunity map, scored shortlist, baseline metrics, risk inventory.
- **Gate criteria:** Top opportunity has a measurable baseline; PDPL impact assessed.

### 2. Design
- **Purpose:** Specify the target workflow, dataset shape, governance, and ROI hypothesis.
- **Deliverables:** Workflow diagram, data contract, policy bindings, KPI plan.
- **Gate criteria:** Workflow approved by client + governance; KPI plan signed off.

### 3. Build
- **Purpose:** Construct the workflow on Core OS, not on bespoke infrastructure.
- **Deliverables:** Working workflow in client tenant; configured policies; eval harness.
- **Gate criteria:** Workflow passes initial eval set; no orphan infra outside Core OS.

### 4. Govern
- **Purpose:** Bind the workflow to policies, approvals, audit, and PDPL guardrails.
- **Deliverables:** Policy bindings; approval matrix; audit log enabled; DSR path defined.
- **Gate criteria:** Governance Runtime confirms 100% policy coverage of model calls.

### 5. Validate
- **Purpose:** Prove the workflow works at quality before exposing it to live load.
- **Deliverables:** Eval results; pilot dataset run; QA gate report.
- **Gate criteria:** QA score ≥ 85; eval pass rate above threshold; no critical defects.

### 6. Deliver
- **Purpose:** Cut over to production and train the client team.
- **Deliverables:** Production cutover; training; SLA & on-call setup; user adoption plan.
- **Gate criteria:** SLA met for 1 week; ≥ 80% intended users active.

### 7. Prove
- **Purpose:** Capture the ROI as a Proof Pack and case study.
- **Deliverables:** Proof Pack (`docs/PROOF_PACK_V6_STANDARD.md`); ROI evidence; case study draft.
- **Gate criteria:** Proof Pack entered into Proof Ledger; client signs off on numbers.

### 8. Operate
- **Purpose:** Run the workflow on a monthly retainer; tune it; expand scope.
- **Deliverables:** Retainer SoW; monthly value report; backlog of new workflows.
- **Gate criteria:** Retainer signed within 60 days of cutover.

### 9. Compound
- **Purpose:** Extract reusable assets and productize repeated work into Core OS.
- **Deliverables:** Capital Ledger entries; productization candidates; published insights.
- **Gate criteria:** ≥ 2 capital assets registered; ≥ 1 productization candidate filed.

## How the Method is enforced

- **QA gate** at the end of each phase (`docs/product/QUALITY_AS_CODE.md`).
- **Per-phase deliverables** are templated in Core OS — clients cannot skip a phase silently.
- **The Proof Pack** is required before invoicing the final milestone.
- **The Productization Ledger** is required to record at least one entry per engagement (`docs/product/PRODUCTIZATION_LEDGER.md`).

## Public positioning
The Method is published externally as Dealix's signature methodology, the same way category-defining firms publish theirs. It anchors:

- Sales pitches and proposals.
- Sprint, pilot, and retainer SoW templates.
- Academy curriculum.
- Partner certification path.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement brief | Diagnose deliverables | BU Delivery | Per project |
| Per-phase QA gate | Pass/fail + remediation | QA Lead | Per phase |
| Proof Pack | Capital + productization candidates | BU GM | Per project |
| Method-version updates | Group-wide rollout | Head of Services | Quarterly |

## Metrics
- **Method adherence rate** — % engagements completing all 9 phases.
- **Per-phase pass rate** — % phases passing QA gate first time.
- **Time-per-phase** — median days per phase.
- **Compound contribution per engagement** — capital assets created.
- **Method version adoption** — % active engagements on the latest Method version.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — non-negotiable operating rules.
- `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md` — Arabic master operating model.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/PROOF_PACK_V6_STANDARD.md` — Proof Pack standard.
- `docs/product/QUALITY_AS_CODE.md` — QA-as-code.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
